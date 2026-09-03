#!/usr/bin/env python3
"""Sanitize n8n workflow exports for a public Git repository."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

PLACEHOLDER = "__REDACTED_SECRET__"
CREDENTIAL_ID = "__CREDENTIAL_ID__"
CREDENTIAL_NAME = "__CREDENTIAL_NAME__"

SENSITIVE_NAME = re.compile(
    r"(authorization|password|passphrase|api[_ -]?key|access[_ -]?token|"
    r"refresh[_ -]?token|session[_ -]?token|page[_ -]?access[_ -]?token|secret)",
    re.IGNORECASE,
)
SAFE_TYPE_NAME = re.compile(r"(credential|auth).*type|type.*(credential|auth)", re.IGNORECASE)

SECRET_PATTERNS = [
    ("bearer", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{16,}")),
    ("openai_like", re.compile(r"\bsk-[A-Za-z0-9_-]{16,}")),
    ("github", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}")),
    ("google_api", re.compile(r"\bAIza[0-9A-Za-z_-]{20,}")),
    ("aws_access", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    (
        "private_key",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ),
    (
        "jwt",
        re.compile(
            r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"
        ),
    ),
]


def is_expression(value: str) -> bool:
    stripped = value.lstrip()
    return stripped.startswith("=") or "{{" in value or "$credentials" in value or "$env" in value


def is_sensitive_name(name: str) -> bool:
    return bool(SENSITIVE_NAME.search(name)) and not bool(SAFE_TYPE_NAME.search(name))


def redact_patterns(value: str, stats: dict[str, int]) -> str:
    result = value
    for label, pattern in SECRET_PATTERNS:
        result, count = pattern.subn(PLACEHOLDER, result)
        stats[label] = stats.get(label, 0) + count
    return result


def sanitize(value: Any, stats: dict[str, int], parent_key: str = "") -> Any:
    if isinstance(value, dict):
        cleaned: dict[str, Any] = {}
        for key, item in value.items():
            if key == "credentials" and isinstance(item, dict):
                refs: dict[str, Any] = {}
                for credential_type, ref in item.items():
                    if isinstance(ref, dict):
                        refs[credential_type] = {
                            k: (
                                CREDENTIAL_ID
                                if k == "id"
                                else CREDENTIAL_NAME
                                if k == "name"
                                else sanitize(v, stats, k)
                            )
                            for k, v in ref.items()
                        }
                    else:
                        refs[credential_type] = sanitize(ref, stats, credential_type)
                cleaned[key] = refs
                stats["credential_references"] = stats.get("credential_references", 0) + len(refs)
                continue
            if (
                isinstance(item, str)
                and is_sensitive_name(key)
                and not is_expression(item)
            ):
                cleaned[key] = PLACEHOLDER
                stats["sensitive_keys"] = stats.get("sensitive_keys", 0) + 1
            else:
                cleaned[key] = sanitize(item, stats, key)
        name = cleaned.get("name")
        item_value = cleaned.get("value")
        if (
            isinstance(name, str)
            and is_sensitive_name(name)
            and isinstance(item_value, str)
            and not is_expression(item_value)
            and item_value != PLACEHOLDER
        ):
            cleaned["value"] = PLACEHOLDER
            stats["sensitive_named_values"] = stats.get("sensitive_named_values", 0) + 1
        return cleaned
    if isinstance(value, list):
        return [sanitize(item, stats, parent_key) for item in value]
    if isinstance(value, str):
        return redact_patterns(value, stats)
    return value


def validation_errors(value: Any, path: tuple[str, ...] = ()) -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        name = value.get("name")
        item_value = value.get("value")
        if (
            isinstance(name, str)
            and is_sensitive_name(name)
            and isinstance(item_value, str)
            and not is_expression(item_value)
            and item_value != PLACEHOLDER
        ):
            errors.append("literal sensitive parameter at " + ".".join(path))
        for key, item in value.items():
            if (
                isinstance(item, str)
                and is_sensitive_name(key)
                and not is_expression(item)
                and item != PLACEHOLDER
            ):
                errors.append("literal sensitive key at " + ".".join(path + (key,)))
            errors.extend(validation_errors(item, path + (key,)))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(validation_errors(item, path + (str(index),)))
    elif isinstance(value, str):
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(value):
                errors.append(f"{label} pattern at {'.'.join(path)}")
    return errors


def load_workflows(directory: Path) -> list[tuple[Path, dict[str, Any]]]:
    workflows = []
    for path in sorted(directory.glob("*.json")):
        if path.name == "manifest.json":
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("nodes"), list):
            raise ValueError(f"{path.name}: not an n8n workflow document")
        if not isinstance(data.get("connections"), dict):
            raise ValueError(f"{path.name}: missing connections object")
        workflows.append((path, data))
    if not workflows:
        raise ValueError("no workflow JSON files found")
    return workflows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path, nargs="?")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    workflows = load_workflows(args.source)
    if args.check_only:
        all_errors = []
        for source_path, workflow in workflows:
            all_errors.extend(
                f"{source_path.name}: {error}"
                for error in validation_errors(workflow)
            )
        if all_errors:
            print("\n".join(all_errors), file=sys.stderr)
            return 2
        print(f"Security check passed for {len(workflows)} workflows")
        return 0

    if args.destination is None:
        parser.error("destination is required unless --check-only is used")
    if args.destination.exists():
        shutil.rmtree(args.destination)
    args.destination.mkdir(parents=True)

    manifest: list[dict[str, Any]] = []
    total_stats: dict[str, int] = {}
    all_errors: list[str] = []

    for source_path, workflow in workflows:
        stats: dict[str, int] = {}
        cleaned = sanitize(workflow, stats)
        errors = validation_errors(cleaned)
        all_errors.extend(f"{source_path.name}: {error}" for error in errors)
        output_path = args.destination / source_path.name
        output_path.write_text(
            json.dumps(cleaned, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        manifest.append(
            {
                "id": cleaned.get("id"),
                "name": cleaned.get("name"),
                "active": cleaned.get("active", False),
                "archived": cleaned.get("isArchived", False),
                "file": source_path.name,
                "redactions": sum(stats.values()),
            }
        )
        for key, count in stats.items():
            total_stats[key] = total_stats.get(key, 0) + count

    if all_errors:
        print("\n".join(all_errors), file=sys.stderr)
        return 2

    (args.destination / "manifest.json").write_text(
        json.dumps(
            {
                "workflowCount": len(manifest),
                "workflows": manifest,
                "redactionCounts": total_stats,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"Sanitized {len(manifest)} workflows; "
        f"redactions={sum(total_stats.values())}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env bash
set -Eeuo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONTAINER="${N8N_CONTAINER:-n8n}"
CONTAINER_TMP="/tmp/n8n-git-workflows"
HOST_TMP="$(mktemp -d /tmp/n8n-git-backup.XXXXXX)"
LOCK_FILE="/tmp/n8n-git-backup.lock"

cleanup() {
  docker exec "$CONTAINER" rm -rf "$CONTAINER_TMP" >/dev/null 2>&1 || true
  rm -rf "$HOST_TMP"
}
trap cleanup EXIT

exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  echo "Another n8n Git backup is already running" >&2
  exit 3
fi

docker inspect "$CONTAINER" >/dev/null
docker exec "$CONTAINER" rm -rf "$CONTAINER_TMP"
docker exec "$CONTAINER" mkdir -p "$CONTAINER_TMP"
docker exec "$CONTAINER" n8n export:workflow --backup --output="$CONTAINER_TMP/"
mkdir -p "$HOST_TMP/raw"
docker cp "$CONTAINER:$CONTAINER_TMP/." "$HOST_TMP/raw/" >/dev/null

python3 "$REPO_ROOT/scripts/sanitize_workflows.py"   "$HOST_TMP/raw" "$HOST_TMP/sanitized"

source_count="$(find "$HOST_TMP/raw" -maxdepth 1 -type f -name '*.json' | wc -l)"
manifest_count="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["workflowCount"])' "$HOST_TMP/sanitized/manifest.json")"
if [[ "$source_count" -ne "$manifest_count" ]]; then
  echo "Workflow count mismatch: source=$source_count manifest=$manifest_count" >&2
  exit 4
fi

next_dir="$REPO_ROOT/workflows.next"
rm -rf "$next_dir"
mkdir -p "$next_dir"
cp -a "$HOST_TMP/sanitized/." "$next_dir/"
python3 "$REPO_ROOT/scripts/sanitize_workflows.py" --check-only "$next_dir"
rm -rf "$REPO_ROOT/workflows"
mv "$next_dir" "$REPO_ROOT/workflows"

git -C "$REPO_ROOT" add   .gitignore README.md deploy scripts workflows docs/governance

if git -C "$REPO_ROOT" diff --cached --quiet; then
  echo "No sanitized workflow changes to commit"
  exit 0
fi

git -C "$REPO_ROOT" commit -m "chore: update sanitized n8n workflows $(date +%F)"
git -C "$REPO_ROOT" push origin main

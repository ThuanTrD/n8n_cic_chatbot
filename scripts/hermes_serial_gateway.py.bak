#!/usr/bin/env python3
"""Bounded serial HTTP gateway for Hermes model requests."""

from __future__ import annotations

import json
import os
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import ClassVar

BIND_HOST = os.getenv("HERMES_GATEWAY_BIND", "172.18.0.1")
PORT = int(os.getenv("HERMES_GATEWAY_PORT", "18644"))
TARGET_ORIGIN = os.getenv(
    "HERMES_TARGET_ORIGIN",
    "https://league-providing-smoking-upc.trycloudflare.com",
).rstrip("/")
CONCURRENCY = int(os.getenv("HERMES_GATEWAY_CONCURRENCY", "1"))
MAX_QUEUE = int(os.getenv("HERMES_GATEWAY_MAX_QUEUE", "20"))
QUEUE_TIMEOUT = float(os.getenv("HERMES_GATEWAY_QUEUE_TIMEOUT", "480"))
UPSTREAM_TIMEOUT = float(os.getenv("HERMES_GATEWAY_UPSTREAM_TIMEOUT", "300"))
MAX_BODY_BYTES = int(os.getenv("HERMES_GATEWAY_MAX_BODY_BYTES", str(2 * 1024 * 1024)))
MAX_RESPONSE_BYTES = int(
    os.getenv("HERMES_GATEWAY_MAX_RESPONSE_BYTES", str(16 * 1024 * 1024))
)

ALLOWED_REQUEST_HEADERS = {
    "authorization",
    "content-type",
    "accept",
    "user-agent",
    "x-api-key",
    "api-key",
}
ALLOWED_PATHS = {"/v1/chat/completions", "/v1/models"}


class QueueState:
    def __init__(self) -> None:
        self.gate = threading.BoundedSemaphore(CONCURRENCY)
        self.lock = threading.Lock()
        self.waiting = 0
        self.active = 0
        self.completed = 0

    def acquire(self) -> tuple[bool, str]:
        with self.lock:
            if self.waiting >= MAX_QUEUE:
                return False, "queue_full"
            self.waiting += 1
        acquired = self.gate.acquire(timeout=QUEUE_TIMEOUT)
        with self.lock:
            self.waiting -= 1
            if acquired:
                self.active += 1
        return acquired, "acquired" if acquired else "queue_timeout"

    def release(self) -> None:
        with self.lock:
            self.active -= 1
            self.completed += 1
        self.gate.release()

    def snapshot(self) -> dict[str, int]:
        with self.lock:
            return {
                "active": self.active,
                "waiting": self.waiting,
                "completed": self.completed,
                "concurrency": CONCURRENCY,
                "maxQueue": MAX_QUEUE,
            }


STATE = QueueState()


class HermesGatewayHandler(BaseHTTPRequestHandler):
    server_version = "HermesSerialGateway/1.0"
    protocol_version = "HTTP/1.1"

    def log_message(self, _format: str, *_args: object) -> None:
        return

    def send_json(self, status: int, value: dict[str, object]) -> None:
        body = json.dumps(value, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = urllib.parse.urlsplit(self.path).path
        if path == "/health":
            self.send_json(200, {"status": "ok", **STATE.snapshot()})
            return
        if path != "/v1/models":
            self.send_json(404, {"error": "not_found"})
            return
        self.forward_request(b"")

    def do_POST(self) -> None:
        path = urllib.parse.urlsplit(self.path).path
        if path != "/v1/chat/completions":
            self.send_json(404, {"error": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_json(400, {"error": "invalid_content_length"})
            return
        if length <= 0:
            self.send_json(400, {"error": "empty_body"})
            return
        if length > MAX_BODY_BYTES:
            self.send_json(413, {"error": "body_too_large"})
            return
        self.forward_request(self.rfile.read(length))

    def forward_request(self, body: bytes) -> None:
        acquired, reason = STATE.acquire()
        if not acquired:
            status = 429 if reason == "queue_full" else 503
            self.send_json(status, {"error": reason})
            return
        started = time.monotonic()
        try:
            split = urllib.parse.urlsplit(self.path)
            target = TARGET_ORIGIN + split.path
            if split.query:
                target += "?" + split.query
            headers = {
                name: value
                for name, value in self.headers.items()
                if name.lower() in ALLOWED_REQUEST_HEADERS
            }
            request = urllib.request.Request(
                target,
                data=body if self.command == "POST" else None,
                headers=headers,
                method=self.command,
            )
            try:
                with urllib.request.urlopen(request, timeout=UPSTREAM_TIMEOUT) as response:
                    payload = response.read(MAX_RESPONSE_BYTES + 1)
                    if len(payload) > MAX_RESPONSE_BYTES:
                        self.send_json(502, {"error": "upstream_response_too_large"})
                        return
                    self.send_response(response.status)
                    self.send_header(
                        "Content-Type",
                        response.headers.get("Content-Type", "application/json"),
                    )
                    self.send_header("Content-Length", str(len(payload)))
                    self.send_header("Cache-Control", "no-store")
                    self.end_headers()
                    self.wfile.write(payload)
            except urllib.error.HTTPError as error:
                payload = error.read(MAX_RESPONSE_BYTES)
                self.send_response(error.code)
                self.send_header(
                    "Content-Type",
                    error.headers.get("Content-Type", "application/json"),
                )
                self.send_header("Content-Length", str(len(payload)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(payload)
            except (urllib.error.URLError, TimeoutError):
                self.send_json(502, {"error": "upstream_unavailable"})
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            STATE.release()
            _elapsed = time.monotonic() - started


class BoundedThreadingHTTPServer(ThreadingHTTPServer):
    daemon_threads: ClassVar[bool] = True
    request_queue_size: ClassVar[int] = MAX_QUEUE + CONCURRENCY


def main() -> None:
    if CONCURRENCY < 1 or MAX_QUEUE < 0:
        raise SystemExit("Invalid gateway concurrency configuration")
    server = BoundedThreadingHTTPServer((BIND_HOST, PORT), HermesGatewayHandler)
    server.serve_forever(poll_interval=0.25)


if __name__ == "__main__":
    main()

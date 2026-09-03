#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class MockState:
    lock = threading.Lock()
    active = 0
    max_active = 0


class MockHandler(BaseHTTPRequestHandler):
    def log_message(self, _format: str, *_args: object) -> None:
        return

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        self.rfile.read(length)
        with MockState.lock:
            MockState.active += 1
            MockState.max_active = max(MockState.max_active, MockState.active)
        time.sleep(0.2)
        with MockState.lock:
            MockState.active -= 1
        body = b'{"ok":true}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def request(url: str, body: bytes = b'{"model":"test"}') -> int:
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer test"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            response.read()
            return response.status
    except urllib.error.HTTPError as error:
        error.read()
        return error.code


def main() -> None:
    upstream_port = free_port()
    gateway_port = free_port()
    upstream = ThreadingHTTPServer(("127.0.0.1", upstream_port), MockHandler)
    upstream_thread = threading.Thread(target=upstream.serve_forever, daemon=True)
    upstream_thread.start()

    script = Path(__file__).resolve().parents[1] / "scripts" / "hermes_serial_gateway.py"
    env = {
        **os.environ,
        "HERMES_GATEWAY_BIND": "127.0.0.1",
        "HERMES_GATEWAY_PORT": str(gateway_port),
        "HERMES_TARGET_ORIGIN": f"http://127.0.0.1:{upstream_port}",
        "HERMES_GATEWAY_CONCURRENCY": "1",
        "HERMES_GATEWAY_MAX_QUEUE": "20",
        "HERMES_GATEWAY_QUEUE_TIMEOUT": "5",
        "HERMES_GATEWAY_UPSTREAM_TIMEOUT": "5",
        "HERMES_GATEWAY_MAX_BODY_BYTES": "1024",
    }
    gateway = subprocess.Popen([sys.executable, str(script)], env=env)
    try:
        health = f"http://127.0.0.1:{gateway_port}/health"
        for _ in range(50):
            try:
                with urllib.request.urlopen(health, timeout=0.2) as response:
                    if response.status == 200:
                        break
            except Exception:
                time.sleep(0.05)
        else:
            raise AssertionError("gateway did not start")

        url = f"http://127.0.0.1:{gateway_port}/v1/chat/completions"
        statuses: list[int] = []
        threads = [
            threading.Thread(target=lambda: statuses.append(request(url)))
            for _ in range(5)
        ]
        started = time.monotonic()
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        elapsed = time.monotonic() - started

        assert sorted(statuses) == [200] * 5, statuses
        assert MockState.max_active == 1, MockState.max_active
        assert elapsed >= 0.9, elapsed
        assert request(url, b"x" * 1025) == 413

        with urllib.request.urlopen(health, timeout=1) as response:
            metrics = json.loads(response.read())
        assert metrics["concurrency"] == 1
        assert metrics["completed"] == 5
        print(
            f"passed requests=5 max_active={MockState.max_active} "
            f"elapsed={elapsed:.2f}s oversize=413"
        )
    finally:
        gateway.terminate()
        try:
            gateway.wait(timeout=3)
        except subprocess.TimeoutExpired:
            gateway.kill()
        upstream.shutdown()


if __name__ == "__main__":
    main()

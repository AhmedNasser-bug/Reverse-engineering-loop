"""
Real-Time Web Dashboard Server for Reverse Engineering Loop Harness.
Provides REST API, Server-Sent Events (SSE) streaming, OpenUI component serving,
and Human-in-the-Loop invariant approval (Stage 2 & 4).
Runs out-of-the-box using Python's standard library with zero external dependencies.
"""

import os
import sys
import json
import time
import mimetypes
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import parse_qs, urlparse

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = Path(__file__).resolve().parent / "static"
LOOP_ENG_DIR = PROJECT_ROOT / "02-loop-engineering"

# Import LoopManager dynamically
from importlib.machinery import SourceFileLoader
loop_mgr_file = str(LOOP_ENG_DIR / "loop_manager.py")
loop_module = SourceFileLoader("loop_manager", loop_mgr_file).load_module()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/status":
            self._handle_status()
        elif path == "/api/rubric":
            self._handle_rubric()
        elif path == "/api/events":
            self._handle_sse_events()
        else:
            # Serve static files from static directory
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else ""
        payload = json.loads(body) if body else {}

        if path == "/api/approve":
            self._handle_approve(payload)
        elif path == "/api/step":
            self._handle_step()
        elif path == "/api/reset":
            self._handle_reset()
        else:
            self.send_response(404)
            self.end_headers()

    def _send_json(self, data: dict, status_code: int = 200):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def _handle_status(self):
        lm = loop_module.LoopManager()
        data = {
            "state": lm.state,
            "config": lm.loop_config,
            "server_time": time.time()
        }
        self._send_json(data)

    def _handle_rubric(self):
        rubric_file = LOOP_ENG_DIR / "RUBRIC.md"
        content = rubric_file.read_text(encoding="utf-8") if rubric_file.exists() else "No rubric found."
        self._send_json({"rubric": content})

    def _handle_approve(self, payload: dict):
        approver = payload.get("approver", "human_web_user")
        lm = loop_module.LoopManager()
        lm.approve_invariant(approved_by=approver)
        self._send_json({"status": "SUCCESS", "message": f"Invariant approved by {approver}."})

    def _handle_step(self):
        lm = loop_module.LoopManager()
        try:
            result = lm.run_iteration()
            self._send_json({"status": "SUCCESS", "iteration_result": result, "state": lm.state})
        except Exception as e:
            self._send_json({"status": "ERROR", "message": str(e)}, status_code=400)

    def _handle_reset(self):
        lm = loop_module.LoopManager()
        lm.state["status"] = "READY"
        lm.state["current_iteration"] = 0
        lm.state["cumulative_cost_usd"] = 0.00
        lm.state["latest_rubric_score"] = 0.00
        lm.state["iterations"] = []
        lm._save_state()
        self._send_json({"status": "RESET", "state": lm.state})

    def _handle_sse_events(self):
        """Streams real-time Server-Sent Events to connected web clients."""
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        lm = loop_module.LoopManager()
        # Initial state event
        event_payload = json.dumps({"type": "STATE_UPDATE", "data": lm.state})
        self.wfile.write(f"data: {event_payload}\n\n".encode("utf-8"))
        self.wfile.flush()


def run_dashboard_server(port: int = 8080):
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    server_address = ("127.0.0.1", port)
    httpd = ThreadedHTTPServer(server_address, DashboardHandler)
    print(f"\n========================================================")
    print(f"  REVERSE ENGINEERING LOOP - REAL-TIME WEB DASHBOARD")
    print(f"  URL: http://127.0.0.1:{port}")
    print(f"  Press Ctrl+C to terminate.")
    print(f"========================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_dashboard_server(port)

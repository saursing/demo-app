"""Hello-world web app for the EKS DevSecOps demo (standard library only)."""

import json
import os
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VERSION = os.environ.get("APP_VERSION", "dev")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/healthz":
            code, body, ctype = 200, "ok\n", "text/plain"
        elif self.path == "/":
            payload = {"message": "Hello, World!", "version": VERSION, "pod": socket.gethostname()}
            code, body, ctype = 200, json.dumps(payload) + "\n", "application/json"
        else:
            code, body, ctype = 404, "not found\n", "text/plain"
        data = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    print(f"demo-app {VERSION} listening on :8080", flush=True)
    ThreadingHTTPServer(("", 8080), Handler).serve_forever()

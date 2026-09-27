"""Small local-only HTTP target used for the authorized engineering demo."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"""<!doctype html><html><head><title>IK Systems Local Demo</title></head><body><h1>Authorized Extraction Demo</h1><p>Local test target.</p></body></html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


def create_server(port: int = 8765):
    return ThreadingHTTPServer(("127.0.0.1", port), DemoHandler)

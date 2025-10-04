#!/usr/bin/env python3
"""Simple HTTP healthcheck server that probes backend and streamlit and returns 200 only when both are healthy."""
import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests

BACKEND_HEALTH = os.environ.get('BACKEND_HEALTH', 'http://127.0.0.1:8081/health')
STREAMLIT_URL = os.environ.get('STREAMLIT_URL', 'http://127.0.0.1:8501/app/')
PORT = int(os.environ.get('HEALTH_PORT', '8090'))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        backend_status = None
        streamlit_status = None
        try:
            r1 = requests.get(BACKEND_HEALTH, timeout=2)
            backend_status = r1.status_code
        except Exception:
            backend_status = None
        try:
            r2 = requests.get(STREAMLIT_URL, timeout=2, allow_redirects=True)
            streamlit_status = r2.status_code
        except Exception:
            streamlit_status = None

        ok_backend = backend_status is not None and backend_status < 400
        ok_streamlit = streamlit_status is not None and streamlit_status < 400

        if ok_backend and ok_streamlit:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(503)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            payload = {'backend_status': backend_status, 'streamlit_status': streamlit_status}
            self.wfile.write(json.dumps(payload).encode())


def run():
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    print(f'Healthcheck listening on 0.0.0.0:{PORT}, checking {BACKEND_HEALTH} and {STREAMLIT_URL}')
    server.serve_forever()


if __name__ == '__main__':
    run()

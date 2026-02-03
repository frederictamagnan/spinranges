#!/usr/bin/env python3
"""Simple HTTP server to serve the web folder."""

import http.server
import socketserver
import os
import webbrowser

PORT = 8000
WEB_DIR = "web"

os.chdir(WEB_DIR)

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    url = f"http://localhost:{PORT}"
    print(f"Serving at {url}")
    print("Press Ctrl+C to stop")
    webbrowser.open(url)
    httpd.serve_forever()

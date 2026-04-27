"""
Simple HTTP server to serve PestVid frontend
"""
import http.server
import socketserver
import os

PORT = 8080
DIRECTORY = "public"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

os.chdir(DIRECTORY)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving PestVid frontend at http://localhost:{PORT}")
    print(f"API server is running at http://localhost:5000")
    print(f"Press Ctrl+C to stop")
    httpd.serve_forever()
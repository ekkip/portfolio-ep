#!/usr/bin/env python3
"""
Development server with no-cache headers for CSS files
"""
import http.server
import socketserver
from pathlib import Path

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add no-cache headers for CSS files
        if self.path.endswith('.css'):
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        super().end_headers()

if __name__ == '__main__':
    PORT = 8000
    Handler = NoCacheHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Server running at http://localhost:{PORT}/")
        print("CSS files will be served with no-cache headers")
        print("Press Ctrl+C to stop")
        httpd.serve_forever()

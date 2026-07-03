#!/usr/bin/env python3
"""
ICN Blog — Local Development Server
Run: python serve.py
Then open: http://localhost:8080
"""

import http.server
import socketserver
import os
import sys
import webbrowser
from pathlib import Path

# Configuration
PORT = 8080
HOST = 'localhost'
DIRECTORY = Path(__file__).parent

class ICNBlogHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler with proper MIME types and caching."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)
    
    def end_headers(self):
        # Add CORS headers for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Pretty logging
        status_code = args[1] if len(args) > 1 else ''
        color = '\033[92m' if '200' in str(status_code) else '\033[93m'
        reset = '\033[0m'
        sys.stdout.write(f"{color}[{status_code}]{reset} {args[0]}\n")

def main():
    """Start the development server."""
    
    # Check if directory exists
    if not (DIRECTORY / 'index.html').exists():
        print("❌ Error: index.html not found!")
        print(f"   Make sure you're in the icn-blog directory.")
        sys.exit(1)
    
    try:
        with socketserver.TCPServer((HOST, PORT), ICNBlogHandler) as httpd:
            url = f"http://{HOST}:{PORT}"
            
            print("=" * 50)
            print("   🖥️  ICN Blog — Development Server")
            print("=" * 50)
            print(f"   📂 Serving: {DIRECTORY}")
            print(f"   🌐 URL: {url}")
            print(f"   🔧 Press Ctrl+C to stop")
            print("=" * 50)
            
            # Open browser automatically
            webbrowser.open(url)
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped.")
        sys.exit(0)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {PORT} is already in use!")
            print(f"   Try: python serve.py --port {PORT + 1}")
        else:
            print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='ICN Blog Development Server')
    parser.add_argument('--port', type=int, default=PORT, help='Port to listen on')
    args = parser.parse_args()
    PORT = args.port
    main()
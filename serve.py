#!/usr/bin/env python3
"""
ICN Blog — Local Development Server
Run: python serve.py
Then open: http://localhost:8080
"""

import http.server
import json
import socketserver
import sys
import webbrowser
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

# Configuration
PORT = 8080
HOST = 'localhost'
DIRECTORY = Path(__file__).parent
CONTACT_MESSAGES_FILE = DIRECTORY / 'contact-messages.jsonl'


class ICNBlogHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler with proper MIME types, caching, and basic contact form support."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/api/contact':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            payload = json.loads(body)
            result = save_contact_message(payload)
            self.send_response(200 if result['saved'] else 500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

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


def save_contact_message(payload, output_path=None):
    """Persist a portfolio contact message to a JSONL file."""
    if output_path is None:
        output_path = CONTACT_MESSAGES_FILE

    record = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'name': (payload.get('name') or '').strip(),
        'email': (payload.get('email') or '').strip(),
        'subject': (payload.get('subject') or '').strip(),
        'message': (payload.get('message') or '').strip(),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open('a', encoding='utf-8') as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + '\n')

    return {'saved': True, 'message': 'Contact message received', 'file': str(output_path)}


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
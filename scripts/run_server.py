import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PORT = 5173
DIST_DIR = Path(__file__).resolve().parent.parent / "web" / "dist"

if not DIST_DIR.exists():
    print(f"Error: {DIST_DIR} not found. Please build the web project first.")
    sys.exit(1)

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST_DIR), **kwargs)

    def end_headers(self):
        # Enable CORS and UTF-8
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

def main():
    print("=" * 60)
    print("📖 মুফাস্সির ক্লাস নোট ওয়েবসাইট (তাফসীরুল জালালাইন)")
    print(f"অনুবাদ ও তাহকীক: মুফতী মুহাম্মাদ মুহিব্বুল্লাহ")
    print(f"প্রকাশক: মাকতাবাতুল ইসহাক, ঢাকা")
    print("=" * 60)
    print(f"লোকাল সার্ভার চালু হচ্ছে: http://localhost:{PORT}")
    print("ব্রাউজারে ওয়েবসাইট ওপেন করা হচ্ছে...")
    print("সার্ভার বন্ধ করতে Ctrl + C চাপুন।")
    print("=" * 60)

    # Open browser automatically
    webbrowser.open(f"http://localhost:{PORT}")

    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nসার্ভার বন্ধ করা হয়েছে।")

if __name__ == "__main__":
    main()

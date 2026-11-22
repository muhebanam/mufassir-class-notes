import http.server
import socketserver
import threading
import urllib.request
import json
import time
from pathlib import Path

PORT = 9005
web_dir = Path(r"d:\আমার গবেষণা\জালালাইন\web\dist")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(web_dir), **kwargs)
    def log_message(self, format, *args):
        pass

httpd = socketserver.TCPServer(("127.0.0.1", PORT), Handler)
t = threading.Thread(target=httpd.serve_forever, daemon=True)
t.start()

time.sleep(0.5)

try:
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/") as r:
        html = r.read().decode("utf-8")
        assert 'id="root"' in html
        print("✓ 1. index.html OK (HTTP 200)")

    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/data/surahs.json") as r:
        surahs = json.loads(r.read().decode("utf-8"))
        assert len(surahs) == 91
        print(f"✓ 2. surahs.json OK (91/91 surahs served)")

    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/data/24/ruku-5.json") as r:
        r5 = json.loads(r.read().decode("utf-8"))
        assert len(r5["ayahs"]) == 9
        a35 = [a for a in r5["ayahs"] if a["ayah"] == 35][0]
        assert "نُورِهِ" in a35["text_uthmani"]
        print(f"✓ 3. ruku-5.json OK (Ayah 35 Uthmani: {a35['text_uthmani'][:45]}...)")

    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/data/search_index.json") as r:
        s_idx = json.loads(r.read().decode("utf-8"))
        assert len(s_idx) == 3445
        print(f"✓ 4. search_index.json OK (3,445/3,445 verses indexed)")

    print("ALL 4 HTTP SERVER VERIFICATION CHECKS PASSED 100%!")
finally:
    httpd.shutdown()

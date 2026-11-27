# -*- coding: utf-8 -*-
"""
Surah 25 (Al-Furqan) harvest via tafsir-center MCP + Turath archive.
Usage:
  python scripts/harvest_surah25_nuzul.py <start> <end>
  python scripts/harvest_surah25_nazm.py <start> <end>
Outputs raw MCP responses into _work/s025/mcp/*.json
"""
import json, ssl, sys, time, urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUT = BASE_DIR / "_work" / "s025" / "mcp"
OUT.mkdir(parents=True, exist_ok=True)

ctx = ssl._create_unverified_context()
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "User-Agent": "Antigravity/1.0",
}

def call_mcp(name, arguments):
    payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
               "params": {"name": name, "arguments": arguments}}
    req = urllib.request.Request("https://mcp.tafsir.net/mcp",
                                 data=json.dumps(payload).encode("utf-8"), headers=HEADERS)
    for attempt in range(3):
        try:
            resp = urllib.request.urlopen(req, context=ctx, timeout=90)
            text = resp.read().decode("utf-8")
            for line in text.splitlines():
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    return json.loads(data["result"]["content"][0]["text"])
        except Exception as e:
            print(f"  retry {attempt+1} {name} {arguments}: {e}", flush=True)
            time.sleep(2)
    return None

def save(fname, obj):
    (OUT / fname).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")

def run(start, end):
    for a in range(start, end + 1):
        f = OUT / f"ayah_{a:02d}.json"
        if f.exists():
            print(f"ayah {a}: cached", flush=True)
            continue
        bundle = {}
        t0 = time.time()
        bundle["nuzool"] = call_mcp("fetch_nuzool_reason", {"surah": 25, "ayah": a})
        bundle["mathur"] = call_mcp("fetch_tafsir", {"surah": 25, "ayah": a, "sources": ["mathur"]})
        bundle["ibn_ashur"] = call_mcp("fetch_tafsir", {"surah": 25, "ayah": a, "sources": ["ibn_ashur"]})
        bundle["razi"] = call_mcp("fetch_tafsir", {"surah": 25, "ayah": a, "sources": ["razi"]})
        save(f"ayah_{a:02d}.json", bundle)
        print(f"ayah {a}: done in {time.time()-t0:.1f}s", flush=True)

if __name__ == "__main__":
    s = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    e = int(sys.argv[2]) if len(sys.argv) > 2 else 77
    run(s, e)
    print("HARVEST DONE", s, e)

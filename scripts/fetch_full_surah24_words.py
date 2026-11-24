#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetch complete word-by-word data for all 64 ayahs of Surah 24 from the Medina Munawwara Bahouth Database.
Saves to reference/surah24_full_words.json.
"""

import json
import ssl
import sys
import time
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "reference" / "surah24_full_words.json"
URL = "https://bahouth.tafsir.net/mcp"
CTX = ssl._create_unverified_context()

def call_bahouth_words(surah: int, ayah: int, max_retries=3):
    payload = {
        "jsonrpc": "2.0",
        "id": int(time.time() * 1000) % 1000000,
        "method": "tools/call",
        "params": {
            "name": "list_verse_words",
            "arguments": {"verse_key": f"{surah}-{ayah}"}
        }
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "text/event-stream, application/json",
            "User-Agent": "Antigravity/2.0"
        }
    )

    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, context=CTX, timeout=12) as resp:
                raw_resp = resp.read().decode("utf-8")
                resp_json = json.loads(raw_resp)
                if "result" in resp_json and "content" in resp_json["result"]:
                    content_list = resp_json["result"]["content"]
                    if content_list and content_list[0].get("type") == "text":
                        return json.loads(content_list[0]["text"])
                return resp_json.get("result", {})
        except Exception as e:
            time.sleep(1 + attempt)
            if attempt == max_retries - 1:
                print(f"[WARN] Error fetching {surah}:{ayah}: {e}", file=sys.stderr)
                return {}

def main():
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            all_words = json.load(f)
    else:
        all_words = {}

    print("Fetching complete word list for Surah 24 (64 ayahs)...")
    total_words = 0
    for a in range(1, 65):
        v_key = f"24:{a}"
        if v_key in all_words and len(all_words[v_key]) > 0:
            words = all_words[v_key]
        else:
            res = call_bahouth_words(24, a)
            words = res.get("words", [])
            all_words[v_key] = words
            time.sleep(0.08)
        
        total_words += len(words)
        print(f"  Ayah {a:02d}: {len(words)} words")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_words, f, ensure_ascii=False, indent=2)

    print(f"\n[SUCCESS] Saved all {len(all_words)} ayahs ({total_words} total words) to {OUTPUT_FILE.name}")

if __name__ == "__main__":
    main()

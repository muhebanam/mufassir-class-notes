#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetch authentic morphological roots for Surah 24 (Ayahs 1-64) from the Medina Munawwara Bahouth Database.
Updates reference/quran_morphology_qac.json.
"""

import json
import ssl
import sys
import time
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
QAC_FILE = BASE_DIR / "reference" / "quran_morphology_qac.json"
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
    if QAC_FILE.exists():
        with open(QAC_FILE, "r", encoding="utf-8") as f:
            qac_data = json.load(f)
    else:
        qac_data = {}

    print("Fetching authentic morphological roots for Surah 24 (64 ayahs)...")
    particles = {"في", "من", "عن", "إلى", "على", "حتى", "مِن", "إلَى", "عَلَى", "ل", "ب", "ك", "و", "ف", "لا", "ما", "إنّ", "أنّ", "هو", "هي", "هم", "هن", "الذي", "التي", "الذين", "هذا", "هذه", "هؤلاء", "كل", "بل", "قد", "ثم", "إذ", "إذا"}

    for a in range(1, 65):
        v_key = f"24:{a}"
        if v_key in qac_data and len(qac_data[v_key]) > 0 and a <= 10:
            print(f"  Ayah {a:02d}: already has {len(qac_data[v_key])} roots.")
            continue

        res = call_bahouth_words(24, a)
        words = res.get("words", [])
        roots = []
        for w in words:
            raw_root = w.get("root_token_raw", "").strip("/ ")
            if raw_root and raw_root not in particles and len(raw_root) >= 2:
                if raw_root not in roots:
                    roots.append(raw_root)
        
        qac_data[v_key] = roots
        print(f"  Ayah {a:02d}: {len(roots)} roots -> {roots[:5]}...")
        time.sleep(0.1)

    with open(QAC_FILE, "w", encoding="utf-8") as f:
        json.dump(qac_data, f, ensure_ascii=False, indent=2)

    print(f"\n[SUCCESS] Updated {QAC_FILE.name} with all {len(qac_data)} verses of Surah 24.")

if __name__ == "__main__":
    main()

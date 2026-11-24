#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update reference/quran_morphology_qac.json with all roots present in reference/surah24_full_words.json.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
QAC_FILE = BASE_DIR / "reference" / "quran_morphology_qac.json"
FULL_WORDS_FILE = BASE_DIR / "reference" / "surah24_full_words.json"

with open(QAC_FILE, "r", encoding="utf-8") as f:
    qac = json.load(f)

with open(FULL_WORDS_FILE, "r", encoding="utf-8") as f:
    full_words = json.load(f)

updated_count = 0
for v_key, words in full_words.items():
    roots_in_v = list(qac.get(v_key, []))
    for w in words:
        r = w.get("root_token_raw", "").strip("/ ")
        if r and len(r) >= 2 and r not in roots_in_v:
            roots_in_v.append(r)
            updated_count += 1
    qac[v_key] = roots_in_v

with open(QAC_FILE, "w", encoding="utf-8") as f:
    json.dump(qac, f, ensure_ascii=False, indent=2)

print(f"Updated qac.json with {updated_count} additional roots across {len(qac)} verses.")

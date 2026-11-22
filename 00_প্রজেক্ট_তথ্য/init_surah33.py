# -*- coding: utf-8 -*-
"""
Initialize Surah 33 (Al-Ahzab)
Set up directory, ruku_map.json, and print statistics.
"""

import json
from pathlib import Path

output_path = r'C:/Users/USER/.gemini/antigravity/brain/7caaeec8-bdfa-40da-93eb-62b94af954b1/.system_generated/steps/3211/output.txt'
with open(output_path, 'r', encoding='utf-8') as f:
    d = json.load(f)

v_all = d['verses']
total_verses = len(v_all)
total_words = sum(v['word_count'] for v in v_all)
total_letters = sum(v['letter_count'] for v in v_all)

print(f"Surah 33 (Al-Ahzab): {total_verses} Verses, {total_words} Words, {total_letters} Letters.")

# Standard rukus for Surah 33 (9 rukus):
ruku_ranges = [
    (1, 1, 8),
    (2, 9, 20),
    (3, 21, 27),
    (4, 28, 34),
    (5, 35, 40),
    (6, 41, 52),
    (7, 53, 58),
    (8, 59, 68),
    (9, 69, 73)
]

ruku_list = []
for r_no, s, e in ruku_ranges:
    rv = [v for v in v_all if s <= v['ayah_number'] <= e]
    w = sum(v['word_count'] for v in rv)
    l = sum(v['letter_count'] for v in rv)
    ruku_info = {
        "ruku_number": r_no,
        "ayah_start": s,
        "ayah_end": e,
        "total_ayahs": len(rv),
        "total_words": w,
        "total_letters": l,
        "file_name": f"রুকু-{r_no:02d}_আয়াত_{s}-{e}.md"
    }
    ruku_list.append(ruku_info)
    print(f"Ruku {r_no:02d}: Ayahs {s:02d}-{e:02d} | {len(rv)} ayahs | {w} words | {l} letters")

# Update ruku_map.json
with open('00_প্রজেক্ট_তথ্য/ruku_map.json', 'r', encoding='utf-8') as f:
    m = json.load(f)

m['surahs']['33'] = {
    "surah_id": 33,
    "name_ar": "الأحزاب",
    "name_bn": "আল-আহযাব",
    "total_ayahs": 73,
    "total_rukus": 9,
    "total_words": total_words,
    "total_letters": total_letters,
    "rukus": ruku_list
}

with open('00_প্রজেক্ট_তথ্য/ruku_map.json', 'w', encoding='utf-8') as f:
    json.dump(m, f, ensure_ascii=False, indent=2)

# Create directory structure for Surah 33
s33_dir = Path('৩৩_সূরা_আল-আহযাব')
s33_sources = s33_dir / '_sources'
s33_sources.mkdir(parents=True, exist_ok=True)

print("Surah 33 initialized successfully in ruku_map.json and directories created!")

import json
import os
from pathlib import Path

step_file = r'C:/Users/USER/.gemini/antigravity/brain/7caaeec8-bdfa-40da-93eb-62b94af954b1/.system_generated/steps/2984/output.txt'
with open(step_file, encoding='utf-8') as f:
    data = json.load(f)

verses = data['verses']
print(f"Total verses: {len(verses)}")
print(f"Total words: {sum(v['word_count'] for v in verses)}")
print(f"Total letters: {sum(v['letter_count'] for v in verses)}")

# Traditional Indo-Pak Ruku boundaries for Surah 31 (Luqman):
# Ruku 1: 1-11 (11 ayahs)
# Ruku 2: 12-19 (8 ayahs) - Wasaya Luqman
# Ruku 3: 20-30 (11 ayahs) - Signs of Allah in creation & Kalimatullah
# Ruku 4: 31-34 (4 ayahs) - Ships in ocean, day of accountability & 5 keys of Ghaib

rukus_info = [
    {"ruku": 1, "start": 1, "end": 11},
    {"ruku": 2, "start": 12, "end": 19},
    {"ruku": 3, "start": 20, "end": 30},
    {"ruku": 4, "start": 31, "end": 34}
]

for r in rukus_info:
    r_verses = [v for v in verses if r["start"] <= v["ayah_number"] <= r["end"]]
    w = sum(v["word_count"] for v in r_verses)
    l = sum(v["letter_count"] for v in r_verses)
    pages = sorted(list(set(v["page_number"] for v in r_verses)))
    print(f"Ruku {r['ruku']}: Ayahs {r['start']}-{r['end']} | Count: {len(r_verses)} | Words: {w} | Letters: {l} | Pages: {pages}")

# Create directories
s31_dir = Path(r"d:\আমার গবেষণা\জালালাইন\৩১_সূরা_লুকমান")
sources_dir = s31_dir / "_sources"
sources_dir.mkdir(parents=True, exist_ok=True)
print(f"Directory ensured: {sources_dir}")

# Register in ruku_map.json
ruku_map_path = Path(r"d:\আমার গবেষণা\জালালাইন\00_প্রজেক্ট_তথ্য\ruku_map.json")
with open(ruku_map_path, 'r', encoding='utf-8') as f:
    rmap = json.load(f)

rmap.setdefault("surahs", {})
rmap["surahs"]["31"] = {
    "name_ar": "لقمان",
    "name_bn": "লুকমান",
    "total_ayahs": 34,
    "total_rukus": 4,
    "rukus": [
        {"ruku": 1, "ayah_start": 1, "ayah_end": 11, "ayah_count": 11},
        {"ruku": 2, "ayah_start": 12, "ayah_end": 19, "ayah_count": 8},
        {"ruku": 3, "ayah_start": 20, "ayah_end": 30, "ayah_count": 11},
        {"ruku": 4, "ayah_start": 31, "ayah_end": 34, "ayah_count": 4}
    ]
}

with open(ruku_map_path, 'w', encoding='utf-8') as f:
    json.dump(rmap, f, ensure_ascii=False, indent=2)

print("ruku_map.json updated with Surah 31!")

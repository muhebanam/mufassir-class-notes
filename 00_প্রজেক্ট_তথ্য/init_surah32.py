import json
from pathlib import Path

step_file = r'C:/Users/USER/.gemini/antigravity/brain/7caaeec8-bdfa-40da-93eb-62b94af954b1/.system_generated/steps/3076/output.txt'
with open(step_file, encoding='utf-8') as f:
    data = json.load(f)

verses = data['verses']
print(f"Total verses: {len(verses)}")
print(f"Total words: {sum(v['word_count'] for v in verses)}")
print(f"Total letters: {sum(v['letter_count'] for v in verses)}")

# Traditional Indo-Pak Ruku boundaries for Surah 32 (As-Sajdah):
# Ruku 1: 1-11 (11 ayahs)
# Ruku 2: 12-22 (11 ayahs) - contains Sajdah Tilawat at ayah 15
# Ruku 3: 23-30 (8 ayahs)

rukus_info = [
    {"ruku": 1, "start": 1, "end": 11},
    {"ruku": 2, "start": 12, "end": 22},
    {"ruku": 3, "start": 23, "end": 30}
]

for r in rukus_info:
    r_verses = [v for v in verses if r["start"] <= v["ayah_number"] <= r["end"]]
    w = sum(v["word_count"] for v in r_verses)
    l = sum(v["letter_count"] for v in r_verses)
    pages = sorted(list(set(v["page_number"] for v in r_verses)))
    print(f"Ruku {r['ruku']}: Ayahs {r['start']}-{r['end']} | Count: {len(r_verses)} | Words: {w} | Letters: {l} | Pages: {pages}")

# Create directories
s32_dir = Path(r"d:\আমার গবেষণা\জালালাইন\৩২_সূরা_আস-সাজদাহ")
sources_dir = s32_dir / "_sources"
sources_dir.mkdir(parents=True, exist_ok=True)
print(f"Directory ensured: {sources_dir}")

# Register in ruku_map.json
ruku_map_path = Path(r"d:\আমার গবেষণা\জালালাইন\00_প্রজেক্ট_তথ্য\ruku_map.json")
with open(ruku_map_path, 'r', encoding='utf-8') as f:
    rmap = json.load(f)

rmap.setdefault("surahs", {})
rmap["surahs"]["32"] = {
    "name_ar": "السجدة",
    "name_bn": "আস-সাজদাহ",
    "total_ayahs": 30,
    "total_rukus": 3,
    "rukus": [
        {"ruku": 1, "ayah_start": 1, "ayah_end": 11, "ayah_count": 11},
        {"ruku": 2, "ayah_start": 12, "ayah_end": 22, "ayah_count": 11, "sajdah_ayah": 15},
        {"ruku": 3, "ayah_start": 23, "ayah_end": 30, "ayah_count": 8}
    ]
}

with open(ruku_map_path, 'w', encoding='utf-8') as f:
    json.dump(rmap, f, ensure_ascii=False, indent=2)

print("ruku_map.json updated with Surah 32!")

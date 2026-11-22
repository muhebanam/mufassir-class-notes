import json
import re
from pathlib import Path

base_dir = Path(r"d:\আমার গবেষণা\জালালাইন")
with open(base_dir / "00_প্রজেক্ট_তথ্য" / "master_mcp_cache.json", "r", encoding="utf-8") as f:
    master = json.load(f)

with open(base_dir / "00_প্রজেক্ট_তথ্য" / "ruku_map.json", "r", encoding="utf-8") as f:
    ruku_map = json.load(f)["surahs"]

pages = master["turath_pages"]
v_by_s = master["verses_by_surah"]

# Let's see how many pages mention keywords or verses from Surahs 48..54
for sid in range(48, 55):
    s_info = ruku_map[str(sid)]
    rukus = s_info["rukus"]
    print(f"\nSurah {sid}: {s_info['name_bn']} ({s_info['name_ar']}) - {len(rukus)} rukus")
    for r_idx, (start_a, end_a) in enumerate(rukus, 1):
        # find matching pages
        # test first and last ayah text snippets
        first_verse = v_by_s[str(sid)][start_a - 1]["text_raw"]
        last_verse = v_by_s[str(sid)][end_a - 1]["text_raw"]
        
        # simple words
        first_words = [w for w in first_verse.split() if len(w) > 3][:3]
        
        matched_pages = []
        for p in pages:
            # check if any first words are in p['text_raw']
            txt = p["text_raw"]
            if any(w in txt for w in first_words):
                matched_pages.append((p["book_id"], p["page_id"]))
        print(f"  Ruku {r_idx} (Ayah {start_a}..{end_a}): matched {len(matched_pages)} pages in cache")

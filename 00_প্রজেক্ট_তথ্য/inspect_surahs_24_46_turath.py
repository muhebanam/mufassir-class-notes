import json
import re
from pathlib import Path

base_dir = Path(".")
ruku_map = json.load(open("00_প্রজেক্ট_তথ্য/ruku_map.json", encoding="utf-8"))["surahs"]
master = json.load(open("00_প্রজেক্ট_তথ্য/master_mcp_cache.json", encoding="utf-8"))

all_cached_tps = set((p["book_id"], p["page_id"]) for p in master["turath_pages"])

print(f"Total Turath pages in master cache: {len(all_cached_tps)}")

missing_citations = []
unwhitelisted_tids = []

for sid in range(24, 47):
    sinfo = ruku_map[str(sid)]
    sdir = base_dir / sinfo["dir_name"]
    for md_file in sdir.glob("*.md"):
        if md_file.name.startswith("00_") or "Audit" in md_file.name:
            continue
        content = md_file.read_text(encoding="utf-8")
        
        # Check citations
        pairs = re.findall(r"turath:\s*(\d+)\s*,\s*(?:page|p|পৃষ্ঠা)[:=]?\s*([০-৯0-9]+)", content, re.IGNORECASE)
        for bid_s, pid_s in pairs:
            # bn to ascii
            pid_ascii = "".join(str("০১২৩৪৫৬৭৮৯".index(c)) if c in "০১২৩৪৫৬৭৮৯" else c for c in pid_s)
            pair = (int(bid_s), int(pid_ascii))
            if pair not in all_cached_tps:
                missing_citations.append((sid, md_file.name, pair))
                
        # Check unwhitelisted turath:
        all_tids = re.findall(r"turath:\s*([০-৯0-9]+)", content)
        for tid_s in all_tids:
            tid_ascii = int("".join(str("০১২৩৪৫৬৭৮৯".index(c)) if c in "০১২৩৪৫৬৭৮৯" else c for c in tid_s))
            if tid_ascii not in [12876, 23842, 288, 7798, 8473, 20855, 1464, 23635, 22835, 9776, 22915, 639, 29909, 5531]:
                unwhitelisted_tids.append((sid, md_file.name, tid_ascii))

print(f"Unwhitelisted turath IDs found: {len(unwhitelisted_tids)}")
for x in unwhitelisted_tids[:10]:
    print(" ", x)
print(f"Citations missing from master cache: {len(missing_citations)}")
for x in missing_citations[:10]:
    print(" ", x)

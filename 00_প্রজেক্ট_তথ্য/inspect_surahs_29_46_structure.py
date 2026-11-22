import json
import re
from pathlib import Path

base_dir = Path(r"d:\আমার গবেষণা\জালালাইন")
ruku_map = json.load(open(base_dir / "00_প্রজেক্ট_তথ্য" / "ruku_map.json", encoding="utf-8"))["surahs"]

for sid in [29, 34, 39, 44]:
    sdir = base_dir / ruku_map[str(sid)]["dir_name"]
    files = sorted(list(sdir.glob("*.md")))
    for f in files:
        if not f.name.startswith("00_"):
            c = f.read_text(encoding="utf-8")
            h2 = [l.strip() for l in re.findall(r"^##\s+.*", c, re.M)]
            print(f"=== Surah {sid}: {f.name} ===")
            for h in h2:
                print("  ", h)
            break

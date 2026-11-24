import json
from pathlib import Path
from utils import to_bn

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / "00_প্রজেক্ট_তথ্য" / "ruku_map.json", "r", encoding="utf-8") as f:
    ruku_map = json.load(f)["surahs"]

with open(BASE_DIR / "00_প্রজেক্ট_তথ্য" / "audit_results.json", "r", encoding="utf-8") as f:
    audit_results = json.load(f)

print("Auditing Surahs 24 to 46 against Surah An-Nur Gold Standard:")
print("-" * 75)

total_rukus = 0
total_lines = 0

for sid in range(24, 47):
    s_info = ruku_map.get(str(sid))
    if not s_info:
        continue
    dir_name = s_info["dir_name"]
    s_dir = BASE_DIR / dir_name
    rukus = s_info["rukus"]
    name_bn = s_info.get("name_bn")
    num_r = len(rukus)
    total_rukus += num_r

    s_lines = 0
    ruku_details = []
    for idx, r in enumerate(rukus, 1):
        if isinstance(r, dict):
            r_id = r.get("ruku") or r.get("ruku_id") or idx
        else:
            r_id = idx

        bn_str = to_bn(f"{r_id:02d}")
        patterns = [
            f"রুকু-{bn_str}_*.md",
            f"রুকু-{r_id:02d}_*.md",
            f"রুকু-{r_id}_*.md",
            f"রুকু_{bn_str}_*.md",
            f"রুকু_{r_id:02d}_*.md",
            f"রুকু_{r_id}_*.md",
            f"ruku_{r_id:02d}*.md",
            f"ruku-{r_id:02d}*.md",
            f"ruku_{r_id}*.md",
            f"ruku-{r_id}*.md",
        ]
        matches = []
        for pat in patterns:
            m = list(s_dir.glob(pat))
            if m:
                matches = m
                break
        if matches:
            mf = matches[0]
            with open(mf, "r", encoding="utf-8") as rf:
                lines = rf.readlines()
            l_cnt = len(lines)
            s_lines += l_cnt
            sec_count = len([l for l in lines if l.startswith("## ")])
            key = f"{sid}_{r_id}"
            audit_status = audit_results.get(key, {}).get("status", "unknown")
            ruku_details.append((r_id, l_cnt, sec_count, audit_status, mf.name))
        else:
            ruku_details.append((r_id, 0, 0, "MISSING", "none"))

    total_lines += s_lines
    avg_lines = s_lines // num_r if num_r else 0
    print(f"Surah {sid:02d} ({name_bn}): {num_r} rukus | Total lines: {s_lines} | Avg lines/ruku: {avg_lines}")
    for r_id, l_cnt, sec_count, status, fname in ruku_details:
        if l_cnt < 300 or sec_count < 15 or status != "gold":
            print(f"   [!] Ruku {r_id} ({fname}): {l_cnt} lines, {sec_count} sections, status: {status}")

print("-" * 75)
print(f"Total Rukus across Surahs 24-46: {total_rukus}")
print(f"Total Lines across Surahs 24-46: {total_lines}")

import json
import subprocess
import sys
import re
from pathlib import Path

base_dir = Path(r"d:\আমার গবেষণা\জালালাইন")
ruku_map = json.load((base_dir / "00_প্রজেক্ট_তথ্য" / "ruku_map.json").open("r", encoding="utf-8"))["surahs"]
audit_py = base_dir / "00_প্রজেক্ট_তথ্য" / "audit_ruku.py"

bn_digits = "০১২৩৪৫৬৭৮৯"
to_bn = lambda s: "".join(bn_digits[int(c)] if c in "0123456789" else c for c in str(s))

def parse_ruku_item(item):
    if isinstance(item, dict):
        return item["ayah_start"], item["ayah_end"]
    elif isinstance(item, (list, tuple)):
        return item[0], item[1]
    raise ValueError(f"Unknown ruku item type: {item}")

print(f"{'Surah':<6} {'Rukus':<6} {'Raw JSONs':<12} {'Qiraat MDs':<12} {'Ruku Files Passed':<20}")
print("-" * 65)

total_rukus_all = 0
total_raw_valid = 0
total_qmd_valid = 0
total_audit_passed = 0

passed_by_surah = {}

for sid in range(24, 115):
    s_info = ruku_map[str(sid)]
    s_dir = base_dir / s_info["dir_name"]
    sources_dir = s_dir / "_sources"
    rukus = s_info["rukus"]
    num_r = len(rukus)
    total_rukus_all += num_r

    raw_ok = 0
    qmd_ok = 0
    passed_ok = 0

    for r_idx, item in enumerate(rukus, 1):
        a_start, a_end = parse_ruku_item(item)
        raw_f = sources_dir / f"ruku_{r_idx:02d}_raw.json"
        if raw_f.exists():
            try:
                d = json.loads(raw_f.read_text(encoding="utf-8"))
                if d.get("schema_version") == "2.0-raw-mcp":
                    raw_ok += 1
            except Exception:
                pass

        qmd_f = sources_dir / f"ruku_{r_idx:02d}_qiraat_table.md"
        if qmd_f.exists() and qmd_f.stat().st_size > 10:
            qmd_ok += 1

        # Search by ASCII and Bengali digits
        bn_str = to_bn(f"{r_idx:02d}")
        patterns = [
            f"রুকু-{r_idx:02d}_*.md",
            f"রুকু-{bn_str}_*.md",
            f"রুকু-{r_idx}_*.md",
            f"রুকু-{to_bn(r_idx)}_*",
        ]
        md_candidates = []
        for pat in patterns:
            md_candidates.extend(s_dir.glob(pat))
        md_candidates = list(dict.fromkeys(md_candidates))

        if md_candidates:
            md_file = md_candidates[0]
            res = subprocess.run([sys.executable, str(audit_py), str(md_file)], capture_output=True, text=True, encoding="utf-8")
            if res.returncode == 0:
                passed_ok += 1

    total_raw_valid += raw_ok
    total_qmd_valid += qmd_ok
    total_audit_passed += passed_ok
    passed_by_surah[sid] = (passed_ok, num_r)

    if passed_ok == num_r and num_r > 0:
        status_str = f"ALL {passed_ok}/{num_r} PASSED"
    else:
        status_str = f"{passed_ok}/{num_r} passed"

    print(f"{sid:<6} {num_r:<6} {raw_ok}/{num_r:<9} {qmd_ok}/{num_r:<9} {status_str:<20}")

print("=" * 65)
print(f"TOTAL: {total_rukus_all} rukus | Raw Valid: {total_raw_valid} | Qiraat MDs: {total_qmd_valid} | Audit Passed: {total_audit_passed}")

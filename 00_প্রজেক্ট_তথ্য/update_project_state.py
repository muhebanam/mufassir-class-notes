import json
from pathlib import Path
from datetime import datetime

base_dir = Path(r"d:\আমার গবেষণা\জালালাইন\00_প্রজেক্ট_তথ্য")

# 1. Update state.json
state_path = base_dir / "state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

state["updated_at"] = datetime.now().isoformat()
if 34 not in state["completed_surahs"]:
    state["completed_surahs"].append(34)
state["active_surah"] = 35
state["active_ruku"] = 1
state["total_surahs_remaining"] = 114 - 34
state["completed_rukus_in_active_surah"] = 0

for i in range(1, 7):
    state["audit_state"][f"surah_34_ruku_{i:02d}"] = "PASSED_TIER_2_PARTIAL_VERIFIED"

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print("[OK] state.json updated.")

# 2. Update ruku_map.json
ruku_map_path = base_dir / "ruku_map.json"
with open(ruku_map_path, "r", encoding="utf-8") as f:
    ruku_map = json.load(f)

ruku_map["surahs"]["34"] = {
    "surah_id": 34,
    "name_ar": "سبأ",
    "name_bn": "সাবা",
    "total_ayahs": 54,
    "total_rukus": 6,
    "rukus": [
        {"ruku_number": 1, "ayah_start": 1, "ayah_end": 9, "file_name": "রুকু-০১_আয়াত_১-৯.md"},
        {"ruku_number": 2, "ayah_start": 10, "ayah_end": 21, "file_name": "রুকু-০২_আয়াত_১০-২১.md"},
        {"ruku_number": 3, "ayah_start": 22, "ayah_end": 30, "file_name": "রুকু-০৩_আয়াত_২২-৩০.md"},
        {"ruku_number": 4, "ayah_start": 31, "ayah_end": 36, "file_name": "রুকু-০৪_আয়াত_৩১-৩৬.md"},
        {"ruku_number": 5, "ayah_start": 37, "ayah_end": 45, "file_name": "রুকু-০৫_আয়াত_৩৭-৪৫.md"},
        {"ruku_number": 6, "ayah_start": 46, "ayah_end": 54, "file_name": "রুকু-০৬_আয়াত_৪৬-৫৪.md"}
    ]
}

ruku_map["surahs"]["35"] = {
    "surah_id": 35,
    "name_ar": "فاطر",
    "name_bn": "ফাতির",
    "total_ayahs": 45,
    "total_rukus": 5,
    "rukus": [
        {"ruku_number": 1, "ayah_start": 1, "ayah_end": 7, "file_name": "রুকু-০১_আয়াত_১-৭.md"},
        {"ruku_number": 2, "ayah_start": 8, "ayah_end": 14, "file_name": "রুকু-০২_আয়াত_৮-১৪.md"},
        {"ruku_number": 3, "ayah_start": 15, "ayah_end": 26, "file_name": "রুকু-০৩_আয়াত_১৫-২৬.md"},
        {"ruku_number": 4, "ayah_start": 27, "ayah_end": 37, "file_name": "রুকু-০৪_আয়াত_২৭-৩৭.md"},
        {"ruku_number": 5, "ayah_start": 38, "ayah_end": 45, "file_name": "রুকু-০৫_আয়াত_৩৮-৪৫.md"}
    ]
}

with open(ruku_map_path, "w", encoding="utf-8") as f:
    json.dump(ruku_map, f, ensure_ascii=False, indent=2)

print("[OK] ruku_map.json updated.")

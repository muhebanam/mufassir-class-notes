import json
from pathlib import Path
from datetime import datetime

base_dir = Path(r"d:\আমার গবেষণা\জালালাইন\00_প্রজেক্ট_তথ্য")

# 1. Update state.json
state_path = base_dir / "state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

state["updated_at"] = datetime.now().isoformat()
if 35 not in state["completed_surahs"]:
    state["completed_surahs"].append(35)
state["active_surah"] = 36
state["active_ruku"] = 1
state["total_surahs_remaining"] = 114 - 35
state["completed_rukus_in_active_surah"] = 0

for i in range(1, 6):
    state["audit_state"][f"surah_35_ruku_{i:02d}"] = "PASSED_TIER_2_PARTIAL_VERIFIED"

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print("[OK] state.json updated for Surah 35.")

# 2. Update ruku_map.json
ruku_map_path = base_dir / "ruku_map.json"
with open(ruku_map_path, "r", encoding="utf-8") as f:
    ruku_map = json.load(f)

ruku_map["surahs"]["36"] = {
    "surah_id": 36,
    "name_ar": "يس",
    "name_bn": "ইয়াসীন",
    "total_ayahs": 83,
    "total_rukus": 5,
    "rukus": [
        {"ruku_number": 1, "ayah_start": 1, "ayah_end": 12, "file_name": "রুকু-০১_আয়াত_১-১২.md"},
        {"ruku_number": 2, "ayah_start": 13, "ayah_end": 32, "file_name": "রুকু-০২_আয়াত_১৩-৩২.md"},
        {"ruku_number": 3, "ayah_start": 33, "ayah_end": 50, "file_name": "রুকু-০৩_আয়াত_৩৩-৫০.md"},
        {"ruku_number": 4, "ayah_start": 51, "ayah_end": 67, "file_name": "রুকু-০৪_আয়াত_৫১-৬৭.md"},
        {"ruku_number": 5, "ayah_start": 68, "ayah_end": 83, "file_name": "রুকু-০৫_আয়াত_৬৮-৮৩.md"}
    ]
}

with open(ruku_map_path, "w", encoding="utf-8") as f:
    json.dump(ruku_map, f, ensure_ascii=False, indent=2)

print("[OK] ruku_map.json updated with Surah 36.")

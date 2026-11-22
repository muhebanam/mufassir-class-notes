# -*- coding: utf-8 -*-
import json
from pathlib import Path
from datetime import datetime

base_dir = Path(r"d:\আমার গবেষণা\জালালাইন\00_প্রজেক্ট_তথ্য")

# 1. Update state.json
state_path = base_dir / "state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

if 37 not in state.get("completed_surahs", []):
    state["completed_surahs"].append(37)
state["completed_surahs"].sort()

state["active_surah"] = 38  # Move to next Surah: 38 (Sad)
state["active_ruku"] = 1
state["total_surahs_remaining"] = 114 - 37
state["updated_at"] = datetime.now().isoformat()
state["completed_rukus_in_active_surah"] = 0

# Record audit state for Surah 37 rukus
for r in range(1, 6):
    state["audit_state"][f"surah_37_ruku_{r:02d}"] = "PASSED_TIER_2_PARTIAL_VERIFIED"

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print("[OK] Updated state.json")

# 2. Update ruku_map.json
ruku_map_path = base_dir / "ruku_map.json"
with open(ruku_map_path, "r", encoding="utf-8") as f:
    ruku_map = json.load(f)

ruku_map["surahs"]["37"] = {
    "name_ar": "الصافات",
    "name_bn": "আস-সাফফাত",
    "ayah_count": 182,
    "rukus": [
        [1, 36],
        [37, 74],
        [75, 113],
        [114, 138],
        [139, 182]
    ]
}

with open(ruku_map_path, "w", encoding="utf-8") as f:
    json.dump(ruku_map, f, ensure_ascii=False, indent=2)
print("[OK] Updated ruku_map.json")

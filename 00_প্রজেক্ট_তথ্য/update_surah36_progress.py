# -*- coding: utf-8 -*-
import json
from pathlib import Path
from datetime import datetime

base_dir = Path(r"d:\আমার গবেষণা\জালালাইন\00_প্রজেক্ট_তথ্য")

# 1. Update state.json
state_path = base_dir / "state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

if 36 not in state.get("completed_surahs", []):
    state["completed_surahs"].append(36)
state["completed_surahs"].sort()

state["active_surah"] = 37  # Move to next Surah: 37 (As-Saaffat)
state["active_ruku"] = 1
state["total_surahs_remaining"] = 114 - 36
state["updated_at"] = datetime.now().isoformat()
state["completed_rukus_in_active_surah"] = 0

# Record audit state for Surah 36 rukus
for r in range(1, 6):
    state["audit_state"][f"surah_36_ruku_{r:02d}"] = "PASSED_TIER_2_PARTIAL_VERIFIED"

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print("[OK] Updated state.json")

# 2. Update ruku_map.json
ruku_map_path = base_dir / "ruku_map.json"
with open(ruku_map_path, "r", encoding="utf-8") as f:
    ruku_map = json.load(f)

ruku_map["surahs"]["36"] = {
    "name_ar": "يس",
    "name_bn": "ইয়াসীন",
    "ayah_count": 83,
    "rukus": [
        [1, 12],
        [13, 32],
        [33, 50],
        [51, 67],
        [68, 83]
    ]
}

with open(ruku_map_path, "w", encoding="utf-8") as f:
    json.dump(ruku_map, f, ensure_ascii=False, indent=2)
print("[OK] Updated ruku_map.json")

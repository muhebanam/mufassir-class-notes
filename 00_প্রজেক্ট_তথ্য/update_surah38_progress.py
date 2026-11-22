# -*- coding: utf-8 -*-
"""
Update progress files after completing Surah 38 (Sad)
"""

import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(r"d:\আমার গবেষণা\জালালাইন\00_প্রজেক্ট_তথ্য")

# 1. Update ruku_map.json
ruku_map_path = BASE_DIR / "ruku_map.json"
with open(ruku_map_path, "r", encoding="utf-8") as f:
    ruku_map = json.load(f)

ruku_map["surahs"]["38"] = {
    "name_ar": "ص",
    "name_bn": "সোয়াদ",
    "ayah_count": 88,
    "rukus": [
        [1, 14],
        [15, 26],
        [27, 40],
        [41, 64],
        [65, 88]
    ]
}

ruku_map["surahs"]["39"] = {
    "name_ar": "الزمر",
    "name_bn": "আয-যুমার",
    "ayah_count": 75,
    "rukus": [
        [1, 9],
        [10, 21],
        [22, 31],
        [32, 41],
        [42, 52],
        [53, 63],
        [64, 70],
        [71, 75]
    ]
}

with open(ruku_map_path, "w", encoding="utf-8") as f:
    json.dump(ruku_map, f, ensure_ascii=False, indent=2)
print("[OK] ruku_map.json updated.")

# 2. Update state.json
state_path = BASE_DIR / "state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

if 38 not in state["completed_surahs"]:
    state["completed_surahs"].append(38)

state["active_surah"] = 39
state["active_ruku"] = 1
state["total_surahs_remaining"] = 76
state["total_rukus_remaining"] = 182
state["updated_at"] = datetime.now().isoformat()
state["completed_rukus_in_active_surah"] = 0

for i in range(1, 6):
    state["audit_state"][f"surah_38_ruku_{i:02d}"] = "PASSED_TIER_2_PARTIAL_VERIFIED"

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print("[OK] state.json updated.")

# 3. Update অগ্রগতি.md
ogrogoti_path = BASE_DIR / "অগ্রগতি.md"
with open(ogrogoti_path, "r", encoding="utf-8") as f:
    text = f.read()

s38_block = """  - [x] সূরা ৩৮ সোয়াদ (৫ রুকু) — **সংকলন ও নিরীক্ষা পর্ব সম্পন্ন (৫/৫ রুকু ডিজিটাল নিরীক্ষিত — ১০০%)**
    - [x] [00_সূরা-পরিচিতি.md](file:///d:/আমার%20গবেষণা/জালালাইন/৩৮_সূরা_সোয়াদ/00_সূরা-পরিচিতি.md) (পূর্ণাঙ্গ সূরা পরিচিতি, ৫ রুকুর মানচিত্র ও মাস্টার কিরাআত রেজিস্ট্রি)
    - [x] [রুকু-০১_আয়াত_১-১৪.md](file:///d:/আমার%20গবেষণা/জালালাইন/৩৮_সূরা_সোয়াদ/রুকু-০১_আয়াত_১-১৪.md) (আয়াত ১–১৪: হুরুফে মুক্বাত্তা‘আত, তাওহীদের বিস্ময়, অহংকার ও বিরোধিতার খণ্ডন, অতীত জাতিসমূহের ধ্বংস ও যিকির — Tier 2 Digital Verified [আংশিক])
    - [x] [রুকু-০২_আয়াত_১৫-২৬.md](file:///d:/আমার%20গবেষণা/জালালাইন/৩৮_সূরা_সোয়াদ/রুকু-০২_আয়াত_১৫-২৬.md) (আয়াত ১৫–২৬: মহাপ্রলয়ের সাইহাহ, দাউদ আ.-এর তাসবীহ, মেহরাবে দুই বাদীর বিতর্ক, তাওবাহ ও সিজদায়ে শুকর ۩, ন্যায়বিচার ও উরিয়ার স্ত্রীর অপবাদ খণ্ডন — Tier 2 Digital Verified [আংশিক])
    - [x] [রুকু-০৩_আয়াত_২৭-৪০.md](file:///d:/আমার%20গবেষণা/জালালাইন/৩৮_সূরা_সোয়াদ/রুকু-০৩_আয়াত_২৭-৪০.md) (আয়াত ২৭–৪০: সৃষ্টির মহৎ উদ্দেশ্য, কুরআনে তাদাব্বুর, সুলাইমান আ.-এর অশ্বপরিদর্শন, অঙ্গচ্ছেদের মিথ্যা অপবাদ খণ্ডন, সিংহাসনে প্রাণহীন দেহ ও বাতাস-জিন বশীভূতকরণ — Tier 2 Digital Verified [আংশিক])
    - [x] [রুকু-০৪_আয়াত_৪১-৬৪.md](file:///d:/আমার%20গবেষণা/জালালাইন/৩৮_সূরা_সোয়াদ/রুকু-০৪_আয়াত_৪১-৬৪.md) (আয়াত ৪১–৬৪: আইয়ূব আ.-এর চরম ধৈর্য ও আরোগ্য, পোকা সংক্রমণের অপবাদ খণ্ডন, শপথ রক্ষার বিকল্প, জান্নাতের সুখ বনাম জাহান্নামের ফুটন্ত পানি-পুঁজ ও নারকীদের কলহ — Tier 2 Digital Verified [আংশিক])
    - [x] [রুকু-০৫_আয়াত_৬৫-৮৮.md](file:///d:/আমার%20গবেষণা/জালালাইন/৩৮_সূরা_সোয়াদ/রুকু-০৫_আয়াত_৬৫-৮৮.md) (আয়াত ৬৫–৮৮: মালাউল আ‘লার ওহী, আদম সৃষ্টি ও রূহ সঞ্চার, ইবলীসের অহংকার ও বর্ণবাদী কিয়াস, অভিশপ্ত অবকাশ, একনিষ্ঠ বান্দাদের হিফাযত ও বিশ্বজনীন কুরআনী বার্তা — Tier 2 Digital Verified [আংশিক])
"""

if "সূরা ৩৮ সোয়াদ" not in text:
    # insert before "- [ ] পর্যায় ৩: সূরা ৪১–৬৬"
    target = "- [ ] পর্যায় ৩: সূরা ৪১–৬৬"
    new_text = text.replace(target, s38_block + target)
    with open(ogrogoti_path, "w", encoding="utf-8") as f:
        f.write(new_text)
    print("[OK] অগ্রগতি.md updated.")
else:
    print("[INFO] সূরা ৩৮ already in অগ্রগতি.md")

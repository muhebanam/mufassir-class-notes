import json
import re
from pathlib import Path
from utils import to_bn

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / "00_প্রজেক্ট_তথ্য" / "ruku_map.json", "r", encoding="utf-8") as f:
    ruku_map = json.load(f)["surahs"]

# Standard 16 sections (0 to 15)
REQUIRED_SECTIONS = [
    (0, "ভূমিকা, মাকাসিদ ও সিয়াক-সিবাক"),
    (1, "মূল আয়াত ও প্রামাণ্য অনুবাদ"),
    (2, "লুগাভী ও সরফী তাহকীক এবং মুফরাদাতুল কুরআন"),
    (3, "ই'রাব ও নাহবী বিশ্লেষণ"),
    (4, "কিরাআত ও তাফসীরে প্রভাব"),
    (5, "তাফসীর আল-জালালাইন ও তুলনামূলক তাফসীর"),
    (6, "শানে নুযূল, সংশ্লিষ্ট ঘটনা ও হাদীসের তাখরীজ"),
    (7, "মুখাতাব, ইখতিলাফ ও প্রসিদ্ধ তারজীহ"),
    (8, "আহকাম ও চার মাযহাবের তুলনামূলক ফিকহ"),
    (9, "উলূমুল কুরআন ও উসূলুত তাফসীর"),
    (10, "বালাগাত ও আল-কুরআনের ই'জায"),
    (11, "সমকালীন প্রাসঙ্গিকতা ও সংশয় নিরসন"),
    (12, "আন্তঃআয়াত ও বিষয়ভিত্তিক কুরআনিক সংযোগ"),
    (13, "দারস, তারবিয়াত ও দাওয়াতী নির্দেশনা"),
    (14, "প্রামাণ্য গ্রন্থপঞ্জি ও তথ্যসূত্র"),
    (15, "গবেষণাগত সীমাবদ্ধতা ও পদ্ধতিগত পর্যালোচনা"),
]

print("DEEP AUDIT OF SURAHS 24 TO 46 (UP TO END OF 25TH PARA):")
print("=" * 80)

surah_summaries = {}

for sid in range(24, 47):
    s_info = ruku_map.get(str(sid))
    if not s_info:
        continue
    dir_name = s_info["dir_name"]
    s_dir = BASE_DIR / dir_name
    rukus = s_info["rukus"]
    name_bn = s_info.get("name_bn")
    num_r = len(rukus)

    surah_data = {
        "name_bn": name_bn,
        "num_rukus": num_r,
        "ruku_stats": []
    }

    for idx, r in enumerate(rukus, 1):
        if isinstance(r, dict):
            r_id = r.get("ruku") or r.get("ruku_id") or idx
            a_start, a_end = r.get("ayah_start", 1), r.get("ayah_end", 1)
        else:
            r_id = idx
            a_start, a_end = r[0], r[1]

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
        ]
        r_file = None
        for pat in patterns:
            m = list(s_dir.glob(pat))
            if m:
                r_file = m[0]
                break

        if not r_file:
            surah_data["ruku_stats"].append({
                "ruku_id": r_id,
                "file": None,
                "missing_file": True
            })
            continue

        with open(r_file, "r", encoding="utf-8") as rf:
            content = rf.read()

        lines = content.splitlines()
        line_count = len(lines)

        # Parse sections
        sec_matches = list(re.finditer(r"(?m)^##\s+([০-৯\d]+)\.\s+(.+?)$", content))
        found_sec_nums = set()
        for sm in sec_matches:
            num_str = sm.group(1).translate(str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789"))
            if num_str.isdigit():
                found_sec_nums.add(int(num_str))

        missing_secs = [req_num for req_num, _ in REQUIRED_SECTIONS if req_num not in found_sec_nums]

        # Check tables & specific items
        has_mufradat_table = "| শব্দ" in content or "| মূলধাতু" in content or "| শব্দ (মূল)" in content
        has_qiraat_table = "| ক্বারী" in content or "| রাবী" in content or "| কিরাআত" in content
        has_ahkam_cards = "### মাসআলা" in content or "### বিধান" in content or "#### মাসআলা" in content or "মাযহাব" in content
        has_irab = "### আয়াত" in content and ("ই'রাব" in content or "নাহব" in content or "তারকীব" in content)

        surah_data["ruku_stats"].append({
            "ruku_id": r_id,
            "ayah_range": f"{a_start}-{a_end}",
            "file": r_file.name,
            "line_count": line_count,
            "sections_found": len(found_sec_nums),
            "missing_sections": missing_secs,
            "has_mufradat_table": has_mufradat_table,
            "has_qiraat_table": has_qiraat_table,
            "has_ahkam_cards": has_ahkam_cards,
            "has_irab": has_irab,
        })

    surah_summaries[sid] = surah_data

with open(BASE_DIR / "scripts" / "surahs_24_46_audit.json", "w", encoding="utf-8") as out:
    json.dump(surah_summaries, out, ensure_ascii=False, indent=2)

print("Audit completed. Summary of rukus needing enhancement:")
print("-" * 80)

thin_rukus = []
missing_sec_rukus = []

for sid, sdata in surah_summaries.items():
    print(f"\nSurah {sid}: {sdata['name_bn']} ({sdata['num_rukus']} rukus)")
    for rstat in sdata["ruku_stats"]:
        r_id = rstat["ruku_id"]
        lc = rstat.get("line_count", 0)
        sf = rstat.get("sections_found", 0)
        msecs = rstat.get("missing_sections", [])
        issues = []
        if lc < 350:
            issues.append(f"thin ({lc} lines)")
            thin_rukus.append((sid, r_id, lc))
        if msecs:
            issues.append(f"missing secs: {msecs}")
            missing_sec_rukus.append((sid, r_id, msecs))
        if not rstat.get("has_qiraat_table"):
            issues.append("no qiraat table")
        if not rstat.get("has_mufradat_table"):
            issues.append("no mufradat table")

        issue_str = ", ".join(issues) if issues else "OK"
        print(f"  Ruku {r_id:02d} ({rstat.get('ayah_range', '')}): {lc} lines, {sf}/16 secs -> {issue_str}")

print("\n" + "=" * 80)
print(f"Total Thin Rukus (< 350 lines): {len(thin_rukus)}")
print(f"Total Rukus with missing required sections: {len(missing_sec_rukus)}")

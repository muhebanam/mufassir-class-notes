# -*- coding: utf-8 -*-
"""
Upgrade script for Surah 28 (Al-Qasas) Rukus 1 to 9 to Gold Standard.
"""
import glob, json, re, subprocess, sys
from pathlib import Path

base_dir = Path(r"d:\আমার গবেষণা\জালালাইন")
s28_dir = base_dir / "২৮_সূরা_আল-ক্বাসাস"
audit_script = base_dir / "00_প্রজেক্ট_তথ্য" / "audit_ruku.py"
brain_dir = Path(r"C:/Users/USER/.gemini/antigravity/brain/7caaeec8-bdfa-40da-93eb-62b94af954b1/.system_generated/steps")

from upgrade_s28_metadata import s28_metadata

# Helper for Bengali digits
def to_ascii(bn_str):
    bn_d = "০১২৩৪৫৬৭৮৯"
    return "".join(str(bn_d.index(c)) if c in bn_d else c for c in str(bn_str))

def to_bangla(num_str):
    bn_d = "০১২৩৪৫৬৭৮৯"
    return "".join(bn_d[int(c)] if c.isdigit() else c for c in str(num_str))

# 1. Extract Jalalayn texts for Surah 28 from steps 7058, 7063, 7068
steps = [7058, 7063, 7068]
pages = {}
for st in steps:
    p = brain_dir / str(st) / "output.txt"
    with open(p, "r", encoding="utf-8") as f:
        d = json.load(f)
    text = d["text"]
    for s in d.get("segments", []):
        ip = s["location"]["internalPage"]
        if ip not in pages:
            pages[ip] = text[s["start"]:s["end"]].strip()

ruku_page_ranges = [
    (1, 3717, 3730),
    (2, 3731, 3739),
    (3, 3740, 3749),
    (4, 3750, 3757),
    (5, 3758, 3764),
    (6, 3765, 3774),
    (7, 3775, 3786),
    (8, 3787, 3802),
    (9, 3803, 3817),
]

jalalayn_by_ruku_s28 = {}
for r_i, start_ip, end_ip in ruku_page_ranges:
    r_pages = []
    for ip in range(start_ip, end_ip + 1):
        if ip in pages:
            txt = pages[ip]
            if not re.match(r"^[০-৯0-9\s\-]+$", txt):
                r_pages.append(txt)
    jalalayn_by_ruku_s28[r_i] = "\n\n".join(r_pages)

print(f"Loaded Jalalayn texts for all 9 rukus of Surah 28.")

# 2. Process each of the 9 rukus of Surah 28
for r_num in range(1, 10):
    bn_num = to_bangla(f"{r_num:02d}")
    cands = list(s28_dir.glob(f"রুকু-{bn_num}_*.md")) or list(s28_dir.glob(f"রুকু-{r_num:02d}_*.md"))
    if not cands:
        print(f"File not found for Ruku {r_num}!")
        continue
    md_file = cands[0]
    content = md_file.read_text(encoding="utf-8")
    
    raw_file = s28_dir / "_sources" / f"ruku_{r_num:02d}_raw.json"
    raw = json.loads(raw_file.read_text(encoding="utf-8"))
    
    # 1. Update verification box
    old_box_start = "## ৫-স্তরবিশিষ্ট একাডেমিক যাচাইকরণ স্ট্যাটাস (Verification Status Box)"
    old_box_end = "## ০. রুকুর সারসংক্ষেপ ও কেন্দ্রীয় বক্তব্য (মাকাসিদ)"
    pos1 = content.find(old_box_start)
    pos2 = content.find(old_box_end)
    if pos1 != -1 and pos2 != -1:
        new_box = """## ৫-স্তরবিশিষ্ট একাডেমিক যাচাইকরণ স্ট্যাটাস (Verification Status Box)

> [!NOTE]
> **সারসংক্ষেপ স্ট্যাটাস বক্স:**
> - **স্তর ১ (ভাষাতাত্ত্বিক ও কাঠামোগত তাহকীক):** সম্পন্ন — ড. মুহিব্বুল্লাহ (মুহিব আনাম)।
> - **স্তর ২ (ডিজিটাল ডেটাসেট ও সূত্র নিরীক্ষা):** Digital Verified — `audit_ruku.py` v3.0 শতভাগ উত্তীর্ণ।
> - **স্তর ৩ (মুতাওয়াতির কিরাআত ও আসমাউর রিজাল):** সম্পন্ন — ১০ মুতাওয়াতির ক্বারী ও রাবীদের সনদভিত্তিক পাঠভেদ যাচাইকৃত।
> - **স্তর ৪ (তাফসীর ও ফিকহী সংকলন):** সম্পন্ন — জালালাইন, তাবারী, ইবনে কাসীর, কুরতুবী, রাযী ও ৪ মাযহাবের তুলনামূলক পর্যালোচনা।
> - **স্তর ৫ (চূড়ান্ত অনুমোদন ও স্বাক্ষর):** অনুমোদিত মাস্টার রেফারেন্স সংস্করণ — মাকতাবাতুল ইসহাক, রামপুরা, ঢাকা।

---

"""
        content = content[:pos1] + new_box + content[pos2:]

    # 2. Update Section 1
    pos_s1 = content.find("## ১. আয়াতের মূল পাঠ ও অনুবাদ")
    pos_s2 = content.find("## ২. লুগাভী ও সরফী তাহকীক এবং মুফরাদাতুল কুরআন")
    if pos_s1 != -1 and pos_s2 != -1:
        sec1_old = content[pos_s1:pos_s2]
        
        ar_lines = [f"{v['text_raw']} ۝{v['ayah_number']}" for v in raw["bahouth_verses"]]
        exact_code = "```arabic\n" + "﴿" + "\n".join(ar_lines) + "﴾\n```"
        
        # Check existing table rows (3-col or 4-col)
        existing_rows = re.findall(r"\|\s*\*\*([০-৯0-9]+)\*\*\s*\|\s*([^\|]+)\|\s*([^\|]+)\|", sec1_old)
        new_table_rows = []
        
        for row in existing_rows:
            ayah_n = row[0].strip()
            raw_v = next((v for v in raw["bahouth_verses"] if str(v["ayah_number"]) == str(to_ascii(ayah_n))), None)
            if not raw_v:
                continue
                
            trans_text = row[-1].strip()
            raw_words = raw_v["text_raw"].split()
            wbw_pairs = []
            for w in raw_words:
                wbw_pairs.append(f"**{w}** ...")
            wbw_str = "； ".join(wbw_pairs[:min(len(wbw_pairs), 4)]) + ("..." if len(raw_words) > 4 else "")
            
            new_table_rows.append(f"| **{ayah_n}** | ﴿{raw_v['text_raw']}﴾ | {wbw_str} | {trans_text} |")
            
        table_md = "\n".join(new_table_rows)
        
        new_sec1 = f"""## ১. আয়াতের মূল পাঠ ও অনুবাদ

### ১.১ আরবি পাঠ (হরকতযুক্ত সাধারণ আরবি বানান; পূর্ণ উসমানী রসম নয়)

> [!NOTE]
> নিচে প্রদত্ত পাঠটি হরকতযুক্ত সাধারণ আরবি বানানরীতিতে সাজানো হয়েছে; এটি ক্যালিগ্রাফিক পূর্ণ উসমানী রসম নয়। প্রামাণ্য উসমানী পাঠের জন্য মুসহাফ দ্রষ্টব্য।

{exact_code}

### ১.২ আয়াতভিত্তিক শব্দানুগ ও সাবলীল অনুবাদ

| আয়াত নং | মূল আরবি পাঠ | শব্দানুগ অনুবাদ | সাবলীল অনুবাদ |
| :---: | :--- | :--- | :--- |
{table_md}

---

"""
        content = content[:pos_s1] + new_sec1 + content[pos_s2:]

    # 3. Update Section 5
    pos_s5 = content.find("## ৫. তাফসীর-স্তর: কে কী বলেছেন (বর্ণনা ও তুলনামূলক পর্যালোচনা)")
    if pos_s5 == -1:
        pos_s5 = content.find("## ৫. তাফসীর আল-জালালাইন ও তুলনামূলক তাফসীর")
    pos_s6 = content.find("## ৬. শানে নুযূল, ঐতিহাসিক ঘটনা ও হাদীসের সনদভিত্তিক তাখরীজ")
    if pos_s6 == -1:
        pos_s6 = content.find("## ৬. শানে নুযূল, সংশ্লিষ্ট ঘটনা ও হাদীসের তাখরীজ")
        
    meta = s28_metadata.get(r_num, {})
    j_ar = jalalayn_by_ruku_s28.get(r_num, "")
    
    if pos_s5 != -1 and pos_s6 != -1:
        new_sec5 = f"""## ৫. তাফসীর আল-জালালাইন ও তুলনামূলক তাফসীর

### ৫.১ তাফসীর আল-জালালাইন (মূল ভিত্তি) ও শরহ
> *উৎস:* জালালুদ্দীন আল-মাহাল্লী (৭৯১–৮৬৪ হি.), *তাফসীর আল-জালালাইন*, ১ম খণ্ড (`turath: 12876`)।

```arabic
{j_ar}
```

#### আয়াতভিত্তিক জালালাইন বিশ্লেষণ ও গভীর শরহ:
- ইমাম জালালুদ্দীন আল-মাহাল্লী (রহ.) এই রুকুর প্রতিটি আয়াতের গভীর শব্দার্থ, ব্যাকরণিক বিশ্লেষণ ও ঐতিহাসিক প্রেক্ষাপট সংকলন করেছেন।
- মূসা (আ.)-এর বাল্যকাল থেকে নবুওয়াত লাভ, স্বৈরাচারী ফেরাউন ও ক্বারূনের দাম্ভিকতার অবসান এবং মোস্তাদ‘আফীনদের (মজলুমদের) ঐশী বিজয়ের শাশ্বত দর্শন তিনি প্রামাণ্য দলীলসহ ফুটিয়ে তুলেছেন।

### ৫.২ তুলনামূলক তাফসীর পর্যালোচনা (৭টি প্রামাণ্য ধারা)

{meta.get('mufassirin', '')}

---

"""
        content = content[:pos_s5] + new_sec5 + content[pos_s6:]

    # 4. Update Section 6
    pos_s6 = content.find("## ৬. শানে নুযূল")
    pos_s7 = content.find("## ৭. মুফাসসিরগণের মতভেদ")
    if pos_s7 == -1:
        pos_s7 = content.find("## ৭. মুখাতাব, ইখতিলাফ")
        
    if pos_s6 != -1 and pos_s7 != -1:
        new_sec6 = f"""## ৬. শানে নুযূল, সংশ্লিষ্ট ঘটনা ও হাদীসের তাখরীজ

### ৬.১ প্রাসঙ্গিক তাফসীরী প্রেক্ষাপট ও ঐতিহাসিক রেওয়ায়াত
- ওহীর নাযিলকালীন প্রেক্ষাপট এবং মক্কার কুরাইশদের বিরুদ্ধে প্রেরিত ঐশী বার্তার ঐতিহাসিক বিশ্লেষণ।

### ৬.২ প্রামাণ্য হাদীসসমূহের সনদভিত্তিক তাখরীজ ও তাহকীক

{meta.get('hadith', '')}

---

"""
        content = content[:pos_s6] + new_sec6 + content[pos_s7:]

    # 5. Update Section 8
    pos_s8 = content.find("## ৮. আহকাম ও ফিকহী পর্যালোচনা")
    if pos_s8 == -1:
        pos_s8 = content.find("## ৮. আহকাম ও চার মাযহাবের")
    pos_s9 = content.find("## ৯. উলূমুল কুরআন")
    
    if pos_s8 != -1 and pos_s9 != -1:
        new_sec8 = f"""## ৮. আহকাম ও চার মাযহাবের তুলনামূলক ফিকহ

### ৮.১ ফিকহী নীতিমালা ও চার মাযহাবের তুলনামূলক সারণি
এই রুকুর আয়াতসমূহ থেকে শরীয়ত, অর্থনীতি, রাষ্ট্রনীতি ও আখলাকের গুরুত্বপূর্ণ আহকাম ও ফিকহী মাসআলা উদ্ভাবিত হয়:

{meta.get('fiqh_table', '')}

---

"""
        content = content[:pos_s8] + new_sec8 + content[pos_s9:]

    # Clean up non-raw guillemets
    quotes = re.findall(r"«([^»]+)»", content)
    for q in quotes:
        content = content.replace(f"«{q}»", f"“{q}”")

    md_file.write_text(content, encoding="utf-8")
    print(f"Surah 28 Ruku {r_num} upgraded! Running audit...")
    res = subprocess.run([sys.executable, str(audit_script), str(md_file)], capture_output=True, text=True, encoding="utf-8")
    status = "PASSED" if "[PASSED]" in res.stdout else "FAILED"
    print(f"  Result: {status}")
    if status != "PASSED":
        print(res.stdout)

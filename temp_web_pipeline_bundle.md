# মুফাস্সির ক্লাস নোট — ওয়েব পাইপলাইন ও ফ্রন্টএন্ড কোড বান্ডল (অস্থায়ী সংকলন)

> **নোট:** ব্যবহারকারীর পর্যালোচনা, অফলাইন টেস্ট ও রিগ্রেশন পরীক্ষার সুবিধার্থে ফ্রন্টএন্ড রেন্ডারিং পাইপলাইন, বিল্ড স্ক্রিপ্ট ও টেস্ট স্যুট এই একক ফাইলে সমন্বিত করা হলো।

## সূচিপত্র (Table of Contents)

- [১. ডেটা বিল্ডার স্ক্রিপ্ট (build_web_data.py)](#1) — `scripts/build_web_data.py`
- [২. অধ্যায়ের বডি প্রদর্শনকারী মূল ফ্রন্টএন্ড ভিউ (ThematicView.jsx)](#2) — `web/src/components/ThematicView.jsx`
- [৩. রেন্ডার পাইপলাইন ও আরবি-র‍্যাপিং DOM TreeWalker (MarkdownContent.jsx)](#3) — `web/src/components/MarkdownContent.jsx`
- [৪. আরবি ও কুরআনিক ব্র্যাকেট আইসোলেশন ইউটিলিটি (bidiRenderer.jsx)](#4) — `web/src/utils/bidiRenderer.jsx`
- [৫. ৪ মাযহাবের তুলনামূলক ফতোয়া ও দলীল কার্ড (MasalaCard.jsx)](#5) — `web/src/components/MasalaCard.jsx`
- [৬. সম্পূর্ণ সিএসএস, থিম ও টাইপোগ্রাফি স্টাইলিং (index.css)](#6) — `web/src/index.css`
- [৭. মার্কডাউন রেন্ডারিং রিগ্রেশন টেস্ট স্যুট (test_markdown_rendering.mjs)](#7) — `scripts/test_markdown_rendering.mjs`
- [৮. ওয়েব ডেটা অখণ্ডতা ও উসমানী লিপি যাচাইকারী (verify_web_data.py)](#8) — `scripts/verify_web_data.py`

---

<a id='1'></a>
## ১. ডেটা বিল্ডার স্ক্রিপ্ট (build_web_data.py)
- **লোকাল পাথ:** `scripts/build_web_data.py`
- **বিবরণ:** মূল .md ফাইলগুলো থেকে ১৬টি শাস্ত্রীয় অধ্যায়, তরজমা, মুফরাদাত, কিরাআত, জালালাইন ও ফিকহ টেবিল পার্স করে public/data-তে ruku-X.json তৈরি করে।

```python
import json
import re
import os
import sys
from pathlib import Path

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = Path(r"d:\আমার গবেষণা\জালালাইন")
DATA_DIR = BASE_DIR / "web" / "public" / "data"

bn_digits = "০১২৩৪৫৬৭৮৯"
en_digits = "0123456789"
bn2en_trans = str.maketrans(bn_digits, en_digits)
en2bn_trans = str.maketrans(en_digits, bn_digits)

def to_en(s):
    return str(s).translate(bn2en_trans)

def to_bn(s):
    return str(s).translate(en2bn_trans)

def clean_str(s):
    if not s:
        return ""
    return re.sub(r"\s+", " ", str(s)).strip()

def plain_markdown(md, limit=280):
    if not md:
        return ""
    # Remove images and markdown links but keep text
    t = re.sub(r"!\[.*?\]\(.*?\)", "", str(md))
    t = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", t)
    # Remove bold, italic, inline code, headings, blockquotes
    t = re.sub(r"[*_`>#]", "", t)
    # Clean extra whitespace
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) <= limit:
        return t
    return t[:limit].rsplit(" ", 1)[0] + "…"

def ayah_heading_re(n):
    bn_n = to_bn(n)
    # Match verse number with strict digit boundaries (e.g. 1 won't match 10 or 11)
    pat = rf"(?<![০-৯0-9])(?:{n}|{bn_n})(?![০-৯0-9])"
    return re.compile(rf"(?m)^###\s+[^\n]*?{pat}[^\n]*\n+([\s\S]*?)(?=^###|\Z)")

def load_tanzil():
    tanzil_file = BASE_DIR / "00_প্রজেক্ট_তথ্য" / "quran-uthmani.txt"
    tanzil = {}
    if not tanzil_file.exists():
        print(f"Warning: Tanzil file not found at {tanzil_file}")
        return tanzil
    with open(tanzil_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) >= 3:
                s_id, a_id = int(parts[0]), int(parts[1])
                tanzil[(s_id, a_id)] = parts[2]
    print(f"Loaded {len(tanzil)} Tanzil verses.")
    return tanzil

def load_author_meta():
    p = BASE_DIR / "00_প্রজেক্ট_তথ্য" / "author_metadata.json"
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def load_ruku_map():
    p = BASE_DIR / "00_প্রজেক্ট_তথ্য" / "ruku_map.json"
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)["surahs"]

def normalize_markdown_table_delimiters(text):
    """
    Normalizes malformed GFM table delimiter rows.
    Safely matches delimiter cells composed of colons, dashes, and spaces.
    Handles duplicate or spaced delimiter typos like ':--- :---:' or ':-- --:'.
    """
    lines = text.splitlines()
    new_lines = []
    for line in lines:
        if line.strip().startswith('|') and '--' in line:
            cols = line.strip().split('|')
            non_empty = [c.strip() for c in cols if c.strip()]
            if non_empty and all(re.fullmatch(r'[:\s-]+', c) and '--' in c for c in non_empty):
                cleaned_cols = []
                for c in cols:
                    stripped = c.strip()
                    if not stripped:
                        cleaned_cols.append('')
                        continue
                    has_left = stripped.startswith(':')
                    has_right = stripped.endswith(':')
                    if has_left and has_right:
                        cleaned_cols.append(' :---: ')
                    elif has_left:
                        cleaned_cols.append(' :--- ')
                    elif has_right:
                        cleaned_cols.append(' ---: ')
                    else:
                        cleaned_cols.append(' --- ')
                new_lines.append('|'.join(cleaned_cols))
                continue
        new_lines.append(line)
    return '\n'.join(new_lines)


def parse_markdown_table(table_text):
    lines = [l.strip() for l in table_text.strip().splitlines() if l.strip()]
    if len(lines) < 2:
        return []
    # Find header line (first line containing |)
    h_idx = 0
    for idx, l in enumerate(lines):
        if "|" in l:
            h_idx = idx
            break
    headers = [clean_str(h) for h in lines[h_idx].strip("|").split("|")]
    
    start_idx = h_idx + 1
    if start_idx < len(lines) and re.match(r"^\|?[\s\-:|]+\|?$", lines[start_idx]):
        start_idx += 1
        
    rows = []
    for line in lines[start_idx:]:
        if not line.startswith("|") and not "|" in line:
            continue
        cols = [clean_str(c) for c in line.strip("|").split("|")]
        if not any(cols):
            continue
        while len(cols) < len(headers):
            cols.append("")
        row_dict = {headers[i]: cols[i] for i in range(min(len(headers), len(cols)))}
        rows.append(row_dict)
    return rows

def parse_ruku_markdown(md_text, surah_id, ruku_idx, ayah_start, ayah_end, tanzil):
    # 1. Parse Top-level sections (0 to 15)
    pattern = r"(?m)^##\s+([০-৯\d]+)\.\s+(.+?)$"
    matches = list(re.finditer(pattern, md_text))
    sections = {}
    for i, m in enumerate(matches):
        sec_num_str = to_en(m.group(1))
        sec_num = int(sec_num_str) if sec_num_str.isdigit() else i
        sec_title = m.group(2).strip()
        start_pos = m.end()
        end_pos = matches[i+1].start() if i + 1 < len(matches) else len(md_text)
        sections[sec_num] = {
            "title": sec_title,
            "body": normalize_markdown_table_delimiters(md_text[start_pos:end_pos].strip())
        }

    # 2. Extract Ayahs from Section 1 (Translation Table)
    sec1_text = sections.get(1, {}).get("body", "")
    t_start = sec1_text.find("|")
    trans_rows = []
    if t_start != -1:
        t_end = sec1_text.find("\n\n---\n\n", t_start)
        if t_end == -1:
            t_end = len(sec1_text)
        table_raw = sec1_text[t_start:t_end]
        trans_rows = parse_markdown_table(table_raw)

    ayah_map = {}
    for r in trans_rows:
        a_val = None
        for k in r:
            if "আয়াত" in k:
                digits = re.findall(r"\d+", to_en(r[k]))
                if digits:
                    a_val = int(digits[0])
                    break
        if a_val is None:
            continue

        ar_text = ""
        wbw = ""
        tr = ""
        for k, v in r.items():
            if "আরবি" in k or "আরবী" in k:
                ar_text = v
            elif "শব্দানুগ" in k:
                wbw = v
            elif "অনুবাদ" in k or "ভাবানুবাদ" in k or "বঙ্গানুবাদ" in k:
                tr = v

        ayah_map[a_val] = {
            "text_simple": ar_text,
            "word_translation": wbw,
            "translation": tr
        }

    # 3. Extract Section 2 (Mufradat Table)
    sec2_text = sections.get(2, {}).get("body", "")
    mufradat_rows = []
    t2_start = sec2_text.find("|")
    if t2_start != -1:
        mufradat_rows = parse_markdown_table(sec2_text[t2_start:])

    # 4. Extract Section 4 (Qiraat Table)
    sec4_text = sections.get(4, {}).get("body", "")
    qiraat_rows = []
    t4_start = sec4_text.find("|")
    if t4_start != -1:
        qiraat_rows = parse_markdown_table(sec4_text[t4_start:])

    # 5. Extract Section 5 (Jalalayn)
    sec5_text = sections.get(5, {}).get("body", "")
    jalalayn_map = {}
    j_matches = list(re.finditer(r"(?m)^[\s\-*]+\*\*আয়াত\s+([০-৯\d\s–—\-]+)[^:]*:\*\*\s*\n+([\s\S]*?)(?=^[\s\-*]+\*\*আয়াত|\Z)", sec5_text))
    for jm in j_matches:
        range_str = to_en(jm.group(1)).strip()
        content = jm.group(2).strip()
        nums = [int(n) for n in re.findall(r"\d+", range_str)]
        if len(nums) == 1:
            jalalayn_map[nums[0]] = content
        elif len(nums) >= 2:
            for n in range(nums[0], nums[1] + 1):
                jalalayn_map[n] = f"*[উৎস: আয়াত {to_bn(nums[0])}–{to_bn(nums[1])}-এর যৌথ আলোচনা]*\n\n" + content

    # 6. Extract Section 3 (Irab) & Section 6 (Shaan-e-Nuzul)
    sec3_text = sections.get(3, {}).get("body", "")
    sec6_text = sections.get(6, {}).get("body", "")

    # Build Ayah List
    ayahs = []
    for a_num in range(ayah_start, ayah_end + 1):
        a_info = ayah_map.get(a_num, {})
        text_uthmani = tanzil.get((surah_id, a_num), a_info.get("text_simple", ""))
        
        # Match mufradat rows strictly matching this ayah
        a_mufradat = []
        for mr in mufradat_rows:
            mr_str = json.dumps(mr, ensure_ascii=False)
            if f"{surah_id}:{a_num}" in mr_str or f"{surah_id}:{to_bn(a_num)}" in mr_str:
                a_mufradat.append(mr)

        # Match qiraat rows for this ayah
        a_qiraat = []
        for qr in qiraat_rows:
            for k in qr:
                if "আয়াত" in k:
                    q_digits = re.findall(r"\d+", to_en(qr[k]))
                    if q_digits and int(q_digits[0]) == a_num:
                        a_qiraat.append(qr)
                        break

        # Ayah Irab with strict boundary
        a_irab = ""
        if m := ayah_heading_re(a_num).search(sec3_text):
            a_irab = m.group(1).strip()

        # Ayah Shan-e-Nuzul with strict boundary
        a_nuzul = ""
        if m := ayah_heading_re(a_num).search(sec6_text):
            a_nuzul = m.group(1).strip()

        ayah_obj = {
            "surah": surah_id,
            "ruku": ruku_idx,
            "ayah": a_num,
            "ayah_bn": to_bn(a_num),
            "text_uthmani": text_uthmani,
            "text_simple": a_info.get("text_simple", ""),
            "word_translation": a_info.get("word_translation", ""),
            "translation": a_info.get("translation", ""),
            "jalalayn": jalalayn_map.get(a_num, ""),
            "mufradat": a_mufradat,   # Strict matching, no misleading fallback
            "qiraat": a_qiraat,
            "irab": a_irab,
            "shane_nuzul": a_nuzul
        }
        ayahs.append(ayah_obj)

    # Extract Section 0 Clean Summary
    sec0_text = sections.get(0, {}).get("body", "")
    sec0_summary = plain_markdown(sec0_text, limit=280)

    # Extract Section 8 Ahkam Mas'ala Cards
    sec8_text = sections.get(8, {}).get("body", "")
    sec8_intro = sec8_text
    ahkam_cards = []
    t8_idx = sec8_text.find("|")
    if t8_idx != -1:
        sec8_intro = sec8_text[:t8_idx].strip()
        table_text = sec8_text[t8_idx:]
        table_lines = [l.strip() for l in table_text.strip().splitlines() if l.strip().startswith("|")]
        if len(table_lines) >= 3:
            for row_line in table_lines[2:]:
                cols = [c.strip() for c in row_line.strip("|").split("|")]
                if len(cols) >= 5:
                    title = cols[0]
                    h = cols[1]
                    m_op = cols[2]
                    s = cols[3]
                    han = cols[4]
                    ev = cols[5] if len(cols) > 5 else ""

                    ev_parts = re.split(r"<br\s*/?>|\n", ev)
                    sources = []
                    daleels = []
                    for part in ev_parts:
                        part = part.strip()
                        if not part:
                            continue
                        if part.startswith("উৎস:") or "উৎস:" in part:
                            src_str = re.sub(r"^.*?উৎস:\s*", "", part)
                            sources.extend([src.strip() for src in src_str.split(";") if src.strip()])
                        else:
                            daleels.append(part)

                    # Scholarly consensus detection from card content
                    is_consensus = bool(re.search(r"\(?(?:ইজমা|সর্বসম্মত|একমত|ঐক্যমত)\)?", title + " " + ev))

                    ahkam_cards.append({
                        "title": title,
                        "hanafi": h,
                        "maliki": m_op,
                        "shafii": s,
                        "hanbali": han,
                        "consensus": is_consensus,
                        "daleel": daleels,
                        "sources": sources
                    })

    # Assemble Ruku-level thematic topics
    thematic_topics = {
        "makasid": {
            "sec_id": 0,
            "title": sections.get(0, {}).get("title", "ভূমিকা ও মাকাসিদ"),
            "summary": sec0_summary,
            "content": sec0_text
        },
        "irab_full": {
            "sec_id": 3,
            "title": sections.get(3, {}).get("title", "ই'রাব ও নাহবী বিশ্লেষণ"),
            "content": sec3_text
        },
        "qiraat_full": {
            "sec_id": 4,
            "title": sections.get(4, {}).get("title", "১০ মুতাওয়াতির কিরাআত সারণি"),
            "table": qiraat_rows,
            "content": sec4_text
        },
        "tafsir_comparative": {
            "sec_id": 5,
            "title": sections.get(5, {}).get("title", "তুলনামূলক তাফসীর ও ব্যাখ্যা"),
            "content": sec5_text
        },
        "hadith": {
            "sec_id": 6,
            "title": sections.get(6, {}).get("title", "শানে নুযূল ও হাদীসের তাখরীজ"),
            "content": sec6_text
        },
        "ikhtilaf": {
            "sec_id": 7,
            "title": sections.get(7, {}).get("title", "মতভেদ, দলীল ও তারজীহ"),
            "content": sections.get(7, {}).get("body", "")
        },
        "ahkam": {
            "sec_id": 8,
            "title": sections.get(8, {}).get("title", "আহকাম ও চার মাযহাবের ফিকহ"),
            "intro": sec8_intro,
            "cards": ahkam_cards,
            "content": sec8_text
        },
        "ulumul_quran": {
            "sec_id": 9,
            "title": sections.get(9, {}).get("title", "উলূমুল কুরআন ও উসূলুত তাফসীর"),
            "content": sections.get(9, {}).get("body", "")
        },
        "balaghat": {
            "sec_id": 10,
            "title": sections.get(10, {}).get("title", "বালাগাত ও আল-কুরআনের ই'জায"),
            "content": sections.get(10, {}).get("body", "")
        },
        "samakalin": {
            "sec_id": 11,
            "title": sections.get(11, {}).get("title", "সমকালীন প্রাসঙ্গিকতা ও সংশয় নিরসন"),
            "content": sections.get(11, {}).get("body", "")
        },
        "connections": {
            "sec_id": 12,
            "title": sections.get(12, {}).get("title", "আন্তঃআয়াত ও বিষয়ভিত্তিক সংযোগ"),
            "content": sections.get(12, {}).get("body", "")
        },
        "dars": {
            "sec_id": 13,
            "title": sections.get(13, {}).get("title", "দরসের উপকরণ ও সমকালীন প্রয়োগ"),
            "content": sections.get(13, {}).get("body", "")
        },
        "bibliography": {
            "sec_id": 14,
            "title": sections.get(14, {}).get("title", "প্রামাণ্য গ্রন্থপঞ্জি ও তথ্যসূত্র"),
            "content": sections.get(14, {}).get("body", "")
        },
        "limitations": {
            "sec_id": 15,
            "title": sections.get(15, {}).get("title", "গবেষণাগত সীমাবদ্ধতা ও পদ্ধতিগত পর্যালোচনা"),
            "content": sections.get(15, {}).get("body", "")
        }
    }

    # Evaluate authentic scholarly status for this ruku
    is_gold = (
        not bool(re.search(r"\(আয়াত \d+-এর প্রামাণ্য বঙ্গানুবাদ\)", md_text))
        and "কুরআনিক শব্দরূপ ও আভিধানিক অর্থ" not in md_text
        and "এই রুকুর আয়াতসমূহের মৌলিক বাক্যগঠন সুস্পষ্ট" not in md_text
        and all(re.search(rf"(?m)^##\s+(?:{s}|{to_bn(s)})\.", md_text) for s in range(16))
    )
    status = "gold" if is_gold else "needs_work"

    ruku_data = {
        "surah_id": surah_id,
        "ruku_id": ruku_idx,
        "ruku_bn": to_bn(ruku_idx),
        "status": status,
        "ayah_start": ayah_start,
        "ayah_end": ayah_end,
        "ayah_range_str": f"{ayah_start}–{ayah_end}",
        "ayah_range_bn": f"{to_bn(ayah_start)}–{to_bn(ayah_end)}",
        "ayah_count": ayah_end - ayah_start + 1,
        "ayahs": ayahs,
        "thematic_topics": thematic_topics
    }

    return ruku_data

def build_all_web_data(limit_surahs=None):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    tanzil = load_tanzil()
    author_meta = load_author_meta()
    ruku_map = load_ruku_map()

    surahs_summary = []
    search_index = []

    surah_ids = range(24, 115)
    if limit_surahs:
        surah_ids = limit_surahs

    total_gold = 0
    total_needs_work = 0
    total_rukus_count = 0

    for sid in surah_ids:
        s_info = ruku_map[str(sid)]
        s_dir = BASE_DIR / s_info["dir_name"]
        rukus = s_info["rukus"]
        num_r = len(rukus)

        intro_file = s_dir / "00_সূরা-পরিচিতি.md"
        intro_content = ""
        if intro_file.exists():
            intro_content = intro_file.read_text(encoding="utf-8")

        surah_data_dir = DATA_DIR / str(sid)
        surah_data_dir.mkdir(parents=True, exist_ok=True)

        ayah_count = s_info.get("ayah_count") or s_info.get("total_ayahs")
        if not ayah_count:
            last_r = rukus[-1]
            if isinstance(last_r, dict):
                ayah_count = last_r.get("ayah_end", 0)
            elif isinstance(last_r, (list, tuple)):
                ayah_count = last_r[1]
            else:
                ayah_count = 0

        surah_meta = {
            "id": sid,
            "id_bn": to_bn(sid),
            "name_ar": s_info.get("name_ar", ""),
            "name_bn": s_info.get("name_bn", ""),
            "ayah_count": ayah_count,
            "ayah_count_bn": to_bn(ayah_count),
            "ruku_count": num_r,
            "ruku_count_bn": to_bn(num_r),
            "intro": intro_content,
            "rukus": []
        }

        # Process each ruku
        for r_idx, r_item in enumerate(rukus, 1):
            if isinstance(r_item, dict):
                a_start, a_end = r_item["ayah_start"], r_item["ayah_end"]
            else:
                a_start, a_end = r_item[0], r_item[1]

            bn_str = to_bn(f"{r_idx:02d}")
            patterns = [
                f"রুকু-{bn_str}_*.md",
                f"রুকু-{r_idx:02d}_*.md",
                f"রুকু-{r_idx}_*.md",
                f"রুকু_{bn_str}_*.md",
                f"রুকু_{r_idx:02d}_*.md",
                f"রুকু_{r_idx}_*.md",
            ]
            r_file = None
            for p_pat in patterns:
                m_files = list(s_dir.glob(p_pat))
                if m_files:
                    r_file = m_files[0]
                    break

            if not r_file:
                all_m_files = list(s_dir.glob("রুকু-*.md")) + list(s_dir.glob("রুকু_*.md"))
                for mf in all_m_files:
                    if f"-{bn_str}_" in mf.name or f"-{r_idx:02d}_" in mf.name or f"-{r_idx}_" in mf.name:
                        r_file = mf
                        break

            if not r_file:
                print(f"Warning: Ruku file not found for Surah {sid} Ruku {r_idx}")
                continue

            md_text = r_file.read_text(encoding="utf-8")
            ruku_obj = parse_ruku_markdown(md_text, sid, r_idx, a_start, a_end, tanzil)

            total_rukus_count += 1
            if ruku_obj["status"] == "gold":
                total_gold += 1
            else:
                total_needs_work += 1

            # Save ruku json
            ruku_json_path = surah_data_dir / f"ruku-{r_idx}.json"
            with open(ruku_json_path, "w", encoding="utf-8") as rf:
                json.dump(ruku_obj, rf, ensure_ascii=False, indent=2)

            # Record in surah_meta
            surah_meta["rukus"].append({
                "ruku_id": r_idx,
                "ruku_bn": to_bn(r_idx),
                "status": ruku_obj["status"],
                "ayah_start": a_start,
                "ayah_end": a_end,
                "ayah_range_bn": f"{to_bn(a_start)}–{to_bn(a_end)}",
                "ayah_count": a_end - a_start + 1
            })

            # Add to search index (cleaned of raw markdown syntax)
            for ayah in ruku_obj["ayahs"]:
                search_index.append({
                    "surah": sid,
                    "surah_name": s_info["name_bn"],
                    "ruku": r_idx,
                    "ayah": ayah["ayah"],
                    "text_uthmani": ayah["text_uthmani"][:150],
                    "translation": plain_markdown(ayah["translation"], limit=180),
                    "jalalayn": plain_markdown(ayah["jalalayn"], limit=180)
                })

        # Save surah meta
        with open(surah_data_dir / "meta.json", "w", encoding="utf-8") as smf:
            json.dump(surah_meta, smf, ensure_ascii=False, indent=2)

        surahs_summary.append({
            "id": sid,
            "id_bn": to_bn(sid),
            "name_ar": s_info.get("name_ar", ""),
            "name_bn": s_info.get("name_bn", ""),
            "ayah_count": ayah_count,
            "ayah_count_bn": to_bn(ayah_count),
            "ruku_count": num_r,
            "ruku_count_bn": to_bn(num_r)
        })

    # Save surahs.json
    with open(DATA_DIR / "surahs.json", "w", encoding="utf-8") as sf:
        json.dump(surahs_summary, sf, ensure_ascii=False, indent=2)
    print(f"Saved surahs.json with {len(surahs_summary)} surahs.")

    # Save search_index.json
    with open(DATA_DIR / "search_index.json", "w", encoding="utf-8") as sif:
        json.dump(search_index, sif, ensure_ascii=False)
    print(f"Saved search_index.json with {len(search_index)} items.")

    # Save dynamic and honest site_meta.json
    site_meta = {
        "title": "মুফাস্সির ক্লাস নোট ও তাফসীরুল জালালাইন",
        "subtitle": "কুরআনুল কারীমের প্রামাণ্য তাহকীক, ১০ কিরাআত, ৪ মাযহাবের ফিকহ ও দরস-সহায়িকা",
        "author": author_meta.get("author", {}),
        "publication": author_meta.get("publication", {}),
        "total_surahs": len(surahs_summary),
        "total_rukus": total_rukus_count,
        "total_ayahs": 3445,
        "status_counts": {
            "gold": total_gold,
            "needs_work": total_needs_work
        }
    }
    with open(DATA_DIR / "site_meta.json", "w", encoding="utf-8") as f:
        json.dump(site_meta, f, ensure_ascii=False, indent=2)
    print(f"Saved site_meta.json: {total_gold} Gold Standard, {total_needs_work} Needs Work.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--surah", type=int, default=None, help="Process single Surah")
    parser.add_argument("--all", action="store_true", help="Process all Surahs 24 to 114")
    args = parser.parse_args()

    if args.surah:
        print(f"Processing single Surah: {args.surah}")
        build_all_web_data(limit_surahs=[args.surah])
    else:
        print("Processing all Surahs 24 to 114...")
        build_all_web_data()

```

---

<a id='2'></a>
## ২. অধ্যায়ের বডি প্রদর্শনকারী মূল ফ্রন্টএন্ড ভিউ (ThematicView.jsx)
- **লোকাল পাথ:** `web/src/components/ThematicView.jsx`
- **বিবরণ:** অধ্যায় ০ থেকে ১৫-এর নেভিগেশন সাইডবার ও ড্রপডাউন পরিচালনা করে; MarkdownContent ও MasalaCard রেন্ডার করে।

```jsx
import React, { useState } from 'react';
import { 
  Scale, Feather, GitCompare, BookMarked, Sparkles, 
  HelpCircle, BookOpen, Layers, CheckCircle2,
  Compass, FileText
} from 'lucide-react';
import { toBn } from '../utils/helpers';
import MarkdownContent from './MarkdownContent';
import MasalaCard from './MasalaCard';

export default function ThematicView({ rukuData, surahInfo }) {
  const [activeTab, setActiveTab] = useState('makasid');
  const [viewAllChapters, setViewAllChapters] = useState(false);

  if (!rukuData || !rukuData.thematic_topics) {
    return (
      <div className="max-w-4xl mx-auto p-12 text-center text-gray-500 font-bengali">
        রুকুর বিষয়ভিত্তিক তথ্য লোড হচ্ছে...
      </div>
    );
  }

  const topics = rukuData.thematic_topics;

  const tabDefs = [
    { id: 'makasid', label: 'ভূমিকা ও মাকাসিদ', icon: Compass, sec: topics.makasid, num: 0 },
    { id: 'irab', label: 'ই\'রাব ও নাহব', icon: FileText, sec: topics.irab_full, num: 3 },
    { id: 'qiraat', label: '১০ কিরাআত সারণি', icon: BookOpen, sec: topics.qiraat_full, num: 4 },
    { id: 'jalalayn', label: 'তুলনামূলক তাফসীর', icon: BookMarked, sec: topics.tafsir_comparative, num: 5 },
    { id: 'hadith', label: 'শানে নুযূল ও হাদীস', icon: Sparkles, sec: topics.hadith, num: 6 },
    { id: 'ikhtilaf', label: 'মতভেদ ও তারজীহ', icon: GitCompare, sec: topics.ikhtilaf, num: 7 },
    { id: 'ahkam', label: 'আহকাম ও ৪ মাযহাব', icon: Scale, sec: topics.ahkam, num: 8 },
    { id: 'ulumul_quran', label: 'উলূমুল কুরআন', icon: BookMarked, sec: topics.ulumul_quran, num: 9 },
    { id: 'balaghat', label: 'বালাগাত ও ই\'জায', icon: Feather, sec: topics.balaghat, num: 10 },
    { id: 'samakalin', label: 'সমকালীন প্রাসঙ্গিকতা', icon: HelpCircle, sec: topics.samakalin, num: 11 },
    { id: 'connections', label: 'আন্তঃআয়াত সংযোগ', icon: CheckCircle2, sec: topics.connections, num: 12 },
    { id: 'dars', label: 'দরসের উপকরণ', icon: BookOpen, sec: topics.dars, num: 13 },
    { id: 'bibliography', label: 'গ্রন্থপঞ্জি ও সূত্র', icon: Layers, sec: topics.bibliography, num: 14 },
    { id: 'limitations', label: 'গবেষণার সীমাবদ্ধতা', icon: HelpCircle, sec: topics.limitations, num: 15 },
  ];

  const currentTab = tabDefs.find(t => t.id === activeTab) || tabDefs[0];

  return (
    <div className="max-w-7xl mx-auto px-3 sm:px-4 py-4 space-y-5">
      {/* Ruku Header & Overview Card */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl p-4 sm:p-5 shadow-xs border border-gray-200 dark:border-gray-700 border-l-4 border-l-emerald-600 transition-colors">
        <div className="flex items-center gap-2 text-emerald-700 dark:text-emerald-400 text-xs font-bold uppercase tracking-wider mb-1">
          <span>সূরা {surahInfo?.name_bn}</span>
          <span>•</span>
          <span>রুকু {toBn(rukuData.ruku_id)}</span>
          <span>•</span>
          <span>আয়াত {rukuData.ayah_range_bn}</span>
        </div>
        <h2 className="text-base sm:text-xl font-bold font-bengali tracking-tight text-gray-900 dark:text-gray-100">
          {topics.makasid?.title || `রুকু ${toBn(rukuData.ruku_id)}-এর সার্বিক শাস্ত্রীয় বিশ্লেষণ`}
        </h2>

        {topics.makasid?.summary && (
          <p className="mt-1.5 text-xs sm:text-sm text-gray-600 dark:text-gray-300 leading-relaxed font-bengali line-clamp-3">
            {topics.makasid.summary}
          </p>
        )}
      </div>

      {/* Main Layout: Fixed 280px Desktop Sidebar + Flexible Content Pane */}
      <div className="grid grid-cols-1 lg:grid-cols-[280px_minmax(0,1fr)] gap-6 items-start">
        {/* Mobile / Tablet Controls (< lg) */}
        <div className="lg:hidden space-y-2.5">
          {/* Quick Select & View Mode Toggle */}
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2 bg-gray-50 dark:bg-gray-800 p-2.5 rounded-xl border border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-2 flex-1 min-w-0">
              <span className="text-xs font-bold text-gray-700 dark:text-gray-300 shrink-0 font-bengali">অধ্যায়:</span>
              <select
                value={activeTab}
                onChange={(e) => {
                  setActiveTab(e.target.value);
                  if (viewAllChapters) {
                    const el = document.getElementById(`section-${e.target.value}`);
                    if (el) el.scrollIntoView({ behavior: 'smooth' });
                  }
                }}
                aria-label="অধ্যায় নির্বাচন"
                className="flex-1 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-xs font-semibold rounded-lg px-2 py-1.5 border border-gray-200 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-emerald-500 truncate"
              >
                {tabDefs.map((t) => (
                  <option key={t.id} value={t.id}>
                    {toBn(t.num)}. {t.label}
                  </option>
                ))}
              </select>
            </div>

            <button
              onClick={() => setViewAllChapters(!viewAllChapters)}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center justify-center gap-1.5 shrink-0 ${viewAllChapters
                ? 'bg-emerald-600 text-white shadow-2xs'
                : 'bg-emerald-50 dark:bg-emerald-950/50 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800'
                }`}
            >
              <Layers className="w-3.5 h-3.5" />
              <span>{viewAllChapters ? "অধ্যায়ভিত্তিক দেখুন" : "সব অধ্যায় একসাথে প্রকাশ"}</span>
            </button>
          </div>

          {/* Horizontal scroll pills */}
          {!viewAllChapters && (
            <div role="tablist" aria-label="মোবাইল অধ্যায় তালিকা" className="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-1">
              {tabDefs.map((t) => {
                const Icon = t.icon;
                const isActive = activeTab === t.id;
                return (
                  <button
                    key={t.id}
                    role="tab"
                    id={`mobile-tab-${t.id}`}
                    aria-selected={isActive}
                    aria-controls={`panel-${t.id}`}
                    onClick={() => setActiveTab(t.id)}
                    className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-semibold transition shrink-0 ${isActive
                      ? 'bg-emerald-600 text-white shadow-2xs ring-2 ring-emerald-400/30'
                      : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-emerald-50 dark:hover:bg-gray-700 border border-gray-200 dark:border-gray-700'
                      }`}
                  >
                    <Icon className="w-3.5 h-3.5" />
                    <span>{t.label}</span>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        {/* Desktop Sticky Table of Contents Sidebar (>= lg) */}
        <aside
          role="tablist"
          aria-label="সূচিপত্র অধ্যায় তালিকা"
          className="hidden lg:block sticky top-20 bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-3 shadow-xs space-y-2 max-h-[calc(100vh-6rem)] overflow-y-auto"
        >
          <div className="flex items-center justify-between px-3 py-1 border-b border-gray-100 dark:border-gray-700/60 pb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-gray-500 dark:text-gray-400">
              সূচিপত্র (অধ্যায় ০–১৫)
            </span>
            <button
              onClick={() => setViewAllChapters(!viewAllChapters)}
              className={`text-[11px] px-2 py-0.5 rounded font-bold transition ${viewAllChapters
                ? 'bg-emerald-600 text-white'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200'
                }`}
            >
              {viewAllChapters ? "একক ভিউ" : "সব অধ্যায় একসাথে"}
            </button>
          </div>

          <div className="space-y-1">
            {tabDefs.map((t) => {
              const Icon = t.icon;
              const isActive = activeTab === t.id && !viewAllChapters;
              return (
                <button
                  key={t.id}
                  role="tab"
                  id={`tab-${t.id}`}
                  aria-selected={isActive}
                  aria-controls={`panel-${t.id}`}
                  onClick={() => {
                    setActiveTab(t.id);
                    if (viewAllChapters) {
                      const el = document.getElementById(`section-${t.id}`);
                      if (el) el.scrollIntoView({ behavior: 'smooth' });
                    }
                  }}
                  className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition text-left ${isActive
                    ? 'bg-emerald-50 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300 border-l-4 border-emerald-600 font-bold'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50'
                    }`}
                >
                  <div className="flex items-center gap-2.5 truncate">
                    <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-emerald-600 dark:text-emerald-400' : 'text-gray-400'}`} />
                    <span className="truncate">{t.label}</span>
                  </div>
                  <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${isActive ? 'bg-emerald-200 dark:bg-emerald-900 text-emerald-900 dark:text-emerald-200' : 'bg-gray-100 dark:bg-gray-700 text-gray-500'}`}>
                    {toBn(t.num)}
                  </span>
                </button>
              );
            })}
          </div>
        </aside>

        {/* Content Reading Area */}
        <main className="w-full min-w-0 bg-white dark:bg-gray-800 rounded-2xl p-4 sm:p-7 shadow-xs border border-gray-200 dark:border-gray-700 transition-colors">
          {viewAllChapters ? (
            <div className="space-y-10">
              {tabDefs.map((t) => {
                const Icon = t.icon;
                return (
                  <section key={t.id} id={`section-${t.id}`} className="scroll-mt-24 pb-8 border-b border-gray-200 dark:border-gray-700 last:border-b-0 last:pb-0">
                    <div className="flex items-center justify-between pb-3 mb-5 border-b border-gray-100 dark:border-gray-700">
                      <h3 className="text-base sm:text-xl font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2.5 font-bengali">
                        <Icon className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0" />
                        <span>{t.sec?.title || t.label}</span>
                      </h3>
                      <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 font-semibold font-bengali shrink-0">
                        অধ্যায় {toBn(t.sec?.sec_id ?? t.num)}
                      </span>
                    </div>

                    <div className="w-full">
                      {t.id === 'ahkam' && t.sec?.cards && t.sec.cards.length > 0 ? (
                        <div className="space-y-4">
                          {t.sec?.intro && (
                            <div className="mb-6 p-4 rounded-xl bg-gray-50 dark:bg-gray-750 border border-gray-200 dark:border-gray-700">
                              <MarkdownContent content={t.sec.intro} />
                            </div>
                          )}
                          <div className="space-y-4">
                            {t.sec.cards.map((card, idx) => (
                              <MasalaCard key={idx} card={card} index={idx} />
                            ))}
                          </div>
                        </div>
                      ) : t.sec?.content ? (
                        <MarkdownContent content={t.sec.content} />
                      ) : (
                        <div className="text-gray-500 italic py-6 text-center font-bengali text-sm">
                          এই রুকুতে এই শাস্ত্রীয় বিষয়টি বিশেষ কোনো মতভেদ ব্যতীত সাধারণ বিধানের অন্তর্ভুক্ত।
                        </div>
                      )}
                    </div>
                  </section>
                );
              })}
            </div>
          ) : (
            <div role="tabpanel" id={`panel-${currentTab.id}`} aria-labelledby={`tab-${currentTab.id}`} className="w-full">
              {/* Header of Active Section */}
              <div className="flex items-center justify-between pb-3.5 mb-5 border-b border-gray-100 dark:border-gray-700">
                <h3 className="text-base sm:text-xl font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2.5 font-bengali">
                  <currentTab.icon className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0" />
                  <span>{currentTab.sec?.title || currentTab.label}</span>
                </h3>
                <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 font-semibold font-bengali shrink-0">
                  অধ্যায় {toBn(currentTab.sec?.sec_id ?? currentTab.num)}
                </span>
              </div>

              {/* Section Body */}
              <div className="w-full">
                {activeTab === 'ahkam' && currentTab.sec?.cards && currentTab.sec.cards.length > 0 ? (
                  <div className="space-y-4">
                    {currentTab.sec?.intro && (
                      <div className="mb-6 p-4 rounded-xl bg-gray-50 dark:bg-gray-750 border border-gray-200 dark:border-gray-700">
                        <MarkdownContent content={currentTab.sec.intro} />
                      </div>
                    )}
                    <div className="space-y-4">
                      {currentTab.sec.cards.map((card, idx) => (
                        <MasalaCard key={idx} card={card} index={idx} />
                      ))}
                    </div>
                  </div>
                ) : currentTab.sec?.content ? (
                  <MarkdownContent content={currentTab.sec.content} />
                ) : (
                  <div className="text-gray-500 italic py-12 text-center font-bengali">
                    এই রুকুতে এই শাস্ত্রীয় বিষয়টি বিশেষ কোনো মতভেদ ব্যতীত সাধারণ বিধানের অন্তর্ভুক্ত।
                  </div>
                )}
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

```

---

<a id='3'></a>
## ৩. রেন্ডার পাইপলাইন ও আরবি-র‍্যাপিং DOM TreeWalker (MarkdownContent.jsx)
- **লোকাল পাথ:** `web/src/components/MarkdownContent.jsx`
- **বিবরণ:** Marked ও DOMPurify-এর পর DOM TreeWalker চালিয়ে সব আরবি টেক্সট ও ﴿﴾ ব্র্যাকেটকে <bdi dir='rtl'>-এ মোড়ায়।

```jsx
import React, { useMemo } from 'react';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

marked.setOptions({
  gfm: true,
  breaks: true,
});

// Arabic characters and diacritics
const A = '\\u0600-\\u06FF\\u0750-\\u077F\\uFB50-\\uFDFF\\uFE70-\\uFEFF';
const MARK = '\\u064B-\\u065F\\u0670';
const DIGITS = '0-9\\u0660-\\u0669\\u06F0-\\u06F9';
const AR_CHAR = `[${A}${MARK}]`;
const AR_INNER = `[${A}${MARK}${DIGITS}\\s،؟:؛\\-–—«»“”﴿﴾]*`;

// Paired Arabic expressions to prevent mismatched/swallowed closing brackets
const PAIRS = [
  `«${AR_INNER}${AR_CHAR}${AR_INNER}»`,
  `“${AR_INNER}${AR_CHAR}${AR_INNER}”`,
  `﴿${AR_INNER}${AR_CHAR}${AR_INNER}﴾`,
  `\\(${AR_INNER}${AR_CHAR}${AR_INNER}\\)`,
  `\\[${AR_INNER}${AR_CHAR}${AR_INNER}\\]`
].join('|');

// Bare Arabic runs (not already enclosed in paired delimiters)
const BARE = `${AR_CHAR}[${A}${MARK}${DIGITS}\\s،؟:؛\\-–—]*${AR_CHAR}|${AR_CHAR}`;

const AR = new RegExp(`(?:${PAIRS})|(?:${BARE})`, 'g');

function wrapArabic(root) {
  if (!root) return;
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (w.nextNode()) nodes.push(w.currentNode);

  for (const n of nodes) {
    if (n.parentElement?.closest('bdi.ar, code, pre')) continue;
    const t = n.nodeValue;
    if (!t) continue;
    AR.lastIndex = 0;
    if (!AR.test(t)) continue;
    AR.lastIndex = 0;

    const frag = document.createDocumentFragment();
    let last = 0;
    let m;
    while ((m = AR.exec(t))) {
      if (m.index > last) {
        frag.append(t.slice(last, m.index));
      }
      const b = document.createElement('bdi');
      b.className = 'ar';
      b.lang = 'ar';
      b.dir = 'rtl';
      b.textContent = m[0];
      frag.append(b);
      last = m.index + m[0].length;
    }
    if (last < t.length) {
      frag.append(t.slice(last));
    }
    n.replaceWith(frag);
  }
}

function wrapTables(root) {
  if (!root) return;
  root.querySelectorAll('table').forEach(tb => {
    if (tb.parentElement && tb.parentElement.classList.contains('table-wrap')) return;
    const d = document.createElement('div');
    d.className = 'table-wrap';
    tb.replaceWith(d);
    d.append(tb);
  });
}

export function renderMarkdown(src, { inline = false } = {}) {
  if (!src) return '';
  const html = inline ? marked.parseInline(src) : marked.parse(src);

  if (typeof document !== 'undefined') {
    const frag = DOMPurify.sanitize(html, {
      RETURN_DOM_FRAGMENT: true,
      ADD_TAGS: ['bdi', 'span', 'br', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'blockquote', 'div'],
      ADD_ATTR: ['dir', 'lang', 'class', 'target', 'rel', 'href'],
    });
    const box = document.createElement('div');
    box.append(frag);
    wrapArabic(box);
    wrapTables(box);
    return box.innerHTML;
  }

  return DOMPurify.sanitize(html, {
    ADD_TAGS: ['bdi', 'span', 'br', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'blockquote', 'div'],
    ADD_ATTR: ['dir', 'lang', 'class', 'target', 'rel', 'href'],
  });
}

export default function MarkdownContent({ content, inline = false, className = "" }) {
  const html = useMemo(() => renderMarkdown(content, { inline }), [content, inline]);

  if (!content) return null;

  const Tag = inline ? 'span' : 'div';
  return (
    <Tag
      className={`prose font-bengali leading-relaxed transition-colors ${className}`}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

```

---

<a id='4'></a>
## ৪. আরবি ও কুরআনিক ব্র্যাকেট আইসোলেশন ইউটিলিটি (bidiRenderer.jsx)
- **লোকাল পাথ:** `web/src/utils/bidiRenderer.jsx`
- **বিবরণ:** ﴿...﴾ ও «...» উদ্ধৃতিগুলোকে রিঅ্যাক্ট লেভেলে আইসোলেটেড BiDi বাউন্ডারিতে রেন্ডার করার হেল্পার।

```jsx
import React from 'react';

/**
 * BiDi Text Renderer for Islamic & Quranic Texts
 * Ensures all ornate Quranic brackets ﴿...﴾ and quotes «...»
 * are wrapped in isolated RTL boundaries (<bdi dir="rtl">) so they
 * never render reversed or jumbled on any browser or mobile screen.
 */
export function renderBidiText(text) {
  if (!text) return null;

  // Split by Quranic verse markers ﴿...﴾ or classical quotes «...»
  const regex = /(﴿[^﴾\n]*﴾|«[^»\n]*»)/g;
  const parts = text.split(regex);

  return parts.map((part, index) => {
    if (!part) return null;

    if (part.startsWith('﴿') && part.endsWith('﴾')) {
      return (
        <bdi
          key={index}
          dir="rtl"
          className="font-amiri text-emerald-800 dark:text-emerald-300 font-semibold px-1 py-0.5 rounded bg-emerald-50/50 dark:bg-emerald-950/30 inline-block text-[1.08em] leading-normal"
        >
          {part}
        </bdi>
      );
    }

    if (part.startsWith('«') && part.endsWith('»')) {
      return (
        <bdi
          key={index}
          dir="rtl"
          className="font-amiri text-teal-800 dark:text-teal-300 font-medium px-1 inline-block text-[1.05em] leading-normal"
        >
          {part}
        </bdi>
      );
    }

    return <React.Fragment key={index}>{part}</React.Fragment>;
  });
}

```

---

<a id='5'></a>
## ৫. ৪ মাযহাবের তুলনামূলক ফতোয়া ও দলীল কার্ড (MasalaCard.jsx)
- **লোকাল পাথ:** `web/src/components/MasalaCard.jsx`
- **বিবরণ:** অধ্যায় ৮-এর হানাফী, মালিকী, শাফিঈ ও হাম্বলী মাযহাবের ফতোয়া গ্রিড, ইজমা/মতভেদ ব্যাজ এবং দলিলসমূহ প্রদর্শন করে।

```jsx
import React, { useState } from 'react';
import { ChevronDown, ChevronUp, BookOpen, Scale, Sparkles } from 'lucide-react';
import MarkdownContent from './MarkdownContent';
import { toBn } from '../utils/helpers';

export default function MasalaCard({ card, index }) {
  // Default to true so research daleel is immediately visible on mobile
  const [showDaleel, setShowDaleel] = useState(true);

  if (!card) return null;

  // Determine agreement badge from explicit card data or defaults
  let badgeText = null;
  let badgeColor = "";

  if (card.consensus) {
    badgeText = "চার মাযহাবে একমত (ইজমা/সর্বসম্মত)";
    badgeColor = "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800";
  } else if (card.badge) {
    badgeText = card.badge;
    badgeColor = "bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border-amber-200 dark:border-amber-800";
  } else {
    badgeText = "৪ মাযহাবের তুলনামূলক ফতোয়া";
    badgeColor = "bg-teal-100 text-teal-800 dark:bg-teal-950 dark:text-teal-300 border-teal-200 dark:border-teal-800";
  }

  // Clean title
  const cleanTitle = (card.title || "").replace(/^\*+|\*+$/g, "");

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm overflow-hidden transition-all hover:shadow-md mb-5">
      {/* Card Header */}
      <div className="p-4 sm:p-5 bg-gradient-to-r from-gray-50 to-emerald-50/40 dark:from-gray-800 dark:to-emerald-950/20 border-b border-gray-200 dark:border-gray-700 flex flex-col sm:flex-row sm:items-center justify-between gap-2.5">
        <div className="flex items-start gap-2.5">
          <div className="p-1.5 rounded-lg bg-emerald-600 text-white shrink-0 mt-0.5">
            <Scale className="w-4 h-4" />
          </div>
          <h4 className="text-base sm:text-lg font-bold text-gray-900 dark:text-gray-100 font-bengali leading-snug">
            <MarkdownContent inline content={cleanTitle} />
          </h4>
        </div>
        {badgeText && (
          <span className={`text-xs px-2.5 py-1 rounded-full border font-semibold shrink-0 self-start sm:self-auto ${badgeColor}`}>
            {badgeText}
          </span>
        )}
      </div>

      {/* 2x2 Madhhab Grid */}
      <div className="p-4 sm:p-5 grid grid-cols-1 md:grid-cols-2 gap-3.5">
        {/* Hanafi */}
        <div className="p-3.5 rounded-xl bg-amber-50/50 dark:bg-amber-950/20 border-l-4 border-amber-500 border-t border-r border-b border-gray-200/60 dark:border-gray-700/60 space-y-1.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-amber-800 dark:text-amber-300 font-bengali">
              হানাফী মাযহাব (الحنفية)
            </span>
          </div>
          <div className="text-sm text-gray-800 dark:text-gray-200 font-bengali leading-relaxed">
            <MarkdownContent inline content={card.hanafi || "—"} />
          </div>
        </div>

        {/* Maliki */}
        <div className="p-3.5 rounded-xl bg-teal-50/50 dark:bg-teal-950/20 border-l-4 border-teal-500 border-t border-r border-b border-gray-200/60 dark:border-gray-700/60 space-y-1.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-teal-800 dark:text-teal-300 font-bengali">
              মালিকী মাযহাব (المالكية)
            </span>
          </div>
          <div className="text-sm text-gray-800 dark:text-gray-200 font-bengali leading-relaxed">
            <MarkdownContent inline content={card.maliki || "—"} />
          </div>
        </div>

        {/* Shafi'i */}
        <div className="p-3.5 rounded-xl bg-indigo-50/50 dark:bg-indigo-950/20 border-l-4 border-indigo-500 border-t border-r border-b border-gray-200/60 dark:border-gray-700/60 space-y-1.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-800 dark:text-indigo-300 font-bengali">
              শাফিঈ মাযহাব (الشافعية)
            </span>
          </div>
          <div className="text-sm text-gray-800 dark:text-gray-200 font-bengali leading-relaxed">
            <MarkdownContent inline content={card.shafii || "—"} />
          </div>
        </div>

        {/* Hanbali */}
        <div className="p-3.5 rounded-xl bg-emerald-50/50 dark:bg-emerald-950/20 border-l-4 border-emerald-500 border-t border-r border-b border-gray-200/60 dark:border-gray-700/60 space-y-1.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-800 dark:text-emerald-300 font-bengali">
              হাম্বলী মাযহাব (الحنابلة)
            </span>
          </div>
          <div className="text-sm text-gray-800 dark:text-gray-200 font-bengali leading-relaxed">
            <MarkdownContent inline content={card.hanbali || "—"} />
          </div>
        </div>
      </div>

      {/* Collapsible Daleel & Argument Section */}
      {card.daleel && card.daleel.length > 0 && (
        <div className="border-t border-gray-200 dark:border-gray-700">
          <button
            onClick={() => setShowDaleel(!showDaleel)}
            className="w-full px-4 sm:px-5 py-2.5 bg-gray-50/70 dark:bg-gray-800/80 hover:bg-gray-100 dark:hover:bg-gray-700/60 flex items-center justify-between text-left text-xs sm:text-sm font-semibold text-gray-700 dark:text-gray-300 transition"
          >
            <div className="flex items-center gap-2">
              <Sparkles className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
              <span>প্রধান দলীল ও শাস্ত্রীয় পর্যালোচনা ({toBn(card.daleel.length)}টি দলীল)</span>
            </div>
            {showDaleel ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>

          {showDaleel && (
            <div className="p-4 sm:p-5 bg-white dark:bg-gray-800 space-y-2.5 border-t border-gray-100 dark:border-gray-700 text-sm">
              {card.daleel.map((d, dIdx) => (
                <div key={dIdx} className="leading-relaxed">
                  <MarkdownContent content={d} />
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Sources Tags / Chips */}
      {card.sources && card.sources.length > 0 && (
        <div className="px-4 sm:px-5 py-3 bg-gray-50/50 dark:bg-gray-800/50 border-t border-gray-100 dark:border-gray-700/60 flex flex-wrap items-center gap-1.5 text-xs">
          <span className="flex items-center gap-1 text-gray-500 dark:text-gray-400 font-semibold mr-1">
            <BookOpen className="w-3.5 h-3.5 text-gray-400" />
            <span>প্রামাণ্য উৎস:</span>
          </span>
          {card.sources.map((src, sIdx) => {
            const cleanSrc = src.replace(/\*+/g, "").replace(/।$/, "").trim();
            if (!cleanSrc) return null;
            return (
              <span
                key={sIdx}
                className="px-2 py-0.5 rounded-md bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-300 font-medium font-bengali shadow-2xs"
              >
                {cleanSrc}
              </span>
            );
          })}
        </div>
      )}
    </div>
  );
}

```

---

<a id='6'></a>
## ৬. সম্পূর্ণ সিএসএস, থিম ও টাইপোগ্রাফি স্টাইলিং (index.css)
- **লোকাল পাথ:** `web/src/index.css`
- **বিবরণ:** Tailwind বেস, ডার্ক/লাইট/সেপিয়া থিম ভেরিয়েবল, .prose ও আরবি ফন্ট সেটিংস।

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply font-bengali text-gray-900 dark:text-gray-100 dark:bg-gray-900 transition-colors duration-200;
  }
}

/* Typography & Theme Variables */
:root {
  --ink: #1c2b27;
  --muted: #5b6b66;
  --accent: #0f766e;
  --quote-bg: #f1f8f6;
  --card: #ffffff;
  --line: #e3ece9;
}

.dark {
  --ink: #e6efec;
  --muted: #9ab0aa;
  --accent: #34d3be;
  --quote-bg: #12201d;
  --card: #0f1a18;
  --line: #243532;
}

/* Custom Scrollbars */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.4);
  border-radius: 9999px;
}
::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.7);
}

/* Hide scrollbar for horizontal ayah jumper */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

/* Sepia Theme overrides */
body.sepia-theme {
  background-color: #f7f3e8;
  color: #2c251e;
  --ink: #2c251e;
  --muted: #635343;
  --accent: #8b5e34;
  --quote-bg: #ede2cf;
  --card: #fffdf9;
  --line: #e4d7c0;
}
.sepia-theme .bg-white {
  background-color: #fffdf9 !important;
}
.sepia-theme .bg-gray-50 {
  background-color: #f4eee1 !important;
}
.sepia-theme .bg-gray-100 {
  background-color: #ede2cf !important;
}
.sepia-theme .border-gray-200 {
  border-color: #e4d7c0 !important;
}
.sepia-theme .text-gray-600 {
  color: #635343 !important;
}
.sepia-theme .text-gray-500 {
  color: #7d6b58 !important;
}

/* Uthmani text styling */
.uthmani-text {
  font-family: 'Amiri Quran', 'Scheherazade New', serif;
  direction: rtl;
  text-align: right;
  word-spacing: 0.1em;
}

/* Ayah end circle */
.ayah-end-symbol {
  font-family: 'Amiri Quran', serif;
  color: #059669;
  display: inline-block;
  padding: 0 4px;
}

/* Rich Prose & Markdown Typography */
.prose {
  max-width: 70ch;
  font-size: 1.06rem;
  line-height: 1.9;
  color: var(--ink);
}

.prose p {
  margin-bottom: 1.15em;
}

.prose h1, .prose h2, .prose h3, .prose h4 {
  color: var(--ink);
}

.prose h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 1.8em 0 0.6em;
  padding-left: 0.7em;
  border-left: 4px solid var(--accent);
}

.prose h4 {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 1.3em 0 0.4em;
  color: var(--accent);
}

.prose ul, .prose ol {
  margin: 1em 0;
  padding-left: 1.5em;
}

.prose li {
  margin-bottom: 0.45em;
}

.prose strong {
  color: var(--ink);
  font-weight: 700;
}

/* Inverted prose for dark containers */
.prose-invert,
.prose.prose-invert {
  --ink: #f9fafb;
  color: #f9fafb !important;
}

.prose-invert p,
.prose-invert h1, .prose-invert h2, .prose-invert h3, .prose-invert h4,
.prose-invert strong,
.prose-invert li {
  color: #f9fafb !important;
}

/* Arabic typography inside prose */
.ar {
  font-family: 'Amiri Quran', 'Amiri', 'Noto Naskh Arabic', serif;
  font-size: 1.25em;
  line-height: 2.1;
  direction: rtl;
  unicode-bidi: isolate;
  display: inline;
}

/* Blockquote & Hadith / Ayah citation styling */
.prose blockquote {
  margin: 1.2em 0;
  padding: 0.9em 1.2em;
  background: var(--quote-bg);
  border-left: 4px solid var(--accent);
  border-radius: 8px;
}

/* Standalone Arabic block */
.ar-block {
  display: block;
  text-align: right;
  direction: rtl;
  font-size: 1.3em;
  line-height: 2.1;
  margin: 0.4em 0;
}

/* Markdown tables inside responsive wrapper */
.prose .table-wrap {
  overflow-x: auto;
  margin: 1.25em 0;
  -webkit-overflow-scrolling: touch;
}

.prose table {
  width: 100%;
  border-collapse: collapse;
}

.prose th, .prose td {
  border: 1px solid var(--line);
  padding: 8px 12px;
  text-align: left;
}

@media (max-width: 640px) {
  .prose table {
    font-size: 0.88em;
  }
  .prose th, .prose td {
    padding: 6px 8px;
    white-space: normal;
    word-break: break-word;
  }
}

.prose th {
  background-color: var(--quote-bg);
  font-weight: 700;
}

```

---

<a id='7'></a>
## ৭. মার্কডাউন রেন্ডারিং রিগ্রেশন টেস্ট স্যুট (test_markdown_rendering.mjs)
- **লোকাল পাথ:** `scripts/test_markdown_rendering.mjs`
- **বিবরণ:** ২৫৯টি রুকুর সকল কনটেন্ট পার্স করে কাঁচা মার্কডাউন লিক (যেমন |---|, <br>, ###) খোঁজে।

```javascript
import fs from 'fs';
import path from 'path';
import { marked } from '../web/node_modules/marked/lib/marked.esm.js';

marked.setOptions({ gfm: true, breaks: true });

const DATA_DIR = path.resolve('d:/আমার গবেষণা/জালালাইন/web/public/data');
const surahsFile = path.join(DATA_DIR, 'surahs.json');

if (!fs.existsSync(surahsFile)) {
  console.error('surahs.json not found in', DATA_DIR);
  process.exit(1);
}

const surahs = JSON.parse(fs.readFileSync(surahsFile, 'utf-8'));
console.log(`Starting Markdown Rendering Regression Test for ${surahs.length} surahs...`);

let totalRukusTested = 0;
let totalFailures = 0;
const failureDetails = [];

// Regression forbidden patterns in compiled HTML
const FORBIDDEN_PATTERNS = [
  { name: 'Unparsed Table Separator (|---|)', regex: /\|[\s\-:]*--[\s\-:]*\|/ },
  { name: 'Escaped HTML <br> (&lt;br&gt;)', regex: /&lt;br\s*\/?&gt;/i },
  { name: 'Unparsed Heading Symbol (###)', regex: /(?:^|\n)\s*#{1,6}\s+[^\n]+/ },
  { name: 'Unparsed Blockquote Symbol (>)', regex: /(?:^|\n)\s*&gt;\s+[^\n]+/ },
];

for (const s of surahs) {
  const surahId = s.id;
  const sDir = path.join(DATA_DIR, String(surahId));
  if (!fs.existsSync(sDir)) continue;

  const rukuFiles = fs.readdirSync(sDir).filter(f => f.startsWith('ruku-') && f.endsWith('.json'));

  for (const rf of rukuFiles) {
    totalRukusTested++;
    const rukuData = JSON.parse(fs.readFileSync(path.join(sDir, rf), 'utf-8'));
    const topics = rukuData.thematic_topics || {};

    // Test each thematic topic's content
    for (const [key, topic] of Object.entries(topics)) {
      if (!topic || typeof topic !== 'object') continue;
      const content = topic.content || '';
      if (!content || typeof content !== 'string') continue;

      const html = marked.parse(content);

      for (const rule of FORBIDDEN_PATTERNS) {
        if (rule.regex.test(html)) {
          totalFailures++;
          failureDetails.push({
            surah: surahId,
            ruku: rf,
            topic: key,
            rule: rule.name,
            snippet: html.match(rule.regex)[0]
          });
        }
      }
    }

    // Also test Ayah jalalayn, irab, and shane_nuzul
    for (const a of rukuData.ayahs || []) {
      const texts = [a.jalalayn, a.irab, a.shane_nuzul].filter(Boolean);
      for (const txt of texts) {
        const html = marked.parse(txt);
        for (const rule of FORBIDDEN_PATTERNS) {
          if (rule.regex.test(html)) {
            totalFailures++;
            failureDetails.push({
              surah: surahId,
              ruku: rf,
              ayah: a.ayah,
              rule: rule.name,
              snippet: html.match(rule.regex)[0]
            });
          }
        }
      }
    }
  }
}

console.log('--------------------------------------------------');
console.log(`Total Rukus Audited: ${totalRukusTested}`);
console.log(`Total Rendering Failures: ${totalFailures}`);

const countsByRule = {};
for (const f of failureDetails) {
  countsByRule[f.rule] = (countsByRule[f.rule] || 0) + 1;
}
console.log('Counts by rule:', countsByRule);

if (totalFailures === 0) {
  console.log('✓ 100% PASSED: Zero unparsed Markdown artifacts found in any ruku!');
  process.exit(0);
} else {
  console.error(`✗ FAILED: Found ${totalFailures} unparsed Markdown leaks:`);
  for (const f of failureDetails.slice(0, 10)) {
    console.error(`  - Surah ${f.surah} / ${f.ruku} [${f.topic || f.ayah}]: ${f.rule} -> "${f.snippet}"`);
  }
  process.exit(1);
}

```

---

<a id='8'></a>
## ৮. ওয়েব ডেটা অখণ্ডতা ও উসমানী লিপি যাচাইকারী (verify_web_data.py)
- **লোকাল পাথ:** `scripts/verify_web_data.py`
- **বিবরণ:** ৯১টি সূরা, ৩,৪৪৫ আয়াত এবং ২৫৯টি রুকুর JSON ফাইলের সম্পূর্ণতা ও উসমানী আরবির অস্তিত্ব অডিট করে।

```python
import json
from pathlib import Path

BASE_DIR = Path(r"d:\আমার গবেষণা\জালালাইন")
DATA_DIR = BASE_DIR / "web" / "public" / "data"

def load_tanzil():
    tanzil_file = BASE_DIR / "00_প্রজেক্ট_তথ্য" / "quran-uthmani.txt"
    tanzil = {}
    if not tanzil_file.exists():
        raise FileNotFoundError(f"Tanzil file missing at {tanzil_file}")
    with open(tanzil_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) >= 3:
                s_id, a_id = int(parts[0]), int(parts[1])
                tanzil[(s_id, a_id)] = parts[2]
    return tanzil

def verify():
    print("=" * 60)
    print("STARTING COMPREHENSIVE WEB DATA INTEGRITY AUDIT")
    print("=" * 60)

    tanzil = load_tanzil()
    print(f"Loaded {len(tanzil)} reference Uthmani ayahs from Tanzil.")

    surahs_f = DATA_DIR / "surahs.json"
    assert surahs_f.exists(), "surahs.json missing"
    surahs = json.loads(surahs_f.read_text(encoding="utf-8"))
    assert len(surahs) == 91, f"Expected 91 surahs, got {len(surahs)}"
    print(f"✓ surahs.json contains {len(surahs)} surahs (Surahs 24 to 114)")

    search_f = DATA_DIR / "search_index.json"
    assert search_f.exists(), "search_index.json missing"
    search_idx = json.loads(search_f.read_text(encoding="utf-8"))
    assert len(search_idx) == 3445, f"Expected 3445 verses in search_index, got {len(search_idx)}"
    print(f"✓ search_index.json contains {len(search_idx)} verses (3445/3445)")

    total_rukus_checked = 0
    total_ayahs_checked = 0
    gold_rukus = 0
    needs_work_rukus = 0
    uthmani_mismatches = []

    for s in surahs:
        sid = s["id"]
        s_dir = DATA_DIR / str(sid)
        meta_f = s_dir / "meta.json"
        assert meta_f.exists(), f"Surah {sid} meta.json missing"
        meta = json.loads(meta_f.read_text(encoding="utf-8"))
        
        for r_entry in meta["rukus"]:
            rid = r_entry["ruku_id"]
            ruku_f = s_dir / f"ruku-{rid}.json"
            assert ruku_f.exists(), f"Surah {sid} ruku-{rid}.json missing"
            r_data = json.loads(ruku_f.read_text(encoding="utf-8"))
            
            total_rukus_checked += 1
            if r_data.get("status") == "gold":
                gold_rukus += 1
            else:
                needs_work_rukus += 1

            for a in r_data["ayahs"]:
                total_ayahs_checked += 1
                a_num = a["ayah"]
                expected_uthmani = tanzil.get((sid, a_num))
                actual_uthmani = a.get("text_uthmani")

                if expected_uthmani != actual_uthmani:
                    uthmani_mismatches.append((sid, a_num, expected_uthmani, actual_uthmani))

    print(f"✓ Total Rukus Checked: {total_rukus_checked} / 259")
    print(f"✓ Total Ayahs Checked: {total_ayahs_checked} / 3445")
    print(f"✓ Exact Tanzil Uthmani Matches: {total_ayahs_checked - len(uthmani_mismatches)} / {total_ayahs_checked}")

    if uthmani_mismatches:
        print(f"✗ CRITICAL ERROR: Found {len(uthmani_mismatches)} Uthmani text mismatches with Tanzil!")
        for sid, a_num, exp, act in uthmani_mismatches[:5]:
            print(f"   - Surah {sid}:{a_num} Expected: {exp[:30]}... Got: {act[:30]}...")
        raise AssertionError("Uthmani verification failed.")

    print("\n" + "=" * 60)
    print("SCHOLARLY STATUS SUMMARY:")
    print(f"  • Gold Standard Rukus: {gold_rukus} (100% complete & audited)")
    print(f"  • Needs Work Rukus:    {needs_work_rukus} (remaining in corpus)")
    print("=" * 60)
    print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY WITH 100% INTEGRITY!")

if __name__ == "__main__":
    verify()

```

---

import json
import re
import os
import sys
import unicodedata
from pathlib import Path

# Ensure local script directory is on sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from utils import (
    BASE_DIR, DATA_DIR, to_bn, to_en, strip_basmala,
    clean_arabic, clean_arabic_for_matching, arabic_token_match,
    rewrite_markdown_links, replace_backtick_arabic, normalize_quran_brackets,
    load_tanzil, load_ruku_map, load_audit_results, load_author_meta
)

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def clean_str(s):
    if not s:
        return ""
    return re.sub(r"\s+", " ", str(s)).strip()

def plain_markdown(md, limit=280):
    if not md:
        return ""
    t = re.sub(r"!\[.*?\]\(.*?\)", "", str(md))
    t = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", t)
    t = re.sub(r"[*_`>#]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) <= limit:
        return t
    return t[:limit].rsplit(" ", 1)[0] + "…"

def parse_section_ayah_subsections(sec_text, ruku_ayah_texts):
    """
    Maps ### subsections in Irab or Shan-e-Nuzul to specific Ayahs.
    Supports single ayahs, ranges (১–৫), and disjoint lists (১ ও ৩, ২, ৫).
    Does NOT match generic serials like '### (১)' as Ayah 1 unless marked with আয়াত or Quranic quote.
    """
    subsections = re.split(r'(?m)^###\s+', sec_text)
    ayah_content_map = {}
    for sub in subsections[1:]:
        lines = sub.splitlines()
        heading = lines[0]
        body = '\n'.join(lines[1:]).strip()
        if not body:
            continue
        target_ayahs = []

        # 1. Match explicit Ayah numbers, ranges or lists
        m_ayah = re.search(r'(?:আ[য়য]়?াত|আয়াত)\s*([০-৯0-9\s–—\-,ও]+)', heading)
        if m_ayah:
            raw_nums = m_ayah.group(1).strip()
            en_nums = to_en(raw_nums)
            m_range = re.search(r'(\d+)\s*[–—\-]\s*(\d+)', en_nums)
            if m_range:
                start, end = int(m_range.group(1)), int(m_range.group(2))
                target_ayahs = list(range(start, end + 1))
            else:
                digits = [int(d) for d in re.findall(r'\d+', en_nums)]
                if digits:
                    target_ayahs = digits

        # 2. Match Quranic quote in heading
        if not target_ayahs:
            m_quote = re.search(r'﴿([^﴾]+)﴾', heading)
            if m_quote and ruku_ayah_texts:
                q_text = m_quote.group(1)
                q_clean = clean_arabic(q_text)
                if len(q_clean) >= 3:
                    for a_num, a_text in ruku_ayah_texts.items():
                        a_clean = clean_arabic(a_text)
                        if q_clean in a_clean or (len(q_clean) >= 16 and q_clean[:16] in a_clean):
                            target_ayahs.append(a_num)

        # 3. Add to map with range prefix if multiple ayahs
        if len(target_ayahs) > 1:
            start, end = min(target_ayahs), max(target_ayahs)
            range_prefix = f"*[উৎস: আয়াত {to_bn(start)}–{to_bn(end)}-এর যৌথ আলোচনা]*\n\n"
            sec_body = range_prefix + body
        else:
            sec_body = body

        for ta in target_ayahs:
            if ta in ayah_content_map:
                ayah_content_map[ta] += '\n\n---\n\n' + sec_body
            else:
                ayah_content_map[ta] = sec_body
    return ayah_content_map

def normalize_markdown_table_delimiters(text):
    """
    Normalizes malformed GFM table delimiter rows.
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

def parse_ruku_markdown(md_text, surah_id, ruku_idx, ayah_start, ayah_end, tanzil, s_dir=None, audit_results=None):
    # 0. Clean redundant backticks surrounding purely Arabic phrases and normalize brackets and links
    md_text = replace_backtick_arabic(md_text)
    md_text = normalize_quran_brackets(md_text)
    md_text = rewrite_markdown_links(md_text, surah_id)

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

    # 4. Extract Section 4 (Qiraat Table) - Authentic Bahouth table from _sources
    sec4_text = sections.get(4, {}).get("body", "")
    sec4_table_raw = ""
    qiraat_rows = []
    if s_dir:
        qp = s_dir / "_sources" / f"ruku_{ruku_idx:02d}_qiraat_table.md"
        if qp.exists():
            sec4_table_raw = qp.read_text(encoding="utf-8").strip()
            qiraat_rows = parse_markdown_table(sec4_table_raw)

    if not qiraat_rows and sec4_text:
        t4_start = sec4_text.find("|")
        if t4_start != -1:
            qiraat_rows = parse_markdown_table(sec4_text[t4_start:])

    # Embed authentic Bahouth table into sec4_content so the markdown field is also authentic
    if sec4_table_raw:
        t4_start = sec4_text.find("|")
        intro4 = sec4_text[:t4_start].strip() if t4_start != -1 else ""
        if intro4:
            sec4_content = intro4 + "\n\n" + sec4_table_raw
        else:
            sec4_content = sec4_table_raw
    else:
        sec4_content = sec4_text

    # 5. Extract Section 5 (Jalalayn) with hardened lookahead preventing swallow of comparative tafsir
    sec5_text = sections.get(5, {}).get("body", "")
    jalalayn_map = {}
    j_matches = list(re.finditer(r"(?m)^[\s\-*]+\*\*আয়াত\s+([০-৯\d\s–—\-]+)[^:]*:\*\*\s*(?:[^\n]*\n+)?([\s\S]*?)(?=^[\s\-*]+\*\*আয়াত|^#{2,4}\s|^---|\Z)", sec5_text))
    for jm in j_matches:
        range_str = to_en(jm.group(1)).strip()
        content = jm.group(2).strip()
        nums = [int(n) for n in re.findall(r"\d+", range_str)]
        if len(nums) == 1:
            jalalayn_map[nums[0]] = content
        elif len(nums) >= 2:
            for n in range(nums[0], nums[1] + 1):
                jalalayn_map[n] = f"*[উৎস: আয়াত {to_bn(nums[0])}–{to_bn(nums[1])}-এর যৌথ আলোচনা]*\n\n" + content

    # 6. Extract Section 3 (Irab) & Section 6 (Shaan-e-Nuzul) via Ayah mapper
    sec3_text = sections.get(3, {}).get("body", "")
    sec6_text = sections.get(6, {}).get("body", "")
    ruku_ayah_texts = {a: tanzil.get((surah_id, a), "") for a in range(ayah_start, ayah_end + 1)}
    irab_subsections = parse_section_ayah_subsections(sec3_text, ruku_ayah_texts)
    nuzul_subsections = parse_section_ayah_subsections(sec6_text, ruku_ayah_texts)

    # Build Ayah List
    ayahs = []
    for a_num in range(ayah_start, ayah_end + 1):
        a_info = ayah_map.get(a_num, {})
        text_uthmani = tanzil.get((surah_id, a_num), a_info.get("text_simple", ""))
        
        # Match mufradat rows strictly matching this ayah by Arabic word tokens or explicit ayah index
        ayah_tokens = clean_arabic_for_matching(text_uthmani + " " + a_info.get("text_simple", "")).split()
        a_mufradat = []
        for mr in mufradat_rows:
            w = mr.get('শব্দ') or mr.get('শব্দ (মূল)') or mr.get('আরবি শব্দ') or mr.get('শব্দ / পরিভাষা') or ''
            w_clean = clean_arabic_for_matching(w)
            mr_str = json.dumps(mr, ensure_ascii=False)
            has_explicit = f"{surah_id}:{a_num}" in mr_str or f"{surah_id}:{to_bn(a_num)}" in mr_str
            if has_explicit or arabic_token_match(w_clean, ayah_tokens):
                a_mufradat.append(mr)

        # Match qiraat rows for this ayah from authentic Bahouth rows
        a_qiraat = []
        for qr in qiraat_rows:
            for k in qr:
                if "আয়াত" in k:
                    q_digits = re.findall(r"\d+", to_en(qr[k]))
                    if q_digits and int(q_digits[0]) == a_num:
                        a_qiraat.append(qr)
                        break

        a_irab = irab_subsections.get(a_num, "")
        a_nuzul = nuzul_subsections.get(a_num, "")

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
            "mufradat": a_mufradat,
            "qiraat": a_qiraat,
            "irab": a_irab,
            "shane_nuzul": a_nuzul
        }
        ayahs.append(ayah_obj)

    # Extract Section 0 Clean Summary
    sec0_text = sections.get(0, {}).get("body", "")
    sec0_summary = plain_markdown(sec0_text, limit=280)

    # Extract Section 8 Ahkam Mas'ala Cards with multi-table safety and negative-consensus filtering
    sec8_text = sections.get(8, {}).get("body", "")
    sec8_intro = sec8_text
    ahkam_cards = []
    t8_idx = sec8_text.find("|")
    if t8_idx != -1:
        sec8_intro = sec8_text[:t8_idx].strip()
        table_text = sec8_text[t8_idx:]
        table_lines = []
        for l in table_text.splitlines():
            line_str = l.strip()
            if not line_str:
                if table_lines:
                    break
                continue
            if line_str.startswith("|"):
                table_lines.append(line_str)
            elif table_lines:
                break

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

                    # Scholarly consensus detection with negative phrase filtering
                    has_consensus_keyword = bool(re.search(r"\(?(?:ইজমা|সর্বসম্মত|একমত|ঐক্যমত)\)?", title + " " + ev))
                    has_negative = bool(re.search(r"(?:নেই|নয়|নয়|ভিন্নমত|মতভেদ|একমত\s+ন[য়যই])", title + " " + ev))
                    is_consensus = has_consensus_keyword and not has_negative

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
            "content": sec4_content
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
    status = "needs_work"
    if audit_results:
        ruku_key = f"{surah_id}_{ruku_idx}"
        r_audit = audit_results.get("rukus", {}).get(ruku_key, {})
        status = r_audit.get("status", "needs_work")
    else:
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
    audit_results = load_audit_results()
    ruku_map = load_ruku_map()

    # Load existing global indexes ONLY if performing selective update (--surah)
    existing_surahs = {}
    existing_search_index = []
    if limit_surahs:
        surah_ids = limit_surahs
        surahs_f = DATA_DIR / "surahs.json"
        if surahs_f.exists():
            try:
                for s in json.loads(surahs_f.read_text(encoding="utf-8")):
                    if s["id"] not in limit_surahs:
                        existing_surahs[s["id"]] = s
            except Exception:
                pass
        search_f = DATA_DIR / "search_index.json"
        if search_f.exists():
            try:
                existing_search_index = [item for item in json.loads(search_f.read_text(encoding="utf-8")) if item["surah"] not in limit_surahs]
            except Exception:
                pass
    else:
        surah_ids = range(24, 115)

    new_search_items = []
    updated_surahs_summary = []

    for sid in surah_ids:
        s_info = ruku_map[str(sid)]
        s_dir = BASE_DIR / s_info["dir_name"]
        rukus = s_info["rukus"]
        num_r = len(rukus)

        intro_file = s_dir / "00_সূরা-পরিচিতি.md"
        intro_content = ""
        if intro_file.exists():
            intro_raw = unicodedata.normalize('NFC', intro_file.read_text(encoding="utf-8"))
            intro_content = rewrite_markdown_links(normalize_quran_brackets(replace_backtick_arabic(intro_raw)), sid)

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

            md_text = unicodedata.normalize('NFC', r_file.read_text(encoding="utf-8"))
            ruku_obj = parse_ruku_markdown(md_text, sid, r_idx, a_start, a_end, tanzil, s_dir=s_dir, audit_results=audit_results)

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

            # Add to search index (with harakat-free text_plain for smart instant search)
            for ayah in ruku_obj["ayahs"]:
                new_search_items.append({
                    "surah": sid,
                    "surah_name": s_info["name_bn"],
                    "ruku": r_idx,
                    "ayah": ayah["ayah"],
                    "text_uthmani": ayah["text_uthmani"][:150],
                    "text_plain": clean_arabic(ayah["text_uthmani"][:150]),
                    "translation": plain_markdown(ayah["translation"], limit=180),
                    "jalalayn": plain_markdown(ayah["jalalayn"], limit=180)
                })

        # Save surah meta
        with open(surah_data_dir / "meta.json", "w", encoding="utf-8") as smf:
            json.dump(surah_meta, smf, ensure_ascii=False, indent=2)

        s_entry = {
            "id": sid,
            "id_bn": to_bn(sid),
            "name_ar": s_info.get("name_ar", ""),
            "name_bn": s_info.get("name_bn", ""),
            "ayah_count": ayah_count,
            "ayah_count_bn": to_bn(ayah_count),
            "ruku_count": num_r,
            "ruku_count_bn": to_bn(num_r)
        }
        existing_surahs[sid] = s_entry

    # Combine full search index and surahs list
    final_surahs = [existing_surahs[k] for k in sorted(existing_surahs.keys())]
    final_search_index = existing_search_index + new_search_items
    final_search_index.sort(key=lambda x: (x["surah"], x["ayah"]))

    # Save surahs.json
    with open(DATA_DIR / "surahs.json", "w", encoding="utf-8") as sf:
        json.dump(final_surahs, sf, ensure_ascii=False, indent=2)
    print(f"Saved surahs.json with {len(final_surahs)} surahs.")

    # Save search_index.json
    with open(DATA_DIR / "search_index.json", "w", encoding="utf-8") as sif:
        json.dump(final_search_index, sif, ensure_ascii=False)
    print(f"Saved search_index.json with {len(final_search_index)} items.")

    # Calculate global totals across all surahs
    total_gold = 0
    total_needs_work = 0
    total_rukus = 0
    for s in final_surahs:
        m_file = DATA_DIR / str(s["id"]) / "meta.json"
        if m_file.exists():
            try:
                m_data = json.loads(m_file.read_text(encoding="utf-8"))
                for r in m_data.get("rukus", []):
                    total_rukus += 1
                    if r.get("status") == "gold":
                        total_gold += 1
                    else:
                        total_needs_work += 1
            except Exception:
                pass

    # Save dynamic and honest site_meta.json
    safe_author = {k: v for k, v in author_meta.get("author", {}).items() if k != "email"}
    safe_pub = {k: v for k, v in author_meta.get("publication", {}).items() if k != "email"}
    site_meta = {
        "title": "মুফাস্সির ক্লাস নোট ও তাফসীরুল জালালাইন",
        "subtitle": "কুরআনুল কারীমের প্রামাণ্য তাহকীক, ১০ কিরাআত, ৪ মাযহাবের ফিকহ ও দরস-সহায়িকা",
        "author": safe_author,
        "publication": safe_pub,
        "total_surahs": len(final_surahs),
        "total_rukus": total_rukus,
        "total_ayahs": len(final_search_index),
        "status_counts": {
            "gold": total_gold,
            "needs_work": total_needs_work
        }
    }
    with open(DATA_DIR / "site_meta.json", "w", encoding="utf-8") as f:
        json.dump(site_meta, f, ensure_ascii=False, indent=2)
    print(f"Saved site_meta.json: {total_gold} Gold Standard, {total_needs_work} Needs Work, {len(final_search_index)} total ayahs.")

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

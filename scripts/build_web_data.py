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

def clean_pipeline_artifacts(text):
    """
    Strips internal pipeline tags (e.g. [src:t7798-p16671]) and standardizes brackets.
    """
    if not text:
        return ""
    # Strip internal pipeline tags
    text = re.sub(r'\[src:[^\]]+\]', '', text)
    # Normalize broken brackets
    text = normalize_quran_brackets(text)
    return text.strip()

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


def parse_surah_intro_metadata(intro_raw, first_ruku_md=""):
    """
    Extracts revelation_type, subtitle, and ruku_map_table (ruku_id -> topic summary)
    from 00_সূরা-পরিচিতি.md (and fallback from ruku-1 header if missing).
    """
    revelation_type = ""
    subtitle = ""
    ruku_topics_map = {}

    combined_header = (intro_raw[:1500] if intro_raw else "") + "\n" + (first_ruku_md[:1000] if first_ruku_md else "")
    m_rev = re.search(r'\*\*(?:অবতীর্ণের স্থান|ধরন|সূরার ধরন|নুযূল)\s*:\*\*\s*([^|\n]+)', combined_header)
    if m_rev:
        revelation_type = clean_str(re.sub(r'[*`]', '', m_rev.group(1)))
    else:
        m_rev2 = re.search(r'(?m)(?:মাক্কী\s*/\s*মাদানী(?:\s*\([^)]+\))?|মাক্কী(?:\s*সূরা)?|মাদানী(?:\s*সূরা)?)', combined_header)
        if m_rev2:
            revelation_type = clean_str(m_rev2.group(0))

    if intro_raw:
        # Extract Section 6 (মাকাসিদুস সূরা) first concise sentence for subtitle
        m_sec6 = re.search(r'(?m)^##\s*[৬6]\.\s*[^\n]+\n+([\s\S]*?)(?=^##\s*[৭7]\.|\Z)', intro_raw)
        if m_sec6:
            sec6_clean = plain_markdown(m_sec6.group(1), limit=180)
            first_sent = re.split(r'[।\.!?]\s*', sec6_clean)[0].strip()
            if len(first_sent) >= 20:
                subtitle = first_sent[:160] + ("…" if len(first_sent) > 160 else "")

        # Extract Section 7 table (রুকুভিত্তিক বিষয়বস্তুর পূর্ণাঙ্গ মানচিত্র)
        m_sec7 = re.search(r'(?m)^##\s*[৭7]\.\s*[^\n]+\n+([\s\S]*?)(?=^##\s*[৮8]\.|\Z)', intro_raw)
        if m_sec7:
            t_start = m_sec7.group(1).find("|")
            if t_start != -1:
                rows = parse_markdown_table(m_sec7.group(1)[t_start:])
                for r in rows:
                    r_id = None
                    topic_txt = ""
                    for k, v in r.items():
                        if "রুকু" in k and "লিংক" not in k and "ফাইল" not in k:
                            digits = re.findall(r"\d+", to_en(v))
                            if digits:
                                r_id = int(digits[0])
                        elif "বিষয়" in k or "বিধান" in k or "আলোচ্য" in k:
                            topic_txt = clean_str(re.sub(r'[*`]', '', v))
                    if r_id is not None and topic_txt:
                        ruku_topics_map[r_id] = topic_txt

    return revelation_type, subtitle, ruku_topics_map


def extract_ruku_outline(ruku_obj, sec0_raw="", intro_ruku_desc="", ayahs_list=None):
    """
    Extracts concise title, summary, and subtopics [{text, ayahs}] for MindMap and SurahScopeView
    across ANY surah (24-114) without relying on hardcoded Surah 24 data.
    """
    ayah_range_bn = ruku_obj.get("ayah_range_bn", "")
    tt = ruku_obj.get("thematic_topics", {})
    makasid_content = sec0_raw or tt.get("makasid", {}).get("content", "")
    makasid_summary = tt.get("makasid", {}).get("summary", "")

    # 1. Summary
    summary = intro_ruku_desc if (intro_ruku_desc and len(intro_ruku_desc) >= 25) else makasid_summary
    if not summary:
        summary = plain_markdown(makasid_content, limit=220)

    # 2. Subtopics from Section 0 bullets (before সিয়াক-সিবাক / নাযম)
    subtopics = []
    sec0_pre = re.split(r'(?m)^###\s+.*(?:সিয়াক|নাযম|সংযোগ)', makasid_content)[0]
    for line in sec0_pre.splitlines():
        s_line = line.strip()
        m_item = re.match(r'^(?:[-*]|\d+\.)\s+(?:\*\*([^*]+)\*\*:?\s*(.*)|([^:]+):\s*(.*))$', s_line)
        if not m_item:
            continue
        if m_item.group(1) is not None:
            head = plain_markdown(m_item.group(1), limit=100).rstrip(':').strip()
            rest = plain_markdown(m_item.group(2), limit=120)
        else:
            head = plain_markdown(m_item.group(3), limit=100).rstrip(':').strip()
            rest = plain_markdown(m_item.group(4), limit=120)

        if not head or head.startswith(("পূর্ববর্তী", "পরবর্তী", "সূত্র", "নাযমুল")):
            continue
        if head in ("কেন্দ্রীয় বক্তব্য", "সারসংক্ষেপ"):
            continue

        am = re.search(r'\(?\s*(?:আ[য়য]়?াত|آية)\s*([০-৯0-9]+(?:\s*[–—\-ও,]\s*[০-৯0-9]+)*)\s*\)?', head + " " + rest)
        ayahs_ref = am.group(1).strip() if am else ayah_range_bn
        clean_head = re.sub(r'\s*\((?:আ[য়য]়?াত|آية)[^)]*\)', '', head).strip()
        if len(clean_head) < 10 and rest:
            clean_head = (clean_head + ": " + rest)[:75]
        subtopics.append({"text": clean_head, "ayahs": ayahs_ref})
        if len(subtopics) >= 5:
            break

    # Fallback 2a: from munasabat current_ayah_focus if available
    if not subtopics and ayahs_list:
        for a in ayahs_list:
            mun = a.get("munasabat") or {}
            focus = mun.get("current_ayah_focus", "")
            if focus:
                short_f = re.split(r'[।—\.]', focus)[0].strip()[:75]
                if short_f:
                    subtopics.append({"text": short_f, "ayahs": to_bn(a.get("ayah", ""))})
            if len(subtopics) >= 4:
                break

    # Fallback 2b: from connections table (sec12)
    if not subtopics:
        conn_content = tt.get("connections", {}).get("content", "")
        t_idx = conn_content.find("|")
        if t_idx != -1:
            for row in parse_markdown_table(conn_content[t_idx:]):
                vals = list(row.values())
                if vals and vals[0] and "প্রযোজ্য" not in vals[0]:
                    col0 = plain_markdown(vals[0], limit=80)
                    am = re.search(r'(?:আ[য়য]়?াত)\s*([০-৯0-9]+(?:\s*[–—\-]\s*[০-৯0-9]+)?)', col0)
                    a_ref = am.group(1) if am else ayah_range_bn
                    txt = re.sub(r'\s*\(?(?:আ[য়য]়?াত)\s*[০-৯0-9–—\-]+\)?', '', col0).strip()
                    if txt:
                        subtopics.append({"text": txt, "ayahs": a_ref})
                if len(subtopics) >= 4:
                    break

    # Fallback 2c: split prose summary into concise thematic clauses
    if not subtopics and summary:
        clauses = [c.strip() for c in re.split(r'[।;]', summary) if len(c.strip()) >= 12]
        for cl in clauses[:3]:
            subtopics.append({"text": cl[:85] + ("…" if len(cl) > 85 else ""), "ayahs": ayah_range_bn})

    # 3. Title: concise phrase from intro_ruku_desc or summary or first subtopic
    title_src = intro_ruku_desc or summary or (subtopics[0]["text"] if subtopics else "")
    # Strip boilerplate prefix like "সূরা আন-নাস (৬ আয়াত...)"
    title_clean = re.sub(r'^সূরা\s+\S+(?:\s+\([^)]+\))?(?:-এর|-এ|-তে|\s+হলো)?\s*', '', title_src).strip()
    if len(title_clean) < 15:
        title_clean = title_src
    # Split only on sentence/major clause boundaries (not commas inside parentheses)
    first_clause = re.split(r'[।;—:]', title_clean)[0].strip()
    if len(first_clause) > 68:
        first_clause = first_clause[:68].rsplit(" ", 1)[0].rstrip(",، ") + "…"
    if len(first_clause) < 12 and subtopics:
        first_clause = subtopics[0]["text"][:68]

    return first_clause, summary, subtopics

def parse_section_ayah_subsections(sec_text, ruku_ayah_texts, ayah_start=None, ayah_end=None, fallback_to_whole=False, return_covers=False):
    """
    Universal Ayah Subsection Mapper.
    Supports ###, ####, bullet points (- **আয়াত...**, * **আয়াত...**), numbered lists (1. **আয়াত...**, 1. আয়াত...),
    and Quranic quotes.
    If fallback_to_whole is True and no individual ayahs matched, maps whole-section content to all ayahs in ruku.
    If return_covers is True, returns (ayah_content_map, ayah_covers_map).
    """
    if not sec_text or not sec_text.strip():
        return ({}, {}) if return_covers else {}

    # Delimiter for subsections
    delim_pattern = r'(?m)^(?:#{3,4}\s+|[\s\-*]+\*\*(?:আ[য়য]়?াত|আয়াত)|\d+\.\s+(?:\*\*)?(?:আ[য়য]়?াত|আয়াত))'
    splits = list(re.finditer(delim_pattern, sec_text))
    ayah_content_map = {}
    ayah_covers_map = {}

    if splits:
        sections_found = []
        for i, sp in enumerate(splits):
            start = sp.start()
            end = splits[i+1].start() if i + 1 < len(splits) else len(sec_text)
            chunk = sec_text[start:end].strip()
            lines = chunk.splitlines()
            heading = lines[0]
            body = '\n'.join(lines[1:]).strip() if len(lines) > 1 else ''
            sections_found.append((heading, chunk, body))

        for heading, chunk, body in sections_found:
            target_ayahs = []
            # Match explicit range (e.g. আয়াত ১–৫)
            m_range = re.search(r'(?:আ[য়য]়?াত|আয়াত)\s*([০-৯0-9]+)\s*[–—\-]\s*([০-৯0-9]+)', heading)
            if m_range:
                s, e = int(to_en(m_range.group(1))), int(to_en(m_range.group(2)))
                target_ayahs = list(range(s, e + 1))
            else:
                m_single = re.search(r'(?:আ[য়য]়?াত|আয়াত)\s*([০-৯0-9\s,ও]+)', heading)
                if m_single:
                    raw = to_en(m_single.group(1))
                    digits = [int(d) for d in re.findall(r'\d+', raw)]
                    if digits:
                        target_ayahs = digits
                else:
                    m_colon = re.search(r'\d+:([০-৯0-9]+)', heading)
                    if m_colon:
                        target_ayahs = [int(to_en(m_colon.group(1)))]

            # Quranic quote in heading
            if not target_ayahs and ruku_ayah_texts:
                m_quote = re.search(r'﴿([^﴾]+)﴾', heading)
                if m_quote:
                    q_clean = clean_arabic(m_quote.group(1))
                    if len(q_clean) >= 3:
                        for a_num, a_text in ruku_ayah_texts.items():
                            a_clean = clean_arabic(a_text)
                            if q_clean in a_clean:
                                target_ayahs.append(a_num)

            if not target_ayahs:
                continue

            content_to_add = clean_pipeline_artifacts(chunk)
            covers_val = None
            if len(target_ayahs) > 1:
                s_min, s_max = min(target_ayahs), max(target_ayahs)
                covers_val = [s_min, s_max]
                range_prefix = f"*[উৎস: আয়াত {to_bn(s_min)}–{to_bn(s_max)}-এর যৌথ আলোচনা]*\n\n"
                content_to_add = range_prefix + content_to_add

            for ta in target_ayahs:
                ayah_covers_map[ta] = covers_val
                if ta in ayah_content_map:
                    ayah_content_map[ta] += '\n\n---\n\n' + content_to_add
                else:
                    ayah_content_map[ta] = content_to_add

    # Fallback to whole section if requested and no per-ayah map or partial map
    if fallback_to_whole and ayah_start is not None and ayah_end is not None:
        clean_sec = clean_pipeline_artifacts(sec_text)
        if clean_sec:
            whole_prefix = f"*[উৎস: আয়াত {to_bn(ayah_start)}–{to_bn(ayah_end)}-এর রুকুভিত্তিক সামগ্রিক আলোচনা]*\n\n"
            for a_num in range(ayah_start, ayah_end + 1):
                if a_num not in ayah_content_map or not ayah_content_map[a_num].strip():
                    ayah_content_map[a_num] = whole_prefix + clean_sec
                    ayah_covers_map[a_num] = [ayah_start, ayah_end]

    if return_covers:
        return ayah_content_map, ayah_covers_map
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

    # 5. Extract Section 5 (Jalalayn & Comparative Tafsir)
    sec5_text = sections.get(5, {}).get("body", "")
    jalalayn_map = {}
    jalalayn_covers_map = {}
    comparative_map = {}
    comparative_covers_map = {}
    ruku_ayah_texts = {a: tanzil.get((surah_id, a), "") for a in range(ayah_start, ayah_end + 1)}

    # Check if section 5 is split into Comparative and Jalalayn subsections
    # Handles both orders: Comparative -> Jalalayn AND Jalalayn -> Comparative
    h3_chunks = re.split(r"(?m)(?=^###\s+)", sec5_text)
    jalal_chunks = []
    comp_chunks = []
    has_h3 = any(c.lstrip().startswith("### ") for c in h3_chunks)
    if has_h3:
        for chunk in h3_chunks:
            if not chunk.strip():
                continue
            first_line = chunk.splitlines()[0]
            if first_line.startswith("### ") and "জালালাইন" in first_line:
                jalal_chunks.append(chunk)
            elif first_line.startswith("### "):
                comp_chunks.append(chunk)
        jalal_part = "\n\n".join(jalal_chunks) if jalal_chunks else sec5_text
        comp_part = "\n\n".join(comp_chunks) if comp_chunks else sec5_text
    else:
        comp_part = sec5_text
        jalal_part = sec5_text

    # 5a. Extract Jalalayn map from jalal_part
    j_matches = list(re.finditer(r"(?m)^[\s\-*]+\*\*আয়াত\s+([০-৯\d\s–—\-]+)[^:]*:\*\*\s*(?:[^\n]*\n+)?([\s\S]*?)(?=^[\s\-*]+\*\*আয়াত|^#{2,4}\s|^---|\Z)", jalal_part))
    for jm in j_matches:
        range_str = to_en(jm.group(1)).strip()
        content = clean_pipeline_artifacts(jm.group(2).strip())
        nums = [int(n) for n in re.findall(r"\d+", range_str)]
        if len(nums) == 1:
            jalalayn_map[nums[0]] = content
            jalalayn_covers_map[nums[0]] = None
        elif len(nums) >= 2:
            s_min, s_max = min(nums[0], nums[1]), max(nums[0], nums[1])
            for n in range(s_min, s_max + 1):
                jalalayn_map[n] = content
                jalalayn_covers_map[n] = [s_min, s_max]

    missing_jalal = [a for a in range(ayah_start, ayah_end + 1) if a not in jalalayn_map or not jalalayn_map[a].strip()]
    if missing_jalal:
        j_subs, j_covs = parse_section_ayah_subsections(jalal_part, ruku_ayah_texts, ayah_start=ayah_start, ayah_end=ayah_end, fallback_to_whole=False, return_covers=True)
        for ma in missing_jalal:
            if ma in j_subs:
                jalalayn_map[ma] = j_subs[ma]
                jalalayn_covers_map[ma] = j_covs.get(ma)

    # 5b. Extract Comparative Tafsir map from comp_part
    c_matches = list(re.finditer(r"(?m)^#{3,4}\s+আয়াত\s+([০-৯\d\s–—\-]+)[^\n]*\n+([\s\S]*?)(?=^#{3,4}\s+আয়াত|^#{2,3}\s|^---|\Z)", comp_part))
    for cm in c_matches:
        range_str = to_en(cm.group(1)).strip()
        content = clean_pipeline_artifacts(cm.group(2).strip())
        nums = [int(n) for n in re.findall(r"\d+", range_str)]
        if len(nums) == 1:
            comparative_map[nums[0]] = content
            comparative_covers_map[nums[0]] = None
        elif len(nums) >= 2:
            s_min, s_max = min(nums[0], nums[1]), max(nums[0], nums[1])
            for n in range(s_min, s_max + 1):
                comparative_map[n] = content
                comparative_covers_map[n] = [s_min, s_max]

    missing_comp = [a for a in range(ayah_start, ayah_end + 1) if a not in comparative_map or not comparative_map[a].strip()]
    if missing_comp:
        c_subs, c_covs = parse_section_ayah_subsections(comp_part, ruku_ayah_texts, ayah_start=ayah_start, ayah_end=ayah_end, fallback_to_whole=False, return_covers=True)
        for ma in missing_comp:
            if ma in c_subs:
                comparative_map[ma] = c_subs[ma]
                comparative_covers_map[ma] = c_covs.get(ma)

    # Fallbacks for missing jalalayn
    missing_ayahs = [a for a in range(ayah_start, ayah_end + 1) if a not in jalalayn_map or not jalalayn_map[a].strip()]
    if missing_ayahs and sec5_text:
        m_jalal = re.search(r"(?m)^###\s+[ক\w\.\s]*জালালাইন[^\n]*\n([\s\S]*?)(?=^###\s+|\Z)", sec5_text)
        if m_jalal:
            jalal_text = clean_pipeline_artifacts(m_jalal.group(1).strip())
            if jalal_text:
                for ma in missing_ayahs:
                    jalalayn_map[ma] = f"*[উৎস: রুকুর জালালাইন সারসংক্ষেপ]*\n\n" + jalal_text
                    jalalayn_covers_map[ma] = [ayah_start, ayah_end]
        else:
            sec5_clean = clean_pipeline_artifacts(sec5_text)
            if sec5_clean:
                for ma in missing_ayahs:
                    jalalayn_map[ma] = f"*[উৎস: রুকুর তুলনামূলক তাফসীর ও সারসংক্ষেপ]*\n\n" + sec5_clean
                    jalalayn_covers_map[ma] = [ayah_start, ayah_end]

    # 6. Extract Section 3 (Irab) & Section 6 (Shaan-e-Nuzul) via Ayah mapper
    sec3_text = sections.get(3, {}).get("body", "")
    sec6_text = sections.get(6, {}).get("body", "")
    irab_map, irab_covers_map = parse_section_ayah_subsections(sec3_text, ruku_ayah_texts, ayah_start=ayah_start, ayah_end=ayah_end, fallback_to_whole=False, return_covers=True)
    nuzul_map, nuzul_covers_map = parse_section_ayah_subsections(sec6_text, ruku_ayah_texts, ayah_start=ayah_start, ayah_end=ayah_end, fallback_to_whole=False, return_covers=True)

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

        a_irab = irab_map.get(a_num, "")
        a_nuzul = nuzul_map.get(a_num, "")

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
            "jalalayn_covers": jalalayn_covers_map.get(a_num),
            "comparative_tafsir": comparative_map.get(a_num, ""),
            "comparative_tafsir_covers": comparative_covers_map.get(a_num),
            "mufradat": a_mufradat,
            "qiraat": a_qiraat,
            "irab": a_irab,
            "irab_covers": irab_covers_map.get(a_num),
            "shane_nuzul": a_nuzul,
            "shane_nuzul_covers": nuzul_covers_map.get(a_num)
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

                    # Scholarly consensus detection with negative phrase and madhhab conflict filtering
                    has_consensus_keyword = bool(re.search(r"(?:\(\s*ইজমা\s*\)|ঐকমত্য\s*\(ইজমা\)|চার\s+মাযহাবই?\s+একমত|সর্বসম্মত\s+(?:মাসআলা|সিদ্ধান্ত|ফতোয়া|ফতোয়া))", title + " " + ev))
                    has_negative = bool(re.search(r"(?:নেই|নয়|নয়|ভিন্নমত|মতভেদ|তারজীহ|একমত\s+ন[য়যই])", title + " " + ev[:100]))
                    madhhab_blob = f"{h} || {m_op} || {s} || {han}"
                    has_madhhab_conflict = bool(re.search(r"(?:সহীহ|বৈধ)", madhhab_blob) and re.search(r"(?:বাতিল|হারাম|ফাসিদ)", madhhab_blob))
                    is_consensus = has_consensus_keyword and not has_negative and not has_madhhab_conflict

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
        status = "needs_work"

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
        intro_raw = ""
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

        # Peek first ruku markdown for header fallback if intro_raw lacks revelation_type/subtitle
        first_ruku_md = ""
        for p_pat in [f"রুকু-০১_*.md", f"রুকু-01_*.md", f"রুকু-1_*.md"]:
            m_f = list(s_dir.glob(p_pat))
            if m_f:
                first_ruku_md = unicodedata.normalize('NFC', m_f[0].read_text(encoding="utf-8"))
                break

        revelation_type, subtitle, ruku_topics_map = parse_surah_intro_metadata(intro_raw, first_ruku_md)

        surah_meta = {
            "id": sid,
            "id_bn": to_bn(sid),
            "name_ar": s_info.get("name_ar", ""),
            "name_bn": s_info.get("name_bn", ""),
            "revelation_type": revelation_type,
            "subtitle": subtitle,
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

            # Save ruku json with non-destructive preservation of enriched academic data
            # Also load durable enrichments from _sources/ruku_XX_enrichments.json if present
            enrichments_path = s_dir / "_sources" / f"ruku_{r_idx:02d}_enrichments.json"
            source_enrich_map = {}
            if enrichments_path.exists():
                try:
                    enrich_data = json.loads(enrichments_path.read_text(encoding="utf-8"))
                    for ea in enrich_data.get("ayahs", []):
                        enum = ea.get("ayah") or ea.get("number")
                        if enum is not None:
                            source_enrich_map[int(enum)] = ea
                except Exception:
                    pass

            ruku_json_path = surah_data_dir / f"ruku-{r_idx}.json"
            old_ayah_map = {}
            if ruku_json_path.exists():
                try:
                    old_data = json.loads(ruku_json_path.read_text(encoding="utf-8"))
                    old_ayah_map = {a.get("ayah") or a.get("number"): a for a in old_data.get("ayahs", [])}
                except Exception:
                    pass

            for a in ruku_obj["ayahs"]:
                num = a.get("ayah") or a.get("number")
                enrich_a = source_enrich_map.get(num, {})
                old_a = old_ayah_map.get(num, {})
                if enrich_a.get("tahqeeq") and isinstance(enrich_a["tahqeeq"], list):
                    a["tahqeeq"] = enrich_a["tahqeeq"]
                elif "tahqeeq" in old_a and old_a["tahqeeq"] and isinstance(old_a["tahqeeq"], list):
                    a["tahqeeq"] = old_a["tahqeeq"]
                if enrich_a.get("munasabat"):
                    a["munasabat"] = enrich_a["munasabat"]
                elif "munasabat" in old_a and old_a["munasabat"]:
                    a["munasabat"] = old_a["munasabat"]
                if not a.get("translation") and old_a.get("translation"):
                    a["translation"] = old_a["translation"]
                if not a.get("shane_nuzul") and old_a.get("shane_nuzul"):
                    a["shane_nuzul"] = old_a["shane_nuzul"]
                if not a.get("jalalayn") and old_a.get("jalalayn"):
                    a["jalalayn"] = old_a["jalalayn"]
                if not a.get("comparative_tafsir") and old_a.get("comparative_tafsir"):
                    a["comparative_tafsir"] = old_a["comparative_tafsir"]
                if not a.get("irab") and old_a.get("irab"):
                    a["irab"] = old_a["irab"]
                if a.get("comparative_tafsir_covers") is None and old_a.get("comparative_tafsir_covers"):
                    a["comparative_tafsir_covers"] = old_a["comparative_tafsir_covers"]
                if a.get("shane_nuzul_covers") is None and old_a.get("shane_nuzul_covers"):
                    a["shane_nuzul_covers"] = old_a["shane_nuzul_covers"]
                if a.get("jalalayn_covers") is None and old_a.get("jalalayn_covers"):
                    a["jalalayn_covers"] = old_a["jalalayn_covers"]
                if a.get("irab_covers") is None and old_a.get("irab_covers"):
                    a["irab_covers"] = old_a["irab_covers"]
            with open(ruku_json_path, "w", encoding="utf-8") as rf:
                json.dump(ruku_obj, rf, ensure_ascii=False, indent=2)

            # Extract structured title, summary & subtopics for SurahScopeView + MindMap
            m_sec0_raw = re.search(r'(?m)^##\s*[০0]\.\s*[^\n]+\n+([\s\S]*?)(?=^##\s*[১1]\.|\Z)', md_text)
            sec0_raw_text = m_sec0_raw.group(1).strip() if m_sec0_raw else ""
            r_title, r_summary, r_subtopics = extract_ruku_outline(
                ruku_obj,
                sec0_raw=sec0_raw_text,
                intro_ruku_desc=ruku_topics_map.get(r_idx, ""),
                ayahs_list=ruku_obj.get("ayahs", [])
            )

            # Fallback surah subtitle from Ruku 1 summary if Section 6 was missing
            if r_idx == 1 and not surah_meta.get("subtitle") and r_summary:
                first_s = re.split(r'[।\.!?]\s*', r_summary)[0].strip()
                if len(first_s) >= 20:
                    surah_meta["subtitle"] = first_s[:160] + ("…" if len(first_s) > 160 else "")

            # Record in surah_meta
            surah_meta["rukus"].append({
                "ruku_id": r_idx,
                "ruku_bn": to_bn(r_idx),
                "status": ruku_obj["status"],
                "ayah_start": a_start,
                "ayah_end": a_end,
                "ayah_range_bn": f"{to_bn(a_start)}–{to_bn(a_end)}",
                "ayah_count": a_end - a_start + 1,
                "title": r_title,
                "summary": r_summary,
                "subtopics": r_subtopics
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

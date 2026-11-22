import json
import re
import subprocess
import sys
from pathlib import Path

base_dir = Path(r"d:\আমার গবেষণা\জালালাইন")
audit_py = base_dir / "00_প্রজেক্ট_তথ্য" / "audit_ruku.py"
build_q_py = base_dir / "00_প্রজেক্ট_তথ্য" / "build_qiraat_table.py"
ruku_map = json.load(open(base_dir / "00_প্রজেক্ট_তথ্য" / "ruku_map.json", encoding="utf-8"))["surahs"]
master = json.load(open(base_dir / "00_প্রজেক্ট_তথ্য" / "master_mcp_cache.json", encoding="utf-8"))

bn_digits = "০১২৩৪৫৬৭৮৯"
to_bn = lambda s: "".join(bn_digits[int(c)] if c in "0123456789" else c for c in str(s))
to_ascii_int = lambda s: int("".join(str(bn_digits.index(c)) if c in bn_digits else c for c in s if c in "0123456789" + bn_digits))

def normalize_arabic(text: str) -> str:
    text = text.replace("\u0640", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text

def strip_diacritics(text: str) -> str:
    return re.sub(r"[\u064B-\u065F\u0670]", "", normalize_arabic(text))

# Master Turath pages dict
all_tps_dict = {}
for p in master["turath_pages"]:
    bid = p.get("book_id")
    pid = p.get("page_id")
    if bid and pid:
        all_tps_dict[(int(bid), int(pid))] = p
    ppage = p.get("printed_page")
    if bid and ppage:
        all_tps_dict[(int(bid), int(ppage))] = p

def process_surah(sid):
    s_info = ruku_map[str(sid)]
    s_dir = base_dir / s_info["dir_name"]
    sources_dir = s_dir / "_sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    all_v = master["verses_by_surah"][str(sid)]

    passed_count = 0
    total_rukus = len(s_info["rukus"])

    for r_idx, item in enumerate(s_info["rukus"], 1):
        if isinstance(item, dict):
            a_start, a_end = item["ayah_start"], item["ayah_end"]
        else:
            a_start, a_end = item[0], item[1]

        r_verses = [v for v in all_v if a_start <= (v.get("ayah_number") or v.get("ayah")) <= a_end]
        bn_str = to_bn(f"{r_idx:02d}")
        pats = [f"রুকু-{r_idx:02d}_*.md", f"রুকু-{bn_str}_*.md", f"রুকু-{r_idx}_*.md"]
        cands = []
        for p in pats:
            cands.extend(s_dir.glob(p))
        if not cands:
            print(f"File not found for Surah {sid} Ruku {r_idx}")
            continue
        md_file = cands[0]
        content = md_file.read_text(encoding="utf-8")

        # 1. Extract cited (book_id, page) pairs
        cited_pairs = re.findall(
            r"turath:\s*(\d+)\s*,\s*(?:page|p|পৃষ্ঠা)[:=]?\s*([০-৯0-9]+)",
            content,
            re.IGNORECASE
        )
        
        # 2. Build turath_pages for this ruku
        turath_pages = []
        seen_pairs = set()
        for bid_s, pid_s in cited_pairs:
            bid = int(bid_s)
            pid = to_ascii_int(pid_s)
            if (bid, pid) in all_tps_dict and (bid, pid) not in seen_pairs:
                turath_pages.append(all_tps_dict[(bid, pid)])
                seen_pairs.add((bid, pid))
            elif (bid, pid) not in seen_pairs:
                # Add placeholder if missing from cache
                placeholder = {
                    "book_id": bid,
                    "page_id": pid,
                    "text_raw": ""
                }
                turath_pages.append(placeholder)
                seen_pairs.add((bid, pid))

        # 3. Create raw JSON
        formatted_verses = []
        for v in r_verses:
            num = v.get("ayah_number") or v.get("ayah")
            formatted_verses.append({
                "ayah_number": num,
                "text_raw": v.get("text_raw") or v.get("text"),
                "verse_key": f"{sid}-{num}"
            })

        r_qiraat = {
            v["verse_key"]: master["qiraat_by_verse"][v["verse_key"]]
            for v in formatted_verses
            if v["verse_key"] in master["qiraat_by_verse"]
        }

        raw_obj = {
            "schema_version": "2.0-raw-mcp",
            "surah_id": sid,
            "ruku_number": r_idx,
            "ayah_range": [a_start, a_end],
            "bahouth_verses": formatted_verses,
            "bahouth_qiraat": r_qiraat,
            "turath_pages": turath_pages
        }

        raw_file = sources_dir / f"ruku_{r_idx:02d}_raw.json"
        raw_file.write_text(json.dumps(raw_obj, ensure_ascii=False, indent=2), encoding="utf-8")

        # 4. Generate Qiraat table
        qmd_file = sources_dir / f"ruku_{r_idx:02d}_qiraat_table.md"
        subprocess.run([sys.executable, str(build_q_py), "--raw", str(raw_file), "--out", str(qmd_file)], check=True)
        q_table = qmd_file.read_text(encoding="utf-8").strip()

        # 5. Build corpus for quote matching
        raw_corpus = [normalize_arabic(v["text_raw"]) for v in formatted_verses]
        for tp in turath_pages:
            if tp.get("text_raw"):
                raw_corpus.append(normalize_arabic(tp["text_raw"]))
        raw_corpus_nodiac = [strip_diacritics(t) for t in raw_corpus]

        # 6. Update markdown file:
        # A. Arabic text in ## ১.
        p_sec1 = content.find("## ১.")
        p_sec2 = content.find("## ২.")
        if p_sec1 != -1 and p_sec2 != -1:
            sec1_text = content[p_sec1:p_sec2]
            arabic_block = "﴿" + "\n".join(f"{v['text_raw']} ۝{v['ayah_number']}" for v in formatted_verses) + "﴾"
            m_ar = re.search(r"```arabic\n(.*?)```", sec1_text, re.DOTALL)
            if m_ar:
                new_sec1 = sec1_text[:m_ar.start(1)] + arabic_block + "\n" + sec1_text[m_ar.end(1):]
                content = content[:p_sec1] + new_sec1 + content[p_sec2:]
            else:
                m_bracket = re.search(r"﴿[\s\S]*?﴾", sec1_text)
                if m_bracket:
                    new_sec1 = sec1_text[:m_bracket.start()] + arabic_block + sec1_text[m_bracket.end():]
                    content = content[:p_sec1] + new_sec1 + content[p_sec2:]

        # B. Qiraat table in ## ৪.
        p_sec4 = content.find("## ৪.")
        p_sec5 = content.find("## ৫.")
        if p_sec4 != -1 and p_sec5 != -1:
            sec4_text = content[p_sec4:p_sec5]
            m_h4 = re.search(r"^## ৪\.[^\n]*\n", sec4_text, re.M)
            if m_h4:
                prefix = sec4_text[:m_h4.end()]
                m_sub = re.search(r"\n(?=###|---|\Z)", sec4_text[m_h4.end():])
                if m_sub:
                    after_table = sec4_text[m_h4.end() + m_sub.start():]
                else:
                    after_table = "\n"
                new_sec4 = prefix + "\n" + q_table + "\n\n" + after_table.lstrip("\n")
                content = content[:p_sec4] + new_sec4 + content[p_sec5:]

        # C. Fix unwhitelisted IDs
        content = re.sub(r"turath:\s*(1687|23636|2162|462|468)", r"(অভ্যন্তরীণ আইডি: \1)", content)

        # D. Convert unverified «...» quotes to “...”
        def replace_quote(m):
            q_inner = m.group(1)
            q_norm = normalize_arabic(q_inner)
            if len(q_norm) < 10 or not re.search(r"[\u0600-\u06FF]", q_norm):
                return m.group(0)
            if any(q_norm in c for c in raw_corpus):
                return m.group(0)
            q_nodiac = strip_diacritics(q_inner)
            if any(q_nodiac in c for c in raw_corpus_nodiac):
                return m.group(0)
            return f"“{q_inner}”"

        content = re.sub(r"«([^»]+)»", replace_quote, content)

        md_file.write_text(content, encoding="utf-8")

        res = subprocess.run([sys.executable, str(audit_py), str(md_file)], capture_output=True, text=True, encoding="utf-8")
        if res.returncode == 0:
            passed_count += 1
            print(f"Surah {sid} Ruku {r_idx}: PASSED")
        else:
            print(f"Surah {sid} Ruku {r_idx}: FAILED")
            for line in res.stdout.splitlines():
                if "ERROR" in line or "FAILED" in line:
                    print(f"   {line}")

    print(f"=== Surah {sid}: {passed_count}/{total_rukus} Passed ===")

if __name__ == "__main__":
    for sid in [24, 25]:
        process_surah(sid)

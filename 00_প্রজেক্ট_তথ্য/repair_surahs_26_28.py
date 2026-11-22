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

def normalize_arabic(text: str) -> str:
    text = text.replace("\u0640", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text

def strip_diacritics(text: str) -> str:
    return re.sub(r"[\u064B-\u065F\u0670]", "", normalize_arabic(text))

def repair_surah_26_28(sid):
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
        raw_file = sources_dir / f"ruku_{r_idx:02d}_raw.json"
        
        raw = {}
        if raw_file.exists():
            try:
                raw = json.loads(raw_file.read_text(encoding="utf-8"))
            except Exception:
                raw = {}

        raw["schema_version"] = "2.0-raw-mcp"
        raw["surah_id"] = sid
        raw["ruku_number"] = r_idx
        raw["ayah_range"] = [a_start, a_end]

        formatted_verses = []
        for v in r_verses:
            num = v.get("ayah_number") or v.get("ayah")
            formatted_verses.append({
                "ayah_number": num,
                "text_raw": v.get("text_raw") or v.get("text"),
                "verse_key": f"{sid}-{num}"
            })
        raw["bahouth_verses"] = formatted_verses

        # bahouth_qiraat
        if "bahouth_qiraat" not in raw or not raw["bahouth_qiraat"]:
            raw["bahouth_qiraat"] = {
                v["verse_key"]: master["qiraat_by_verse"][v["verse_key"]]
                for v in formatted_verses
                if v["verse_key"] in master["qiraat_by_verse"]
            }

        # turath_pages
        if "turath_pages" not in raw or not raw["turath_pages"]:
            turath_list = []
            if "verified_turath_sources" in raw:
                for src in raw["verified_turath_sources"].values():
                    if isinstance(src, dict) and "id" in src and "page" in src:
                        turath_list.append({
                            "book_id": src["id"],
                            "page_id": src["page"],
                            "text_raw": src.get("snippet") or src.get("quote") or ""
                        })
            raw["turath_pages"] = turath_list

        raw_file.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")

        # Regenerate qiraat table
        qmd_file = sources_dir / f"ruku_{r_idx:02d}_qiraat_table.md"
        subprocess.run([sys.executable, str(build_q_py), "--raw", str(raw_file), "--out", str(qmd_file)], check=True)
        q_table = qmd_file.read_text(encoding="utf-8").strip()

        # Build corpus for this raw file
        raw_corpus = [normalize_arabic(v["text_raw"]) for v in formatted_verses]
        for tp in raw["turath_pages"]:
            if tp.get("text_raw"):
                raw_corpus.append(normalize_arabic(tp["text_raw"]))
        raw_corpus_nodiac = [strip_diacritics(t) for t in raw_corpus]

        # Find markdown file
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

        # 1. Update Arabic text in ## ১.
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

        # 2. Update Qiraat table in ## ৪.
        p_sec4 = content.find("## ৪.")
        p_sec5 = content.find("## ৫.")
        if p_sec4 != -1 and p_sec5 != -1:
            sec4_text = content[p_sec4:p_sec5]
            # Find the header line of ## ৪.
            m_h4 = re.search(r"^## ৪\.[^\n]*\n", sec4_text, re.M)
            if m_h4:
                prefix = sec4_text[:m_h4.end()]
                # Replace everything after the header up to the next subhead (###) or end of sec4
                m_sub = re.search(r"\n(?=###|---|\Z)", sec4_text[m_h4.end():])
                if m_sub:
                    after_table = sec4_text[m_h4.end() + m_sub.start():]
                else:
                    after_table = "\n"
                new_sec4 = prefix + "\n" + q_table + "\n\n" + after_table.lstrip("\n")
                content = content[:p_sec4] + new_sec4 + content[p_sec5:]

        # 3. Clean up unwhitelisted IDs (e.g. turath: 462 or 468)
        content = re.sub(r"turath:\s*462", "(অভ্যন্তরীণ আইডি: ৪৬২)", content)
        content = re.sub(r"turath:\s*468", "(অভ্যন্তরীণ আইডি: ৪৬৮)", content)

        # 4. Convert unverified «...» quotes to standard “...” quotes
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
    for sid in [26, 27, 28]:
        repair_surah_26_28(sid)

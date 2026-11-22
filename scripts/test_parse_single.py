import json
import re
from pathlib import Path

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

def load_tanzil():
    tanzil_file = BASE_DIR / "00_প্রজেক্ট_তথ্য" / "quran-uthmani.txt"
    tanzil = {}
    if not tanzil_file.exists():
        print("Warning: Tanzil file not found at", tanzil_file)
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

def clean_md(text):
    if not text:
        return ""
    return text.strip()

def parse_markdown_table(table_text):
    lines = [l.strip() for l in table_text.strip().splitlines() if l.strip()]
    if len(lines) < 2:
        return []
    headers = [h.strip() for h in lines[0].strip("|").split("|")]
    # skip separator line
    start_idx = 1
    if len(lines) > 1 and re.match(r"^\|?[\s\-:|]+\|?$", lines[1]):
        start_idx = 2
    rows = []
    for line in lines[start_idx:]:
        if not line.startswith("|") and not "|" in line:
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        # Pad columns if needed
        while len(cols) < len(headers):
            cols.append("")
        row_dict = {headers[i]: cols[i] for i in range(len(headers))}
        rows.append(row_dict)
    return rows

def test_parse_surah_24_ruku_1():
    tanzil = load_tanzil()
    ruku_file = BASE_DIR / "২৪_সূরা_আন-নূর" / "রুকু-০১_আয়াত_১-১০.md"
    text = ruku_file.read_text(encoding="utf-8")
    
    # Check section 1 table
    sec1_match = re.search(r"### \(১\) ২[^\n]*\n+([\s\S]*?)(?=## ২\.|$)", text)
    if sec1_match:
        table_raw = sec1_match.group(1)
        # Find table start
        t_start = table_raw.find("|")
        if t_start != -1:
            table_str = table_raw[t_start:]
            rows = parse_markdown_table(table_str)
            print(f"Parsed {len(rows)} translation rows.")
            for r in rows[:2]:
                print("Row sample:", r)
    
    # Check section 2 table (Mufradat)
    sec2_match = re.search(r"## ২\. লুগাভী ও সরফী[^\n]*\n+([\s\S]*?)(?=## ৩\.|$)", text)
    if sec2_match:
        table_raw = sec2_match.group(1)
        t_start = table_raw.find("|")
        if t_start != -1:
            rows = parse_markdown_table(table_raw[t_start:])
            print(f"Parsed {len(rows)} mufradat rows.")
            if rows:
                print("Mufradat sample:", rows[0])
                
    # Check section 5 (Jalalayn)
    sec5_match = re.search(r"### ক\. তাফসীর আল-জালালাইন[^\n]*\n+([\s\S]*?)(?=### খ\.|$)", text)
    if sec5_match:
        j_text = sec5_match.group(1)
        items = re.findall(r"-\s+\*\*আয়াত\s+([০-৯\d]+)\s*:\*\*\s*\n+([\s\S]*?)(?=-\s+\*\*আয়াত|\Z)", j_text)
        print(f"Parsed {len(items)} Jalalayn items.")
        for a_num, content in items[:2]:
            print(f"Ayah {to_en(a_num)} Jalalayn length: {len(content)}")

if __name__ == "__main__":
    test_parse_surah_24_ruku_1()

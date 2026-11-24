# -*- coding: utf-8 -*-
"""
Converts all Western/English numerals (0-9) and English transliterations
in Qiraat tables across all ruku JSON files to classical Eastern Arabic numerals (٠-٩).
"""

import glob
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "web" / "public" / "data"

AR_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")

def convert_qiraat_text(val: str) -> str:
    if not isinstance(val, str):
        return val
    # Remove Latin transliteration relics like '- Dammah', '- Kasrah'
    cleaned = re.sub(r'\s*-\s*(?:Dammah|Kasrah)\b', '', val)
    # Translate digits to Arabic
    return cleaned.translate(AR_DIGITS)

def process_file(file_path: Path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    if not isinstance(data, dict):
        return False

    modified = False

    # 1. thematic_topics -> qiraat_full -> table
    thematic = data.get("thematic_topics", {})
    if isinstance(thematic, dict):
        qf = thematic.get("qiraat_full", {})
        if isinstance(qf, dict) and "table" in qf and isinstance(qf["table"], list):
            for row in qf["table"]:
                if isinstance(row, dict):
                    for k in list(row.keys()):
                        old_v = row[k]
                        if isinstance(old_v, str):
                            new_v = convert_qiraat_text(old_v)
                            if new_v != old_v:
                                row[k] = new_v
                                modified = True

    # 2. ayahs -> qiraat
    ayahs = data.get("ayahs", [])
    if isinstance(ayahs, list):
        for ayah in ayahs:
            if isinstance(ayah, dict) and "qiraat" in ayah and isinstance(ayah["qiraat"], list):
                for row in ayah["qiraat"]:
                    if isinstance(row, dict):
                        for k in list(row.keys()):
                            old_v = row[k]
                            if isinstance(old_v, str):
                                new_v = convert_qiraat_text(old_v)
                                if new_v != old_v:
                                    row[k] = new_v
                                    modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        return True
    return False

def main():
    json_files = list(DATA_DIR.glob("**/*.json"))
    print(f"Scanning {len(json_files)} JSON files in {DATA_DIR}...")
    updated_count = 0
    for p in json_files:
        if process_file(p):
            updated_count += 1
            print(f"  ✓ Updated {p.relative_to(BASE_DIR)}")

    print(f"\nDone! Updated {updated_count} files with Arabic numerals in Qiraat tables.")

if __name__ == "__main__":
    main()

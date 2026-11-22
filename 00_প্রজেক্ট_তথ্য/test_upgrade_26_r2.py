import json
import subprocess
import sys
from pathlib import Path

raw_file = Path(r"২৬_সূরা_আশ-শুআরা\_sources\ruku_02_raw.json")
raw = json.loads(raw_file.read_text(encoding="utf-8"))
raw["schema_version"] = "2.0-raw-mcp"

if "bahouth_verses" not in raw and "verses" in raw:
    raw["bahouth_verses"] = []
    for v in raw["verses"]:
        num = v.get("ayah") or v.get("ayah_number")
        txt = v.get("text") or v.get("text_raw")
        raw["bahouth_verses"].append({
            "ayah_number": num,
            "text_raw": txt,
            "verse_key": f"{raw['surah_id']}-{num}"
        })

if "turath_pages" not in raw and "verified_turath_sources" in raw:
    raw["turath_pages"] = []
    for src in raw["verified_turath_sources"].values():
        if isinstance(src, dict) and "id" in src and "page" in src:
            raw["turath_pages"].append({
                "book_id": src["id"],
                "page_id": src["page"],
                "text_raw": src.get("snippet") or src.get("quote") or ""
            })

raw_file.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")

md_file = Path(r"২৬_সূরা_আশ-শুআরা\রুকু-০২_আয়াত_১০-২০.md")
res = subprocess.run([sys.executable, "00_প্রজেক্ট_তথ্য/audit_ruku.py", str(md_file)], capture_output=True, text=True, encoding="utf-8")
print(res.stdout)

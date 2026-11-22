import json
import re
import subprocess
import sys
from pathlib import Path

base_dir = Path(r"d:\আমার গবেষণা\জালালাইন")
audit_py = base_dir / "00_প্রজেক্ট_তথ্য" / "audit_ruku.py"
build_q_py = base_dir / "00_প্রজেক্ট_তথ্য" / "build_qiraat_table.py"

bn_digits = "০১২৩৪৫৬৭৮৯"
to_bn = lambda n: "".join(bn_digits[int(c)] for c in str(n))

raw_file = Path(r"২৬_সূরা_আশ-শুআরা\_sources\ruku_02_raw.json")
raw = json.loads(raw_file.read_text(encoding="utf-8"))
raw["schema_version"] = "2.0-raw-mcp"

# Ensure bahouth_verses
if "verses" in raw and ("bahouth_verses" not in raw or not raw["bahouth_verses"]):
    raw["bahouth_verses"] = []
    for v in raw["verses"]:
        num = v.get("ayah") or v.get("ayah_number")
        txt = v.get("text") or v.get("text_raw")
        raw["bahouth_verses"].append({
            "ayah_number": num,
            "text_raw": txt,
            "verse_key": f"26-{num}"
        })

# Ensure turath_pages
if "verified_turath_sources" in raw and ("turath_pages" not in raw or not raw["turath_pages"]):
    raw["turath_pages"] = []
    for src in raw["verified_turath_sources"].values():
        if isinstance(src, dict) and "id" in src and "page" in src:
            raw["turath_pages"].append({
                "book_id": src["id"],
                "page_id": src["page"],
                "text_raw": src.get("snippet") or src.get("quote") or ""
            })

raw_file.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")

# Regenerate qiraat table
qmd_file = Path(r"২৬_সূরা_আশ-শুআরা\_sources\ruku_02_qiraat_table.md")
subprocess.run([sys.executable, str(build_q_py), "--raw", str(raw_file), "--out", str(qmd_file)], check=True)
q_table = qmd_file.read_text(encoding="utf-8").strip()

# Now update the markdown file
md_file = Path(r"২৬_সূরা_আশ-শুআরা\রুকু-০২_আয়াত_১০-২০.md")
content = md_file.read_text(encoding="utf-8")

# 1. Update Arabic block in ## ১.
verses = raw["bahouth_verses"]
arabic_block = "\n".join(f"{v['text_raw']} ﴿{to_bn(v['ayah_number'])}﴾" for v in verses)

# Find ```arabic block in ## ১.
p_sec1 = content.find("## ১.")
p_sec2 = content.find("## ২.")
sec1_text = content[p_sec1:p_sec2]

# Replace arabic block in sec1
m_ar = re.search(r"```arabic\n(.*?)```", sec1_text, re.DOTALL)
if m_ar:
    new_sec1 = sec1_text[:m_ar.start(1)] + arabic_block + "\n" + sec1_text[m_ar.end(1):]
    content = content[:p_sec1] + new_sec1 + content[p_sec2:]
else:
    # Look for ﴿...﴾ block in sec1
    m_bracket = re.search(r"﴿[\s\S]*?﴾", sec1_text)
    if m_bracket:
        new_sec1 = sec1_text[:m_bracket.start()] + "﴿" + "\n".join(f"{v['text_raw']} ۝{v['ayah_number']}" for v in verses) + "﴾" + sec1_text[m_bracket.end():]
        content = content[:p_sec1] + new_sec1 + content[p_sec2:]

# 2. Update Qiraat table in ## ৪.
p_sec4 = content.find("## ৪.")
p_sec5 = content.find("## ৫.")
sec4_text = content[p_sec4:p_sec5]

# Find table in sec4
m_tbl = re.search(r"(\|.*?\n)\n*(?=###|---|\Z)", sec4_text, re.DOTALL)
if m_tbl:
    new_sec4 = sec4_text[:m_tbl.start()] + q_table + "\n\n" + sec4_text[m_tbl.end():]
    content = content[:p_sec4] + new_sec4 + content[p_sec5:]

md_file.write_text(content, encoding="utf-8")

res = subprocess.run([sys.executable, str(audit_py), str(md_file)], capture_output=True, text=True, encoding="utf-8")
print(res.stdout)

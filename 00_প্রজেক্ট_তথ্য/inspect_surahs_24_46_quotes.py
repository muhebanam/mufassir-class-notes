import json
import re
from pathlib import Path

base_dir = Path(".")
ruku_map = json.load(open("00_প্রজেক্ট_তথ্য/ruku_map.json", encoding="utf-8"))["surahs"]
master = json.load(open("00_প্রজেক্ট_তথ্য/master_mcp_cache.json", encoding="utf-8"))

def normalize_arabic(text: str) -> str:
    text = text.replace("\u0640", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text

def strip_diacritics(text: str) -> str:
    return re.sub(r"[\u064B-\u065F\u0670]", "", normalize_arabic(text))

# Build full corpus of text_raw
corpus_norm = []
corpus_nodiac = []

for s_verses in master["verses_by_surah"].values():
    for v in s_verses:
        raw = v.get("text_raw", "")
        if raw:
            norm = normalize_arabic(raw)
            corpus_norm.append(norm)
            corpus_nodiac.append(strip_diacritics(raw))

for p in master["turath_pages"]:
    raw = p.get("text_raw", "")
    if raw:
        norm = normalize_arabic(raw)
        corpus_norm.append(norm)
        corpus_nodiac.append(strip_diacritics(raw))

print(f"Total corpus chunks: {len(corpus_norm)}")

failing_quotes = []

for sid in range(24, 47):
    sinfo = ruku_map[str(sid)]
    sdir = base_dir / sinfo["dir_name"]
    for md_file in sdir.glob("*.md"):
        if md_file.name.startswith("00_") or "Audit" in md_file.name:
            continue
        content = md_file.read_text(encoding="utf-8")
        quotes = re.findall(r"«([^»]+)»", content)
        for q in quotes:
            q_norm = normalize_arabic(q)
            if len(q_norm) < 10 or not re.search(r"[\u0600-\u06FF]", q_norm):
                continue
            # Check match
            match = any(q_norm in c for c in corpus_norm)
            if not match:
                q_nodiac = strip_diacritics(q)
                match = any(q_nodiac in c for c in corpus_nodiac)
            if not match:
                failing_quotes.append((sid, md_file.name, q_norm[:60]))

print(f"Total failing quotes in Surahs 24-46: {len(failing_quotes)}")
for x in failing_quotes[:15]:
    print(" ", x)

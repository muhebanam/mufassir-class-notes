import json
import subprocess
import sys
from pathlib import Path

base_dir = Path(r"d:\আমার গবেষণা\জালালাইন")
conv_dir = Path(r"C:\Users\USER\.gemini\antigravity\brain\7caaeec8-bdfa-40da-93eb-62b94af954b1\.system_generated")
steps_dir = conv_dir / "steps"
transcript_path = conv_dir / "logs" / "transcript_full.jsonl"

# 1. Parse bahouth outputs from transcript_full.jsonl
surah_verses = {}
verse_qiraat = {}

for line in transcript_path.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    for key in ["\"surah_id\": 105", "\"surah_id\": 106", "\"surah_id\": 107", "\"surah_id\": 108", "\"surah_id\": 109",
                "\"surah_id\": 110", "\"surah_id\": 111", "\"surah_id\": 112", "\"surah_id\": 113", "\"surah_id\": 114"]:
        pass
    try:
        obj = json.loads(line)
    except Exception:
        continue
    # Walk JSON recursively to find tool responses with verse_count/verses or annotations
    def walk(node):
        if isinstance(node, dict):
            if "surah_id" in node and "verses" in node and isinstance(node["verses"], list):
                sid = node["surah_id"]
                if 105 <= sid <= 114:
                    surah_verses[sid] = node["verses"]
            if "verse_key" in node and "annotations" in node and isinstance(node["annotations"], list):
                vk = node["verse_key"]
                s_part = int(vk.split("-")[0])
                if 105 <= s_part <= 114:
                    verse_qiraat[vk] = node
            for v in node.values():
                if isinstance(v, str) and "{" in v:
                    try:
                        walk(json.loads(v[v.find("{"):]))
                    except Exception:
                        pass
                else:
                    walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)
    walk(obj)

print(f"Extracted bahouth surahs: {sorted(surah_verses.keys())} | qiraat verses: {len(verse_qiraat)}")

# 2. Parse Turath step files into individual pages
step_ids = ["5024", "5025", "5026", "5029", "5030", "5031", "5036", "5039", "5040", "5041", "5068"]
all_pages = []  # list of {book_id, book_name, page_id, printed_page, text_raw}

for sid in step_ids:
    txt = (steps_dir / sid / "output.txt").read_text(encoding="utf-8")
    d = json.loads(txt[txt.find("{"):])
    bid = int(d["book"]["id"])
    bname = d["book"]["title"]
    full_text = d["text"]
    for seg in d.get("segments", []):
        loc = seg["location"]
        seg_text = full_text[seg["start"]:seg["end"]]
        all_pages.append({
            "book_id": bid,
            "book_name": bname,
            "page_id": int(loc["internalPage"]),
            "printed_page": int(loc.get("printedPage", 0)),
            "text_raw": seg_text,
        })

# Deduplicate by (book_id, page_id)
seen_bp = set()
unique_pages = []
for p in all_pages:
    k = (p["book_id"], p["page_id"])
    if k not in seen_bp:
        seen_bp.add(k)
        unique_pages.append(p)

print(f"Extracted unique Turath pages: {len(unique_pages)}")

# Surah keywords to match pages to Surahs 105..114
surah_markers = {
    105: ["الفيل", "أصحاب الفيل", "أبابيل", "سجيل"],
    106: ["قريش", "لإيلاف", "الشتاء والصيف"],
    107: ["الماعون", "أرأيت الذي يكذب", "يدع اليتيم"],
    108: ["الكوثر", "إنا أعطيناك", "شانئك"],
    109: ["الكافرون", "يا أيها الكافرون", "لكم دينكم"],
    110: ["النصر", "جاء نصر الله", "أفواجا"],
    111: ["المسد", "تبت يدا", "أبي لهب", "حمالة الحطب"],
    112: ["الإخلاص", "قل هو الله أحد", "الصمد"],
    113: ["الفلق", "برب الفلق", "النفاثات"],
    114: ["الناس", "برب الناس", "الوسواس الخناس"],
}

surah_dirs = {
    105: "105_সূরা_আল-ফীল",
    106: "106_সূরা_কুরাইশ",
    107: "107_সূরা_আল-মা‘ঊন",
    108: "108_সূরা_আল-কাউসার",
    109: "109_সূরা_আল-কাফিরূন",
    110: "110_সূরা_আন-নাসর",
    111: "111_সূরা_আল-লাহাব",
    112: "112_সূরা_আল-ইখলাস",
    113: "113_সূরা_আল-ফালাক্ব",
    114: "114_সূরা_আন-নাস",
}

rmap = json.loads((base_dir / "00_প্রজেক্ট_তথ্য" / "ruku_map.json").read_text(encoding="utf-8"))
build_q = base_dir / "00_প্রজেক্ট_তথ্য" / "build_qiraat_table.py"

digest_lines = []

for s_num in range(105, 115):
    s_dir = base_dir / surah_dirs[s_num]
    src_dir = s_dir / "_sources"
    src_dir.mkdir(parents=True, exist_ok=True)

    verses = surah_verses.get(s_num, [])
    q_map = {v["verse_key"]: verse_qiraat[v["verse_key"]] for v in verses if v["verse_key"] in verse_qiraat}

    markers = surah_markers[s_num]
    matched_pages = [p for p in unique_pages if any(m in p["text_raw"] for m in markers)]

    raw_obj = {
        "schema_version": "2.0-raw-mcp",
        "surah_id": s_num,
        "surah_name_bn": rmap["surahs"][str(s_num)]["name_bn"],
        "ruku_number": 1,
        "ayah_range": [1, len(verses)],
        "bahouth_verses": verses,
        "bahouth_qiraat": q_map,
        "turath_pages": matched_pages,
    }

    raw_path = src_dir / "ruku_01_raw.json"
    raw_path.write_text(json.dumps(raw_obj, ensure_ascii=False, indent=2), encoding="utf-8")

    q_out = src_dir / "ruku_01_qiraat_table.md"
    subprocess.run([sys.executable, str(build_q), "--raw", str(raw_path), "--out", str(q_out)], check=True)

    jal_pages = [p for p in matched_pages if p["book_id"] == 12876]
    digest_lines.append(f"=== SURAH {s_num} ({surah_dirs[s_num]}) | verses={len(verses)} | turath_pages={len(matched_pages)} ===")
    for jp in jal_pages:
        digest_lines.append(f"[Jalalayn p.{jp['page_id']}/printed {jp['printed_page']}]: {jp['text_raw'][:300].replace(chr(10), ' ')}")

scratch_dir = Path(r"C:\Users\USER\.gemini\antigravity\brain\7caaeec8-bdfa-40da-93eb-62b94af954b1\scratch")
scratch_dir.mkdir(parents=True, exist_ok=True)
(scratch_dir / "pilot_105_114_digest.txt").write_text("\n".join(digest_lines), encoding="utf-8")
print("Pilot 105-114 raw JSON & qiraat tables ready!")

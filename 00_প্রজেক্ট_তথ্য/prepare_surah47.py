import json
import subprocess
import sys
from pathlib import Path

base_dir = Path(r"d:\আমার গবেষণা\জালালাইন")
conv_dir = Path(r"C:\Users\USER\.gemini\antigravity\brain\7caaeec8-bdfa-40da-93eb-62b94af954b1\.system_generated")
steps_dir = conv_dir / "steps"
transcript_path = conv_dir / "logs" / "transcript_full.jsonl"

s47_txt = (steps_dir / "5143" / "output.txt").read_text(encoding="utf-8")
surah_verses = json.loads(s47_txt[s47_txt.find("{"):]).get("verses", [])
verse_qiraat = {}

for line in transcript_path.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    try:
        obj = json.loads(line)
    except Exception:
        continue
    def walk(node):
        if isinstance(node, dict):
            if node.get("surah_id") == 47 and isinstance(node.get("verses"), list):
                surah_verses[:] = node["verses"]
            if isinstance(node.get("verse_key"), str) and node["verse_key"].startswith("47-") and isinstance(node.get("annotations"), list):
                verse_qiraat[node["verse_key"]] = node
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

print(f"Surah 47 verses: {len(surah_verses)} | qiraat verses: {len(verse_qiraat)}")

# Parse Turath pages from steps 5148, 5149, 5150, 5163, 5164
all_pages = []
for sid in ["5148", "5149", "5150", "5163", "5164"]:
    t = (steps_dir / sid / "output.txt").read_text(encoding="utf-8")
    d = json.loads(t[t.find("{"):])
    if "passages" in d:
        for p in d["passages"]:
            loc = p["location"]
            all_pages.append({
                "book_id": int(p["book"]["id"]),
                "book_name": p["book"]["title"],
                "page_id": int(loc["internalPage"]),
                "printed_page": int(loc.get("printedPage", 0)),
                "text_raw": p["text"]
            })
    else:
        bid = int(d["book"]["id"])
        bname = d["book"]["title"]
        ft = d["text"]
        for seg in d.get("segments", []):
            loc = seg["location"]
            all_pages.append({
                "book_id": bid,
                "book_name": bname,
                "page_id": int(loc["internalPage"]),
                "printed_page": int(loc.get("printedPage", 0)),
                "text_raw": ft[seg["start"]:seg["end"]]
            })

# Deduplicate
seen = set()
unique_pages = []
for p in all_pages:
    k = (p["book_id"], p["page_id"])
    if k not in seen:
        seen.add(k)
        unique_pages.append(p)

print(f"Surah 47 unique Turath pages: {len(unique_pages)}")

ruku_ranges = [
    (1, 1, 11),
    (2, 12, 19),
    (3, 20, 28),
    (4, 29, 38),
]

s_dir = base_dir / "47_সূরা_মুহাম্মদ"
src_dir = s_dir / "_sources"
src_dir.mkdir(parents=True, exist_ok=True)
build_q = base_dir / "00_প্রজেক্ট_তথ্য" / "build_qiraat_table.py"

digest = []
for r_num, a_start, a_end in ruku_ranges:
    r_verses = [v for v in surah_verses if a_start <= v["ayah_number"] <= a_end]
    r_qiraat = {v["verse_key"]: verse_qiraat[v["verse_key"]] for v in r_verses if v["verse_key"] in verse_qiraat}
    
    # Approximate Jalalayn slicing (5153..5191) + Ibn Kathir + Tabari + Qurtubi
    # Include all unique_pages relevant (or full Surah 47 Turath corpus per ruku so traceability is exact)
    raw_obj = {
        "schema_version": "2.0-raw-mcp",
        "surah_id": 47,
        "surah_name_bn": "মুহাম্মদ",
        "ruku_number": r_num,
        "ayah_range": [a_start, a_end],
        "bahouth_verses": r_verses,
        "bahouth_qiraat": r_qiraat,
        "turath_pages": unique_pages,
    }
    raw_path = src_dir / f"ruku_{r_num:02d}_raw.json"
    raw_path.write_text(json.dumps(raw_obj, ensure_ascii=False, indent=2), encoding="utf-8")
    q_out = src_dir / f"ruku_{r_num:02d}_qiraat_table.md"
    subprocess.run([sys.executable, str(build_q), "--raw", str(raw_path), "--out", str(q_out)], check=True)

digest.append("=== JALALAYN SURAH 47 ===")
for p in sorted([x for x in unique_pages if x["book_id"] == 12876], key=lambda x: x["page_id"]):
    digest.append(f"[12876 p.{p['page_id']}/pr.{p['printed_page']}] {p['text_raw'].replace(chr(10), ' ')}")

scratch_dir = Path(r"C:\Users\USER\.gemini\antigravity\brain\7caaeec8-bdfa-40da-93eb-62b94af954b1\scratch")
(scratch_dir / "surah47_jalalayn.txt").write_text("\n".join(digest), encoding="utf-8")
print("Surah 47 raw JSONs & qiraat tables ready!")

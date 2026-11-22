import json
import re
from pathlib import Path

base_dir = Path(r"d:\আমার গবেষণা\জালালাইন")
conv_parent = Path(r"C:\Users\USER\.gemini\antigravity\brain")

all_subagents = [
    "7caaeec8-bdfa-40da-93eb-62b94af954b1", # parent
    "dd6e59b7-3289-431a-9777-0a336e6683ff", # 48-54
    "f9f25886-4108-4358-ba36-72cc9f774b73", # 55-61
    "6ebc809e-3c03-4842-8d46-56784be0b5c2", # 62-69
    "585daf7e-71c1-4a4f-a7bf-f1dd836e49e0", # 70-79
    "b7bbca99-ad08-4ab6-8acd-a9aba0945fc7", # 80-91
    "a0fc8fb5-3d0d-4d84-87a9-8cf05e718c17", # 92-104
]

verses_by_surah = {}
qiraat_by_verse = {}
turath_pages = {} # (book_id, page_id) -> dict

def process_dict(d):
    if not isinstance(d, dict):
        return
    # check bahouth verses
    if "surah_id" in d and "verses" in d and isinstance(d["verses"], list):
        sid = int(d["surah_id"])
        verses_by_surah[sid] = d["verses"]
    # check bahouth qiraat
    if "verse_key" in d and "annotations" in d and isinstance(d["annotations"], list):
        vk = d["verse_key"]
        qiraat_by_verse[vk] = d
    # check turath get_context
    if "book" in d and "text" in d and "segments" in d and isinstance(d["segments"], list):
        try:
            bid = int(d["book"]["id"])
            bname = d["book"]["title"]
            full_text = d["text"]
            for seg in d["segments"]:
                loc = seg["location"]
                pid = int(loc["internalPage"])
                ppage = loc.get("printedPage")
                turath_pages[(bid, pid)] = {
                    "book_id": bid,
                    "book_name": bname,
                    "page_id": pid,
                    "printed_page": int(ppage) if ppage is not None else None,
                    "text_raw": full_text[seg["start"]:seg["end"]],
                }
        except Exception:
            pass
    # check turath retrieve
    if "passages" in d and isinstance(d["passages"], list):
        for p in d["passages"]:
            try:
                bid = int(p["book"]["id"])
                bname = p["book"]["title"]
                full_text = p["text"]
                for seg in p.get("segments", []):
                    loc = seg["location"]
                    pid = int(loc["internalPage"])
                    ppage = loc.get("printedPage")
                    turath_pages[(bid, pid)] = {
                        "book_id": bid,
                        "book_name": bname,
                        "page_id": pid,
                        "printed_page": int(ppage) if ppage is not None else None,
                        "text_raw": full_text[seg["start"]:seg["end"]],
                    }
            except Exception:
                pass

for cid in all_subagents:
    cdir = conv_parent / cid
    if not cdir.exists():
        continue
    # 1. check scratch files
    scratch_dir = cdir / "scratch"
    if scratch_dir.exists():
        for f in scratch_dir.glob("*.json"):
            try:
                content = json.loads(f.read_text(encoding="utf-8"))
                if "verses_by_surah" in content:
                    for s, v in content["verses_by_surah"].items():
                        verses_by_surah[int(s)] = v
                if "qiraat_by_key" in content:
                    for k, v in content["qiraat_by_key"].items():
                        qiraat_by_verse[k] = v
                if "verses" in content and isinstance(content["verses"], dict):
                    for s, v in content["verses"].items():
                        verses_by_surah[int(s)] = v
                if "qiraat" in content and isinstance(content["qiraat"], dict):
                    for k, v in content["qiraat"].items():
                        qiraat_by_verse[k] = v
                if "turath_by_book" in content:
                    for b_str, pages in content["turath_by_book"].items():
                        bid = int(b_str)
                        for p in pages:
                            turath_pages[(bid, p["page_id"])] = p
            except Exception:
                pass

    # 2. check steps output.txt
    steps_dir = cdir / ".system_generated" / "steps"
    if steps_dir.exists():
        for out_file in steps_dir.glob("*/output.txt"):
            try:
                txt = out_file.read_text(encoding="utf-8").strip()
                idx = txt.find("{")
                if idx != -1:
                    process_dict(json.loads(txt[idx:]))
            except Exception:
                pass

# Also merge existing _sources/*.json
for raw_file in base_dir.glob("*/*_sources/*raw.json"):
    try:
        raw = json.loads(raw_file.read_text(encoding="utf-8"))
        if raw.get("schema_version") == "2.0-raw-mcp":
            for v in raw.get("bahouth_verses", []):
                sid = int(v["surah_id"])
                if sid not in verses_by_surah:
                    verses_by_surah[sid] = []
                existing_vids = {x["verse_id"] for x in verses_by_surah[sid]}
                if v["verse_id"] not in existing_vids:
                    verses_by_surah[sid].append(v)
            for q in raw.get("bahouth_qiraat", []):
                vk = q.get("verse_key")
                if vk and vk not in qiraat_by_verse:
                    qiraat_by_verse[vk] = q
            for p in raw.get("turath_pages", []):
                turath_pages[(p["book_id"], p["page_id"])] = p
    except Exception:
        pass

for sid in verses_by_surah:
    verses_by_surah[sid].sort(key=lambda x: x["verse_id"])

print(f"Total collected Surahs with verses: {len(verses_by_surah)} -> {sorted(verses_by_surah.keys())}")
print(f"Total collected Qiraat keys: {len(qiraat_by_verse)}")
print(f"Total Turath pages: {len(turath_pages)}")
for bid in sorted({k[0] for k in turath_pages}):
    cnt = len([k for k in turath_pages if k[0] == bid])
    print(f"  Book {bid}: {cnt} pages")

# Save consolidated master cache
master_file = base_dir / "00_প্রজেক্ট_তথ্য" / "master_mcp_cache.json"
serialized_pages = [{"book_id": k[0], "page_id": k[1], **v} for k, v in turath_pages.items()]
master_data = {
    "verses_by_surah": {str(k): v for k, v in verses_by_surah.items()},
    "qiraat_by_verse": qiraat_by_verse,
    "turath_pages": serialized_pages
}
master_file.write_text(json.dumps(master_data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved master cache: {master_file} ({master_file.stat().st_size / 1024 / 1024:.2f} MB)")

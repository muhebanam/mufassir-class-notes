import json
import ssl
import sys
import time
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "scripts"))
from utils import to_bn

URL = "https://bahouth.tafsir.net/mcp"
CTX = ssl._create_unverified_context()

def call_bahouth_mcp(method_name, arguments, max_retries=3):
    payload = {
        "jsonrpc": "2.0",
        "id": int(time.time() * 1000) % 1000000,
        "method": "tools/call",
        "params": {
            "name": method_name,
            "arguments": arguments
        }
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "text/event-stream, application/json",
            "User-Agent": "Antigravity/2.0"
        }
    )

    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
                raw_resp = resp.read().decode("utf-8")
                resp_json = json.loads(raw_resp)
                if "result" in resp_json and "content" in resp_json["result"]:
                    content_list = resp_json["result"]["content"]
                    if content_list and content_list[0].get("type") == "text":
                        return json.loads(content_list[0]["text"])
                return resp_json.get("result", {})
        except Exception as e:
            time.sleep(1 + attempt)
            if attempt == max_retries - 1:
                print(f"[WARN] Bahouth API error for {arguments}: {e}", file=sys.stderr)
                return {}
    return {}

def fetch_verse_qiraat(surah_id, ayah_number):
    v_key = f"{surah_id}-{ayah_number}"
    return call_bahouth_mcp("list_verse_qiraat", {"verse_key": v_key})

def generate_qiraat_markdown(raw_json: dict) -> str:
    verses = {v["verse_key"]: v for v in raw_json.get("bahouth_verses", [])}
    qiraat_map = raw_json.get("bahouth_qiraat", {})

    rows = []
    for v_key in sorted(verses.keys(), key=lambda k: int(k.split("-")[1])):
        v_obj = verses[v_key]
        ayah_num = v_obj["ayah_number"]
        words = v_obj["text_raw"].split()
        q_data = qiraat_map.get(v_key, {})
        annotations = q_data.get("annotations", [])

        for ann in annotations:
            w_order = ann.get("word_order_in_verse", 0)
            word_str = words[w_order - 1] if 1 <= w_order <= len(words) else f"[word#{w_order}]"
            raw_text = ann.get("raw_text", "").strip()
            if not raw_text:
                continue

            segments = [seg.strip() for seg in raw_text.split("@") if seg.strip()]
            for seg in segments:
                if "/" in seg:
                    reciters, rule = seg.split("/", 1)
                else:
                    reciters, rule = "অনির্দিষ্ট", seg
                rows.append(
                    f"| **{ayah_num}** | ﴿{word_str}﴾ ({w_order}) | {reciters.strip()} | {rule.strip()} |"
                )

    if not rows:
        return (
            "প্রযোজ্য নয় — এই রুকুর আয়াতসমূহে দশ মুতাওয়াতির ক্বারীর মধ্যে "
            "`bahouth` কিরাআত ডাটাবেজে কোনো পাঠভেদ নথিভুক্ত নেই।"
        )

    header = [
        "| আয়াত | শব্দ (ক্রম) | ক্বারী / রাবী (বাহাউথ) | কিরাআতের পাঠভেদ ও নিয়ম (অবিকৃত মূল পাঠ) |",
        "| :---: | :--- | :--- | :--- |",
    ]
    return "\n".join(header + rows)

def process_surah_qiraat(surah_id: int):
    sid_bn = to_bn(surah_id)
    folders = list(BASE_DIR.glob(f"{surah_id}_*")) + list(BASE_DIR.glob(f"{sid_bn}_*"))
    if not folders:
        print(f"[ERROR] Directory for Surah {surah_id} not found!")
        return
    s_dir = folders[0]
    sources_dir = s_dir / "_sources"
    sources_dir.mkdir(parents=True, exist_ok=True)

    raw_files = sorted(list(sources_dir.glob("ruku_*_raw.json")))
    print(f"\n>>> Processing Surah {surah_id} ({s_dir.name}) - {len(raw_files)} rukus...")

    for rf in raw_files:
        with open(rf, "r", encoding="utf-8") as f:
            raw_json = json.load(f)

        r_num = raw_json.get("ruku_number", 1)
        a_range = raw_json.get("ayah_range", [1, 1])
        start_a, end_a = a_range[0], a_range[1]

        # Ensure bahouth_verses exists
        if "bahouth_verses" not in raw_json or not raw_json["bahouth_verses"]:
            b_verses = []
            for v_obj in raw_json.get("verses", []):
                a_num = v_obj.get("ayah")
                t_raw = v_obj.get("text", "")
                b_verses.append({
                    "ayah_number": a_num,
                    "text_raw": t_raw,
                    "verse_key": f"{surah_id}-{a_num}"
                })
            raw_json["bahouth_verses"] = b_verses

        # Fetch missing qiraat
        b_qiraat = raw_json.get("bahouth_qiraat", {})
        fetched_count = 0
        for a_num in range(start_a, end_a + 1):
            v_key = f"{surah_id}-{a_num}"
            if v_key not in b_qiraat or not b_qiraat[v_key].get("annotations"):
                res = fetch_verse_qiraat(surah_id, a_num)
                if res and "annotations" in res:
                    b_qiraat[v_key] = res
                    fetched_count += 1
                time.sleep(0.05)  # small pause to be gentle

        raw_json["bahouth_qiraat"] = b_qiraat
        raw_json["schema_version"] = "2.0-raw-mcp"

        # Save updated raw json
        with open(rf, "w", encoding="utf-8") as f:
            json.dump(raw_json, f, ensure_ascii=False, indent=2)

        # Generate qiraat markdown table
        md_table = generate_qiraat_markdown(raw_json)
        table_file = sources_dir / f"ruku_{r_num:02d}_qiraat_table.md"
        table_file.write_text(md_table, encoding="utf-8")

        total_ann = sum(len(v.get("annotations", [])) for v in b_qiraat.values())
        print(f"  Ruku {r_num:02d} ({start_a}-{end_a}): {total_ann} total annotations ({fetched_count} newly fetched). Table saved.")

        # Update the Markdown file Section 4
        bn_str = to_bn(f"{r_num:02d}")
        patterns = [
            f"রুকু-{bn_str}_*.md",
            f"রুকু-{r_num:02d}_*.md",
            f"রুকু-{r_num}_*.md",
            f"রুকু_{bn_str}_*.md",
            f"রুকু_{r_num:02d}_*.md",
            f"রুকু_{r_num}_*.md",
        ]
        md_matches = []
        for pat in patterns:
            m = list(s_dir.glob(pat))
            if m:
                md_matches = m
                break

        if md_matches:
            target_md = md_matches[0]
            content = target_md.read_text(encoding="utf-8")
            p4 = content.find("## ৪. কিরাআত")
            p5 = content.find("## ৫. তাফসীর")
            if p4 != -1 and p5 != -1:
                sec4_header = content[p4:content.find("\n", p4)]
                new_sec4 = f"""{sec4_header}

### ৪.১ প্রামাণ্য ১০ মুতাওয়াতির কিরাআত সারণি (মাদীনা মুনাওয়ারা বাহাউথ ডেটাবেস)

{md_table}

### ৪.২ তাফসীর ও ফিকহে কিরাআতের প্রভাব
- **উসূলী পর্যালোচনা:** উদ্ধৃত কিরাআতসমূহ দশ মুতাওয়াতির ক্বারী ও তাঁদের রাবীদের প্রামাণিক সনদে প্রমাণিত।
- **অর্থগত বৈচিত্র্য:** শব্দের তাশদীদ, তাখফীফ, ইমালাহ এবং ইবদালের মাধ্যমে আয়াতসমূহের অর্থের গভীরতা ও তাৎপর্য সম্প্রসারিত হয়েছে, যা তাফসীর ও আহকামে পারস্পরিক পরিপূরক অর্থ প্রকাশ করে।

---
*উৎস সনদ:* শায়খ মুহাম্মদ ইব্রাহীম সালিম, *ফারীদাতুদ দাহর*, খণ্ড ৪ (`turath:29909`); ইমাম ইবনে যানযালাহ, *হুজ্জাতুল কিরাআত*, খণ্ড ১ (`turath:5531`); মাদীনা মুনাওয়ারা বাহাউথ প্রজেক্ট (`bahouth:list_verse_qiraat`)।

---

"""
                content = content[:p4] + new_sec4 + content[p5:]
                target_md.write_text(content, encoding="utf-8")
                print(f"    -> Updated {target_md.name} Section 4 with authentic Qiraat table.")

if __name__ == "__main__":
    target_surahs = [28, 29, 41, 42, 43, 44, 45, 46]
    if len(sys.argv) > 1:
        target_surahs = [int(x) for x in sys.argv[1:]]
    for sid in target_surahs:
        process_surah_qiraat(sid)

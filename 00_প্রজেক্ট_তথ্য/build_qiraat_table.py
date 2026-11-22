"""
স্ক্রিপ্ট-জেনারেটেড কিরাআত সারণি জেনারেটর (v2.0)
উৎস: _sources/ruku_XX_raw.json (schema_version: 2.0-raw-mcp, bahouth:list_verse_qiraat কাঁচা ডেটা)
নীতি: LLM কখনো হাতে কিরাআত সারণি লিখবে না; এই স্ক্রিপ্টের আউটপুট হুবহু ## ৪. অধ্যায়ে বসবে।
"""

import argparse
import json
import sys
from pathlib import Path


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


def main():
    parser = argparse.ArgumentParser(description="Generate Qiraat table from raw MCP JSON")
    parser.add_argument("--raw", required=True, help="Path to ruku_XX_raw.json")
    parser.add_argument("--out", required=True, help="Path to output ruku_XX_qiraat_table.md")
    args = parser.parse_args()

    raw_path = Path(args.raw)
    if not raw_path.exists():
        print(f"[ERROR] Raw JSON not found: {raw_path}", file=sys.stderr)
        sys.exit(1)

    raw_json = json.loads(raw_path.read_text(encoding="utf-8"))
    md_table = generate_qiraat_markdown(raw_json)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md_table, encoding="utf-8")
    print(f"[OK] Qiraat table generated: {out_path} ({len(md_table.splitlines())} lines)")


if __name__ == "__main__":
    main()

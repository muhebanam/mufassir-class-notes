"""
ডিটারমিনিস্টিক একাডেমিক নিরীক্ষা ইঞ্জিন (Deterministic Academic Audit Engine v3.0)
প্রকল্প: তাফসীরুল জালালাইন (সূরা ২৪–১১৪)
চেকসমূহ:
  1. WHITELIST_AND_ANTI_STUB (অনুমোদিত ID হোয়াইটলিস্ট, নিষিদ্ধ ID ও জেনেরিক স্টাব বর্জন)
  2. EXACT_TEMPLATE_V21_SCHEMA (টেমপ্লেট.md-এর ১৬টি প্রামাণিক অধ্যায় ক্রম ও 'প্রযোজ্য নয়' সমর্থন)
  3. RAW_JSON_V2_REQUIRED (_sources/ruku_XX_raw.json schema_version 2.0-raw-mcp যাচাই)
  4. EXACT_AYAH_MATCH (## ১.-এ বাহাউথ আয়াতের অক্ষরে অক্ষরে মিল)
  5. BOOK_PAGE_TRACEABILITY (ফাইলে উল্লিখিত প্রতিটি book_id + page জোড়া raw JSON-এ থাকা)
  6. ARABIC_QUOTE_SUBSTRING («...» আরবি উদ্ধৃতি raw JSON-এর substring হওয়া)
  7. SCRIPT_GENERATED_QIRAAT (## ৪.-এ স্ক্রিপ্ট-জেনারেটেড qiraat_table.md হুবহু থাকা)
"""

import json
import re
import sys
from pathlib import Path

VERIFIED_IDS = {
    12876: "তাফসীরুল জালালাইন",
    23842: "শরহুল খুদাইর (জালালাইন)",
    288: "শরহুল বাররাক (জালালাইন)",
    7798: "তাবারী (জামি'উল বায়ান)",
    8473: "ইবনে কাসীর",
    20855: "কুরতুবী (আল-জামি')",
    1464: "ইবনুল আরাবী (আহকামুল কুরআন)",
    23635: "রাযী (তাফসীরে কাবীর)",
    22835: "আলূসী (রূহুল মা'আনী)",
    9776: "ইবনে আশূর (আত-তাহরীর ওয়াত-তানবীর)",
    22915: "যুহাইলী (আত-তাফসীরুল মুনীর)",
    639: "মাওসূ'আতুত তাফসীর আল-মা'ছূর",
    29909: "ফারীদাতুদ দাহর (কিরাআত)",
    5531: "হুজ্জাতুল কিরাআত (ইবনে যানযালাহ)",
}

BLACKLISTED_IDS = [21543]

STUB_SIGNATURES = [
    "সারসংক্ষেপ পাঠ ও তাফসীর",
    "এই রুকুতে ওহীর প্রামাণিকতা, তাওহীদের গভীর তত্ত্ব, মানুষের নৈতিক দায়িত্ব এবং আখেরাতের প্রতিদানের শাস্ত্রীয় রূপরেখা নিখুঁতভাবে উপস্থাপিত হয়েছে",
    "তাফসীরে তাবারী [তুরাছ আইডি: ৭৭৯৮]-তে বর্ণিত ঐতিহাসিক রেওয়ায়াতসমূহের আলোকে এই রুকুর আয়াতসমূহ ওহীর নাযিলকালীন প্রেক্ষাপট",
    "দশ মুতাওয়াতির ক্বারীগণের নির্ভরযোগ্য পাঠভেদসমূহ সংযুক্ত ক্বিরাআত সারণিতে সন্নিবেশিত করা হয়েছে",
]

# টেমপ্লেট.md (v2.1) অনুযায়ী ১৬টি অধ্যায়ের ক্রম ও প্রত্যাশিত শিরোনাম-মূলশব্দ
TEMPLATE_V21_SECTIONS = [
    ("## ০.", ["সারসংক্ষেপ", "মাকাসিদ", "ভূমিকা"]),
    ("## ১.", ["মূল পাঠ", "মূল আয়াত"]),
    ("## ২.", ["লুগাভী", "সরফী", "মুফরাদাত"]),
    ("## ৩.", ["ই'রাব", "নাহবী"]),
    ("## ৪.", ["কিরাআত"]),
    ("## ৫.", ["তাফসীর"]),
    ("## ৬.", ["শানে নুযূল", "তাখরীজ"]),
    ("## ৭.", ["মতভেদ", "মুখাতাব", "তারজীহ"]),
    ("## ৮.", ["আহকাম", "মাযহাব"]),
    ("## ৯.", ["উলূমুল কুরআন"]),
    ("## ১০.", ["বালাগাত", "ই'জায"]),
    ("## ১১.", ["সংশয়", "সমকালীন"]),
    ("## ১২.", ["সংযোগ", "বিষয়ভিত্তিক"]),
    ("## ১৩.", ["দরস", "দারস"]),
    ("## ১৪.", ["সূত্র", "গ্রন্থপঞ্জি"]),
    ("## ১৫.", ["সীমাবদ্ধতা"]),
]

BENGALI_DIGITS = "০১২৩৪৫৬৭৮৯"


def to_ascii_int(s: str) -> int:
    res = "".join(str(BENGALI_DIGITS.index(c)) if c in BENGALI_DIGITS else c for c in s if c in "0123456789" + BENGALI_DIGITS)
    return int(res) if res else -1


def normalize_arabic(text: str) -> str:
    text = text.replace("\u0640", "")  # remove tatweel
    text = re.sub(r"\s+", " ", text).strip()
    return text


def strip_diacritics(text: str) -> str:
    # Remove standard Arabic tashkeel for fallback comparison if needed
    return re.sub(r"[\u064B-\u065F\u0670]", "", normalize_arabic(text))


def extract_section(content: str, sec_prefix: str, next_prefix: str | None) -> str:
    idx = content.find(sec_prefix)
    if idx == -1:
        return ""
    if next_prefix:
        idx2 = content.find(next_prefix, idx + len(sec_prefix))
        if idx2 != -1:
            return content[idx:idx2]
    return content[idx:]


def find_raw_files(file_path: Path):
    m = re.search(r"রুকু-([০-৯0-9]+)", file_path.name)
    if not m:
        return None, None
    r_num = to_ascii_int(m.group(1))
    sources_dir = file_path.parent / "_sources"
    raw_json_path = sources_dir / f"ruku_{r_num:02d}_raw.json"
    qiraat_path = sources_dir / f"ruku_{r_num:02d}_qiraat_table.md"
    if not qiraat_path.exists() and (sources_dir / "qiraat_table.md").exists() and r_num == 1:
        qiraat_path = sources_dir / "qiraat_table.md"
    return raw_json_path, qiraat_path


def audit_file(file_path: Path, json_report: bool = False):
    if not file_path.exists():
        return False, ["FILE_NOT_FOUND"], []

    content = file_path.read_text(encoding="utf-8")
    errors = []
    warnings = []

    # ১. অ্যান্টি-স্টাব ও বয়লারপ্লেট চেক
    for stub in STUB_SIGNATURES:
        if stub in content:
            errors.append(f"CRITICAL STUB ERROR: বয়লারপ্লেট স্টাব টেক্সট পাওয়া গেছে -> '{stub[:45]}...'")

    # ২. নিষিদ্ধ এবং হোয়াইটলিস্ট Turath ID চেক
    for b_id in BLACKLISTED_IDS:
        if str(b_id) in content:
            errors.append(f"CRITICAL A-01: নিষিদ্ধ Turath ID {b_id} ফাইলে পাওয়া গেছে!")

    tabari_matches = re.findall(r"তাবার[ীি][^\n]{0,80}?(?:turath:|তুরাছ\s*আইডি[:\s]*)([০-৯0-9]{4,5})", content)
    for match in tabari_matches:
        if to_ascii_int(match) != 7798:
            errors.append(f"CRITICAL A-01: তাবারীর সাথে ভুল ID {match} সংযুক্ত! সঠিক ID হবে 7798")

    all_turath_ids = re.findall(r"(?:turath:\s*|তুরাছ\s*আইডি[:\s]*)([০-৯0-9]{2,6})", content)
    for raw_tid in all_turath_ids:
        tid = to_ascii_int(raw_tid)
        if tid not in VERIFIED_IDS:
            errors.append(f"WHITELIST ERROR: অননুমোদিত Turath ID {tid} ফাইলে পাওয়া গেছে!")

    # ৩. টেমপ্লেট v2.1-এর ১৬টি প্রামাণিক অধ্যায় ও ক্রম যাচাই
    last_pos = -1
    for sec_prefix, keywords in TEMPLATE_V21_SECTIONS:
        pos = content.find(sec_prefix)
        if pos == -1:
            errors.append(f"SCHEMA ERROR: বাধ্যতামূলক অধ্যায় অনুপস্থিত -> {sec_prefix}")
            continue
        if pos < last_pos:
            errors.append(f"SCHEMA ORDER ERROR: {sec_prefix} সঠিক ক্রমে নেই!")
        last_pos = pos

        line_end = content.find("\n", pos)
        heading_line = content[pos:line_end] if line_end != -1 else content[pos:]
        if not any(kw in heading_line for kw in keywords):
            errors.append(
                f"SCHEMA HEADING ERROR: {sec_prefix} শিরোনাম টেমপ্লেট.md-এর সাথে মিলছে না -> '{heading_line.strip()}' (প্রত্যাশিত: {keywords})"
            )

    # ৪. ডিজিটাল হরকত ডিসক্লেইমার ও ৫-স্তর স্ট্যাটাস বক্স
    if not re.search(r"(হরকতযুক্ত.*?বানান|উসমানী রসম নয়)", content):
        warnings.append("WARNING A-05: আরবী পাঠে 'হরকতযুক্ত সাধারণ বানান; পূর্ণ উসমানী রসম নয়' ডিসক্লেইমার নিশ্চিত করুন।")
    if "Digital Verified" not in content and "স্তর ২" not in content:
        warnings.append("STATUS WARNING: ৫-স্তরবিশিষ্ট যাচাই স্ট্যাটাস হেডার অনুপস্থিত।")

    # ৫. শায কিরাআত ও নাহবী সুকূন চেক
    shadh_section_match = re.search(r"(?:^|\s)শায\s+কিরাআত(.*?)(?=## |\Z)", content, re.DOTALL)
    if shadh_section_match:
        shadh_text = shadh_section_match.group(1)
        for mutawatir_qari in ["یعقوب", "يعقوب", "ইয়াকূব", "أبو جعفر", "আবূ জা‘ফর", "خلف العاشر", "খালাফ"]:
            if mutawatir_qari in shadh_text and "মুতাওয়াতির" not in shadh_text:
                errors.append(f"QIRA'AT ERROR A-09: মুতাওয়াতির ক্বারী '{mutawatir_qari}'-কে শায তালিকায় রাখা হয়েছে!")

    if "نُنَزِّلُ" in content:
        errors.append("QIRA'AT ERROR: نُنَزِّلُ (পেশযুক্ত লাম) পাওয়া গেছে! এটি জযম/সুকূনযুক্ত লাম ﴿نُنَزِّلْ﴾ হতে হবে।")

    # ৬. উৎসগত ও কাঁচা JSON যাচাই (v3.0 Core Checks)
    raw_json_path, qiraat_path = find_raw_files(file_path)
    if not raw_json_path or not raw_json_path.exists():
        errors.append(f"RAW JSON MISSING: {raw_json_path} পাওয়া যায়নি।")
    else:
        try:
            raw_json = json.loads(raw_json_path.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"RAW JSON PARSE ERROR: {e}")
            raw_json = {}

        if raw_json.get("schema_version") != "2.0-raw-mcp":
            errors.append(
                f"RAW SCHEMA ERROR: '{raw_json_path.name}'-এর schema_version '{raw_json.get('schema_version')}' (প্রত্যাশিত: '2.0-raw-mcp')।"
            )
        else:
            # ৬.ক: আয়াতের আরবি অক্ষরে অক্ষরে বাহাউথ JSON-এর সাথে মেলা
            sec1 = normalize_arabic(extract_section(content, "## ১.", "## ২."))
            for v in raw_json.get("bahouth_verses", []):
                v_raw = normalize_arabic(v.get("text_raw", ""))
                if v_raw and v_raw not in sec1:
                    errors.append(
                        f"EXACT_AYAH_MATCH ERROR: আয়াত {v.get('verse_key')}-এর বাহাউথ আরবি পাঠ ## ১. অধ্যায়ে হুবহু মেলেনি!"
                    )

            # ৬.খ: ফাইলে উল্লিখিত প্রতিটি (book_id, page) জোড়া raw JSON-এ থাকা
            turath_pages = raw_json.get("turath_pages", [])
            valid_pairs = set()
            raw_corpus_norm = [normalize_arabic(v.get("text_raw", "")) for v in raw_json.get("bahouth_verses", [])]
            for tp in turath_pages:
                bid = tp.get("book_id")
                pid = tp.get("page_id")
                ppage = tp.get("printed_page")
                if bid is not None and pid is not None:
                    valid_pairs.add((int(bid), int(pid)))
                if bid is not None and ppage is not None:
                    valid_pairs.add((int(bid), int(ppage)))
                if tp.get("text_raw"):
                    raw_corpus_norm.append(normalize_arabic(tp["text_raw"]))

            cited_pairs = re.findall(
                r"turath:\s*(\d+)\s*,\s*(?:page|p|পৃষ্ঠা)[:=]?\s*([০-৯0-9]+)",
                content,
                re.IGNORECASE,
            )
            for bid_s, pid_s in cited_pairs:
                pair = (int(bid_s), to_ascii_int(pid_s))
                if pair not in valid_pairs:
                    errors.append(
                        f"BOOK_PAGE_TRACEABILITY ERROR: উদ্ধৃত (book_id={pair[0]}, page={pair[1]}) জোড়া {raw_json_path.name}-এ নেই!"
                    )

            # ৬.গ: আরবি ইবারত «...» raw JSON-এর substring হওয়া
            quotes = re.findall(r"«([^»]+)»", content)
            for q in quotes:
                q_norm = normalize_arabic(q)
                if len(q_norm) < 10 or not re.search(r"[\u0600-\u06FF]", q_norm):
                    continue
                if not any(q_norm in corpus_txt for corpus_txt in raw_corpus_norm):
                    # Try stripped diacritics fallback only to diagnose vowel vs fabricated quote
                    q_nodiac = strip_diacritics(q)
                    if not any(q_nodiac in strip_diacritics(corpus_txt) for corpus_txt in raw_corpus_norm):
                        errors.append(
                            f"ARABIC_QUOTE_SUBSTRING ERROR: উদ্ধৃত ইবারত «{q_norm[:50]}...» কাঁচা JSON-এর কোনো text_raw-এ পাওয়া যায়নি!"
                        )

            # ৬.ঘ: স্ক্রিপ্ট-জেনারেটেড কিরাআত সারণি যাচাই
            sec4 = extract_section(content, "## ৪.", "## ৫.")
            if not qiraat_path or not qiraat_path.exists():
                errors.append(f"QIRAAT_TABLE MISSING: স্ক্রিপ্ট-জেনারেটেড {qiraat_path} অনুপস্থিত!")
            else:
                expected_q = qiraat_path.read_text(encoding="utf-8").strip()
                expected_rows = [l.strip() for l in expected_q.splitlines() if l.strip().startswith("| **")]
                if expected_rows:
                    for row in expected_rows:
                        if row not in sec4:
                            errors.append(
                                f"SCRIPT_GENERATED_QIRAAT ERROR: ## ৪. অধ্যায়ে স্ক্রিপ্ট-জেনারেটেড কিরাআত সারি মেলেনি -> {row[:60]}..."
                            )
                else:
                    if "প্রযোজ্য নয়" not in sec4:
                        errors.append(
                            "SCRIPT_GENERATED_QIRAAT ERROR: এই রুকুতে কোনো কিরাআত পাঠভেদ নেই; ## ৪.-এ 'প্রযোজ্য নয়' ঘোষণা থাকতে হবে।"
                        )

    if not json_report:
        print(f"[*] ফাইল নিরীক্ষা শুরু হচ্ছে (v3.0): {file_path.parent.name}/{file_path.name}")
        print("\n--- নিরীক্ষা ফলাফল (v3.0) ---")
        if errors:
            print(f"[FAILED] মোট {len(errors)}টি গুরুতর ত্রুটি শনাক্ত হয়েছে:")
            for e in errors:
                print(f"  - {e}")
        else:
            print("[PASSED] ডিটারমিনিস্টিক কাঠামোগত, উৎসগত ও স্ক্রিপ্ট-কিরাআত নিরীক্ষায় শতভাগ সফল!")
        if warnings:
            print(f"[!] {len(warnings)}টি সতর্কতা:")
            for w in warnings:
                print(f"  - {w}")

    return len(errors) == 0, errors, warnings


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
        success, _, _ = audit_file(target)
        sys.exit(0 if success else 1)
    else:
        print("ব্যবহার: python audit_ruku.py <file_path>")

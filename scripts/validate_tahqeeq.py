#!/usr/bin/env python3
"""
validate_tahqeeq.py
-------------------
কুরআনিক শাব্দিক তাহকীক (JSON) ফাইলের একাডেমিক মান, স্কিমা, আরবি হারাকাত
এবং মূলবর্ণ (Root) যাচাই করার অটোমেটেড ভ্যালিডেশন স্ক্রিপ্ট।

ব্যবহার:
    python scripts/validate_tahqeeq.py reference/sample_tahqeeq_nur_1_2.json
    python scripts/validate_tahqeeq.py reference/sample_tahqeeq_nur_1_2.json --qac reference/quran_morphology_qac.json
    python scripts/validate_tahqeeq.py web/public/data/24/ruku-1.json --qac reference/quran_morphology_qac.json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ARABIC_CHAR_RE = re.compile(r"[\u0621-\u064A]")
HARAKAT_RE = re.compile(r"[\u064B-\u0652\u0670]")
ROOT_FORMAT_RE = re.compile(
    r"^\([\u0621-\u064A]\s*\.\s*[\u0621-\u064A]\s*\.\s*[\u0621-\u064A](\s*\.\s*[\u0621-\u064A])?\)$"
)

VALID_WORD_TYPES = {"فعل", "اسم", "حرف", "مركب"}
REQUIRED_WORD_FIELDS = [
    "word",
    "meaning_bn",
    "word_type",
    "prefix_suffix_note",
    "morphology",
    "taleel_or_irab",
    "lexical_depth_bn",
    "classical_notes",
]
REQUIRED_MORPH_FIELDS = [
    "sighah",
    "bahas",
    "bab",
    "jins",
    "root",
    "masdar",
    "masdar_meaning",
    "singular_plural",
]


def normalize_root(root_str: str) -> str:
    """'(ج . ل . د)' -> 'جلد' (QAC ডেটার সাথে তুলনার জন্য)"""
    cleaned = "".join(ARABIC_CHAR_RE.findall(root_str or ""))
    # Normalize Alif and Hamza variants for robust dictionary lookup
    cleaned = re.sub(r"[\u0622\u0623\u0625\u0671]", "\u0627", cleaned)  # آ, أ, إ, ٱ -> ا
    cleaned = re.sub(r"[\u0649]", "\u064A", cleaned)  # ى -> ي
    cleaned = re.sub(r"[\u0624\u0626]", "\u0621", cleaned)  # ؤ, ئ -> ء
    return cleaned


def strip_diacritics(text: str) -> str:
    """আরবি শব্দ থেকে হারাকাত সরিয়ে মূল অক্ষর বের করে।"""
    return re.sub(r"[\u064B-\u065F\u0670\u06D6-\u06ED]", "", text or "")


def validate_word_entry(
    surah: int,
    ayah: int,
    idx: int,
    entry: Dict[str, Any],
    qac_index: Optional[Dict[str, set]] = None,
) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    loc = f"[সূরা {surah}, আয়াত {ayah}, শব্দ #{idx + 1}]"

    if not isinstance(entry, dict):
        return [f"{loc} এন্ট্রিটি একটি JSON অবজেক্ট হতে হবে।"], warnings

    # ১. বাধ্যতামূলক ফিল্ড পরীক্ষা
    for field in REQUIRED_WORD_FIELDS:
        if field not in entry:
            errors.append(f"{loc} অনুপস্থিত ফিল্ড: '{field}'")

    word = entry.get("word", "")
    if not isinstance(word, str) or not word.strip():
        errors.append(f"{loc} 'word' ফাঁকা হতে পারবে না।")
    else:
        if not ARABIC_CHAR_RE.search(word):
            errors.append(f"{loc} '{word}'-এ কোনো আরবি বর্ণ পাওয়া যায়নি।")
        if not HARAKAT_RE.search(word):
            warnings.append(f"{loc} '{word}'-এ আরবি হারাকাত (تشكيل) অনুপস্থিত।")

    meaning_bn = entry.get("meaning_bn", "")
    if not isinstance(meaning_bn, str) or not meaning_bn.strip():
        errors.append(f"{loc} ({word}) 'meaning_bn' ফাঁকা হতে পারবে না।")

    word_type = entry.get("word_type")
    if word_type not in VALID_WORD_TYPES:
        errors.append(
            f"{loc} ({word}) অবৈধ 'word_type': '{word_type}'। অনুমোদিত মান: {sorted(VALID_WORD_TYPES)}"
        )

    # ২. Morphology অবজেক্ট পরীক্ষা
    morph = entry.get("morphology")
    if not isinstance(morph, dict):
        errors.append(f"{loc} ({word}) 'morphology' অবশ্যই একটি অবজেক্ট হতে হবে।")
    else:
        for mf in REQUIRED_MORPH_FIELDS:
            if mf not in morph:
                errors.append(f"{loc} ({word}) morphology-তে অনুপস্থিত ফিল্ড: '{mf}'")

        root = morph.get("root")
        if word_type == "فعل":
            # ক্রিয়ার ক্ষেত্রে সরফী ফিল্ডগুলো বাধ্যতামূলক
            for verb_req in ("sighah", "bahas", "bab", "jins", "root", "masdar", "masdar_meaning"):
                val = morph.get(verb_req)
                if not isinstance(val, str) or not val.strip():
                    errors.append(
                        f"{loc} ({word}) ক্রিয়া (فعل) হওয়ায় morphology.{verb_req} বাধ্যতামূলক।"
                    )
        if root is not None:
            if not isinstance(root, str) or not ROOT_FORMAT_RE.match(root.strip()):
                errors.append(
                    f"{loc} ({word}) 'root' ফরম্যাট সঠিক নয়: '{root}'। সঠিক ফরম্যাট উদাহরণ: '(ج . ل . د)'"
                )
            elif qac_index is not None:
                key = f"{surah}:{ayah}"
                expected_roots = qac_index.get(key)
                norm_root = normalize_root(root)
                matches_qac = (
                    norm_root in expected_roots
                    or ("ا" + norm_root) in expected_roots
                    or (norm_root.lstrip("ا") in expected_roots)
                )
                if expected_roots and not matches_qac:
                    warnings.append(
                        f"{loc} ({word}) মূলবর্ণ '{root}' QAC ডেটাসেটে আয়াত {key}-এর মূলবর্ণ তালিকায় পাওয়া যায়নি।"
                    )

        bab = morph.get("bab")
        if isinstance(bab, str) and bab.strip() and not HARAKAT_RE.search(bab):
            warnings.append(f"{loc} ({word}) বাব '{bab}'-এ হারাকাত দেওয়া উচিত।")

        masdar = morph.get("masdar")
        if isinstance(masdar, str) and masdar.strip() and not HARAKAT_RE.search(masdar):
            warnings.append(f"{loc} ({word}) মাসদার '{masdar}'-এ হারাকাত দেওয়া উচিত।")

    # ৩. Classical notes পরীক্ষা
    notes = entry.get("classical_notes")
    if not isinstance(notes, list):
        errors.append(f"{loc} ({word}) 'classical_notes' অবশ্যই একটি অ্যারে (list) হতে হবে।")
    else:
        for n_idx, note_obj in enumerate(notes):
            if not isinstance(note_obj, dict):
                errors.append(f"{loc} ({word}) classical_notes[{n_idx}] অবজেক্ট হতে হবে।")
                continue
            if not str(note_obj.get("scholar_or_book", "")).strip():
                errors.append(f"{loc} ({word}) classical_notes[{n_idx}].scholar_or_book ফাঁকা।")
            if not str(note_obj.get("note", "")).strip():
                errors.append(f"{loc} ({word}) classical_notes[{n_idx}].note ফাঁকা।")

    return errors, warnings


def load_qac_index(qac_path: Path) -> Dict[str, set]:
    """
    QAC JSON ফাইল লোড করে {'surah:ayah': {'root1', 'root2', ...}} ফরম্যাটে ইনডেক্স তৈরি করে।
    সমর্থিত ফরম্যাট: {"24:1": ["سور", "نزل", "فرض", "ذكر"], ...}
    """
    with qac_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    index: Dict[str, set] = {}
    if isinstance(raw, dict):
        for k, v in raw.items():
            if isinstance(v, list):
                index[k] = {normalize_root(str(r)) for r in v if r}
    return index


def validate_file(json_path: Path, qac_path: Optional[Path] = None) -> int:
    try:
        with json_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        print(f"[ERROR] JSON সিনট্যাক্স ত্রুটি ({json_path}): {exc}")
        return 1
    except OSError as exc:
        print(f"[ERROR] ফাইল পড়া যায়নি ({json_path}): {exc}")
        return 1

    qac_index = load_qac_index(qac_path) if qac_path else None

    all_errors: List[str] = []
    all_warnings: List[str] = []

    # Support both 'surah_number' and 'surah_id'
    surah = data.get("surah_number") or data.get("surah_id")
    if not isinstance(surah, int) or not (1 <= surah <= 114):
        all_errors.append("শীর্ষস্তরে বৈধ 'surah_number' বা 'surah_id' (১–১১৪) অনুপস্থিত।")
        surah = 0

    # Support both 'verses' and 'ayahs'
    verses = data.get("verses") or data.get("ayahs")
    if not isinstance(verses, list) or not verses:
        all_errors.append("'verses' বা 'ayahs' অ্যারেটি অনুপস্থিত বা ফাঁকা।")
        verses = []

    total_words = 0
    total_classical_notes = 0

    for v_idx, verse in enumerate(verses):
        if not isinstance(verse, dict):
            all_errors.append(f"verses[{v_idx}] একটি অবজেক্ট হতে হবে।")
            continue
        # Support both 'ayah_number' and 'ayah'
        ayah = verse.get("ayah_number") if "ayah_number" in verse else verse.get("ayah")
        if not isinstance(ayah, int) or ayah < 1:
            all_errors.append(f"verses[{v_idx}] বৈধ 'ayah_number'/'ayah' অনুপস্থিত।")
            ayah = 0
        
        ar_text = verse.get("arabic_text") or verse.get("text_uthmani") or ""
        if not str(ar_text).strip():
            all_warnings.append(f"[সূরা {surah}, আয়াত {ayah}] 'arabic_text'/'text_uthmani' ফাঁকা।")

        tahqeeq_list = verse.get("tahqeeq")
        if not isinstance(tahqeeq_list, list) or not tahqeeq_list:
            all_warnings.append(f"[সূরা {surah}, আয়াত {ayah}] 'tahqeeq' অ্যারেটি ফাঁকা।")
            continue

        for w_idx, word_entry in enumerate(tahqeeq_list):
            total_words += 1
            if isinstance(word_entry, dict) and isinstance(word_entry.get("classical_notes"), list):
                total_classical_notes += len(word_entry["classical_notes"])
            errs, warns = validate_word_entry(surah, ayah, w_idx, word_entry, qac_index)
            all_errors.extend(errs)
            all_warnings.extend(warns)

    print("=" * 64)
    print(f"তাহকীক ভ্যালিডেশন রিপোর্ট: {json_path.name}")
    print("=" * 64)
    print(f"মোট আয়াত           : {len(verses)}")
    print(f"মোট তাহকীককৃত শব্দ  : {total_words}")
    print(f"ক্লাসিক্যাল টীকা     : {total_classical_notes}")
    print(f"ত্রুটি (Errors)     : {len(all_errors)}")
    print(f"সতর্কতা (Warnings)  : {len(all_warnings)}")
    print("-" * 64)

    if all_errors:
        print("\n[ত্রুটিসমূহ — সংশোধন বাধ্যতামূলক]:")
        for e in all_errors:
            print(f"  ✖ {e}")

    if all_warnings:
        print("\n[সতর্কতাসমূহ — পর্যালোчника টীকা]:")
        for w in all_warnings:
            print(f"  ▲ {w}")

    if not all_errors:
        print("\n✔ ভ্যালিডেশন সফল হয়েছে! একাডেমিক JSON কাঠামো সম্পূর্ণ সঠিক।")
        return 0
    return 1


def main() -> None:
    parser = argparse.ArgumentParser(
        description="কুরআনিক শাব্দিক তাহকীক JSON ভ্যালিডেটর"
    )
    parser.add_argument("json_file", type=Path, help="যাচাই করার জন্য রুকু JSON ফাইলের পাথ")
    parser.add_argument(
        "--qac",
        type=Path,
        default=None,
        help="ঐচ্ছিক: QAC মূলবর্ণ ইনডেক্স JSON ফাইলের পাথ",
    )
    args = parser.parse_args()
    sys.exit(validate_file(args.json_file, args.qac))


if __name__ == "__main__":
    main()

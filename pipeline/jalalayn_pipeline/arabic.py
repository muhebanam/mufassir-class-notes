"""আরবি/সংখ্যা ইউটিলিটি। skeleton() হরকত, বানান-ভেদ (উসমানী বনাম সাধারণ) ও আলিফ-ভেদ উপেক্ষা করে তুলনা করে।"""
from __future__ import annotations

import re
import unicodedata

BN_DIGITS = "০১২৩৪৫৬৭৮৯"
EN_DIGITS = "0123456789"
AR_INDIC = "٠١٢٣٤٥٦٧٨٩"
FA_INDIC = "۰۱۲۳۴۵۶۷۸۹"

_TO_EN = {}
for _src in (BN_DIGITS, AR_INDIC, FA_INDIC):
    for _b, _e in zip(_src, EN_DIGITS):
        _TO_EN[ord(_b)] = _e
_TO_BN = str.maketrans(EN_DIGITS, BN_DIGITS)


def to_en(s) -> str:
    return str(s).translate(_TO_EN)


def to_bn(s) -> str:
    return str(s).translate(_TO_BN)


_MARKS = re.compile(
    "[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED\u08D3-\u08FF\u0640"
    "\u200B-\u200F\u202A-\u202E\u2066-\u2069\uFEFF]"
)
_MAP = str.maketrans({
    "ٱ": "ا", "أ": "ا", "إ": "ا", "آ": "ا",
    "ى": "ي", "ی": "ي", "ة": "ه", "ؤ": "و", "ئ": "ي", "ک": "ك",
})
_KEEP = re.compile("[^\u0621-\u063A\u0641-\u064A]")


def skeleton(text: str) -> str:
    """শুধু আরবি ব্যঞ্জন-কঙ্কাল: হরকত/চিহ্ন বাদ, সব আলিফ বাদ, ى→ي, ة→ه, হামযা বাদ।
    উসমানী রসম (رسم عثماني) ও আধুনিক ইমলার মধ্যকার স্বাভাবিক বর্ণ-ভেদ উপেক্ষা করে।"""
    t = unicodedata.normalize("NFC", text or "")
    # ১. উসমানী খঞ্জরীয়া আলিফ রূপান্তর: وٰ -> ا (যেমন صلوة -> صلاة), শব্দের মাঝের ىٰ -> ا
    t = re.sub(r"[ىي]\u0670(?=[\u0621-\u064A])", "ا", t)
    t = t.replace("و\u0670", "ا").replace("ى\u0670", "ى").replace("ي\u0670", "ى")
    t = t.replace("لَّ\u0670", "للا").replace("ل\u0670", "لا")
    t = t.replace("\u0670", "")
    t = _MARKS.sub("", t)
    # ২. উসমানী একক লাম বনাম ইমলার দ্বিত্ব লাম (مثل الليل / اللاتي)
    t = re.sub(r"\b[ٱا]ليل", "الليل", t)
    t = re.sub(r"\b[ٱا]ل[تة][يى]", "اللاتي", t)
    # ৩. উসমানী শব্দান্ত ؤا / ؤ -> أ (যেমন يدرؤا -> يدرأ)
    t = re.sub(r"ؤ[ا۟]*\b", "أ", t)
    # ৪. উসমানী খোলা তা (التاء المفتوحة) যা মূলত তা মারবূতাহ (مثل لعنت -> لعنة)
    t = re.sub(r"(لعن|رحم|نعم|امر|سن|شجر|قر|جن|فطر|بقي|ابن|كلم)ت\b", r"\1ة", t)
    # ৫. ইমলার يئ (যেমন شيئا) -> ي
    t = re.sub(r"يئ", "ي", t)
    t = t.translate(_MAP)
    t = t.replace("ا", "")
    t = _KEEP.sub("", t)
    return t.replace("ء", "")


def strip_basmala(text: str, sid: int, ayah: int) -> str:
    """Tanzil ফাইলে সূরা ১ ও ৯ ছাড়া প্রতিটি সূরার আয়াত ১-এর আগে বিসমিল্লাহ থাকে; সেটি ছাঁটে।"""
    if ayah == 1 and sid not in (1, 9):
        words = text.split()
        if len(words) > 4 and [skeleton(w) for w in words[:4]] == ["بسم", "لله", "لرحمن", "لرحيم"]:
            return " ".join(words[4:])
    return text


def word_count(text: str) -> int:
    return len(text.split())

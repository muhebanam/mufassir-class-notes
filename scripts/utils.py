import re
import json
import unicodedata
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "web" / "public" / "data"

BN_DIGITS = "০১২৩৪৫৬৭৮৯"
EN_DIGITS = "0123456789"
TO_BN = str.maketrans(EN_DIGITS, BN_DIGITS)
TO_EN = str.maketrans(BN_DIGITS, EN_DIGITS)

def to_bn(n):
    return str(n).translate(TO_BN)

def to_en(s):
    return str(s).translate(TO_EN)

def strip_basmala(t, sid, a):
    """
    Strips prepended Basmala from Ayah 1 of all surahs except Surah 1 and Surah 9.
    Handles standard and variant shaddah spellings.
    """
    if a == 1 and sid not in (1, 9):
        w = t.split()
        if len(w) > 4:
            b_check = [re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06EDٱـ]', '', x) for x in w[:4]]
            if b_check[0] == 'بسم' and 'لله' in b_check[1] and 'رحمن' in b_check[2] and 'رحيم' in b_check[3]:
                return ' '.join(w[4:])
    return t

def clean_arabic(text):
    """
    Strips harakat, tatweel, quranic annotation marks and normalizes alif variants.
    """
    text = text.replace('\u0670', 'ا')  # dagger alif -> alif
    text = text.replace('ـ', '')        # tatweel
    text = re.sub(r'[\u064B-\u065F\u06D6-\u06ED\*\_\`\s۝০-৯0-9]', '', text)
    text = re.sub(r'[ٱآإأءؤئ]', 'ا', text)
    text = text.replace('ة', 'ه').replace('ى', 'ي')
    return text

def clean_arabic_for_matching(text):
    """
    Normalizes Arabic text for token-level dictionary matching.
    """
    text = text.replace('\u0670', 'ا')
    text = text.replace('ـ', '')
    text = re.sub(r'[\u064B-\u065F\u06D6-\u06ED\*\_\`«»"\'\(\)\[\]\{\}]', '', text)
    text = re.sub(r'[ٱآإأءؤئ]', 'ا', text)
    text = text.replace('ة', 'ه').replace('ى', 'ي')
    return text.strip()

def arabic_token_match(word_clean, ayah_tokens):
    """
    Robust word-level token matcher that prevents false-positive substring matches
    by testing against tokens and stripping standard Arabic grammatical prefixes.
    """
    if not word_clean:
        return False
    w_clean = re.sub(r'\s+', '', word_clean)
    if not w_clean:
        return False
    
    # 1. Exact token match
    if w_clean in ayah_tokens:
        return True

    # 2. Prefix stripping (و, ف, ب, ل, ال, وال, فال, بال, لل)
    prefixes = ['ال', 'و', 'ف', 'ب', 'ل', 'وال', 'فال', 'بال', 'لل', 'كال', 'فل']
    for tok in ayah_tokens:
        if tok == w_clean:
            return True
        for p in prefixes:
            if tok.startswith(p) and tok[len(p):] == w_clean:
                return True
            if w_clean.startswith(p) and w_clean[len(p):] == tok:
                return True
    return False

def normalize_quran_brackets(text: str) -> str:
    """
    Standardizes Quranic ayah quotes to authentic ornate brackets:
    Opening on right: \ufd3f (﴿)
    Closing on left: \ufd3e (﴾)
    Replaces reversed ornate brackets: \ufd3e...\ufd3f (﴾...﴿) -> \ufd3f...\ufd3e (﴿...﴾)
    Ensures brackets and Arabic verses stay beautifully paired.
    """
    if not text or not isinstance(text, str):
        return text

    # Convert reversed \ufd3e...\ufd3f -> \ufd3f...\ufd3e when enclosing Arabic characters
    return re.sub(
        r'\uFD3E([^\uFD3E\uFD3F\r\n]*?[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF][^\uFD3E\uFD3F\r\n]*?)\uFD3F',
        r'﴿\g<1>﴾',
        text
    )

def replace_backtick_arabic(text: str) -> str:
    """
    Replaces backticks surrounding Arabic text with guillemets «...»
    so it renders in beautiful Amiri Quran RTL font instead of monospace LTR code.
    """
    if not text or not isinstance(text, str):
        return text

    def repl(m):
        inner = m.group(1)
        # Check if inner contains Arabic characters and no Latin letters / English words
        if re.search(r'[\u0600-\u06FF]', inner) and not re.search(r'[A-Za-z]', inner):
            return f"«{inner.strip()}»"
        return m.group(0)

    return re.sub(r'`([^`\n]+)`', repl, text)

def rewrite_markdown_links(text: str, surah_id: int) -> str:
    """
    Rewrites local relative markdown file links:
    - [রুকু ০১ ➡️](./রুকু-০১_আয়াত_১-১০.md) -> [রুকু ০১ ➡️](#/{surah_id}/ruku-1)
    - [🏠 সূরা পরিচিতি](./00_সূরা-পরিচিতি.md) -> [🏠 সূরা পরিচিতি](#/{surah_id})
    - [সূচিপত্র](00_সূরা-পরিচিতি.md) -> [সূচিপত্র](#/{surah_id})
    """
    if not text or not isinstance(text, str):
        return text

    def replace_link(m):
        link_text = m.group(1)
        target = m.group(2)
        if "00_সূরা-পরিচিতি.md" in target:
            return f"[{link_text}](#/{surah_id})"
        m_ruku = re.search(r'রুকু[-_]([০-৯\d]+)', target)
        if m_ruku:
            r_num = int(to_en(m_ruku.group(1)))
            return f"[{link_text}](#/{surah_id}/ruku-{r_num})"
        if target.endswith('.md'):
            return f"[{link_text}](#/{surah_id})"
        return m.group(0)

    return re.sub(r'\[([^\]]+)\]\(([^)]+\.md)\)', replace_link, text)

def load_tanzil(base_dir=None):
    b = base_dir or BASE_DIR
    tanzil_file = b / "00_প্রজেক্ট_তথ্য" / "quran-uthmani.txt"
    tanzil = {}
    if not tanzil_file.exists():
        raise FileNotFoundError(f"Tanzil file missing at {tanzil_file}")
    with open(tanzil_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) >= 3:
                s_id, a_id = int(parts[0]), int(parts[1])
                tanzil[(s_id, a_id)] = strip_basmala(parts[2], s_id, a_id)
    return tanzil

def load_ruku_map(base_dir=None):
    b = base_dir or BASE_DIR
    p = b / "00_প্রজেক্ট_তথ্য" / "ruku_map.json"
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)["surahs"]

def load_audit_results(base_dir=None):
    b = base_dir or BASE_DIR
    p = b / "00_প্রজেক্ট_তথ্য" / "audit_results.json"
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def load_author_meta(base_dir=None):
    b = base_dir or BASE_DIR
    p = b / "00_প্রজেক্ট_তথ্য" / "author_metadata.json"
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

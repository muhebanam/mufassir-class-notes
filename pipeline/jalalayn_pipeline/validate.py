"""নির্ধারণবাদী (deterministic) যাচাই: ফরম্যাট, উৎস-সাবস্ট্রিং, [src:…] আইডি, সংখ্যা, কুরআন-রেফ, রচয়িতা, কিরাআত-নাম।

LLM-এর আউটপুট এই স্তর পার না হলে ফাইলে যায় না; ত্রুটি-তালিকা সহ এজেন্টকে পুনরায় পাঠানো হয়।
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .arabic import skeleton, to_bn, to_en

BLOCK_RE = re.compile(r"<!--\s*BLOCK:([^\s>]+)\s*-->")
PART_RE = re.compile(r"<!--\s*PART:([A-Z0-9_]+?)_START\s*-->(.*?)<!--\s*PART:\1_END\s*-->", re.S)
SRC_RE = re.compile(r"\[src:([^\]\s]+)\]")
QREF_RE = re.compile(r"\[(Q\d+)\]")
QUOTE_RES = [re.compile(r"﴿([^﴾]+)﴾"), re.compile(r"«([^»]+)»"), re.compile(r"“([^”]+)”")]
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
ARABIC_BACKTICK_RE = re.compile(r"`[^`\n]*[\u0600-\u06FF][^`\n]*`")
FORBIDDEN = [
    r"\(আয়াত\s*[\d০-৯]+-এর প্রামাণ্য বঙ্গানুবাদ\)",
    r"কুরআনিক শব্দরূপ ও আভিধানিক অর্থ",
    r"এই রুকুর আয়াতসমূহের মৌলিক বাক্যগঠন সুস্পষ্ট",
    r"সারসংক্ষেপ পাঠ ও তাফসীর",
]
NUM_PATTERNS = [
    re.compile(r"(?:নং|নম্বর|رقم)\s*[:\-]?\s*\**\s*(\d+)"),
    re.compile(r"(?:পৃ\.|পৃষ্ঠা|ص\.?)\s*(\d+)"),
    re.compile(r"খণ্ড\s*(\d+)"),
    re.compile(r"\((\d+)/(\d+)\)"),
]
AHKAM_HEADER = ["মাসআলা", "হানাফী", "মালিকী", "শাফিঈ", "হাম্বলী", "প্রধান দলীল ও প্রামাণ্য উৎস"]
UNVERIFIED = "যাচাইসাপেক্ষ"


@dataclass
class VCtx:
    sid: int
    ayat_text: dict                      # {ayah: Tanzil text}
    quran: object
    corpus_sk: list                      # উৎস + পূর্ববর্তী আউটপুটের কঙ্কাল-তালিকা
    allowed_ids: set
    id_roles: dict
    source_numbers: set
    qids_by_ayah: dict                   # {ayah: {Q1,..}}
    author: dict
    strict_numbers: bool = True
    min_quote_letters: int = 6
    reader_names: list = field(default_factory=list)


# ---------- পার্সিং ----------

def strip_fences(t: str) -> str:
    t = t.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else ""
        if t.rstrip().endswith("```"):
            t = t.rstrip()[:-3]
    return t.strip()


def parse_output(text: str, keys: list, parts: list):
    errors = []
    text = strip_fences(text)
    pieces = BLOCK_RE.split(text)
    if pieces[0].strip():
        errors.append("প্রথম BLOCK মার্কারের আগে অতিরিক্ত লেখা আছে — শুধু নির্ধারিত ব্লক দিন")
    blocks: dict = {}
    for i in range(1, len(pieces), 2):
        key, body = pieces[i], pieces[i + 1]
        if key in blocks:
            errors.append(f"BLOCK:{key} দুইবার আছে")
        found = {}
        for m in PART_RE.finditer(body):
            found[m.group(1)] = m.group(2).strip()
        if PART_RE.sub("", body).strip():
            errors.append(f"BLOCK:{key}: PART-এর বাইরে লেখা আছে")
        blocks[key] = found
    for k in keys:
        if k not in blocks:
            errors.append(f"BLOCK:{k} নেই")
    for k in blocks:
        if k not in keys:
            errors.append(f"অপ্রত্যাশিত BLOCK:{k} (প্রত্যাশিত: {', '.join(keys)})")
    for k, found in blocks.items():
        if k not in keys:
            continue
        for p in parts:
            if p not in found:
                errors.append(f"BLOCK:{k}: PART {p} নেই")
        for p in found:
            if p not in parts:
                errors.append(f"BLOCK:{k}: অপ্রত্যাশিত PART {p}")
    return blocks, errors


def serialize(blocks: dict) -> str:
    out = []
    for k, parts in blocks.items():
        out.append(f"<!-- BLOCK:{k} -->")
        for p, body in parts.items():
            out.append(f"<!-- PART:{p}_START -->\n{body}\n<!-- PART:{p}_END -->")
    return "\n".join(out) + "\n"


# ---------- সাধারণ চেক ----------

def _fragments(q: str):
    return [f for f in re.split(r"…|\.\.\.|\s\.\s", q) if f.strip()]


def check_quotes(text: str, v: VCtx) -> list:
    errs = []
    joined = "|".join(v.corpus_sk)
    for rx in QUOTE_RES:
        for m in rx.finditer(text):
            for frag in _fragments(m.group(1)):
                sk = skeleton(frag)
                if len(sk) < v.min_quote_letters:
                    continue
                if sk in joined or v.quran.contains(sk):
                    continue
                errs.append(f"উদ্ধৃতি উৎসে/কুরআনে মেলেনি: «{frag.strip()[:50]}…» — প্রদত্ত SRC-তে নেই, তাই লিখবেন না")
    return errs


def check_src_tags(text: str, v: VCtx) -> list:
    errs = []
    for m in SRC_RE.finditer(text):
        if m.group(1) not in v.allowed_ids:
            errs.append(f"অবৈধ উৎস-আইডি [src:{m.group(1)}] — অনুমোদিত: {sorted(v.allowed_ids)[:12]}")
    return errs


def check_numbers(text: str, v: VCtx) -> list:
    if not v.strict_numbers:
        return []
    errs = []
    t = to_en(text)
    for rx in NUM_PATTERNS:
        for m in rx.finditer(t):
            ctx = t[max(0, m.start() - 70): m.end() + 70]
            for n in m.groups():
                if n and n not in v.source_numbers and UNVERIFIED not in ctx:
                    errs.append(f"উৎসে নেই এমন সূত্র-সংখ্যা '{n}' ('{m.group(0)}') — সরান অথবা পাশে '{UNVERIFIED}' লিখুন")
    return errs


def check_quran_refs(text: str, v: VCtx) -> list:
    errs = []
    t = to_en(text)
    for m in re.finditer(r"﴿([^﴾]+)﴾[^\n]{0,60}?(\d+)\s*:\s*(\d+)", t):
        s, a = int(m.group(2)), int(m.group(3))
        if not v.quran.has(s, a):
            errs.append(f"কুরআন-রেফ {s}:{a} বিদ্যমান নয়")
            continue
        vsk = v.quran.verse_skeleton(s, a)
        for frag in _fragments(m.group(1)):
            sk = skeleton(frag)
            if len(sk) >= v.min_quote_letters and sk not in vsk:
                errs.append(f"﴿{frag.strip()[:40]}…﴾ আয়াত {s}:{a}-এ নেই — রেফ ভুল")
    return errs


def check_common(body: str, v: VCtx, allow_ayah_placeholder=False) -> list:
    errs = []
    if ARABIC_BACKTICK_RE.search(body):
        errs.append("আরবি শব্দ ব্যাকটিকে (`…`) আছে — সরান")
    if EMAIL_RE.search(body):
        errs.append("ইমেইল-সদৃশ লেখা আছে")
    for pat in FORBIDDEN:
        if re.search(pat, body):
            errs.append(f"নিষিদ্ধ/জেনেরিক বাক্য: /{pat}/")
    ph = re.findall(r"\{\{[^}]*\}\}", body)
    for p in ph:
        if not (allow_ayah_placeholder and p == "{{AYAH_TEXT}}"):
            errs.append(f"অপূর্ণ প্লেসহোল্ডার {p}")
    for ln in body.splitlines():
        if re.search(r"<br\s*/?>", ln) and not ln.lstrip().startswith("|"):
            errs.append("<br> শুধু টেবিল-সেলে চলবে")
            break
    errs += check_quotes(body, v)
    errs += check_src_tags(body, v)
    errs += check_numbers(body, v)
    errs += check_quran_refs(body, v)
    return errs


def table_rows(body: str) -> list:
    return [l.strip() for l in body.splitlines() if l.strip().startswith("|")]


def cells(row: str) -> list:
    return [c.strip() for c in row.strip().strip("|").split("|")]


def first_lines(body: str, n=1):
    return [l for l in body.splitlines() if l.strip()][:n]


def check_jalalayn_author(body: str, v: VCtx) -> list:
    a = v.author
    errs = []
    if not any(x in body for x in a["must"]):
        errs.append(f"জালালাইনের রচয়িতা হিসেবে {a['name_bn']} উল্লেখ করুন (এই সূরায় অন্য রচয়িতা নয়)")
    for x in a["must_not"]:
        if x in body:
            errs.append(f"ভুল রচয়িতা-নাম '{x}' — এই সূরায় জালালাইন {a['name_bn']}-এর")
    return errs


# ---------- স্কিলভিত্তিক ----------

def validate_task(skill: str, blocks: dict, v: VCtx, keys: list) -> list:
    errs: list = []
    fn = {
        "ayah-translation-jalalayn": _v_trans_jal,
        "ayah-lughah-irab": _v_lughah_irab,
        "ayah-qiraat-note": _v_qiraat,
        "tafsir-hadith-unit": _v_tafsir,
        "ruku-makasid-connections": _v_makasid,
        "ruku-ikhtilaf-ahkam": _v_ahkam,
        "ruku-ulum-balaghat": _v_nonempty,
        "ruku-samakalin-dars": _v_nonempty,
        "ruku-limitations": _v_nonempty,
    }[skill]
    for k in keys:
        if k in blocks:
            errs += [f"[BLOCK:{k}] {e}" for e in fn(k, blocks[k], v)]
    errs += _collisions(blocks)
    return errs


BOILERPLATE_PATTERNS = [
    r"এই রুকুর আয়াতসমূহের মৌলিক বাক্যগঠন সুস্পষ্ট",
    r"\(আয়াত \d+-এর প্রামাণ্য বঙ্গানুবাদ\)",
]

def _collisions(blocks: dict) -> list:
    errs, seen = [], {}
    for k, parts in blocks.items():
        for p in ("IRAB", "JALALAYN", "COMPARATIVE_TAFSIR", "SHANE_NUZUL_HADITH", "QIRAAT_IMPACT"):
            body = parts.get(p)
            if not body or body.strip().upper() == "NONE":
                continue
            for bp in BOILERPLATE_PATTERNS:
                if re.search(bp, body):
                    errs.append(f"{p}: অর্থহীন টেমপ্লেট বয়লারপ্লেট শনাক্ত হয়েছে — সুনির্দিষ্ট প্রামাণ্য একাডেমিক বিশ্লেষণ দিন")
            core = "\n".join(body.splitlines()[1:]).strip()
            if len(core) > 40 and (p, core) in seen:
                errs.append(f"{p}: BLOCK:{k} ও BLOCK:{seen[(p, core)]}-এর বিষয়বস্তু হুবহু এক (ক্রস-আয়াত অনুলিপি)")
            seen[(p, core)] = k
    return errs


def _v_trans_jal(k, parts, v):
    errs = []
    a = int(k)
    bn = to_bn(a)
    row = parts["TRANSLATION_ROW"]
    rows = table_rows(row)
    if len(rows) != 1 or len([l for l in row.splitlines() if l.strip()]) != 1:
        errs.append("TRANSLATION_ROW এক লাইনের একটিই টেবিল-সারি হতে হবে")
    else:
        c = cells(rows[0])
        if len(c) != 4:
            errs.append(f"TRANSLATION_ROW-তে ৪টি সেল চাই, পেয়েছি {len(c)}")
        else:
            if bn not in c[0] and str(a) not in c[0]:
                errs.append(f"প্রথম সেলে আয়াত-নম্বর {bn} নেই")
            if c[1] != "{{AYAH_TEXT}}":
                errs.append("দ্বিতীয় সেলে হুবহু {{AYAH_TEXT}} লিখুন (আরবি পাঠ স্ক্রিপ্ট বসাবে)")
            if not c[2] or not c[3]:
                errs.append("শব্দানুগ/সাবলীল অনুবাদ ফাঁকা")
    errs += check_common(row, v, allow_ayah_placeholder=True)
    jal = parts["JALALAYN"]
    fl = first_lines(jal)
    if not fl or not fl[0].strip().startswith(f"- **আয়াত {bn}:**"):
        errs.append(f"JALALAYN শুরু হবে '- **আয়াত {bn}:**' দিয়ে")
    errs += check_jalalayn_author(jal, v)
    tags = SRC_RE.findall(jal)
    if not any(v.id_roles.get(t) == "jalalayn" for t in tags):
        errs.append("JALALAYN-এ জালালাইন-উৎসের (role=jalalayn) অন্তত একটি [src:ID] চাই")
    if "«" not in jal:
        errs.append("JALALAYN-এ মূল ইবারত «…» ব্লকে দিন")
    errs += check_common(jal, v)
    return errs


def _v_lughah_irab(k, parts, v):
    errs = []
    a = int(k)
    bn = to_bn(a)
    muf = parts["MUFRADAT_ROWS"].strip()
    if muf.upper() != "NONE":
        rows = table_rows(muf)
        if not rows:
            errs.append("MUFRADAT_ROWS-এ টেবিল-সারি নেই (শব্দ না থাকলে শুধু NONE)")
        ask = skeleton(v.ayat_text.get(a, ""))
        for r in rows:
            c = cells(r)
            if all(re.fullmatch(r"[:\-\s]*", x) for x in c):
                errs.append("হেডার/সেপারেটর সারি দেবেন না, শুধু ডেটা সারি")
                continue
            if len(c) != 8:
                errs.append(f"মুফরাদাত সারিতে ৮টি সেল চাই, পেয়েছি {len(c)}")
                continue
            w = skeleton(c[0].replace("*", ""))
            if not w or w not in ask:
                errs.append(f"শব্দ '{c[0]}' এই আয়াতে নেই")
            for idx in (5, 6):
                for n in re.findall(r"\d+", to_en(c[idx])):
                    if n not in v.source_numbers and UNVERIFIED not in c[idx]:
                        errs.append(f"গণনা '{n}' (কলাম {idx + 1}) উৎস/bahouth ক্যাপচারে নেই — '{UNVERIFIED}' লিখুন")
        errs += check_common(muf, v)
    irab = parts["IRAB"]
    fl = first_lines(irab)
    if not fl or not fl[0].strip().startswith(f"### আয়াত {bn}:"):
        errs.append(f"IRAB শুরু হবে '### আয়াত {bn}:' দিয়ে")
    if len([l for l in irab.splitlines() if l.strip()]) < 3:
        errs.append("IRAB খুব সংক্ষিপ্ত (জেনেরিক ভরাট নয়, প্রকৃত ই'রাব দিন)")
    errs += check_common(irab, v)
    return errs


def _v_qiraat(k, parts, v):
    errs = []
    a = int(k)
    bn = to_bn(a)
    body = parts["QIRAAT_IMPACT"]
    fl = first_lines(body)
    if not fl or not fl[0].strip().startswith(f"### আয়াত {bn}"):
        errs.append(f"QIRAAT_IMPACT শুরু হবে '### আয়াত {bn}' দিয়ে")
    refs = set(QREF_RE.findall(body))
    allowed = v.qids_by_ayah.get(a, set())
    if not allowed:
        if refs:
            errs.append(f"এই আয়াতে কোনো কিরাআত পাঠভেদ নেই, তাই [Q#] রেফ প্রযোজ্য নয়")
    else:
        if not refs:
            errs.append("কমপক্ষে একটি [Q#] সারি-রেফ চাই (যেমন [Q3])")
        for r in refs:
            if r not in allowed:
                errs.append(f"[{r}] এই আয়াতের কিরাআত-সারিতে নেই (বৈধ: {sorted(allowed)})")
    low = body
    for name in v.reader_names:
        if name and name in low:
            errs.append(f"মন্তব্যে ক্বারী-নাম '{name}' নিষিদ্ধ — [Q#] দিয়ে সারি নির্দেশ করুন (নাম সারণিতে স্ক্রিপ্ট দেখায়)")
            break
    errs += check_common(body, v)
    return errs


def _v_tafsir(k, parts, v):
    errs = []
    ct = parts["COMPARATIVE_TAFSIR"]
    fl = first_lines(ct)
    if not fl or not fl[0].strip().startswith("#### আয়াত"):
        errs.append("COMPARATIVE_TAFSIR শুরু হবে '#### আয়াত …' দিয়ে")
    if not SRC_RE.search(ct):
        errs.append("COMPARATIVE_TAFSIR-এ অন্তত একটি [src:ID] চাই")
    errs += check_common(ct, v)
    sn = parts["SHANE_NUZUL_HADITH"].strip()
    if sn.upper() != "NONE":
        fl = first_lines(sn)
        if not fl or not fl[0].strip().startswith("### আয়াত"):
            errs.append("SHANE_NUZUL_HADITH শুরু হবে '### আয়াত …' দিয়ে (বা শুধু NONE)")
        if not SRC_RE.search(sn):
            errs.append("SHANE_NUZUL_HADITH-এ [src:ID] চাই — উৎসে না থাকলে NONE লিখুন")
        errs += check_common(sn, v)
    return errs


def _v_makasid(k, parts, v):
    errs = []
    s0 = parts["SEC0_MAKASID"]
    fl = first_lines(s0)
    if not fl or re.match(r"^\s*(#|-|\*|>|\||\d+[.)])", fl[0]):
        errs.append("SEC0_MAKASID-এর প্রথম অনুচ্ছেদ সাধারণ গদ্য হবে (হেডিং/তালিকা/বোল্ড দিয়ে শুরু নয়)")
    else:
        para = s0.split("\n\n")[0]
        if len(para) > 700:
            errs.append("প্রথম অনুচ্ছেদ ২–৩ বাক্যে (≤৭০০ অক্ষর) রাখুন")
    errs += check_common(s0, v)
    s12 = parts["SEC12_CONNECTIONS"]
    if not table_rows(s12) and not s12.strip().startswith("প্রযোজ্য নয়"):
        errs.append("SEC12_CONNECTIONS-এ টেবিল অথবা 'প্রযোজ্য নয় — কারণ' চাই")
    errs += check_common(s12, v)
    return errs


def _v_ahkam(k, parts, v):
    errs = []
    s7 = parts["SEC7_IKHTILAF"]
    if len(s7.strip()) < 20:
        errs.append("SEC7_IKHTILAF খুব ছোট (মতভেদ না থাকলে 'প্রযোজ্য নয় — কারণ' লিখুন)")
    errs += check_common(s7, v)
    s8 = parts["SEC8_AHKAM"]
    rows = table_rows(s8)
    if not rows:
        if not s8.strip().startswith("প্রযোজ্য নয়"):
            errs.append("SEC8_AHKAM-এ ৬-কলাম টেবিল অথবা 'প্রযোজ্য নয় — কারণ' চাই")
    else:
        # একটিই টেবিল: সারিগুলো পরপর হতে হবে
        lines = s8.splitlines()
        idxs = [i for i, l in enumerate(lines) if l.strip().startswith("|")]
        if idxs != list(range(idxs[0], idxs[-1] + 1)):
            errs.append("SEC8_AHKAM-এ একটির বেশি টেবিল/বিচ্ছিন্ন সারি আছে")
        hdr = cells(rows[0])
        if hdr != AHKAM_HEADER:
            errs.append(f"টেবিল-হেডার হুবহু হবে: {' | '.join(AHKAM_HEADER)}")
        for r in rows[2:]:
            c = cells(r)
            if len(c) != 6:
                errs.append(f"সারিতে ৬টি সেল চাই, পেয়েছি {len(c)}: {c[0][:30]}")
                continue
            if "<br>" not in c[5] or "উৎস:" not in c[5]:
                errs.append(f"শেষ কলামে '<br>উৎস: …' চাই: {c[0][:30]}")
    errs += check_common(s8, v)
    return errs


def _v_nonempty(k, parts, v):
    errs = []
    for p, body in parts.items():
        if len(body.strip()) < 20:
            errs.append(f"{p} খুব ছোট/ফাঁকা")
        errs += check_common(body, v)
    return errs

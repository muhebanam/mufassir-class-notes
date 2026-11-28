"""চূড়ান্ত অডিট (মার্জ করা .md-এর ওপর) + audit_results.json লেখা + মানবিক অনুমোদন (approve)।

স্ট্যাটাস: needs_work → digital_verified (সব যান্ত্রিক চেক পাস) → gold (শুধু `jp approve`-এর পর, ফাইল অপরিবর্তিত থাকলে)।
"""
from __future__ import annotations

import re

from .arabic import skeleton, to_bn, to_en
from .project import Project
from .quran import jalalayn_author
from .sources import QIRAAT_NA, load_sources, qiraat_rows_for, render_qiraat_table, verify_hashes, capture_text
from .util import now_iso, read_json, sha256_text, write_json
from .validate import (ARABIC_BACKTICK_RE, EMAIL_RE, FORBIDDEN, SRC_RE, VCtx, check_numbers, check_quotes,
                       check_quran_refs, cells, table_rows)

SEC_RE = re.compile(r"(?m)^##\s+([০-৯0-9]+)\.\s+(.*)$")
MOCK_MARK = "[MOCK-OUTPUT]"


def split_sections(md: str) -> dict:
    ms = list(SEC_RE.finditer(md))
    out = {}
    for i, m in enumerate(ms):
        n = int(to_en(m.group(1)))
        end = ms[i + 1].start() if i + 1 < len(ms) else len(md)
        out.setdefault(n, "")
        out[n] += md[m.end():end].strip()
    return out, [int(to_en(m.group(1))) for m in ms]


def audit_ruku(proj: Project, sid: int, rid: int) -> dict:
    errors, warnings = [], []
    path = proj.ruku_md_path(sid, rid)
    res = {"status": "needs_work", "errors": errors, "warnings": warnings, "checked_at": now_iso(), "pipeline": "jp-audit/1"}
    if not path.exists():
        errors.append(f"ফাইল নেই: {path.name}")
        return res
    md = path.read_text(encoding="utf-8")
    res["md_sha256"] = sha256_text(md)
    a0, a1 = proj.ruku_range(sid, rid)
    ayat = list(range(a0, a1 + 1))
    q = proj.quran

    secs, order = split_sections(md)
    if order != list(range(16)):
        errors.append(f"HEADINGS: অধ্যায় ক্রম ০–১৫ হতে হবে, পেয়েছি {order}")
    caps = load_sources(proj, sid, rid)
    errors += [f"SOURCE_HASH: {e}" for e in verify_hashes(caps)]
    for cid, c in caps.items():
        if c["kind"] == "turath_page":
            if proj.cfg.is_blocked_book(c["book_id"]):
                errors.append(f"BLOCKED_ID: {c['book_id']} ({cid})")
            elif str(c["book_id"]) not in proj.cfg.books.get("allowed", {}):
                errors.append(f"UNKNOWN_ID: {c['book_id']} ({cid})")
    for bid in proj.cfg.books.get("blocked", []):
        if re.search(rf"(?<!\d){bid}(?!\d)", md):
            errors.append(f"BLOCKED_ID: নিষিদ্ধ আইডি {bid} ফাইলে আছে")

    # আয়াত হুবহু (Tanzil) + স্বাধীন bahouth ক্রস-চেক
    rows = [cells(r) for r in table_rows(secs.get(1, ""))][2:]
    got = {}
    for c in rows:
        if len(c) >= 2:
            m = re.search(r"\d+", to_en(c[0]))
            if m:
                got[int(m.group())] = c[1]
    if sorted(got) != ayat:
        errors.append(f"AYAH_COUNT: অধ্যায় ১-এ আয়াত {sorted(got)}, প্রত্যাশিত {ayat[0]}–{ayat[-1]}")
    for a in ayat:
        if a in got and got[a] != q.verse(sid, a):
            errors.append(f"AYAH_EXACT: আয়াত {a} Tanzil-এর সাথে হুবহু নয়")
        if a == 1 and sid not in (1, 9) and skeleton(got.get(a, "")).startswith("بسمللهلرحمنلرحيم") and len(skeleton(got.get(a, ""))) > 18:
            errors.append("BASMALA: আয়াত ১-এ বিসমিল্লাহ ঢুকে আছে")
    bv = caps.get("bah-v")
    if bv:
        bmap = {v["ayah"]: v["text_raw"] for v in bv.get("verses", [])}
        for a in ayat:
            if a in bmap and skeleton(bmap[a]) != skeleton(q.verse(sid, a)):
                errors.append(f"BAHOUTH_VS_TANZIL: আয়াত {a} — বাহাউথ ও Tanzil-এর কঙ্কাল ভিন্ন")
    else:
        warnings.append("bahouth_verses ক্যাপচার নেই — আয়াত-পাঠের স্বাধীন (Tanzil-বহির্ভূত) যাচাই হয়নি")

    # কিরাআত সারণি = স্ক্রিপ্ট-জেনারেটেড
    expected = render_qiraat_table(qiraat_rows_for(caps)) if caps else QIRAAT_NA
    if expected not in secs.get(4, ""):
        errors.append("QIRAAT_TABLE: অধ্যায় ৪-এর সারণি ক্যাপচার থেকে জেনারেটেড সারণির সাথে মেলে না (হাতে বদল?)")

    # সূত্র-আইডি, উদ্ধৃতি, সংখ্যা, কুরআন-রেফ
    all_ids = set(SRC_RE.findall(md))
    for i in sorted(all_ids - set(caps)):
        errors.append(f"SRC_ID: [src:{i}] ক্যাপচারে নেই")
    nums = set()
    texts = []
    for c in caps.values():
        t = capture_text(c)
        texts.append(t)
        nums.update(re.findall(r"\d+", to_en(t)))
        for fld in (c.get("page_id"), c.get("internal_page"), c.get("book_id"),
                    c.get("page"), c.get("volume"), c.get("hadith_number"),
                    c.get("fatwa_id"), c.get("topic_id")):
            if fld is not None:
                nums.update(re.findall(r"\d+", to_en(str(fld))))
    v = VCtx(sid=sid, ayat_text={a: q.verse(sid, a) for a in ayat}, quran=q, corpus_sk=[skeleton(t) for t in texts],
             allowed_ids=set(caps), id_roles={}, source_numbers=nums | {str(a) for a in ayat}, qids_by_ayah={},
             author=jalalayn_author(sid), strict_numbers=proj.cfg.validation["strict_numbers"],
             min_quote_letters=proj.cfg.validation["min_quote_letters"],
             a0=min(ayat), a1=max(ayat))
    for n in (0, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15):
        body = secs.get(n, "")
        errors += [f"QUOTE(§{n}): {e}" for e in check_quotes(body, v)]
        if n != 14:  # গ্রন্থপঞ্জিতে পৃষ্ঠা-আইডি স্ক্রিপ্ট-বসানো
            errors += [f"NUMBER(§{n}): {e}" for e in check_numbers(body, v)]
        errors += [f"QURAN_REF(§{n}): {e}" for e in check_quran_refs(body, v)]
    for n, body in secs.items():
        if ARABIC_BACKTICK_RE.search(body):
            errors.append(f"BACKTICK_ARABIC(§{n})")
    if EMAIL_RE.search(md):
        errors.append("EMAIL: ইমেইল-সদৃশ লেখা আছে")
    for pat in FORBIDDEN:
        if re.search(pat, md):
            errors.append(f"FORBIDDEN_TEXT: /{pat}/")
    if MOCK_MARK in md:
        errors.append("MOCK: মক-আউটপুটের চিহ্ন আছে")

    # জালালাইন রচয়িতা (শুধু জালালাইন-উপঅংশে)
    m = re.search(r"###\s*খ\.[^\n]*\n([\s\S]*)$", secs.get(5, ""))
    jtxt = m.group(0) if m else ""
    a = v.author
    if not any(x in jtxt for x in a["must"]):
        errors.append(f"JALALAYN_AUTHOR: {a['name_bn']} উল্লেখ নেই")
    for x in a["must_not"]:
        if x in jtxt:
            errors.append(f"JALALAYN_AUTHOR: ভুল নাম '{x}'")

    prev = (read_json(proj.cfg.audit_path, {}) or {}).get("rukus", {}).get(proj.audit_key(sid, rid), {})
    res["status"] = "needs_work" if errors else "digital_verified"
    if (not errors and prev.get("approved_by") and prev.get("approved_md_sha256") == res["md_sha256"]):
        res.update(status="gold", approved_by=prev["approved_by"], approved_at=prev.get("approved_at"),
                   approved_md_sha256=prev["approved_md_sha256"])
    save_result(proj, sid, rid, res)
    return res


def save_result(proj: Project, sid: int, rid: int, res: dict) -> None:
    d = read_json(proj.cfg.audit_path, {}) or {}
    d.setdefault("rukus", {})
    d["rukus"][proj.audit_key(sid, rid)] = res
    write_json(proj.cfg.audit_path, d)


def approve(proj: Project, sid: int, rid: int, by: str) -> dict:
    res = audit_ruku(proj, sid, rid)
    if res["status"] == "needs_work":
        raise SystemExit("অনুমোদন সম্ভব নয়: অডিট ব্যর্থ — আগে ত্রুটি সারান:\n  " + "\n  ".join(res["errors"][:10]))
    res.update(status="gold", approved_by=by, approved_at=now_iso(), approved_md_sha256=res["md_sha256"])
    save_result(proj, sid, rid, res)
    return res

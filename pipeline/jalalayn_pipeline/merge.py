"""LLM ছাড়া নিখুঁত একত্রীকরণ: সব PART → ১৬-অধ্যায়ের রুকু .md; আরবি আয়াত, কিরাআত-সারণি ও গ্রন্থপঞ্জি স্ক্রিপ্ট-জেনারেটেড।"""
from __future__ import annotations

import re

from .arabic import to_bn
from .project import Project
from .quran import jalalayn_author
from .sources import load_sources, qiraat_rows_for, render_qiraat_table, QIRAAT_NA
from .tasks import load_tasks
from .util import write_atomic
from .validate import SRC_RE, parse_output

TITLES = {
    0: "ভূমিকা, মাকাসিদ ও সিয়াক-সিবাক", 1: "মূল আয়াত ও প্রামাণ্য অনুবাদ", 2: "লুগাভী, সরফী ও মুফরাদাতুল কুরআন",
    3: "ই'রাব ও নাহবী বিশ্লেষণ", 4: "১০ মুতাওয়াতির কিরাআত ও তাফসীরে প্রভাব", 5: "তাফসীর আল-জালালাইন ও তুলনামূলক তাফসীর",
    6: "শানে নুযূল ও হাদীসের তাখরীজ", 7: "মুখাতাব, ইখতিলাফ ও তারজীহ", 8: "আহকাম ও চার মাযহাবের তুলনামূলক ফিকহ",
    9: "উলূমুল কুরআন ও উসূলুত তাফসীর", 10: "বালাগাত ও আল-কুরআনের ই'জায", 11: "সমকালীন প্রাসঙ্গিকতা ও সংশয় নিরসন",
    12: "আন্তঃআয়াত ও বিষয়ভিত্তিক সংযোগ", 13: "দরসের উপকরণ ও সমকালীন প্রয়োগ", 14: "প্রামাণ্য গ্রন্থপঞ্জি ও তথ্যসূত্র",
    15: "গবেষণাগত সীমাবদ্ধতা ও পদ্ধতিগত পর্যালোচনা",
}
NO_NUZUL = ("এই রুকুর আয়াতসমূহের জন্য সংগৃহীত উৎসে স্বতন্ত্র শানে নুযূল বা সংশ্লিষ্ট হাদীস পাওয়া যায়নি; "
            "এটি উৎস-সংগ্রহের সীমা, বর্ণনার অনুপস্থিতির প্রমাণ নয়।")
NO_MUFRADAT = "প্রযোজ্য নয় — এই রুকুর আয়াতে আলাদা মুফরাদাত-বিশ্লেষণযোগ্য শব্দ নির্বাচিত হয়নি।"


class MergeError(Exception):
    pass


def _load_blocks(proj, sid, rid, tasks):
    wd = proj.work_dir(sid, rid)
    data = {}
    for t in tasks:
        if t.status != "done":
            raise MergeError(f"টাস্ক সম্পন্ন নয়: {t.id} ({t.status}) {t.error[:100]}")
        if t.provider == "mock":
            raise MergeError(f"টাস্ক {t.id} মক-প্রোভাইডারের আউটপুট — আসল ফাইলে মার্জ নিষিদ্ধ")
        blocks, errs = parse_output((wd / t.output).read_text(encoding="utf-8"), t.keys, t.parts)
        if errs:
            raise MergeError(f"{t.id}: সংরক্ষিত আউটপুট অবৈধ: {errs[:2]}")
        data[t.id] = blocks
    return data


def _bibliography(proj, caps, used_ids) -> str:
    groups = {"jalalayn": [], "tafsir": [], "hadith": [], "qiraat": [], "fiqh": [], "other": []}
    for cid in sorted(used_ids):
        c = caps.get(cid)
        if not c:
            continue
        k = c.get("kind")
        if k == "turath_page":
            b = proj.cfg.book(c["book_id"])
            role = b.get("role", "other")
            role = "jalalayn" if role == "sharh" else role
            death = f" (মৃ. {to_bn(b['death_hijri'])} হি.)" if b.get("death_hijri") else ""
            page = f"পৃষ্ঠা-আইডি {to_bn(c.get('page_id'))}" + (f", অভ্যন্তরীণ পৃ. {c['internal_page']}" if c.get("internal_page") else "")
            line = (f"- **{b.get('name_bn', 'বই ' + str(c['book_id']))}** — {b.get('author_bn') or 'লেখক যাচাইসাপেক্ষ'}{death}; "
                    f"Turath আইডি `{c['book_id']}`; {page}। [src:{cid}]")
            groups.get(role, groups["other"]).append(line)
        elif k == "shamela_page":
            role = c.get("role", "tafsir")
            role = "jalalayn" if role == "sharh" else role
            vol = f"খণ্ড {to_bn(c.get('volume'))}, " if c.get("volume") else ""
            page = f"পৃষ্ঠা {to_bn(c.get('page'))}" if c.get("page") else ""
            author = f" — {c.get('author')}" if c.get("author") else ""
            url_str = f" ({c.get('url')})" if c.get("url") else ""
            line = f"- **{c.get('book_title', 'শামেলা কিতাব')}**{author}; শামেলা আইডি `{c.get('book_id')}`; {vol}{page}{url_str}। [src:{cid}]"
            groups.get(role, groups["other"]).append(line)
        elif k == "hadith_mcp":
            line = f"- **হাদীস সংকলন ({c.get('collection')})** — হাদীস নম্বর {to_bn(c.get('hadith_number'))}; Hadith MCP। [src:{cid}]"
            groups["hadith"].append(line)
        elif k == "maher_hadith":
            line = f"- **শায়খ মাহির আল-ফাহল উলূমুল হাদীস লাইব্রেরি** — {c.get('title')}; Maher Al-Fahel MCP। [src:{cid}]"
            groups["hadith"].append(line)
        elif k == "tafsir_mcp":
            role = c.get("role", "tafsir")
            author = f" ({c.get('author')})" if c.get("author") else ""
            line = f"- **{c.get('source_name', 'মারকায তাফসীর')}**{author} — Tafsir Center MCP (`{c.get('subtype')}`)। [src:{cid}]"
            groups.get(role, groups["other"]).append(line)
        elif k == "quran_mcp":
            line = f"- **কুরআন ফাউন্ডেশন (Quran.com)** — সংস্করণ/সাবটাইপ: `{c.get('subtype')}`; Quran.com MCP। [src:{cid}]"
            groups["other"].append(line)
        elif k == "fiqh_fatwa":
            line = f"- **ফতোয়া ও মাসআলা ({c.get('source')})** — ফতোয়া আইডি `{c.get('fatwa_id')}`; IslamQA MCP। [src:{cid}]"
            groups["fiqh"].append(line)

    titles = [("jalalayn", "১. তাফসীরুল জালালাইন ও শরহ"), ("tafsir", "২. তুলনামূলক তাফসীর গ্রন্থাবলি"),
              ("hadith", "৩. হাদীস ও শানে নুযূল সংকলন"), ("qiraat", "৪. কিরাআত গ্রন্থাবলি"),
              ("fiqh", "৫. ফিকহ ও ফতোয়া গ্রন্থাবলি"), ("other", "৬. অন্যান্য ইসলামী গবেষণা উৎস")]
    out = []
    for key, title in titles:
        if groups[key]:
            out.append(f"### {title}\n" + "\n".join(groups[key]))
    out.append("### কুরআনিক পাঠ ও কিরাআত-তথ্য\n- আরবি আয়াত: Tanzil (quran-uthmani) — স্ক্রিপ্ট দ্বারা হুবহু বসানো।\n"
               "- কিরাআত-পাঠভেদ: বাহাউথ ডাটাবেজ — স্ক্রিপ্ট-জেনারেটেড সারণি।")
    return "\n\n".join(out)


def merge_ruku(proj: Project, sid: int, rid: int, allow_incomplete=False):
    tasks = load_tasks(proj, sid, rid)
    if not tasks:
        raise MergeError("টাস্ক পরিকল্পনা নেই — আগে `jp run` চালান")
    data = _load_blocks(proj, sid, rid, tasks)
    caps = load_sources(proj, sid, rid)
    s = proj.surah(sid)
    a0, a1 = proj.ruku_range(sid, rid)
    ayat = list(range(a0, a1 + 1))
    author = jalalayn_author(sid)

    def per_ayah(skill, part):
        out = {}
        for t in tasks:
            if t.skill == skill:
                for k, parts in data[t.id].items():
                    out[int(k)] = parts[part]
        return out

    def ruku_part(skill, part):
        for t in tasks:
            if t.skill == skill:
                return data[t.id]["RUKU"][part]
        raise MergeError(f"স্কিল {skill}-এর টাস্ক নেই")

    rows = per_ayah("ayah-translation-jalalayn", "TRANSLATION_ROW")
    jal = per_ayah("ayah-translation-jalalayn", "JALALAYN")
    muf = per_ayah("ayah-lughah-irab", "MUFRADAT_ROWS")
    irab = per_ayah("ayah-lughah-irab", "IRAB")
    qimp = per_ayah("ayah-qiraat-note", "QIRAAT_IMPACT")
    for a in ayat:
        for name, d in (("অনুবাদ/জালালাইন", rows), ("ই'রাব", irab)):
            if a not in d:
                raise MergeError(f"আয়াত {a}: {name} নেই")

    sec1_rows = [rows[a].replace("{{AYAH_TEXT}}", proj.quran.verse(sid, a)) for a in ayat]
    sec1 = "\n".join(["| আয়াত | মূল আরবি (Tanzil, হুবহু) | শব্দানুগ অনুবাদ | সাবলীল বঙ্গানুবাদ (লেখকের নিজস্ব) |",
                      "| :---: | :--- | :--- | :--- |"] + sec1_rows)
    muf_rows = [muf[a] for a in ayat if a in muf and muf[a].strip().upper() != "NONE"]
    sec2 = ("\n".join(["| শব্দ | মূলধাতু | সীগা / ওযন | আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র | কুরআনিক পরিভাষাগত অর্থ | "
                       "কুরআনে মূলধাতুর মোট প্রয়োগ | নির্দিষ্ট রূপ/শব্দের প্রয়োগ | মোট স্বতন্ত্র আয়াত |",
                       "| :--- | :---: | :--- | :--- | :--- | :---: | :--- | :--- |"] + muf_rows)) if muf_rows else NO_MUFRADAT
    sec3 = "\n\n---\n\n".join(irab[a] for a in ayat)

    qrows = qiraat_rows_for(caps)
    qtable = render_qiraat_table(qrows)
    if qrows:
        notes = "\n\n".join(qimp[a] for a in ayat if a in qimp)
        sec4 = f"### প্রামাণ্য ১০ মুতাওয়াতির কিরাআত সারণি (বাহাউথ সোর্স; স্ক্রিপ্ট-জেনারেটেড)\n\n{qtable}\n\n---\n\n### আয়াতভিত্তিক কিরাআতের তাফসীরী প্রভাব (লেখকের বিশ্লেষণ)\n\n{notes}"
    else:
        sec4 = QIRAAT_NA

    comp = [d["COMPARATIVE_TAFSIR"] for t in tasks if t.skill == "tafsir-hadith-unit" for d in [data[t.id][t.keys[0]]]]
    nuz = [d["SHANE_NUZUL_HADITH"] for t in tasks if t.skill == "tafsir-hadith-unit" for d in [data[t.id][t.keys[0]]]
           if d["SHANE_NUZUL_HADITH"].strip().upper() != "NONE"]
    jal_blocks = "\n\n".join(jal[a] for a in ayat)
    sec5 = (f"### ক. তুলনামূলক তাফসীর (উৎস-ভিত্তিক; প্রতিটি উদ্ধৃতির পাশে উৎস-আইডি ট্যাগ)\n\n" + "\n\n".join(comp) +
            f"\n\n---\n\n### খ. তাফসীরুল জালালাইন — মূল ইবারত ও বঙ্গানুবাদ ({author['name_bn']})\n\n{jal_blocks}")
    sec6 = "\n\n---\n\n".join(nuz) if nuz else NO_NUZUL

    body = {
        0: ruku_part("ruku-makasid-connections", "SEC0_MAKASID"),
        1: sec1, 2: sec2, 3: sec3, 4: sec4, 5: sec5, 6: sec6,
        7: ruku_part("ruku-ikhtilaf-ahkam", "SEC7_IKHTILAF"),
        8: ruku_part("ruku-ikhtilaf-ahkam", "SEC8_AHKAM"),
        9: ruku_part("ruku-ulum-balaghat", "SEC9_ULUM"),
        10: ruku_part("ruku-ulum-balaghat", "SEC10_BALAGHAT"),
        11: ruku_part("ruku-samakalin-dars", "SEC11_SAMAKALIN"),
        12: ruku_part("ruku-makasid-connections", "SEC12_CONNECTIONS"),
        13: ruku_part("ruku-samakalin-dars", "SEC13_DARS"),
    }
    used = set()
    for k in (0, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13):
        used |= set(SRC_RE.findall(body[k]))
    body[14] = _bibliography(proj, caps, used)
    body[15] = (ruku_part("ruku-limitations", "SEC15_LIMITATIONS") +
                "\n- **মানবিক পর্যালোচনা বাকি:** ফিকহী/আকীদাগত তারজীহ, অনুবাদের মান ও মুদ্রিত সংস্করণের সাথে পৃষ্ঠা-মিলকরণ (স্তর ৩–৪)।")

    header = f"# সূরা {s.name_bn}" + (f" ({s.name_ar})" if s.name_ar else "") + f" — রুকু {to_bn(rid)} (আয়াত {to_bn(a0)}–{to_bn(a1)})"
    box = ("| স্তর | অবস্থা | বিবরণ |\n| :---: | :---: | :--- |\n"
           "| ১: Draft | সম্পন্ন | ১৬ অধ্যায় পাইপলাইনে সংকলিত |\n"
           "| ২: Digital Verified | `jp audit` দেখুন | উৎস-সাবস্ট্রিং, আয়াত-মিল, কিরাআত-সারণি, আইডি যাচাই (audit_results.json) |\n"
           "| ৩: Print Verified | `[ ]` | মুদ্রিত সংস্করণের সাথে মিলকরণ বাকি |\n"
           "| ৪: Scholarly Reviewed | `[ ]` | `jp approve` দ্বারা মানবিক অনুমোদনের পর |\n"
           "| ৫: Publication Ready | `[ ]` | — |")
    parts = [header, box] + [f"## {to_bn(n)}. {TITLES[n]}\n\n{body[n]}" for n in range(16)]
    md = "\n\n---\n\n".join(parts) + "\n"
    out = proj.ruku_md_path(sid, rid)
    write_atomic(out, md)
    write_atomic(proj.qiraat_table_file(sid, rid), qtable + "\n")
    return out

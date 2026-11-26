"""টাস্কের প্রম্পট ও যাচাই-প্রেক্ষাপট (VCtx) তৈরি।"""
from __future__ import annotations

import json
import re

from .arabic import skeleton, to_bn, to_en
from .project import Project
from .quran import jalalayn_author
from .sources import capture_text, covers, qiraat_rows_for, render_source, roles
from .tasks import Task, safe_name
from .util import sha256_text
from .validate import SRC_RE, VCtx, parse_output, serialize


def select_sources(proj: Project, sid: int, rid: int, task: Task, caps: dict) -> list:
    rl = roles(proj, caps)
    sk = task.skill
    a0, a1 = proj.ruku_range(sid, rid)
    ruku_range = range(a0, a1 + 1)
    picked = []
    for cid, c in sorted(caps.items()):
        b_roles = set(proj.cfg.roles_of(c.get("book_id"))) if c.get("kind") == "turath_page" else {rl.get(cid, "")}
        if "role" in c:
            b_roles.add(c["role"])
        kind = c.get("kind")
        if sk == "ayah-translation-jalalayn" and (b_roles & {"jalalayn", "sharh"} or kind == "quran_mcp") and covers(c, task.ayat):
            picked.append(c)
        elif sk == "ayah-lughah-irab" and (kind in ("bahouth_root", "quran_mcp") or b_roles & {"lughah", "irab", "morphology"}):
            picked.append(c)
        elif sk == "ayah-qiraat-note" and (b_roles & {"qiraat"} or kind in ("bahouth_qiraat", "tafsir_mcp")) and covers(c, task.ayat):
            picked.append(c)
        elif sk == "tafsir-hadith-unit" and (b_roles & {"tafsir", "jalalayn", "sharh", "hadith", "nuzul"} or kind in ("hadith_mcp", "maher_hadith", "tafsir_mcp", "shamela_page")) and covers(c, task.ayat):
            picked.append(c)
        elif sk == "ruku-makasid-connections" and (b_roles & {"makasid", "topics"} or kind == "bahouth_topics"):
            picked.append(c)
        elif sk == "ruku-ikhtilaf-ahkam" and (b_roles & {"fiqh", "fatwa"}) and covers(c, ruku_range):
            picked.append(c)
        elif sk == "ruku-ulum-balaghat" and (b_roles & {"ulum", "balaghat"}) and covers(c, ruku_range):
            picked.append(c)
        elif sk == "ruku-samakalin-dars" and (b_roles & {"contemporary", "fatwa"}) and covers(c, ruku_range):
            picked.append(c)
    return picked


def prior_text(proj: Project, sid: int, rid: int, task: Task, tasks: list) -> str:
    """উচ্চতর স্তরের টাস্কের জন্য নিম্নস্তরের সম্পন্ন আউটপুট।"""
    if task.level == 1:
        return ""
    chunks = []
    wd = proj.work_dir(sid, rid)
    for t in tasks:
        if t.level < task.level and t.status == "done" and t.output:
            p = wd / t.output
            if p.exists():
                chunks.append(f"### PRIOR OUTPUT — {t.id}\n{p.read_text(encoding='utf-8')}")
    return "\n\n".join(chunks)


def build(proj: Project, sid: int, rid: int, task: Task, caps: dict, tasks: list):
    cfg = proj.cfg
    s = proj.surah(sid)
    a0, a1 = proj.ruku_range(sid, rid)
    author = jalalayn_author(sid)
    srcs = select_sources(proj, sid, rid, task, caps)
    prior = prior_text(proj, sid, rid, task, tasks)
    qrows = [r for r in qiraat_rows_for(caps) if r["ayah"] in task.ayat] if task.skill == "ayah-qiraat-note" else []
    ayat_text = {a: proj.quran.verse(sid, a) for a in task.ayat}

    ctx = {
        "surah": {"id": sid, "name_bn": s.name_bn, "name_ar": s.name_ar},
        "ruku": {"id": rid, "ayah_start": a0, "ayah_end": a1},
        "task": {"id": task.id, "skill": task.skill, "ayat": task.ayat, "block_keys": task.keys, "parts": task.parts},
        "jalalayn_author": author["name_bn"],
        "ayat": [{"num": a, "num_bn": to_bn(a), "words": len(ayat_text[a].split()), "text_uthmani": ayat_text[a]} for a in task.ayat],
        "qiraat_rows": [{"qid": r["qid"], "ayah": r["ayah"], "word": r["word_cell"], "readers": r["readers"], "rule": r["rule"]} for r in qrows],
        "sources": [{"id": c["id"], "kind": c["kind"], "role": roles(proj, {c["id"]: c})[c["id"]],
                     "page_id": c.get("page_id"), "internal_page": c.get("internal_page"), "covers": c.get("covers_ayat")} for c in srcs],
    }
    ctx_json = json.dumps(ctx, ensure_ascii=False, indent=1)
    sources_block = "\n\n".join(render_source(proj, c) for c in srcs) or "(এই টাস্কে কোনো SRC নেই — নতুন কোনো আরবি উদ্ধৃতি বা সূত্র-সংখ্যা লিখবেন না)"
    contract = (f"আউটপুট চুক্তি (Strict Output Contract): BLOCK কী = {task.keys}; প্রতিটি BLOCK-এ ঠিক এই PART-গুলো = {task.parts}। "
                f"BLOCK মার্কার: <!-- BLOCK:কী -->; PART মার্কার: <!-- PART:নাম_START --> … <!-- PART:নাম_END -->।")
    user = (f"# আন্তর্জাতিক ইসলামী একাডেমিক তাহক্বীক টাস্ক (Smart Core 7)\n"
            f"স্কিল: {task.skill} | স্তর: Level {task.level}\n"
            f"সূরা {s.name_bn} ({sid}), রুকু {rid}, আয়াত {a0}–{a1}। এই টাস্কের আয়াত: {task.ayat}\n"
            f"{contract}\n\n"
            f"## CONTEXT_JSON\n```json\n{ctx_json}\n```\n\n## SOURCES (SHA-256 সিলকৃত প্রাথমিক ও মাল্টি-এমসিপি উৎস)\n{sources_block}\n")
    if prior:
        user += f"\n## PRIOR_OUTPUTS (পূর্ববর্তী স্তরের যাচাইকৃত একাডেমিক আউটপুট; এখান থেকে উদ্ধৃত করা যাবে)\n{prior}\n"
    if task.skill == "ruku-limitations":
        gaps_path = proj.work_dir(sid, rid) / "harvest_gaps.json"
        if gaps_path.exists():
            user += f"\n## HARVEST_GAPS (Tier 1 হারভেস্টে অনুপস্থিত উৎসের প্রকৃত তালিকা)\n{gaps_path.read_text(encoding='utf-8')}\n"
    user += "\nকঠোর নির্দেশ: কেবল নির্ধারিত BLOCK ও PART মার্কারের ভেতরে একাডেমিক আউটপুট দিন; বাইরে কোনো ভূমিকা, ব্যাখ্যা বা কোড-ফেন্স (```) নয়।"
    system = cfg.rules_text() + "\n\n---\n\n" + cfg.skill_text(task.skill)
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]

    corpus_texts = [capture_text(c) for c in srcs] + ([prior] if prior else [])
    nums = set()
    for c in srcs:
        for fld in (c.get("page_id"), c.get("internal_page"), c.get("book_id"),
                    c.get("page"), c.get("volume"), c.get("hadith_number"),
                    c.get("fatwa_id"), c.get("topic_id")):
            if fld is not None:
                nums.update(re.findall(r"\d+", to_en(str(fld))))
    for t in corpus_texts:
        nums.update(re.findall(r"\d+", to_en(t)))
    nums.update(re.findall(r"\d+", to_en(" ".join(f"{x['num']}" for x in ctx["ayat"]))))
    allowed = {c["id"] for c in srcs} | set(SRC_RE.findall(prior))
    qids = {}
    for r in qrows:
        qids.setdefault(r["ayah"], set()).add(r["qid"])
    v = VCtx(
        sid=sid, ayat_text=ayat_text, quran=proj.quran,
        corpus_sk=[skeleton(t) for t in corpus_texts],
        allowed_ids=allowed, id_roles=roles(proj, caps), source_numbers=nums,
        qids_by_ayah=qids, author=author,
        strict_numbers=cfg.validation["strict_numbers"], min_quote_letters=cfg.validation["min_quote_letters"],
        reader_names=cfg["reader_names"],
    )
    return messages, v, srcs


def readiness(proj: Project, sid: int, rid: int, task: Task, caps: dict, tasks: list):
    """(প্রস্তুত?, কারণ). উৎস/নির্ভরতা না থাকলে টাস্ক 'blocked' — কখনো উৎস ছাড়া লেখানো হবে না।"""
    rl = roles(proj, caps)
    if task.skill == "ayah-translation-jalalayn":
        for a in task.ayat:
            if not any((rl[c["id"]] in ("jalalayn", "sharh") or c.get("kind") == "quran_mcp") and covers(c, [a]) for c in caps.values()):
                return False, f"আয়াত {a}: জালালাইন (role=jalalayn) উৎস ক্যাপচার নেই"
    if task.skill == "tafsir-hadith-unit":
        if not any((rl[c["id"]] in ("tafsir", "hadith", "nuzul") or c.get("kind") in ("hadith_mcp", "maher_hadith", "tafsir_mcp", "shamela_page")) and covers(c, task.ayat) for c in caps.values()):
            return False, f"আয়াত {task.ayat}: তাফসীর (role=tafsir) উৎস ক্যাপচার নেই"
    if task.level > 1:
        pend = [t.id for t in tasks if t.level < task.level and t.status != "done"]
        if pend:
            return False, f"নির্ভরশীল টাস্ক সম্পন্ন নয়: {pend[:3]}{'…' if len(pend) > 3 else ''}"
    return True, ""

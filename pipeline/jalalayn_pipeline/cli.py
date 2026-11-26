"""কমান্ড-লাইন: python pipeline/jp.py <কমান্ড> …"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import audit as auditmod
from . import context as ctxmod
from .config import Config
from .llm import get_provider
from .merge import MergeError, merge_ruku
from .project import Project
from .quran import validate_map
from .runner import run_ruku
from .sources import ingest, load_sources, verify_hashes
from .tasks import load_tasks, plan, safe_name, save_tasks, tasks_file
from .util import read_json, sha256_text, write_atomic, write_json
from .validate import parse_output, serialize, validate_task


def _rukus(proj: Project, sid: int, ruku):
    n = len(proj.surah(sid).rukus)
    if ruku in (None, "all"):
        return list(range(1, n + 1))
    return [int(ruku)]


def _surahs(args):
    end = getattr(args, "to_surah", None) or args.surah
    return list(range(args.surah, end + 1))


def cmd_validate_map(proj, args):
    errs, info = validate_map(proj.quran, proj.ruku_map)
    for i in info:
        print("ℹ", i)
    for e in errs:
        print("✗", e)
    print("✓ মানচিত্র বৈধ" if not errs else f"✗ {len(errs)}টি ত্রুটি")
    return 1 if errs else 0


def cmd_status(proj, args):
    audit = (read_json(proj.cfg.audit_path, {}) or {}).get("rukus", {})
    sids = [args.surah] if args.surah else sorted(proj.ruku_map)
    tot = {"gold": 0, "digital_verified": 0, "needs_work": 0, "unaudited": 0}
    for sid in sids:
        s = proj.surah(sid)
        c = {"gold": 0, "digital_verified": 0, "needs_work": 0, "unaudited": 0}
        tinfo = []
        for rid in range(1, len(s.rukus) + 1):
            st = audit.get(proj.audit_key(sid, rid), {}).get("status", "unaudited")
            c[st] = c.get(st, 0) + 1
            tasks = load_tasks(proj, sid, rid)
            if tasks:
                tinfo.append(f"r{rid}:{sum(t.status == 'done' for t in tasks)}/{len(tasks)}")
        for k in c:
            tot[k] = tot.get(k, 0) + c[k]
        print(f"সূরা {sid:3d} {s.name_bn:<14} রুকু {len(s.rukus):2d} | gold {c['gold']} | digital {c['digital_verified']} | needs_work {c['needs_work']} | unaudited {c['unaudited']}"
              + (f" | টাস্ক {' '.join(tinfo[:6])}" if tinfo and args.surah else ""))
    print(f"\nমোট: {tot}")
    return 0


def cmd_harvest_plan(proj, args):
    books = proj.cfg.books.get("allowed", {})
    want = [b for b, v in books.items() if v.get("role") in ("jalalayn", "tafsir", "qiraat")]
    for sid in _surahs(args):
        for rid in _rukus(proj, sid, args.ruku):
            a0, a1 = proj.ruku_range(sid, rid)
            reqs = [{"kind": "bahouth_verses", "ayat": [a0, a1], "tool_hint": "bahouth:list_surah_verses"},
                    {"kind": "bahouth_qiraat", "ayat": [a0, a1], "tool_hint": "bahouth:list_verse_qiraat"},
                    {"kind": "bahouth_root", "note": "প্রতি নির্বাচিত শব্দের মূলধাতু: bahouth:find_root / list_root_verses",
                     "file": "JSON envelope, kind=bahouth_root"}]
            for a in range(a0, a1 + 1):
                for b in want:
                    reqs.append({"kind": "turath_page", "book_id": int(b), "book": books[b].get("name_bn"), "role": books[b]["role"],
                                 "ayah": f"{sid}:{a}", "save_as": f"turath_{b}_<page_id>_a{a}.txt",
                                 "note": "একাধিক আয়াত এক পৃষ্ঠায় থাকলে a<from>-<to> ব্যবহার করুন"})
            out = proj.work_dir(sid, rid) / "harvest_requests.json"
            write_json(out, {"surah": sid, "ruku": rid, "inbox_formats": "pipeline/docs/INBOX_FORMAT.md", "requests": reqs})
            print(f"✓ সূরা {sid} রুকু {rid}: {len(reqs)}টি অনুরোধ → {out}")
    return 0


def cmd_ingest(proj, args):
    done, issues = ingest(proj, args.surah, int(args.ruku), Path(args.inbox))
    print(f"✓ নিবন্ধিত: {len(done)}টি — {done}")
    for i in issues:
        print("⚠", i)
    return 1 if issues and not done else 0


def cmd_plan(proj, args):
    tasks = plan(proj, args.surah, int(args.ruku))
    save_tasks(proj, args.surah, int(args.ruku), tasks)
    for t in tasks:
        print(f"{t.level} {t.id:<55} {t.status}")
    print(f"মোট {len(tasks)}টি টাস্ক → {tasks_file(proj, args.surah, int(args.ruku))}")
    return 0


def cmd_run(proj, args):
    provider = None if args.dry_run else get_provider(proj.cfg, args.provider)
    only = set(args.only.split(",")) if args.only else None
    rc = 0
    for sid in _surahs(args):
        for rid in _rukus(proj, sid, args.ruku):
            print(f"\n▶ সূরা {sid} রুকু {rid}")
            s = run_ruku(proj, sid, rid, provider, only=only, force=args.force, dry_run=args.dry_run, concurrency=args.concurrency)
            print(f"  ফল: {s}")
            if s["failed"] or s["halted"]:
                rc = 2
            if s["halted"]:
                return rc
    return rc


def cmd_merge(proj, args):
    rc = 0
    for sid in _surahs(args):
        for rid in _rukus(proj, sid, args.ruku):
            try:
                p = merge_ruku(proj, sid, rid)
                print(f"✓ মার্জ: {p}")
            except MergeError as e:
                print(f"✗ সূরা {sid} রুকু {rid}: {e}")
                rc = 2
    return rc


def cmd_audit(proj, args):
    rc = 0
    for sid in _surahs(args):
        for rid in _rukus(proj, sid, args.ruku):
            r = auditmod.audit_ruku(proj, sid, rid)
            print(f"{'✓' if r['status'] != 'needs_work' else '✗'} সূরা {sid} রুকু {rid}: {r['status']}"
                  + (f" ({len(r['errors'])} ত্রুটি)" if r["errors"] else ""))
            for e in r["errors"][:15]:
                print("   -", e)
            for w in r["warnings"]:
                print("   ⚠", w)
            if r["status"] == "needs_work":
                rc = 2
    return rc


def cmd_approve(proj, args):
    r = auditmod.approve(proj, args.surah, int(args.ruku), args.by)
    print(f"✓ gold: সূরা {args.surah} রুকু {args.ruku} (অনুমোদন: {args.by})")
    return 0


def cmd_prepare_level(proj, args):
    sid, rid = args.surah, int(args.ruku)
    level = int(args.level)
    force = bool(getattr(args, "force", False))
    only = set(args.only.split(",")) if getattr(args, "only", None) else None

    tasks = plan(proj, sid, rid)
    save_tasks(proj, sid, rid, tasks)
    caps = load_sources(proj, sid, rid)
    herr = verify_hashes(caps)
    if herr:
        res = {"ok": False, "error": "উৎস-অখণ্ডতা ব্যর্থ:\n  " + "\n  ".join(herr)}
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 1

    wd = proj.work_dir(sid, rid)
    (wd / "prompts").mkdir(parents=True, exist_ok=True)
    (wd / "parts").mkdir(parents=True, exist_ok=True)

    level_tasks = [t for t in tasks if t.level == level and (not only or t.skill in only)]
    ready, skipped, blocked = [], [], []

    for t in level_tasks:
        ok, why = ctxmod.readiness(proj, sid, rid, t, caps, tasks)
        if not ok:
            t.status = "blocked"
            t.error = why
            blocked.append({"id": t.id, "skill": t.skill, "reason": why})
            continue

        messages, v, _srcs = ctxmod.build(proj, sid, rid, t, caps, tasks)
        h = sha256_text("\n".join(m["content"] for m in messages))
        out_rel = f"parts/{safe_name(t.id)}.md"

        if t.status == "done" and t.done_hash == h and (wd / out_rel).exists() and not force:
            skipped.append({"id": t.id, "skill": t.skill, "output": out_rel})
            continue

        prompt_file = wd / "prompts" / f"{safe_name(t.id)}.json"
        prompt_data = {
            "task_id": t.id,
            "skill": t.skill,
            "level": t.level,
            "ayat": t.ayat,
            "keys": t.keys,
            "parts": t.parts,
            "done_hash": h,
            "messages": messages,
            "system_prompt": messages[0]["content"],
            "user_prompt": messages[1]["content"],
        }
        write_json(prompt_file, prompt_data)
        ready.append({
            "id": t.id,
            "skill": t.skill,
            "level": t.level,
            "ayat": t.ayat,
            "keys": t.keys,
            "parts": t.parts,
            "prompt_file": str(prompt_file.resolve()),
            "done_hash": h,
        })

    save_tasks(proj, sid, rid, tasks)
    res = {
        "ok": True,
        "surah": sid,
        "ruku": rid,
        "level": level,
        "ready": ready,
        "skipped": skipped,
        "blocked": blocked,
    }
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


def cmd_submit_part(proj, args):
    sid, rid = args.surah, int(args.ruku)
    tid = args.task
    reply_file = Path(args.file)
    provider_name = getattr(args, "provider", None) or "agy-subagent"

    if not reply_file.exists():
        res = {"ok": False, "error": f"রিপ্লাই ফাইল পাওয়া যায়নি: {reply_file}"}
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 1

    reply = reply_file.read_text(encoding="utf-8")
    tasks = load_tasks(proj, sid, rid)
    target = None
    for t in tasks:
        if t.id == tid:
            target = t
            break
    if not target:
        res = {"ok": False, "error": f"টাস্ক পাওয়া যায়নি: {tid}"}
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 1

    caps = load_sources(proj, sid, rid)
    messages, v, _srcs = ctxmod.build(proj, sid, rid, target, caps, tasks)
    h = sha256_text("\n".join(m["content"] for m in messages))

    blocks, perrs = parse_output(reply, target.keys, target.parts)
    errs = perrs if perrs else validate_task(target.skill, blocks, v, target.keys)

    wd = proj.work_dir(sid, rid)
    out_rel = f"parts/{safe_name(target.id)}.md"

    if not errs:
        write_atomic(wd / out_rel, serialize(blocks))
        target.output = out_rel
        target.done_hash = h
        target.provider = provider_name
        target.status = "done"
        target.error = ""
        save_tasks(proj, sid, rid, tasks)
        res = {
            "ok": True,
            "task_id": target.id,
            "status": "done",
            "output": out_rel,
            "attempts": target.attempts,
        }
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    else:
        target.attempts += 1
        target.error = "; ".join(errs[:6])
        save_tasks(proj, sid, rid, tasks)
        res = {
            "ok": False,
            "task_id": target.id,
            "status": "failed",
            "attempts": target.attempts,
            "errors": errs,
        }
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 1


def cmd_go(proj, args):
    provider = get_provider(proj.cfg, args.provider)
    rc = 0
    for sid in _surahs(args):
        for rid in _rukus(proj, sid, args.ruku):
            print(f"\n▶ সূরা {sid} রুকু {rid}")
            s = run_ruku(proj, sid, rid, provider, force=args.force, concurrency=args.concurrency)
            print(f"  ফল: {s}")
            if s["halted"]:
                return 2
            if s["failed"] or s["blocked"]:
                print("  ⏭ মার্জ বাদ (ব্যর্থ/ব্লকড টাস্ক আছে) — `jp status`/tasks.json দেখুন")
                rc = 2
                continue
            try:
                merge_ruku(proj, sid, rid)
            except MergeError as e:
                print(f"  ✗ মার্জ: {e}")
                rc = 2
                continue
            r = auditmod.audit_ruku(proj, sid, rid)
            print(f"  অডিট: {r['status']} ({len(r['errors'])} ত্রুটি)")
            if r["status"] == "needs_work":
                rc = 2
    return rc


def build_parser():
    p = argparse.ArgumentParser(prog="jp", description="জালালাইন তাহকীক পাইপলাইন")
    p.add_argument("--base-dir", default=None, help="প্রজেক্ট-রুট (ডিফল্ট: pipeline/-এর অভিভাবক)")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name, fn, surah=True, ruku=True, extra=None, help=""):
        sp = sub.add_parser(name, help=help)
        if surah:
            sp.add_argument("--surah", type=int, required=(name not in ("status",)))
            sp.add_argument("--to-surah", type=int, default=None, help="পরিসর: --surah থেকে --to-surah পর্যন্ত")
        if ruku:
            sp.add_argument("--ruku", default="all", help="রুকু নম্বর বা all")
        if extra:
            extra(sp)
        sp.set_defaults(fn=fn)
        return sp

    add("validate-map", cmd_validate_map, surah=False, ruku=False, help="ruku_map.json বনাম Tanzil যাচাই")
    add("status", cmd_status, ruku=False, help="অগ্রগতি (সব সূরা বা --surah)")
    add("harvest-plan", cmd_harvest_plan, help="কোন উৎস-ক্যাপচার লাগবে তার তালিকা")
    add("ingest", cmd_ingest, extra=lambda s: s.add_argument("--inbox", required=True), help="inbox থেকে উৎস নিবন্ধন (sha256 সিল)")
    add("plan", cmd_plan, help="টাস্ক-পরিকল্পনা")

    def run_extra(s):
        s.add_argument("--only", default=None, help="কমা-বিভক্ত স্কিল-নাম")
        s.add_argument("--force", action="store_true")
        s.add_argument("--dry-run", action="store_true", help="API কল ছাড়া প্রম্পট লিখে রাখে")
        s.add_argument("--provider", default=None, help="litellm | mock")
        s.add_argument("--concurrency", type=int, default=None)

    add("run", cmd_run, extra=run_extra, help="এজেন্ট টাস্ক চালানো (রিজিউমযোগ্য)")
    add("merge", cmd_merge, help="PART → রুকু .md")
    add("audit", cmd_audit, help="অডিট + audit_results.json")
    add("approve", cmd_approve, extra=lambda s: s.add_argument("--by", required=True), help="মানবিক অনুমোদন → gold")

    def prep_extra(s):
        s.add_argument("--level", type=int, required=True, choices=[1, 2, 3], help="কাজের স্তর (1, 2, বা 3)")
        s.add_argument("--only", default=None, help="কমা-বিভক্ত স্কিল-নাম")
        s.add_argument("--force", action="store_true")
    add("prepare-level", cmd_prepare_level, extra=prep_extra, help="সাব-এজেন্টের জন্য নির্দিষ্ট স্তরের প্রম্পট তৈরি করে (JSON)")

    def submit_extra(s):
        s.add_argument("--task", required=True, help="টাস্ক আইডি")
        s.add_argument("--file", required=True, help="এজেন্টের আউটপুট ফাইলের পাথ")
        s.add_argument("--provider", default="agy-subagent", help="প্রোভাইডারের নাম")
    add("submit-part", cmd_submit_part, extra=submit_extra, help="সাব-এজেন্টের আউটপুট যাচাই করে parts/-এ সংরক্ষণ করে (validate.py)")

    def go_extra(s):
        s.add_argument("--force", action="store_true")
        s.add_argument("--provider", default=None)
        s.add_argument("--concurrency", type=int, default=None)

    add("go", cmd_go, extra=go_extra, help="run + merge + audit (এক সূরা/পরিসর)")
    return p


def main(argv=None):
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    args = build_parser().parse_args(argv)
    proj = Project(Config(base_dir=args.base_dir))
    if hasattr(args, "ruku") and args.ruku not in (None, "all") and getattr(args, "surah", None) is None:
        raise SystemExit("--ruku দিলে --surah দিন")
    return args.fn(proj, args)


if __name__ == "__main__":
    sys.exit(main())

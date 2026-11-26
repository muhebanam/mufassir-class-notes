"""টাস্ক-রানার: সমান্তরাল, রিজিউমযোগ্য, যাচাই-ব্যর্থ হলে ত্রুটি-তালিকাসহ পুনঃচেষ্টা, টানা ব্যর্থতায় হল্ট।"""
from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor

from . import context as ctxmod
from .project import Project
from .sources import load_sources, verify_hashes
from .tasks import Task, load_tasks, plan, safe_name, save_tasks
from .util import sha256_text, write_atomic
from .validate import parse_output, serialize, validate_task


def run_ruku(proj: Project, sid: int, rid: int, provider, *, only=None, force=False,
             dry_run=False, concurrency=None, log=print) -> dict:
    cfg = proj.cfg
    tasks = plan(proj, sid, rid)
    save_tasks(proj, sid, rid, tasks)
    caps = load_sources(proj, sid, rid)
    herr = verify_hashes(caps)
    if herr:
        raise SystemExit("উৎস-অখণ্ডতা ব্যর্থ:\n  " + "\n  ".join(herr))

    wd = proj.work_dir(sid, rid)
    (wd / "parts").mkdir(parents=True, exist_ok=True)
    if dry_run:
        (wd / "prompts").mkdir(parents=True, exist_ok=True)
    lock = threading.Lock()
    state = {"consec_fail": 0, "halt": False}
    summary = {"done": 0, "skipped": 0, "failed": 0, "blocked": 0, "dry": 0}
    max_attempts = cfg.run["max_attempts"]
    abort_after = cfg.run["abort_after_failed_tasks"]
    conc = concurrency or cfg.run["concurrency"]

    def finish(t: Task, status: str, err: str = ""):
        with lock:
            t.status, t.error = status, err
            save_tasks(proj, sid, rid, tasks)

    def execute(t: Task):
        if state["halt"]:
            return
        ok, why = ctxmod.readiness(proj, sid, rid, t, caps, tasks)
        if not ok:
            finish(t, "blocked", why)
            with lock:
                summary["blocked"] += 1
            log(f"  ⛔ {t.id}: blocked — {why}")
            return
        messages, v, _srcs = ctxmod.build(proj, sid, rid, t, caps, tasks)
        h = sha256_text("\n".join(m["content"] for m in messages))
        out_rel = f"parts/{safe_name(t.id)}.md"
        if (t.status == "done" and t.done_hash == h and (wd / out_rel).exists() and not force):
            with lock:
                summary["skipped"] += 1
            return
        if dry_run:
            write_atomic(wd / "prompts" / f"{safe_name(t.id)}.txt", "\n\n=====\n\n".join(m["content"] for m in messages))
            with lock:
                summary["dry"] += 1
            return
        err_text = ""
        for attempt in range(1, max_attempts + 1):
            t.attempts += 1
            try:
                reply = provider.complete(messages)
            except Exception as e:  # noqa: BLE001
                err_text = f"API ত্রুটি: {e}"
                continue
            blocks, perrs = parse_output(reply, t.keys, t.parts)
            errs = perrs if perrs else validate_task(t.skill, blocks, v, t.keys)
            if not errs:
                write_atomic(wd / out_rel, serialize(blocks))
                with lock:
                    t.output, t.done_hash, t.provider = out_rel, h, getattr(provider, "name", "?")
                    t.status, t.error = "done", ""
                    state["consec_fail"] = 0
                    summary["done"] += 1
                    save_tasks(proj, sid, rid, tasks)
                log(f"  ✓ {t.id} (চেষ্টা {attempt})")
                return
            err_text = "; ".join(errs[:6])
            fb = "\n".join(f"- {e}" for e in errs[:25])
            messages = messages + [
                {"role": "assistant", "content": reply},
                {"role": "user", "content": (
                    f"আন্তর্জাতিক একাডেমিক যান্ত্রিক যাচাইয়ে (validate.py) আপনার আউটপুটে নিচের ত্রুটিগুলো ধরা পড়েছে:\n{fb}\n\n"
                    f"দয়া করে প্রতিটি ত্রুটি নিখুঁতভাবে সংশোধন করে সম্পূর্ণ আউটপুট (সকল নির্ধারিত BLOCK/PART মার্কারসহ) পুনরায় প্রদান করুন। "
                    f"কোনো উদ্ধৃতি বা সূত্র-সংখ্যা প্রদত্ত SRC-র বাইরে থেকে দেবেন না, আরবি শব্দ ব্যাকটিকে রাখবেন না এবং বাইরে কোনো ভূমিকা বা কোড-ফেন্স দেবেন না।"
                )},
            ]
        finish(t, "failed", err_text)
        with lock:
            summary["failed"] += 1
            state["consec_fail"] += 1
            if state["consec_fail"] >= abort_after:
                state["halt"] = True
        log(f"  ✗ {t.id}: {max_attempts} চেষ্টায়ও ব্যর্থ — {err_text[:160]}")

    for level in (1, 2, 3):
        level_tasks = [t for t in tasks if t.level == level and (not only or t.skill in only)]
        if not level_tasks:
            continue
        log(f"স্তর {level}: {len(level_tasks)}টি টাস্ক")
        with ThreadPoolExecutor(max_workers=conc) as ex:
            list(ex.map(execute, level_tasks))
        if state["halt"]:
            log(f"⛔ টানা {abort_after}টি টাস্ক ব্যর্থ — ব্যাচ থামানো হলো (ত্রুটি দেখুন: {wd / 'tasks.json'})")
            break
    save_tasks(proj, sid, rid, tasks)
    summary["halted"] = state["halt"]
    return summary

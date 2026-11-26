"""Antigravity ডাইনামিক ওয়ার্কফ্লো স্ক্রিপ্ট: জালালাইন Smart Core 7 মাল্টি-এমসিপি হাইব্রিড পাইপলাইন।

এই স্ক্রিপ্টটি `run_workflow` টুলের মাধ্যমে আন্তর্জাতিক ইসলামী একাডেমিক মানদণ্ডে
৩ স্তরের সাব-এজেন্ট দলকে সমান্তরালে পরিচালনা করে:
- Tier 1: ৫ জন বিশেষায়িত Smart Core 7 হারভেস্টার সাব-এজেন্ট (Parallel MCP Fan-Out + SHA-256 Ingest)
- Tier 2: ৯টি স্কিলের জিরো-টুল একাডেমিক লেখক সাব-এজেন্ট (Levels 1 -> 2 -> 3 + Multi-turn validate.py সংশোধন লুপ)
- Tier 3: LLM-মুক্ত যান্ত্রিক মার্জ (Tanzil + Bahouth Qiraat + Multi-MCP অধ্যায় ১৪) ও অডিট গেট

Args schema:
{
  "surah": {"type": "integer", "description": "সূরা নম্বর (১-১১৪)"},
  "ruku": {"type": "integer", "description": "রুকু নম্বর"},
  "skip_harvest": {"type": "boolean", "default": false},
  "force": {"type": "boolean", "default": false},
  "model_tier": {"type": "string", "default": "inherit"}
}
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

args = globals().get("args", {})
surah_id = int(args.get("surah", 112))
ruku_id = int(args.get("ruku", 1))
skip_harvest = bool(args.get("skip_harvest", False))
force = bool(args.get("force", False))
model_tier = str(args.get("model_tier", "inherit"))

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR / "pipeline") not in sys.path:
    sys.path.insert(0, str(BASE_DIR / "pipeline"))

HARVEST_SCHEMA = {
    "type": "object",
    "properties": {
        "specialist_id": {"type": "string"},
        "saved_files": {"type": "array", "items": {"type": "string"}},
        "missing_sources": {"type": "array", "items": {"type": "string"}},
        "notes": {"type": "string"},
    },
    "required": ["specialist_id", "saved_files", "missing_sources"],
}

HARVESTER_SYSTEM_RULES = (
    "তুমি আন্তর্জাতিক ইসলামী তাহক্বীক মানদণ্ডের একজন কঠোর প্রাথমিক উৎস-সংগ্রাহক (Archival Verbatim Harvester)।\n"
    "কঠোর নীতিমালা:\n"
    "১. MCP থেকে প্রাপ্ত মূল আরবি ইবারত, হাদীস, সনদ, কিরাআত ও ফুটনোট হুবহু (verbatim) সংরক্ষণ করবে—কোনো সারসংক্ষেপ, অনুবাদ বা সম্পাদনা নয়।\n"
    "২. কেবল তোমার নির্ধারিত Smart Core 7 MCP সার্ভারগুলো ব্যবহার করবে এবং এক সার্ভারের আইডি অন্য সার্ভারে কপি করবে না।\n"
    "৩. খণ্ডিত সার্চ স্নিপেট দেখে থেমে যাবে না; অবশ্যই পূর্ণ পৃষ্ঠা/হাদীস (get_context / get_page / fetch_hadith) উদ্ধার করবে।\n"
    "৪. turath:get_context-এ সর্বদা internalPage দেবে (printedPage নয়), তবে JSON-এ মুদ্রিত খণ্ড/পৃষ্ঠা সংরক্ষণ করবে।\n"
    "৫. pipeline/harvester_helper.py-এর ফাংশন অথবা docs/INBOX_FORMAT.md-এর নির্ভুল JSON ফরম্যাটে inbox/ ফোল্ডারে সেভ করবে।\n"
    "৬. কোনো তথ্য না পেলে ফাঁকা বা মনগড়া ফাইল বানাবে না—বরং missing_sources[] তালিকায় স্বচ্ছভাবে জানাবে।"
)

HARVESTER_SPECIALISTS = [
    {
        "id": "harvester-quran-qiraat",
        "role": "T1: Quran, Roots, Topics & Qiraat Harvester",
        "servers": "bahouth, quran-mcp, tafsir-center, turath (29909, 5531)",
        "instructions": (
            "তোমার দায়িত্ব (অধ্যায় ১, ২, ৪ ও ১২-এর প্রাথমিক ডেটা):\n"
            "১. bahouth:list_surah_verses(surah_id) চালিয়ে রুকুর আয়াতসমূহ save_bahouth_verses()-এ সেভ করো (আগে না থাকলে)।\n"
            "২. প্রতিটি আয়াতের bahouth:list_verse_qiraat(verse_key) চালিয়ে save_bahouth_qiraat()-এ সেভ করো।\n"
            "৩. bahouth:list_verse_words(verse_key) থেকে মূল শব্দগুলোর root_token_raw নিয়ে bahouth:list_root_verses() চালিয়ে save_bahouth_root()-এ সেভ করো।\n"
            "৪. bahouth:list_verse_topics ও list_topic_verses চালিয়ে save_bahouth_topics()-এ সেভ করো।\n"
            "৫. tafsir-center:fetch_surah_info ও get_qeraat_variants এবং quran-mcp:fetch_quran/fetch_translation সেভ করো।\n"
            "৬. রুকুতে ফারশী কিরাআত-ভেদ থাকলে turath (29909, 5531) থেকে তাওজীহ পৃষ্ঠা save_turath_page()-এ সেভ করো।"
        ),
    },
    {
        "id": "harvester-jalalayn-tafsir",
        "role": "T1: Jalalayn & Comparative Tafsir Harvester",
        "servers": "turath (12876, 23842, 288, 7798, 8473, 20855, 23635, 22835, 9776, 22915, 639), shamela-qg, tafsir-center",
        "instructions": (
            "তোমার দায়িত্ব (অধ্যায় ০, ৫ক, ৫খ ও ৭-এর প্রাথমিক তাফসীর ডেটা):\n"
            "১. বাধ্যতামূলক: turath থেকে তাফসীরুল জালালাইন (12876) ও প্রয়োজনে শরহ (23842 খুদাইর, 288 বাররাক) এর পূর্ণ পৃষ্ঠা save_turath_page()-এ সেভ করো।\n"
            "২. বাধ্যতামূলক: turath থেকে তাবারী (7798), ইবনে কাসীর (8473), কুরতুবী (20855), ইবনে আশূর (9776), যুহাইলী (22915) এবং প্রাসঙ্গিক হলে রাযী (23635), আলূসী (22835), মাওসূ'আহ (639) এর পূর্ণ পৃষ্ঠা সেভ করো।\n"
            "৩. shamela-qg থেকে হাশিয়াতুস সাভী/আল-জামাল (role='sharh') এবং আল-কাশশাফ/আদ-দুররুল মানসূর (role='tafsir') save_shamela_page()-এ সেভ করো।\n"
            "৪. tafsir-center:fetch_tafsir থেকে প্রামাণ্য মুখতাসার ও বাগাবী/সা'দী save_tafsir_mcp()-এ সেভ করো।"
        ),
    },
    {
        "id": "harvester-hadith-nuzul",
        "role": "T1: Asbab al-Nuzul & Two-Tier Hadith Harvester",
        "servers": "tafsir-center, hadith-mcp, maher-alfahel, shamela-qg",
        "instructions": (
            "তোমার দায়িত্ব (অধ্যায় ৬-এর শানে নুযূল ও দ্বিস্তর হাদীস তাখরীজ ডেটা):\n"
            "১. প্রতিটি আয়াতের জন্য tafsir-center:fetch_nuzool_reason(surah, ayah) চালিয়ে save_tafsir_mcp(..., subtype='nuzul', role='nuzul')-এ সেভ করো।\n"
            "২. সংশ্লিষ্ট মারফূ' হাদীসগুলোর জন্য hadith-mcp:search_hadith -> fetch_hadith (পূর্ণ মতন, অধ্যায়, নম্বর, গ্রেড) ও fetch_cross_references (মুতাবা'আত/শওয়াহিদ) চালিয়ে save_hadith_mcp()-এ সেভ করো।\n"
            "৩. সনদ-তাহক্বীক ও মুহাদ্দিসদের হুকুমের জন্য maher-alfahel থেকে প্রামাণ্য নথি save_maher_hadith()-এ সেভ করো।\n"
            "৪. প্রাসঙ্গিক হলে shamela-qg থেকে ওয়াহিদীর আসবাবুন নুযূল বা সুয়ূতীর লুবাবুন নুকূল save_shamela_page(..., role='nuzul')-এ সেভ করো।"
        ),
    },
    {
        "id": "harvester-lughah-balaghat",
        "role": "T1: Lughah, Sarf, Irab & Balaghat Harvester",
        "servers": "tafsir-center, quran-mcp, shamela-qg, turath (9776)",
        "instructions": (
            "তোমার দায়িত্ব (অধ্যায় ২, ৩, ৯ ও ১০-এর ভাষাতাত্ত্বিক ও বালাগাতী ডেটা):\n"
            "১. প্রতিটি আয়াতের জন্য tafsir-center:analyze_word(surah, ayah) চালিয়ে save_tafsir_mcp(..., subtype='word_analysis', role='lughah')-এ সেভ করো।\n"
            "২. quran-mcp:analyze_morphology চালিয়ে save_quran_mcp(..., subtype='morphology', role='morphology')-এ সেভ করো।\n"
            "৩. জটিল শব্দ ও ই'রাবের জন্য shamela-qg থেকে মুফরাদাতুল কুরআন (রাগিব), আদ-দুররুল মাসূন (সামীন হালাবী) বা ই'রাবুল কুরআন (নাহহাস) save_shamela_page(..., role='lughah'/'irab')-এ সেভ করো।\n"
            "৪. বালাগাতের জন্য আল-কাশশাফ/ইবনে আশূরের বালাগাতী অংশ role='balaghat' হিসেবে সেভ করো।"
        ),
    },
    {
        "id": "harvester-fiqh-aqidah",
        "role": "T1: Four-Madhhab Fiqh & Aqidah Harvester",
        "servers": "turath (1464, 20855, 22915), shamela-qg",
        "instructions": (
            "তোমার দায়িত্ব (অধ্যায় ৭, ৮ ও ১১-এর তুলনামূলক ফিকহ, আকীদা ও সংশয় নিরসন ডেটা):\n"
            "১. রুকুতে ফিকহী আহকাম থাকলে turath থেকে ইবনুল আরাবীর আহকামুল কুরআন (1464) ও কুরতুবীর ফিকহী অংশ save_turath_page()-এ সেভ করো।\n"
            "২. shamela-qg থেকে চার মাযহাবের মূল গ্রন্থ (জাস্সাসের আহকামুল কুরআন, বাদায়িউস সানায়ি', আল-মুগনী, আল-মাওসূআতুল ফিকহিয়্যাহ) থেকে সংশ্লিষ্ট মাসআলার পূর্ণ পৃষ্ঠা save_shamela_page(..., role='fiqh')-এ সেভ করো।\n"
            "৩. আকীদাগত সূক্ষ্ম প্রশ্ন বা সংশয় নিরসনের জন্য শানকীতীর দাফ'উ ইয়হামিল ইযতিরাব বা প্রামাণ্য উৎস role='aqidah' হিসেবে সেভ করো।\n"
            "৪. রুকুতে কোনো ফিকহী বিধান না থাকলে তা স্পষ্টভাবে notes ও missing_sources-এ উল্লেখ করো।"
        ),
    },
]


def run_cmd(cmd_list: list[str]) -> tuple[int, str]:
    res = subprocess.run(cmd_list, cwd=str(BASE_DIR), capture_output=True, text=True, encoding="utf-8")
    out = res.stdout if res.stdout else res.stderr
    return res.returncode, out.strip()


async def run_harvester_specialist(spec: dict, inbox_dir: Path, hp_path: Path) -> dict:
    """Tier 1-এর একজন বিশেষায়িত হারভেস্টার সাব-এজেন্টকে সমান্তরালে চালানো।"""
    user_prompt = (
        f"# হারভেস্ট মিশন: {spec['id']}\n"
        f"সূরা: {surah_id} | রুকু: {ruku_id}\n"
        f"লক্ষ্য ইনবক্স ফোল্ডার: {inbox_dir}\n"
        f"হারভেস্ট প্ল্যান ফাইল: {hp_path}\n"
        f"তোমার অনুমোদিত MCP সার্ভারসমূহ: {spec['servers']}\n\n"
        f"## নির্ধারিত দায়িত্ব\n{spec['instructions']}\n\n"
        f"কাজ শেষে অবশ্যই JSON স্কিমা অনুযায়ী specialist_id, saved_files, missing_sources এবং notes রিটার্ন করো।"
    )
    log(f"  ▶ [{spec['id']}] তথ্য উদ্ধার শুরু হচ্ছে ({spec['servers']})")
    res = await agent(
        prompt=HARVESTER_SYSTEM_RULES + "\n\n---\n\n" + user_prompt,
        schema=HARVEST_SCHEMA,
        role=spec["role"],
        model=model_tier,
    )
    log(f"  ✓ [{spec['id']}] সম্পন্ন: {len(res.get('saved_files', []))} ফাইল সেভ, {len(res.get('missing_sources', []))} অনুপস্থিত")
    return res


async def execute_task_with_feedback(task_info: dict, max_attempts: int = 3) -> bool:
    """Tier 2-এর একটি একাডেমিক লেখক টাস্ককে সাব-এজেন্ট দিয়ে চালানো ও validate.py-তে অটো-সংশোধন।"""
    task_id = task_info["id"]
    skill_name = task_info["skill"]
    prompt_file = Path(task_info["prompt_file"])
    pdata = json.loads(prompt_file.read_text(encoding="utf-8"))

    system_prompt = pdata["system_prompt"]
    initial_user_prompt = pdata["user_prompt"]

    worker = agent(
        prompt=system_prompt,
        role=f"L{task_info['level']} Scholar ({skill_name}: {task_id})",
        model=model_tier,
    )

    current_prompt = initial_user_prompt
    for attempt in range(1, max_attempts + 1):
        log(f"  ▶ {task_id} (চেষ্টা {attempt}/{max_attempts})")
        reply = await worker(current_prompt, {"type": "string"})

        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as tf:
            tf.write(reply)
            temp_path = tf.name

        try:
            rc, out = run_cmd([
                sys.executable, "pipeline/jp.py", "submit-part",
                "--surah", str(surah_id),
                "--ruku", str(ruku_id),
                "--task", task_id,
                "--file", temp_path,
                "--provider", f"agy-subagent/{model_tier}",
            ])
            res_json = json.loads(out) if out.startswith("{") else {}
        finally:
            Path(temp_path).unlink(missing_ok=True)

        if rc == 0 and res_json.get("ok"):
            log(f"  ✓ {task_id}: একাডেমিক ও যান্ত্রিক যাচাই পাস ({res_json.get('output')})")
            del worker
            return True

        errors = res_json.get("errors", ["আউটপুট ভ্যালিডেশন ব্যর্থ"])
        err_msg = "\n".join(f"- {e}" for e in errors[:15])
        log(f"  ⚠ {task_id}: {len(errors)}টি ত্রুটি — সংশোধনের জন্য পুনরায় পাঠানো হচ্ছে")
        current_prompt = (
            f"আন্তর্জাতিক একাডেমিক যান্ত্রিক যাচাইয়ে (validate.py) আপনার পূর্ববর্তী আউটপুটে নিচের ত্রুটিগুলো ধরা পড়েছে:\n"
            f"{err_msg}\n\n"
            f"দয়া করে প্রতিটি ত্রুটি নিখুঁতভাবে সংশোধন করে সম্পূর্ণ আউটপুট (সকল নির্ধারিত BLOCK ও PART মার্কারসহ) পুনরায় প্রদান করুন।\n"
            f"মনে রাখবেন: কোনো উদ্ধৃতি বা সূত্র-সংখ্যা প্রদত্ত SRC-র বাইরে থেকে দেবেন না, আরবি শব্দ ব্যাকটিকে দেবেন না, "
            f"এবং ব্লকের বাইরে কোনো ভূমিকা বা কোড-ফেন্স (```) লিখবেন না।"
        )

    log(f"  ✗ {task_id}: {max_attempts} বার চেষ্টার পরও ব্যর্থ!")
    del worker
    return False


async def main():
    log("==========================================================")
    log(f"জালালাইন Smart Core 7 হাইব্রিড ওয়ার্কফ্লো — সূরা {surah_id}, রুকু {ruku_id}")
    log("==========================================================")

    # ----------------------------------------------------
    # ধাপ ১: Tier 1 — ৫-সদস্যের মাল্টি-এমসিপি হারভেস্ট ও SHA-256 সিলিং
    # ----------------------------------------------------
    phase("Tier 1: 5-Specialist Smart Core 7 Harvest & Ingest")
    work_dir = BASE_DIR / "_work" / f"s{surah_id:03d}" / f"r{ruku_id:02d}"
    inbox_dir = work_dir / "inbox"
    inbox_dir.mkdir(parents=True, exist_ok=True)

    rc, hp_out = run_cmd([
        sys.executable, "pipeline/jp.py", "harvest-plan",
        "--surah", str(surah_id),
        "--ruku", str(ruku_id),
    ])
    hp_path = work_dir / "harvest_requests.json"
    log(f"হারভেস্ট প্ল্যান প্রস্তুত: {hp_out.splitlines()[0] if hp_out else 'OK'}")

    # বিদ্যমান _sources ফোল্ডারে লেগেসি ফাইল থাকলে ইনবক্সে আনা
    try:
        from harvester_helper import prepare_inbox_from_existing
        from jalalayn_pipeline.project import Project
        from jalalayn_pipeline.config import Config
    except ImportError:
        from pipeline.harvester_helper import prepare_inbox_from_existing
        from pipeline.jalalayn_pipeline.project import Project
        from pipeline.jalalayn_pipeline.config import Config

    proj = Project(Config(base_dir=BASE_DIR))
    prep_res = prepare_inbox_from_existing(proj, surah_id, ruku_id, inbox_dir)
    if prep_res["copied_legacy_files"]:
        log(f"বিদ্যমান সোর্স ফাইল ইনবক্সে আনা হয়েছে: {prep_res['copied_legacy_files']}")

    if not skip_harvest:
        log("৫ জন বিশেষায়িত Smart Core 7 হারভেস্টার সাব-এজেন্ট সমান্তরালে চালু হচ্ছে...")
        harvest_reports = await parallel(
            HARVESTER_SPECIALISTS,
            lambda spec: run_harvester_specialist(spec, inbox_dir, hp_path),
        )
        gaps = {
            r["specialist_id"]: {
                "saved_files": r.get("saved_files", []),
                "missing_sources": r.get("missing_sources", []),
                "notes": r.get("notes", ""),
            }
            for r in harvest_reports
        }
        (work_dir / "harvest_gaps.json").write_text(
            json.dumps(gaps, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        log("হারভেস্ট রিপোর্ট সংরক্ষিত: harvest_gaps.json")
    else:
        log("skip_harvest=True — বিদ্যমান inbox/ ফাইলগুলো সরাসরি ইনজেস্ট করা হচ্ছে।")

    rc, out = run_cmd([
        sys.executable, "pipeline/jp.py", "ingest",
        "--surah", str(surah_id),
        "--ruku", str(ruku_id),
        "--inbox", str(inbox_dir),
    ])
    log(out)

    # ----------------------------------------------------
    # ধাপ ২–৪: Tier 2 — Levels 1, 2, 3 সমান্তরাল একাডেমিক ড্রাফটিং
    # ----------------------------------------------------
    level_titles = {
        1: "Tier 2 — Level 1: Ayah Batches & Tafsir-Hadith Units (Parallel)",
        2: "Tier 2 — Level 2: Maqasid, Ikhtilaf-Ahkam & Ulum-Balaghat (Parallel)",
        3: "Tier 2 — Level 3: Contemporary Dars & Methodological Limitations (Parallel)",
    }
    for lvl in (1, 2, 3):
        phase(level_titles[lvl])
        rc, out = run_cmd([
            sys.executable, "pipeline/jp.py", "prepare-level",
            "--surah", str(surah_id),
            "--ruku", str(ruku_id),
            "--level", str(lvl),
        ] + (["--force"] if force else []))
        lvl_res = json.loads(out)
        if not lvl_res.get("ok"):
            raise RuntimeError(f"Level {lvl} প্রস্তুতি ব্যর্থ: {lvl_res}")

        ready_tasks = lvl_res.get("ready", [])
        skipped_tasks = lvl_res.get("skipped", [])
        blocked_tasks = lvl_res.get("blocked", [])

        if skipped_tasks:
            log(f"Level {lvl}: {len(skipped_tasks)}টি টাস্ক ইতোমধ্যে সম্পন্ন (Skipped)")
        if blocked_tasks:
            log(f"Level {lvl}: {len(blocked_tasks)}টি টাস্ক ব্লকড (উৎস নেই): {[b['id'] for b in blocked_tasks]}")

        if ready_tasks:
            log(f"Level {lvl}: {len(ready_tasks)}টি বিশেষায়িত লেখক সাব-এজেন্ট সমান্তরালে চলছে...")
            results = await parallel(ready_tasks, execute_task_with_feedback)
            if not all(results):
                raise RuntimeError(f"Level {lvl}-এর এক বা একাধিক টাস্ক ব্যর্থ হয়েছে। ওয়ার্কফ্লো স্থগিত করা হলো।")

    # ----------------------------------------------------
    # ধাপ ৫: Tier 3 — LLM-মুক্ত যান্ত্রিক মার্জ ও অডিট গেট
    # ----------------------------------------------------
    phase("Tier 3: Zero-LLM Merge & Deterministic Audit Gate")
    log("চূড়ান্ত ১৬-অধ্যায়ের রুকু ফাইল একত্রীকরণ (Merge) চালানো হচ্ছে...")
    rc, merge_out = run_cmd([
        sys.executable, "pipeline/jp.py", "merge",
        "--surah", str(surah_id),
        "--ruku", str(ruku_id),
    ])
    log(merge_out)
    if rc != 0:
        raise RuntimeError(f"মার্জ ব্যর্থ: {merge_out}")

    log("কঠোর যান্ত্রিক অডিট (Audit) চালানো হচ্ছে...")
    rc, audit_out = run_cmd([
        sys.executable, "pipeline/jp.py", "audit",
        "--surah", str(surah_id),
        "--ruku", str(ruku_id),
    ])
    log(audit_out)
    log(f"সূরা {surah_id} রুকু {ruku_id} Smart Core 7 পাইপলাইন সফলভাবে সম্পন্ন হয়েছে!")


await main()

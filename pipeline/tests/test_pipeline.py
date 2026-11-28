"""সম্পূর্ণ পাইপলাইনের টেস্ট (মক LLM, কাল্পনিক সূরা ১১২ — আসল API/MCP লাগে না)।
চালান: python -m unittest discover -s pipeline/tests -v   (প্রজেক্ট-রুট থেকে)
"""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from jalalayn_pipeline import audit as auditmod  # noqa: E402
from jalalayn_pipeline.arabic import skeleton, strip_basmala  # noqa: E402
from jalalayn_pipeline.config import Config  # noqa: E402
from jalalayn_pipeline.llm import CallableProvider  # noqa: E402
from jalalayn_pipeline.merge import MergeError, merge_ruku  # noqa: E402
from jalalayn_pipeline.mock_llm import mock_fn  # noqa: E402
from jalalayn_pipeline.project import Project  # noqa: E402
from jalalayn_pipeline.quran import jalalayn_author, normalize_ruku_map, validate_map  # noqa: E402
from jalalayn_pipeline.runner import run_ruku  # noqa: E402
from jalalayn_pipeline.sources import ingest, load_sources  # noqa: E402
from jalalayn_pipeline.tasks import load_tasks, plan  # noqa: E402
from jalalayn_pipeline.util import read_json  # noqa: E402

TANZIL = (
    "112|1|بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ قُلْ هُوَ ٱللَّهُ أَحَدٌ\n"
    "112|2|ٱللَّهُ ٱلصَّمَدُ\n"
    "112|3|لَمْ يَلِدْ وَلَمْ يُولَدْ\n"
    "112|4|وَلَمْ يَكُن لَّهُۥ كُفُوًا أَحَدٌۢ\n"
)
JAL_TXT = "قل هو الله أحد أي الله واحد في ذاته وصفاته الله الصمد المقصود في الحوائج لم يلد ولم يولد وقوله ولم يكن له كفوا أحد ص 57"
TAB1 = "القول في تأويل قوله تعالى قل هو الله أحد يقول تعالى ذكره لنبيه محمد قل هو الله أحد الله الصمد وهو السيد الذي كمل في سؤدده"
TAB2 = "القول في تأويل قوله لم يلد ولم يولد يقول تعالى ذكره لم يكن له ولد ولم يكن له والد ولم يكن له كفوا أحد"
QMD = ("| আয়াত | শব্দ (ক্রম) | ক্বারী / রাবী (বাহাউথ) | কিরাআতের পাঠভেদ ও নিয়ম (অবিকৃত মূল পাঠ) |\n| :---: | :--- | :--- | :--- |\n"
       "| **1** | ﴿أَحَدٌ﴾ (4) | حفص | قرأ بكذا. |\n| **4** | ﴿كُفُوًا﴾ (4) | حمزة | قرأ بإسكان الفاء. |\n")


def make_project(tmp: Path, with_jalalayn=True, extra_inbox=None) -> tuple[Project, Path]:
    info = tmp / "00_প্রজেক্ট_তথ্য"
    info.mkdir(parents=True)
    (info / "quran-uthmani.txt").write_text(TANZIL, encoding="utf-8")
    (info / "ruku_map.json").write_text(json.dumps({"surahs": {"112": {
        "dir_name": "112_সূরা_আল-ইখলাস", "name_bn": "আল-ইখলাস", "name_ar": "الإخلاص", "ayah_count": 4, "rukus": [[1, 4]]}}}, ensure_ascii=False), encoding="utf-8")
    inbox = tmp / "inbox"
    inbox.mkdir()
    if with_jalalayn:
        (inbox / "turath_12876_100_a1-4.txt").write_text(JAL_TXT, encoding="utf-8")
    (inbox / "turath_7798_200_a1-2.txt").write_text(TAB1, encoding="utf-8")
    (inbox / "turath_7798_201_a3-4.txt").write_text(TAB2, encoding="utf-8")
    (inbox / "ruku_01_qiraat_table.md").write_text(QMD, encoding="utf-8")
    (inbox / "root_احد.json").write_text(json.dumps({"kind": "bahouth_root", "root": "احد", "text": "root احد total 85", "covers_ayat": "surah"}, ensure_ascii=False), encoding="utf-8")
    for name, txt in (extra_inbox or {}).items():
        (inbox / name).write_text(txt, encoding="utf-8")
    proj = Project(Config(base_dir=tmp))
    return proj, inbox


def provider(fn=mock_fn, name="test-llm"):
    return CallableProvider(fn, name)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def ready(self, **kw):
        proj, inbox = make_project(self.tmp, **kw)
        done, issues = ingest(proj, 112, 1, inbox)
        return proj, done, issues


class TestBasics(Base):
    def test_basmala_and_skeleton(self):
        t = "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ قُلْ هُوَ"
        self.assertEqual(strip_basmala(t, 112, 1), "قُلْ هُوَ")
        self.assertEqual(strip_basmala(t, 9, 1), t)
        self.assertEqual(skeleton("ٱلرَّحْمَـٰنِ"), skeleton("الرحمن"))
        self.assertEqual(skeleton("لِلنَّـٰسِ"), skeleton("للناس"))

    def test_author_rule(self):
        self.assertEqual(jalalayn_author(1)["key"], "mahalli")
        self.assertEqual(jalalayn_author(2)["key"], "suyuti")
        self.assertEqual(jalalayn_author(17)["key"], "suyuti")
        self.assertEqual(jalalayn_author(18)["key"], "mahalli")
        self.assertEqual(jalalayn_author(114)["key"], "mahalli")

    def test_map_normalization_and_validation(self):
        raw = {"surahs": {
            "5": {"dir_name": "a", "ayah_count": 10, "rukus": [[1, 4], [5, 10]]},
            "6": {"dir_name": "b", "total_ayahs": 6, "rukus": [{"ayah_start": 1, "ayah_end": 3}, {"ayah_start": 4, "ayah_end": 6}]},
            "7": {"dir_name": "c", "rukus": [{"ruku_number": 1, "ayah_start": 1, "ayah_end": 2, "file_name": "x"}, {"ruku_number": 2, "ayah_start": 4, "ayah_end": 5}]},
        }}
        m = normalize_ruku_map(raw)
        self.assertEqual(m[6].ayah_count, 6)
        errs, _ = validate_map(None, m)
        self.assertTrue(any("সূরা 7" in e and "প্রত্যাশিত 3" in e for e in errs))
        self.assertFalse(any("সূরা 5" in e or "সূরা 6" in e for e in errs))

    def test_validate_map_real_project_ok(self):
        proj, _ = make_project(self.tmp)
        errs, info = validate_map(proj.quran, proj.ruku_map)
        self.assertEqual(errs, [])


class TestIngest(Base):
    def test_ingest_ok(self):
        proj, done, issues = self.ready()
        self.assertEqual(issues, [])
        self.assertIn("t12876-p100", done)
        self.assertIn("bah-q", done)
        caps = load_sources(proj, 112, 1)
        self.assertEqual(len(caps["bah-q"]["rows"]), 2)
        self.assertTrue(all(c["sha256"] for c in caps.values()))

    def test_blocked_and_unknown_ids_rejected(self):
        proj, inbox = make_project(self.tmp, extra_inbox={
            "turath_21543_1_a1.txt": "نص خاطئ", "turath_99999_1_a1.txt": "نص مجهول"})
        done, issues = ingest(proj, 112, 1, inbox)
        self.assertTrue(any("নিষিদ্ধ" in i for i in issues))
        self.assertTrue(any("allowed তালিকায় নেই" in i for i in issues))
        self.assertNotIn("t21543-p1", done)
        self.assertNotIn("t99999-p1", done)

    def test_legacy_raw_json(self):
        proj, inbox = make_project(self.tmp)
        raw = {"schema_version": "2.0-raw-mcp",
               "bahouth_verses": [{"verse_key": "112-4", "ayah_number": 4, "text_raw": "ولم يكن له كفوا احد"}],
               "bahouth_qiraat": {"112-4": {"annotations": [{"word_order_in_verse": 5, "raw_text": "حمزة/قرأ بالإسكان@خلف/قرأ بالإسكان"}]}}}
        (inbox / "ruku_01_raw.json").write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
        ingest(proj, 112, 1, inbox)
        caps = load_sources(proj, 112, 1)
        self.assertIn("bah-v", caps)
        self.assertTrue(any(r["readers"] == "খলফ" or r["readers"] == "خلف" for r in caps["bah-q"]["rows"]))


class TestPipeline(Base):
    def full(self):
        proj, done, issues = self.ready()
        p = provider()
        s = run_ruku(proj, 112, 1, p, log=lambda *_: None)
        return proj, p, s

    def test_plan_shapes(self):
        proj, *_ = self.ready()
        tasks = plan(proj, 112, 1)
        skills = [t.skill for t in tasks]
        self.assertEqual(skills.count("tafsir-hadith-unit"), 2)
        self.assertEqual(skills.count("ayah-qiraat-note"), 2)  # আয়াত ১ ও ৪ (অ-পরপর) আলাদা ব্যাচ
        self.assertEqual(skills.count("ayah-translation-jalalayn"), 1)
        self.assertEqual(skills.count("ruku-limitations"), 1)

    def test_end_to_end_digital_verified(self):
        proj, p, s = self.full()
        self.assertEqual((s["failed"], s["blocked"], s["halted"]), (0, 0, False), s)
        out = merge_ruku(proj, 112, 1)
        md = out.read_text(encoding="utf-8")
        self.assertIn("قُلْ هُوَ ٱللَّهُ أَحَدٌ", md)          # স্ক্রিপ্ট-বসানো আয়াত (বিসমিল্লাহ ছাড়া)
        self.assertNotIn("{{AYAH_TEXT}}", md)
        res = auditmod.audit_ruku(proj, 112, 1)
        # মক-আউটপুটে চিহ্ন থাকায় অডিট ফেল হওয়াই সঠিক
        self.assertEqual(res["status"], "needs_work")
        self.assertTrue(any(e.startswith("MOCK") for e in res["errors"]))

    def test_resume_skips_done(self):
        proj, p, s = self.full()
        calls = p.calls
        s2 = run_ruku(proj, 112, 1, p, log=lambda *_: None)
        self.assertEqual(p.calls, calls)
        self.assertEqual(s2["done"], 0)
        self.assertGreater(s2["skipped"], 0)

    def test_force_reruns(self):
        proj, p, s = self.full()
        calls = p.calls
        run_ruku(proj, 112, 1, p, force=True, log=lambda *_: None)
        self.assertGreater(p.calls, calls)

    def test_mock_provider_blocks_merge(self):
        proj, done, _ = self.ready()
        run_ruku(proj, 112, 1, CallableProvider(mock_fn, "mock"), log=lambda *_: None)
        with self.assertRaises(MergeError):
            merge_ruku(proj, 112, 1)

    def test_blocked_without_jalalayn_source(self):
        proj, inbox = make_project(self.tmp, with_jalalayn=False)
        ingest(proj, 112, 1, inbox)
        p = provider()
        s = run_ruku(proj, 112, 1, p, log=lambda *_: None)
        tasks = {t.id: t for t in load_tasks(proj, 112, 1)}
        tj = [t for t in tasks.values() if t.skill == "ayah-translation-jalalayn"][0]
        self.assertEqual(tj.status, "blocked")
        self.assertGreater(s["blocked"], 0)
        # ব্লকড টাস্কে LLM কল হয়নি; নির্ভরশীল ruku-স্তরও ব্লকড
        lim = [t for t in tasks.values() if t.skill == "ruku-limitations"][0]
        self.assertEqual(lim.status, "blocked")
        with self.assertRaises(MergeError):
            merge_ruku(proj, 112, 1)

    def test_fabricated_quote_rejected_with_feedback(self):
        proj, done, _ = self.ready()
        seen = {"fb": 0}

        def bad(messages):
            user = messages[1]["content"]
            if '"skill": "ayah-translation-jalalayn"' in user:
                if len(messages) > 2 and "উদ্ধৃতি উৎসে/কুরআনে মেলেনি" in messages[-1]["content"]:
                    seen["fb"] += 1
                import re
                return re.sub(r"«[^»]+»", "«كلام مختلق لا وجود له في المصدر أبدا»", mock_fn(messages))
            return mock_fn(messages)

        p = provider(bad)
        s = run_ruku(proj, 112, 1, p, log=lambda *_: None)
        tj = [t for t in load_tasks(proj, 112, 1) if t.skill == "ayah-translation-jalalayn"][0]
        self.assertEqual(tj.status, "failed")
        self.assertEqual(tj.attempts, 3)
        self.assertGreaterEqual(seen["fb"], 1)           # ত্রুটি-তালিকা এজেন্টকে ফেরত গেছে
        self.assertGreater(s["failed"], 0)

    def test_halt_after_consecutive_failures(self):
        proj, done, _ = self.ready()
        proj.cfg.c["run"]["abort_after_failed_tasks"] = 2
        proj.cfg.c["run"]["concurrency"] = 1
        s = run_ruku(proj, 112, 1, provider(lambda m: "অর্থহীন আউটপুট"), log=lambda *_: None)
        self.assertTrue(s["halted"])


class TestAuditIntegrity(Base):
    def merged(self):
        proj, done, _ = self.ready()
        # মক নয়, কিন্তু মক-সদৃশ বৈধ আউটপুট: চিহ্ন বাদ দিয়ে
        def clean(messages):
            return mock_fn(messages).replace("[MOCK-OUTPUT]", "সংক্ষিপ্ত বিবরণ")
        run_ruku(proj, 112, 1, provider(clean), log=lambda *_: None)
        merge_ruku(proj, 112, 1)
        return proj

    def test_clean_run_is_digital_verified(self):
        proj = self.merged()
        res = auditmod.audit_ruku(proj, 112, 1)
        self.assertEqual(res["errors"], [], res["errors"])
        self.assertEqual(res["status"], "digital_verified")
        saved = read_json(proj.cfg.audit_path)
        self.assertEqual(saved["rukus"]["112_1"]["status"], "digital_verified")

    def test_detects_ayah_tamper(self):
        proj = self.merged()
        p = proj.ruku_md_path(112, 1)
        p.write_text(p.read_text(encoding="utf-8").replace("ٱللَّهُ ٱلصَّمَدُ", "ٱللَّهُ ٱلأَحَدُ", 1), encoding="utf-8")
        res = auditmod.audit_ruku(proj, 112, 1)
        self.assertTrue(any(e.startswith("AYAH_EXACT") for e in res["errors"]))

    def test_detects_qiraat_table_tamper(self):
        proj = self.merged()
        p = proj.ruku_md_path(112, 1)
        p.write_text(p.read_text(encoding="utf-8").replace("قرأ بإسكان الفاء.", "قرأ بشيء آخر."), encoding="utf-8")
        res = auditmod.audit_ruku(proj, 112, 1)
        self.assertTrue(any(e.startswith("QIRAAT_TABLE") for e in res["errors"]))

    def test_detects_source_tamper(self):
        proj = self.merged()
        f = proj.sources_file(112, 1)
        d = json.loads(f.read_text(encoding="utf-8"))
        for c in d["captures"]:
            if c["id"] == "t7798-p200":
                c["text"] += " إضافة"
        f.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        res = auditmod.audit_ruku(proj, 112, 1)
        self.assertTrue(any(e.startswith("SOURCE_HASH") for e in res["errors"]))

    def test_detects_fabricated_quote_in_final_md(self):
        proj = self.merged()
        p = proj.ruku_md_path(112, 1)
        p.write_text(p.read_text(encoding="utf-8") + "\n> «نص مختلق تماما ليس له أصل في أي مصدر» [src:t7798-p200]\n", encoding="utf-8")
        res = auditmod.audit_ruku(proj, 112, 1)
        self.assertTrue(any("QUOTE" in e for e in res["errors"]))

    def test_blocked_id_in_text(self):
        proj = self.merged()
        p = proj.ruku_md_path(112, 1)
        p.write_text(p.read_text(encoding="utf-8") + "\nতাবারী আইডি 21543\n", encoding="utf-8")
        res = auditmod.audit_ruku(proj, 112, 1)
        self.assertTrue(any(e.startswith("BLOCKED_ID") for e in res["errors"]))

    def test_wrong_jalalayn_author(self):
        proj = self.merged()
        p = proj.ruku_md_path(112, 1)
        p.write_text(p.read_text(encoding="utf-8").replace("মহাল্লী", "সুয়ূতী"), encoding="utf-8")
        res = auditmod.audit_ruku(proj, 112, 1)
        self.assertTrue(any(e.startswith("JALALAYN_AUTHOR") for e in res["errors"]))

    def test_approve_gold_and_revoked_on_change(self):
        proj = self.merged()
        res = auditmod.approve(proj, 112, 1, "মুফতী পরীক্ষক")
        self.assertEqual(res["status"], "gold")
        self.assertEqual(auditmod.audit_ruku(proj, 112, 1)["status"], "gold")   # অপরিবর্তিত থাকলে gold-ই
        p = proj.ruku_md_path(112, 1)
        p.write_text(p.read_text(encoding="utf-8") + "\nঅতিরিক্ত লাইন।\n", encoding="utf-8")
        self.assertEqual(auditmod.audit_ruku(proj, 112, 1)["status"], "digital_verified")  # বদলালে gold বাতিল

    def test_cannot_approve_failed(self):
        proj = self.merged()
        p = proj.ruku_md_path(112, 1)
        p.write_text(p.read_text(encoding="utf-8").replace("ٱللَّهُ ٱلصَّمَدُ", "x", 1), encoding="utf-8")
        with self.assertRaises(SystemExit):
            auditmod.approve(proj, 112, 1, "কেউ")


class TestMultiSurahAndCLI(Base):
    def test_suyuti_surah_and_range(self):
        """ভবিষ্যৎ-সম্প্রসারণ: সূরা ১৭ (সুয়ূতীর অংশ) ও একাধিক সূরা, একই পাইপলাইনে।"""
        proj, inbox = make_project(self.tmp)
        info = self.tmp / "00_প্রজেক্ট_তথ্য"
        (info / "quran-uthmani.txt").write_text(TANZIL + "17|1|بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ سُبْحَـٰنَ ٱلَّذِىٓ أَسْرَىٰ بِعَبْدِهِۦ\n17|2|وَءَاتَيْنَا مُوسَى ٱلْكِتَـٰبَ\n", encoding="utf-8")
        rm = json.loads((info / "ruku_map.json").read_text(encoding="utf-8"))
        rm["surahs"]["17"] = {"dir_name": "17_সূরা_আল-ইসরা", "name_bn": "আল-ইসরা", "name_ar": "الإسراء", "ayah_count": 2, "rukus": [[1, 2]]}
        (info / "ruku_map.json").write_text(json.dumps(rm, ensure_ascii=False), encoding="utf-8")
        proj = Project(Config(base_dir=self.tmp))
        ib2 = self.tmp / "inbox17"
        ib2.mkdir()
        (ib2 / "turath_12876_5_a1-2.txt").write_text("سبحان الذي أسرى بعبده ليلا من المسجد الحرام وآتينا موسى الكتاب ص 3", encoding="utf-8")
        (ib2 / "turath_7798_6_a1-2.txt").write_text("القول في تأويل قوله سبحان الذي أسرى بعبده ليلا يقول تعالى ذكره تنزيها لله", encoding="utf-8")
        ingest(proj, 17, 1, ib2)

        def clean(m):
            return mock_fn(m).replace("[MOCK-OUTPUT]", "সংক্ষিপ্ত বিবরণ")

        run_ruku(proj, 17, 1, provider(clean), log=lambda *_: None)
        merge_ruku(proj, 17, 1)
        res = auditmod.audit_ruku(proj, 17, 1)
        self.assertEqual(res["errors"], [], res["errors"])
        md = proj.ruku_md_path(17, 1).read_text(encoding="utf-8")
        jal = md.split("### খ.")[1].split("## ৬")[0]
        self.assertIn("সুয়ূতী", jal)
        self.assertNotIn("মহাল্লী", jal)
        self.assertNotIn("بِسْمِ", md.split("## ২")[0])          # বিসমিল্লাহ ছাঁটা

    def test_cli_flow(self):
        import subprocess
        proj, inbox = make_project(self.tmp)
        launcher = Path(__file__).resolve().parent.parent / "jp.py"

        def jp(*a):
            r = subprocess.run([sys.executable, str(launcher), "--base-dir", str(self.tmp), *a], capture_output=True, text=True, encoding="utf-8")
            return r.returncode, r.stdout + r.stderr

        rc, out = jp("validate-map")
        self.assertEqual(rc, 0, out)
        rc, out = jp("harvest-plan", "--surah", "112", "--ruku", "1")
        self.assertEqual(rc, 0, out)
        self.assertTrue((proj.work_dir(112, 1) / "harvest_requests.json").exists())
        rc, out = jp("ingest", "--surah", "112", "--ruku", "1", "--inbox", str(inbox))
        self.assertEqual(rc, 0, out)
        rc, out = jp("plan", "--surah", "112", "--ruku", "1")
        self.assertEqual(rc, 0, out)
        rc, out = jp("run", "--surah", "112", "--ruku", "1", "--dry-run")
        self.assertEqual(rc, 0, out)
        self.assertTrue(list((proj.work_dir(112, 1) / "prompts").glob("*.txt")))
        rc, out = jp("go", "--surah", "112", "--provider", "mock")
        self.assertNotEqual(rc, 0)                      # মক-আউটপুট মার্জ/অডিটে আটকায়
        rc, out = jp("status", "--surah", "112")
        self.assertEqual(rc, 0, out)
        self.assertIn("সূরা 112", out)


class TestValidators(Base):
    def test_numbers_strict(self):
        from jalalayn_pipeline.validate import VCtx, check_numbers
        proj, *_ = self.ready()
        v = VCtx(sid=112, ayat_text={}, quran=proj.quran, corpus_sk=[], allowed_ids=set(), id_roles={},
                 source_numbers={"57", "100"}, qids_by_ayah={}, author=jalalayn_author(112))
        self.assertTrue(check_numbers("সহীহ মুসলিম, হাদীস নং ১৬৯০।", v))
        self.assertFalse(check_numbers("সহীহ মুসলিম, হাদীস নং ১৬৯০ (যাচাইসাপেক্ষ)।", v))
        self.assertFalse(check_numbers("জালালাইন পৃষ্ঠা ৫৭।", v))
        self.assertTrue(check_numbers("আল-হিদায়াহ (২/৯৮)।", v))

    def test_quran_ref_check(self):
        from jalalayn_pipeline.validate import VCtx, check_quran_refs
        proj, *_ = self.ready()
        v = VCtx(sid=112, ayat_text={}, quran=proj.quran, corpus_sk=[], allowed_ids=set(), id_roles={},
                 source_numbers=set(), qids_by_ayah={}, author=jalalayn_author(112))
        self.assertEqual(check_quran_refs("﴿لَمْ يَلِدْ وَلَمْ يُولَدْ﴾ [সূরা ইখলাস ১১২:৩]", v), [])
        self.assertTrue(check_quran_refs("﴿لَمْ يَلِدْ وَلَمْ يُولَدْ﴾ [সূরা ইখলাস ১১২:২]", v))
        self.assertTrue(check_quran_refs("﴿قُلْ هُوَ ٱللَّهُ أَحَدٌ﴾ ৯৯৯:১", v))

    def test_qiraat_note_rejects_reader_name(self):
        from jalalayn_pipeline.validate import VCtx, validate_task
        proj, *_ = self.ready()
        v = VCtx(sid=112, ayat_text={1: ""}, quran=proj.quran, corpus_sk=[], allowed_ids=set(), id_roles={},
                 source_numbers=set(), qids_by_ayah={1: {"Q1"}}, author=jalalayn_author(112), reader_names=proj.cfg["reader_names"])
        bad = {"1": {"QIRAAT_IMPACT": "### আয়াত ১ — কিরাআতের তাফসীর ও প্রভাব\n\n- হাফস [Q1] এভাবে পড়েছেন।"}}
        ok = {"1": {"QIRAAT_IMPACT": "### আয়াত ১ — কিরাআতের তাফসীর ও প্রভাব\n\n- প্রথম পাঠ [Q1] অর্থে প্রভাব ফেলে।"}}
        self.assertTrue(validate_task("ayah-qiraat-note", bad, v, ["1"]))
        self.assertEqual(validate_task("ayah-qiraat-note", ok, v, ["1"]), [])
        wrongq = {"1": {"QIRAAT_IMPACT": "### আয়াত ১ — কিরাআতের তাফসীর ও প্রভাব\n\n- প্রথম পাঠ [Q9]।"}}
        self.assertTrue(validate_task("ayah-qiraat-note", wrongq, v, ["1"]))

    def test_arabic_in_backticks_rejected(self):
        from jalalayn_pipeline.validate import VCtx, check_common
        proj, *_ = self.ready()
        v = VCtx(sid=112, ayat_text={}, quran=proj.quran, corpus_sk=[], allowed_ids=set(), id_roles={},
                 source_numbers=set(), qids_by_ayah={}, author=jalalayn_author(112))
        self.assertTrue(check_common("শব্দ `أحد` বলা হয়", v))

    def test_parse_output_strictness(self):
        from jalalayn_pipeline.validate import parse_output
        ok = "<!-- BLOCK:1 -->\n<!-- PART:A_START -->\nx\n<!-- PART:A_END -->\n"
        b, e = parse_output(ok, ["1"], ["A"])
        self.assertEqual(e, [])
        b, e = parse_output("ভূমিকা\n" + ok, ["1"], ["A"])
        self.assertTrue(e)
        b, e = parse_output("```markdown\n" + ok + "```", ["1"], ["A"])
        self.assertEqual(e, [])
        b, e = parse_output(ok, ["1", "2"], ["A"])
        self.assertTrue(any("BLOCK:2 নেই" in x for x in e))

    def test_v_ahkam_rules(self):
        from jalalayn_pipeline.validate import VCtx, validate_task
        proj, *_ = self.ready()
        v = VCtx(sid=112, ayat_text={1: "", 2: "", 3: "", 4: ""}, quran=proj.quran, corpus_sk=[],
                 allowed_ids={"S1"}, id_roles={"S1": "fiqh"}, source_numbers={"1", "2", "3", "4"},
                 qids_by_ayah={}, author=jalalayn_author(112), a0=1, a1=4)

        # 1. প্রযোজ্য নয় পাস করবে
        na_parts = {
            "RUKU": {
                "SEC7_IKHTILAF": "প্রযোজ্য নয় — কোনো প্রধান মতভেদ নেই।",
                "SEC8_AHKAM": "প্রযোজ্য নয় — কোনো ব্যবহারিক ফিকহ নেই।"
            }
        }
        self.assertEqual(validate_task("ruku-ikhtilaf-ahkam", na_parts, v, ["RUKU"]), [])

        # 2. বৈধ টেবিল পাস করবে
        valid_table = (
            "| মাসআলা | হানাফী | মালিকী | শাফিঈ | হাম্বলী | প্রধান দলীল ও প্রামাণ্য উৎস |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
            "| **আল্লাহর একত্বে বিশ্বাস (আয়াত ১)** | ফরজ | ফরজ | ফরজ | ফরজ | দলীল [src:S1]<br>**তারজীহ:** ওয়াজিব<br>**সমসাময়িক উদাহরণ:** শিরকমুক্ত ঈমান<br>উৎস: *কুরতুবী* |\n"
        )
        ok_parts = {
            "RUKU": {
                "SEC7_IKHTILAF": "### মুখাতাব\nপ্রত্যক্ষ সম্বোধন।\n\n### মতভেদ\nবিস্তারিত মতভেদ ও তারজীহ।",
                "SEC8_AHKAM": valid_table
            }
        }
        self.assertEqual(validate_task("ruku-ikhtilaf-ahkam", ok_parts, v, ["RUKU"]), [])

        # 3. আয়াত নম্বর বাদ পড়লে এরর দেবে
        no_ayah_table = valid_table.replace("(আয়াত ১)", "")
        bad_parts1 = {"RUKU": {"SEC7_IKHTILAF": "মুখাতাব ও তারজীহ বিশ্লেষণ।", "SEC8_AHKAM": no_ayah_table}}
        errs1 = validate_task("ruku-ikhtilaf-ahkam", bad_parts1, v, ["RUKU"])
        self.assertTrue(any("আয়াত" in e for e in errs1))

        # 4. রুকুর বাইরের আয়াত নম্বর দিলে এরর দেবে (রুকু ১-৪, দিয়েছে ৯৯)
        out_range_table = valid_table.replace("(আয়াত ১)", "(আয়াত ৯৯)")
        bad_parts2 = {"RUKU": {"SEC7_IKHTILAF": "মুখাতাব ও তারজীহ বিশ্লেষণ।", "SEC8_AHKAM": out_range_table}}
        errs2 = validate_task("ruku-ikhtilaf-ahkam", bad_parts2, v, ["RUKU"])
        self.assertTrue(any("বাইরের আয়াত" in e for e in errs2))

        # 5. সমসাময়িক উদাহরণ না থাকলে এরর দেবে
        no_contemp_table = valid_table.replace("**সমসাময়িক উদাহরণ:**", "**অন্যান্য:**")
        bad_parts3 = {"RUKU": {"SEC7_IKHTILAF": "মুখাতাব ও তারজীহ বিশ্লেষণ।", "SEC8_AHKAM": no_contemp_table}}
        errs3 = validate_task("ruku-ikhtilaf-ahkam", bad_parts3, v, ["RUKU"])
        self.assertTrue(any("সমসাময়িক" in e for e in errs3))


if __name__ == "__main__":
    unittest.main()

"""সাব-এজেন্ট ব্রিজ কমান্ডের টেস্ট (prepare-level ও submit-part)।"""
from __future__ import annotations

import argparse
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from jalalayn_pipeline.cli import cmd_prepare_level, cmd_submit_part
from jalalayn_pipeline.mock_llm import mock_fn
from jalalayn_pipeline.sources import ingest
from test_pipeline import make_project


class TestSubagentBridge(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.proj, self.inbox = make_project(self.tmp)
        ingest(self.proj, 112, 1, self.inbox)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_prepare_level_exports_prompts(self):
        args = argparse.Namespace(surah=112, ruku=1, level=1, only=None, force=False)
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            rc = cmd_prepare_level(self.proj, args)
            out = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        self.assertEqual(rc, 0)
        data = json.loads(out)
        self.assertTrue(data["ok"])
        self.assertGreater(len(data["ready"]), 0)
        first_ready = data["ready"][0]
        self.assertTrue(Path(first_ready["prompt_file"]).exists())

    def test_submit_part_validation_and_success(self):
        # 1. prepare-level দিয়ে টাস্ক প্রম্পট জেনারেট করি
        p_args = argparse.Namespace(surah=112, ruku=1, level=1, only="ayah-translation-jalalayn", force=False)
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            cmd_prepare_level(self.proj, p_args)
            p_out = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        p_data = json.loads(p_out)
        self.assertEqual(len(p_data["ready"]), 1)
        task_id = p_data["ready"][0]["id"]
        prompt_data = json.loads(Path(p_data["ready"][0]["prompt_file"]).read_text(encoding="utf-8"))

        # 2. ভুল আউটপুট দিলে validate.py ধরে কি না (ত্রুটি টেস্ট)
        bad_file = self.tmp / "bad_reply.md"
        bad_file.write_text("ভুল আউটপুট যাতে কোনো BLOCK মার্কার নেই", encoding="utf-8")
        s_bad_args = argparse.Namespace(surah=112, ruku=1, task=task_id, file=str(bad_file), provider="test")

        sys.stdout = io.StringIO()
        try:
            bad_rc = cmd_submit_part(self.proj, s_bad_args)
            bad_out = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        self.assertEqual(bad_rc, 1)
        bad_res = json.loads(bad_out)
        self.assertFalse(bad_res["ok"])
        self.assertGreater(len(bad_res["errors"]), 0)

        # 3. মক ফাংশন থেকে বিশুদ্ধ আউটপুট দিলে সফল হয় কি না
        reply = mock_fn(prompt_data["messages"])
        good_file = self.tmp / "good_reply.md"
        good_file.write_text(reply, encoding="utf-8")
        s_good_args = argparse.Namespace(surah=112, ruku=1, task=task_id, file=str(good_file), provider="test")

        sys.stdout = io.StringIO()
        try:
            good_rc = cmd_submit_part(self.proj, s_good_args)
            good_out = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        self.assertEqual(good_rc, 0)
        good_res = json.loads(good_out)
        self.assertTrue(good_res["ok"])
        self.assertEqual(good_res["status"], "done")

    def test_multi_mcp_ingest_and_bibliography(self):
        from harvester_helper import (
            save_shamela_page, save_tafsir_mcp, save_hadith_mcp,
            save_maher_hadith, save_quran_mcp, save_fiqh_fatwa, save_bahouth_topics
        )
        from jalalayn_pipeline.sources import load_sources, verify_hashes, roles
        from jalalayn_pipeline.merge import _bibliography

        mcp_inbox = self.tmp / "mcp_inbox"
        mcp_inbox.mkdir()

        save_shamela_page(mcp_inbox, 23635, 167, 32, "مفاتيح الغيب", "الرازي", "نص التفسير", role="tafsir", covers_ayat=[1, 2, 3, 4])
        save_tafsir_mcp(mcp_inbox, "tafsir", "112_1", "تفسير الطبري", "ابن جرير", "نص الطبري", covers_ayat=[1])
        save_hadith_mcp(mcp_inbox, "bukhari", "5013", "حديث قل هو الله أحد", text_en="Hadith on Ikhlas", grades="صحيح", covers_ayat=[1, 2, 3, 4])
        save_maher_hadith(mcp_inbox, "mf101", "تحقيق حديث الإخلاص", "نص التحقيق", covers_ayat=[1, 2, 3, 4])
        save_quran_mcp(mcp_inbox, "morphology", "112_1", "إعراب ومورفولوجي", covers_ayat=[1])
        save_fiqh_fatwa(mcp_inbox, "islamqa", "2214", "حكم قراءة الإخلاص", "الجواب مستحب", covers_ayat=[1, 2, 3, 4])
        save_bahouth_topics(mcp_inbox, "top1", [{"topic_id": 101, "title_raw": "توحيد الأسماء والصفات"}], covers_ayat=[1, 2, 3, 4])

        done, issues = ingest(self.proj, 112, 1, mcp_inbox)
        self.assertEqual(len(issues), 0, f"ইনজেস্ট ইস্যু: {issues}")
        self.assertGreaterEqual(len(done), 7)

        caps = load_sources(self.proj, 112, 1)
        errs = verify_hashes(caps)
        self.assertEqual(errs, [], f"হ্যাশ অমিল: {errs}")

        rl = roles(self.proj, caps)
        self.assertEqual(rl["sh23635-p167"], "tafsir")
        self.assertEqual(rl["hm-bukhari-5013"], "hadith")
        self.assertEqual(rl["mf-mf101"], "hadith")
        self.assertEqual(rl["fatwa-islamqa-2214"], "fiqh")
        self.assertEqual(rl["bah-topic-top1"], "topics")

        bib = _bibliography(self.proj, caps, list(caps.keys()))
        self.assertIn("مفاتيح الغيب", bib)
        self.assertIn("হাদীস সংকলন (bukhari)", bib)
        self.assertIn("৫০১৩", bib)
        self.assertIn("শায়খ মাহির আল-ফাহল", bib)
        self.assertIn("تفسير الطبري", bib)
        self.assertIn("IslamQA MCP", bib)

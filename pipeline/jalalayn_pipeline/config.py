"""কনফিগ লোডার। প্রজেক্ট-রুট = pipeline/ ফোল্ডারের অভিভাবক (বা পরিবেশ-চলক JALALAYN_BASE_DIR)।"""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path

PIPE_DIR = Path(__file__).resolve().parent.parent

DEFAULTS = {
    "info_dir": "00_প্রজেক্ট_তথ্য",
    "work_dir": "_work",
    "tanzil_file": "quran-uthmani.txt",
    "audit_file": "audit_results.json",
    "llm": {
        "provider": "litellm",
        "model": "",
        "temperature": 0.2,
        "max_tokens": 8000,
        "timeout": 240,
        "api_retries": 4,
        "backoff_base": 3.0,
    },
    "run": {
        "concurrency": 4,
        "rpm": 30,
        "max_attempts": 3,
        "abort_after_failed_tasks": 3,
        "batch_max_ayat": 4,
        "batch_max_words": 36,
        "unit_max_ayat": 6,
    },
    "validation": {
        "strict_numbers": True,
        "min_quote_letters": 6,
    },
    "reader_names": [
        "নাফি", "নাফে", "ইবনে কাসীর", "ইবনু কাসীর", "আবূ আমর", "আবু আমর", "ইবনে আমির", "ইবনু আমির",
        "আসিম", "আছিম", "হামযা", "হামযাহ", "কিসাঈ", "কিসায়ী", "আবূ জা'ফর", "আবূ জাফর", "ইয়াকূব", "খালাফ",
        "ওয়ারশ", "কালূন", "বাযযী", "কুনবুল", "হিশাম", "ইবনে যাকওয়ান", "শু'বা", "শুবা", "হাফস", "খাল্লাদ",
        "দূরী", "সূসী", "রাওহ", "রুওয়াইস", "ইবনে জাম্মায", "ইবনে ওয়ারদান",
        "نافع", "ابن كثير", "أبو عمرو", "ابن عامر", "عاصم", "حمزة", "الكسائي", "أبو جعفر", "يعقوب", "خلف",
    ],
}


def _merge(a: dict, b: dict) -> dict:
    out = copy.deepcopy(a)
    for k, v in (b or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


class Config:
    def __init__(self, base_dir=None, overrides=None, config_path=None):
        env_base = os.environ.get("JALALAYN_BASE_DIR")
        self.base = Path(base_dir or env_base or PIPE_DIR.parent).resolve()
        data = copy.deepcopy(DEFAULTS)
        cp = Path(config_path) if config_path else PIPE_DIR / "config.json"
        if cp.exists():
            data = _merge(data, json.loads(cp.read_text(encoding="utf-8")))
        if overrides:
            data = _merge(data, overrides)
        if os.environ.get("JP_MODEL"):
            data["llm"]["model"] = os.environ["JP_MODEL"]
        self.c = data
        self.info = self.base / data["info_dir"]
        self.work_root = self.base / data["work_dir"]
        self.pipe = PIPE_DIR
        books_path = self.info / "books.json"
        if not books_path.exists():
            books_path = PIPE_DIR / "books.json"
        self.books = json.loads(books_path.read_text(encoding="utf-8"))
        self.audit_path = self.info / data["audit_file"]

    # সুবিধাজনক অ্যাক্সেসর
    def __getitem__(self, k):
        return self.c[k]

    @property
    def run(self):
        return self.c["run"]

    @property
    def llm(self):
        return self.c["llm"]

    @property
    def validation(self):
        return self.c["validation"]

    def book(self, book_id) -> dict:
        return self.books.get("allowed", {}).get(str(book_id), {})

    def is_blocked_book(self, book_id) -> bool:
        return str(book_id) in set(map(str, self.books.get("blocked", [])))

    def role_of(self, book_id) -> str:
        return self.book(book_id).get("role", "unknown")

    def rules_text(self) -> str:
        return (PIPE_DIR / "rules" / "00-global-rules.md").read_text(encoding="utf-8")

    def skill_text(self, name: str) -> str:
        t = (PIPE_DIR / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        if t.startswith("---"):
            end = t.find("\n---", 3)
            if end != -1:
                t = t[end + 4:]
        return t.strip()

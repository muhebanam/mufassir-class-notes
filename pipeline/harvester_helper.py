"""হারভেস্টার সহায়ক মডিউল: বিদ্যমান সোর্স থেকে ইনবক্স প্রস্তুতকরণ ও MCP ক্যাপচার সেভ করার হেল্পার।"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from jalalayn_pipeline.project import Project
from jalalayn_pipeline.util import now_iso, write_atomic, write_json


def prepare_inbox_from_existing(proj: Project, sid: int, rid: int, inbox_dir: Path) -> dict:
    """বিদ্যমান _sources ফোল্ডারে থাকা raw.json ও qiraat_table.md স্বয়ংক্রিয়ভাবে ইনবক্সে আনে।"""
    inbox_dir = Path(inbox_dir)
    inbox_dir.mkdir(parents=True, exist_ok=True)
    copied = []

    s_dir = proj.surah_dir(sid)
    legacy_raw = s_dir / "_sources" / f"ruku_{rid:02d}_raw.json"
    if legacy_raw.exists():
        dest = inbox_dir / f"ruku_{rid:02d}_raw_legacy.json"
        shutil.copy2(legacy_raw, dest)
        copied.append(dest.name)

    legacy_qmd = s_dir / "_sources" / f"ruku_{rid:02d}_qiraat_table.md"
    if legacy_qmd.exists():
        dest = inbox_dir / f"ruku_{rid:02d}_qiraat_table_legacy.md"
        shutil.copy2(legacy_qmd, dest)
        copied.append(dest.name)

    return {"inbox": str(inbox_dir), "copied_legacy_files": copied}


def save_turath_page(inbox_dir: Path, book_id: int, page_id: int, internal_page: str,
                     covers_ayat: list[int] | str, text: str,
                     tool: str = "turath:get_context", args: dict | None = None) -> Path:
    inbox_dir = Path(inbox_dir)
    inbox_dir.mkdir(parents=True, exist_ok=True)
    cov_str = "asurah" if covers_ayat == "surah" else f"a{covers_ayat[0]}-{covers_ayat[-1]}" if len(covers_ayat) > 1 else f"a{covers_ayat[0]}"
    file_path = inbox_dir / f"turath_{book_id}_{page_id}_{cov_str}.json"
    data = {
        "kind": "turath_page",
        "book_id": int(book_id),
        "page_id": int(page_id),
        "internal_page": str(internal_page),
        "covers_ayat": covers_ayat,
        "text": text.strip(),
        "tool": tool,
        "args": args or {},
        "captured_at": now_iso()
    }
    write_json(file_path, data)
    return file_path


def save_bahouth_qiraat(inbox_dir: Path, rows: list[dict]) -> Path:
    inbox_dir = Path(inbox_dir)
    inbox_dir.mkdir(parents=True, exist_ok=True)
    file_path = inbox_dir / "bahouth_qiraat.json"
    data = {
        "kind": "bahouth_qiraat",
        "rows": rows,
        "tool": "bahouth:list_verse_qiraat",
        "captured_at": now_iso()
    }
    write_json(file_path, data)
    return file_path


def save_bahouth_verses(inbox_dir: Path, verses: list[dict]) -> Path:
    inbox_dir = Path(inbox_dir)
    inbox_dir.mkdir(parents=True, exist_ok=True)
    file_path = inbox_dir / "bahouth_verses.json"
    data = {
        "kind": "bahouth_verses",
        "verses": verses,
        "tool": "bahouth:list_surah_verses",
        "captured_at": now_iso()
    }
    write_json(file_path, data)
    return file_path


def save_bahouth_root(inbox_dir: Path, root: str, text: str, covers_ayat: str = "surah") -> Path:
    inbox_dir = Path(inbox_dir)
    inbox_dir.mkdir(parents=True, exist_ok=True)
    file_path = inbox_dir / f"bahouth_root_{root}.json"
    data = {
        "kind": "bahouth_root",
        "root": root,
        "text": text.strip(),
        "covers_ayat": covers_ayat,
        "tool": "bahouth:find_root",
        "captured_at": now_iso()
    }
    write_json(file_path, data)
    return file_path


def save_shamela_page(inbox_dir: Path, book_id: int, page: int, volume: int | str | None,
                      book_title: str, author: str, text: str, role: str = "tafsir",
                      covers_ayat: list[int] | str = "surah", url: str = "",
                      tool: str = "shamela:get_page") -> Path:
    inbox_dir = Path(inbox_dir)
    inbox_dir.mkdir(parents=True, exist_ok=True)
    cov_str = "asurah" if covers_ayat == "surah" else f"a{covers_ayat[0]}-{covers_ayat[-1]}" if len(covers_ayat) > 1 else f"a{covers_ayat[0]}"
    file_path = inbox_dir / f"shamela_{book_id}_{page}_{cov_str}.json"
    data = {
        "kind": "shamela_page",
        "book_id": int(book_id),
        "page": int(page),
        "volume": volume,
        "book_title": book_title,
        "author": author,
        "url": url,
        "role": role,
        "covers_ayat": covers_ayat,
        "text": text.strip(),
        "tool": tool,
        "captured_at": now_iso()
    }
    write_json(file_path, data)
    return file_path


def save_tafsir_mcp(inbox_dir: Path, subtype: str, key: str, source_name: str,
                    author: str, text: str, covers_ayat: list[int] | str = "surah",
                    role: str = "tafsir", tool: str = "tafsir-center:fetch_tafsir") -> Path:
    inbox_dir = Path(inbox_dir)
    inbox_dir.mkdir(parents=True, exist_ok=True)
    clean_key = str(key).replace(":", "_").replace("-", "_")
    file_path = inbox_dir / f"tafsir_mcp_{subtype}_{clean_key}.json"
    data = {
        "kind": "tafsir_mcp",
        "subtype": subtype,
        "key": str(key),
        "source_name": source_name,
        "author": author,
        "role": role,
        "covers_ayat": covers_ayat,
        "text": text.strip(),
        "tool": tool,
        "captured_at": now_iso()
    }
    write_json(file_path, data)
    return file_path


def save_hadith_mcp(inbox_dir: Path, collection: str, hadith_number: str | int,
                    text_ar: str, text_en: str = "", book_number: int | None = None,
                    chapter_title: str = "", grades: str = "", cross_refs: list | None = None,
                    covers_ayat: list[int] | str = "surah", tool: str = "hadith-mcp:fetch_hadith") -> Path:
    inbox_dir = Path(inbox_dir)
    inbox_dir.mkdir(parents=True, exist_ok=True)
    clean_hnum = str(hadith_number).replace("/", "_").replace(" ", "_")
    file_path = inbox_dir / f"hadith_mcp_{collection}_{clean_hnum}.json"
    data = {
        "kind": "hadith_mcp",
        "collection": collection,
        "hadith_number": str(hadith_number),
        "book_number": book_number,
        "chapter_title": chapter_title,
        "text_ar": text_ar.strip(),
        "text_en": text_en.strip() if text_en else "",
        "grades": grades,
        "cross_refs": cross_refs or [],
        "covers_ayat": covers_ayat,
        "tool": tool,
        "captured_at": now_iso()
    }
    write_json(file_path, data)
    return file_path


def save_maher_hadith(inbox_dir: Path, doc_id: str, title: str, text: str,
                      covers_ayat: list[int] | str = "surah", tool: str = "maher-alfahel") -> Path:
    inbox_dir = Path(inbox_dir)
    inbox_dir.mkdir(parents=True, exist_ok=True)
    file_path = inbox_dir / f"maher_hadith_{doc_id}.json"
    data = {
        "kind": "maher_hadith",
        "doc_id": str(doc_id),
        "title": title,
        "text": text.strip(),
        "covers_ayat": covers_ayat,
        "tool": tool,
        "captured_at": now_iso()
    }
    write_json(file_path, data)
    return file_path


def save_quran_mcp(inbox_dir: Path, subtype: str, key: str, text: str,
                   role: str = "quran", covers_ayat: list[int] | str = "surah",
                   tool: str = "quran-mcp:fetch_quran") -> Path:
    inbox_dir = Path(inbox_dir)
    inbox_dir.mkdir(parents=True, exist_ok=True)
    clean_key = str(key).replace(":", "_").replace("-", "_")
    file_path = inbox_dir / f"quran_mcp_{subtype}_{clean_key}.json"
    data = {
        "kind": "quran_mcp",
        "subtype": subtype,
        "key": str(key),
        "role": role,
        "covers_ayat": covers_ayat,
        "text": text.strip(),
        "tool": tool,
        "captured_at": now_iso()
    }
    write_json(file_path, data)
    return file_path


def save_fiqh_fatwa(inbox_dir: Path, source: str, fatwa_id: str | int, question: str,
                    answer: str, text: str | None = None, covers_ayat: list[int] | str = "surah",
                    tool: str = "islamqa") -> Path:
    inbox_dir = Path(inbox_dir)
    inbox_dir.mkdir(parents=True, exist_ok=True)
    full_text = text.strip() if text else f"প্রশ্ন: {question.strip()}\n\nউত্তর: {answer.strip()}"
    file_path = inbox_dir / f"fatwa_{source}_{fatwa_id}.json"
    data = {
        "kind": "fiqh_fatwa",
        "source": source,
        "fatwa_id": str(fatwa_id),
        "question": question.strip(),
        "answer": answer.strip(),
        "text": full_text,
        "covers_ayat": covers_ayat,
        "tool": tool,
        "captured_at": now_iso()
    }
    write_json(file_path, data)
    return file_path


def save_bahouth_topics(inbox_dir: Path, topic_id: str | int, topics: list[dict],
                        covers_ayat: list[int] | str = "surah", tool: str = "bahouth:list_verse_topics") -> Path:
    inbox_dir = Path(inbox_dir)
    inbox_dir.mkdir(parents=True, exist_ok=True)
    file_path = inbox_dir / f"bahouth_topics_{topic_id}.json"
    data = {
        "kind": "bahouth_topics",
        "topic_id": str(topic_id),
        "topics": topics,
        "covers_ayat": covers_ayat,
        "tool": tool,
        "captured_at": now_iso()
    }
    write_json(file_path, data)
    return file_path

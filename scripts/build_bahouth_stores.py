#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2.3 — বাহাউথ স্টোর জেনারেশন (lazy-loadable)
- roots/index.json = {root_ar: {id: "r0001", count: N}}  (ASCII id)
- roots/r0001.json = {schema_version, root_ar, verses: [{surah, ayah, text_raw, verse_key}]}
- topics/index.json = {topic_id: {id: "t123", count: N}} (server topic_id as string key)
- topics/t123.json = {schema_version, topic_id, title_raw, category_id, subcategory_id, verses: [...]}
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bahouth_common import atomic_write_json, make_schema_envelope


REF_DIR = Path(__file__).resolve().parent.parent / "reference"
OUT_DIR = Path(__file__).resolve().parent.parent / "web" / "public" / "data"


def load_ref(filename: str) -> dict:
    p = REF_DIR / filename
    if not p.exists():
        return {}
    with open(p, "r", encoding="utf-8") as f:
        env = json.load(f)
    return env.get("data", {})


def save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_json(path, data)


def build_roots_store():
    """Generate roots store with deterministic ASCII ids."""
    roots_data = load_ref("bahouth_roots.json")
    if not roots_data:
        print("No roots data found in reference/bahouth_roots.json")
        return

    # Sort roots by Arabic text for deterministic id assignment
    sorted_roots = sorted(roots_data.items(), key=lambda x: x[0])

    roots_dir = OUT_DIR / "roots"
    roots_dir.mkdir(parents=True, exist_ok=True)

    index = {}
    for i, (root_ar, data) in enumerate(sorted_roots, 1):
        rid = f"r{i:04d}"
        verses = data.get("verses", [])
        pag = data.get("pagination", {})
        total = pag.get("total", len(verses))

        # Verify count integrity
        if total != len(verses):
            print(f"[WARN] Root '{root_ar}': pagination.total={total} != collected={len(verses)}")

        # Build per-root file
        root_file = roots_dir / f"{rid}.json"
        root_obj = {
            "schema_version": "1",
            "root_ar": root_ar,
            "count": len(verses),
            "verses": [
                {
                    "surah": v.get("surah_id"),
                    "ayah": v.get("ayah_number"),
                    "verse_key": v.get("verse_key"),
                    "text_raw": v.get("text_raw", "")[:200],  # truncated for size
                    "page_number": v.get("page_number"),
                    "word_count": v.get("word_count"),
                    "letter_count": v.get("letter_count"),
                }
                for v in verses
            ],
        }
        save_json(root_file, root_obj)

        # Index entry
        index[root_ar] = {"id": rid, "count": len(verses)}

    # Save index
    index_file = OUT_DIR / "roots" / "index.json"
    save_json(index_file, {"schema_version": "1", "roots": index})
    print(f"Roots store: {len(index)} roots -> {roots_dir}")


def build_topics_store():
    """Generate topics store using server topic_id as file key."""
    topics_data = load_ref("bahouth_topics.json")
    if not topics_data:
        print("No topics data found in reference/bahouth_topics.json")
        return

    topics_dir = OUT_DIR / "topics"
    topics_dir.mkdir(parents=True, exist_ok=True)

    index = {}
    for tid_str, data in topics_data.items():
        try:
            tid = int(tid_str)
        except ValueError:
            continue

        verses = data.get("verses", [])
        pag = data.get("pagination", {})
        total = pag.get("total", len(verses))

        if total != len(verses):
            print(f"[WARN] Topic {tid}: pagination.total={total} != collected={len(verses)}")

        # Need title_raw, category_id, subcategory_id - these come from verse_topics
        # We don't have them in the global topics data (only verses). 
        # For now, use placeholder; could be enriched from verse_topics if needed.
        topic_file = topics_dir / f"t{tid}.json"
        topic_obj = {
            "schema_version": "1",
            "topic_id": tid,
            "count": len(verses),
            "verses": [
                {
                    "surah": v.get("surah_id"),
                    "ayah": v.get("ayah_number"),
                    "verse_key": v.get("verse_key"),
                    "text_raw": v.get("text_raw", "")[:200],
                    "page_number": v.get("page_number"),
                    "word_count": v.get("word_count"),
                    "letter_count": v.get("letter_count"),
                }
                for v in verses
            ],
        }
        save_json(topic_file, topic_obj)
        index[str(tid)] = {"id": f"t{tid}", "count": len(verses)}

    # Save index
    index_file = OUT_DIR / "topics" / "index.json"
    save_json(index_file, {"schema_version": "1", "topics": index})
    print(f"Topics store: {len(index)} topics -> {topics_dir}")


def main():
    print("Building Bahouth stores...")
    build_roots_store()
    build_topics_store()
    print("Done.")


if __name__ == "__main__":
    main()
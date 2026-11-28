#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T1.4 — বাহাউথ টপিক্স হারভেস্ট (list_verse_topics + list_topic_verses)
- Per-surah: _sources/bahouth_topics.json (verse→topics)
- Global: reference/bahouth_topics.json (topic→verses, append-resume)
Usage: python scripts/harvest_bahouth_topics.py --surah 25 [--retry-failed]
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bahouth_common import (
    BahouthClient,
    atomic_write_json,
    make_schema_envelope,
    extract_payload,
    paginate_collect,
    bahouth_key,
)


REF_FILE = Path(__file__).resolve().parent.parent / "reference" / "bahouth_topics.json"


def load_existing_topics() -> Dict:
    if REF_FILE.exists():
        try:
            with open(REF_FILE, "r", encoding="utf-8") as f:
                env = json.load(f)
            data = env.get("data", {})
            return {int(k): v for k, v in data.items()}
        except Exception:
            pass
    return {}


def save_topics(topics_dict: Dict):
    REF_FILE.parent.mkdir(parents=True, exist_ok=True)
    # Convert int keys to strings for JSON
    str_data = {str(k): v for k, v in topics_dict.items()}
    envelope = make_schema_envelope(str_data)
    atomic_write_json(REF_FILE, envelope)


def load_surah_topics(surah: int) -> Dict:
    BASE = Path(__file__).resolve().parent.parent
    s_dir = BASE / (f"২৫_সূরা_আল-ফুরকান" if surah == 25 else f"surah_{surah}")
    topic_file = s_dir / "_sources" / "bahouth_topics.json"
    if not topic_file.exists():
        return {}
    with open(topic_file, "r", encoding="utf-8") as f:
        env = json.load(f)
    return env.get("data", {})


def save_surah_topics(surah: int, topics_data: Dict):
    BASE = Path(__file__).resolve().parent.parent
    s_dir = BASE / (f"২৫_সূরা_আল-ফুরকান" if surah == 25 else f"surah_{surah}")
    topic_file = s_dir / "_sources" / "bahouth_topics.json"
    topic_file.parent.mkdir(parents=True, exist_ok=True)
    envelope = make_schema_envelope(topics_data)
    atomic_write_json(topic_file, envelope)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--surah", type=int, required=True)
    ap.add_argument("--retry-failed", action="store_true")
    args = ap.parse_args()

    surah = args.surah

    client = BahouthClient()
    global_topics = load_existing_topics()
    surah_topics = load_surah_topics(surah)

    # Get verse count from meta
    BASE = Path(__file__).resolve().parent.parent
    s_dir = BASE / (f"২৫_সূরা_আল-ফুরকান" if surah == 25 else f"surah_{surah}")
    meta_file = s_dir / "_sources" / "bahouth_verse_meta.json"
    verse_count = 0
    if meta_file.exists():
        with open(meta_file, "r", encoding="utf-8") as f:
            env = json.load(f)
        verse_count = len(env.get("data", []))
    if verse_count == 0:
        verse_count = 77 if surah == 25 else 0

    print(f"Surah {surah}: {verse_count} ayahs | Global topics: {len(global_topics)} | Local: {len(surah_topics)}")

    # Step 1: Fetch verse→topics for missing ayahs
    for a in range(1, verse_count + 1):
        v_key = bahouth_key(surah, a)
        if v_key in surah_topics:
            continue

        res = client.list_verse_topics(v_key)
        payload = extract_payload(res)

        if not payload:
            print(f"  [{a:02d}/{verse_count}] {v_key} FAILED", file=sys.stderr)
            continue

        topics = payload.get("topics", [])
        # Normalize: each topic has topic_id, subcategory_id, category_id, title_raw
        surah_topics[v_key] = topics
        print(f"  [{a:02d}/{verse_count}] {v_key} -> {len(topics)} topics")

    # Collect topic_ids from ALL ayahs (including cached)
    new_topic_ids = set()
    for vkey, topics in surah_topics.items():
        for t in topics:
            tid = t.get("topic_id")
            if tid is not None:
                new_topic_ids.add(tid)

    if surah_topics:
        save_surah_topics(surah, surah_topics)

    # Step 2: Fetch topic→verses for new topic_ids not in global
    missing_topic_ids = [tid for tid in new_topic_ids if tid not in global_topics]
    print(f"New topic IDs to harvest globally: {len(missing_topic_ids)}")

    for i, tid in enumerate(missing_topic_ids, 1):
        print(f"  [{i}/{len(missing_topic_ids)}] topic_id={tid} ...", end=" ", flush=True)
        try:
            verses, pag = paginate_collect(client, client.list_topic_verses, tid, limit=50)
            total = pag.get("total")
            if total is not None and len(verses) != total:
                print(f"TRUNCATION WARN: collected={len(verses)} vs total={total}", file=sys.stderr)
            # Normalize verses: keep verse_id, surah_id, ayah_number, verse_key, page_number, text_raw, word_count, letter_count
            global_topics[tid] = {"verses": verses, "pagination": pag}
            print(f"ok ({len(verses)} verses)")
        except Exception as e:
            print(f"FAILED: {e}", file=sys.stderr)

    save_topics(global_topics)
    print(f"Saved global topics: {len(global_topics)} total")


if __name__ == "__main__":
    main()
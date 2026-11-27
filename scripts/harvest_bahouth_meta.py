#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T1.1 — বাহাউথ ভার্স মেটা হারভেস্ট (page_number, word_count, letter_count)
Usage: python scripts/harvest_bahouth_meta.py --surah 25 [--retry-failed]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bahouth_common import (
    BahouthClient,
    HarvestState,
    atomic_write_json,
    make_schema_envelope,
    parse_args_with_retry_flag,
    bahouth_key,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--surah", type=int, required=True)
    ap.add_argument("--retry-failed", action="store_true")
    args = ap.parse_args()

    surah = args.surah
    BASE = Path(__file__).resolve().parent.parent
    s_dir = BASE / f"২৫_সূরা_আল-ফুরকান" if surah == 25 else BASE / f"surah_{surah}"
    sources_dir = s_dir / "_sources"
    sources_dir.mkdir(parents=True, exist_ok=True)

    out_file = sources_dir / "bahouth_verse_meta.json"

    client = BahouthClient()
    state = HarvestState(surah, "verse_meta", sources_dir)

    if args.retry_failed:
        retried = state.retry_failed(client, "list_surah_verses")
        print(f"Retried {retried} failed calls")
        print(state.stats())
        return

    if state.collected:
        print(f"Existing data: {len(state.collected)} items. Use --retry-failed to retry failures.")
        return

    print(f"Fetching verse meta for Surah {surah} via list_surah_verses...")
    res = client.list_surah_verses(surah)

    from bahouth_common import extract_payload
    payload = extract_payload(res)

    if not payload:
        err = res.get("_error") or (res.get("error") if isinstance(res, dict) else "unknown")
        state.add_failed(str(surah), f"list_surah_verses: {err}", {"surah_id": surah})
        print(f"Failed: {err}", file=sys.stderr)
        sys.exit(1)

    verses = payload.get("verses", [])
    print(f"  Received {len(verses)} verses")

    envelope = make_schema_envelope(verses)
    atomic_write_json(out_file, envelope)
    state.collected = verses
    atomic_write_json(state.data_file, state.collected)

    print(f"Saved: {out_file}")
    print(state.stats())


if __name__ == "__main__":
    main()
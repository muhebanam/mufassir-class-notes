#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T1.2 — বাহাউথ শব্দ-স্তর হারভেস্ট (list_verse_words → root_token_raw)
Usage: python scripts/harvest_bahouth_words.py --surah 25 [--retry-failed]
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
    extract_payload,
    bahouth_key,
)


def load_verse_count(surah: int, base_dir: Path) -> int:
    """Try to get verse count from meta file, else default to 77 for surah 25."""
    s_dir = base_dir / (f"২৫_সূরা_আল-ফুরকান" if surah == 25 else f"surah_{surah}")
    meta_file = s_dir / "_sources" / "bahouth_verse_meta.json"
    if meta_file.exists():
        import json
        with open(meta_file, "r", encoding="utf-8") as f:
            env = json.load(f)
        return len(env.get("data", []))
    # Fallback
    return 77 if surah == 25 else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--surah", type=int, required=True)
    ap.add_argument("--retry-failed", action="store_true")
    args = ap.parse_args()

    surah = args.surah
    BASE = Path(__file__).resolve().parent.parent
    s_dir = BASE / (f"২৫_সূরা_আল-ফুরকান" if surah == 25 else f"surah_{surah}")
    sources_dir = s_dir / "_sources"
    sources_dir.mkdir(parents=True, exist_ok=True)

    out_file = sources_dir / "bahouth_words.json"

    verse_count = load_verse_count(surah, BASE)
    if verse_count == 0:
        print(f"Unknown verse count for surah {surah}", file=sys.stderr)
        sys.exit(1)

    client = BahouthClient()
    state = HarvestState(surah, "words", sources_dir)

    if args.retry_failed:
        retried = state.retry_failed(client, "list_verse_words")
        print(f"Retried {retried} failed calls")
        print(state.stats())
        return

    if state.collected:
        done_keys = {item.get("verse_key") for item in state.collected if item.get("verse_key")}
        print(f"Existing: {len(state.collected)} ayahs. Missing: {verse_count - len(done_keys)}")
        # Check if complete
        if len(done_keys) >= verse_count:
            print("Already complete.")
            return

    print(f"Fetching words for Surah {surah} ({verse_count} ayahs)...")

    for a in range(1, verse_count + 1):
        v_key = bahouth_key(surah, a)
        if any(item.get("verse_key") == v_key for item in state.collected):
            continue

        res = client.list_verse_words(v_key)
        payload = extract_payload(res)

        if not payload:
            err = res.get("_error") or (res.get("error") if isinstance(res, dict) else "unknown")
            state.add_failed(v_key, f"list_verse_words: {err}", {"verse_key": v_key})
            print(f"  [{a:02d}/{verse_count}] {v_key} FAILED: {err}", file=sys.stderr)
            continue

        words = payload.get("words", [])
        record = {"verse_key": v_key, "word_count": payload.get("word_count", len(words)), "words": words}
        state.add(record)
        print(f"  [{a:02d}/{verse_count}] {v_key} -> {len(words)} words")

    # Final envelope
    envelope = make_schema_envelope(state.collected)
    atomic_write_json(out_file, envelope)
    print(f"Saved: {out_file}")
    print(state.stats())


if __name__ == "__main__":
    main()
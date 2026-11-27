#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T1.3 — বাহাউথ রুট কনকর্ড্যান্স (list_root_verses → global reference/bahouth_roots.json)
- Unique roots from surah words → paginated harvest → append-resume global file
- Truncation guard: len(verses) == pagination.total
Usage: python scripts/harvest_bahouth_roots.py [--surah 25] [--retry-failed]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bahouth_common import (
    BahouthClient,
    atomic_write_json,
    make_schema_envelope,
    extract_payload,
    paginate_collect,
    strip_root_slashes,
)


REF_FILE = Path(__file__).resolve().parent.parent / "reference" / "bahouth_roots.json"


def load_existing_roots() -> Dict:
    if REF_FILE.exists():
        try:
            with open(REF_FILE, "r", encoding="utf-8") as f:
                env = json.load(f)
            data = env.get("data", {})
            # data = {root_text: {verses: [...], pagination: {...}}}
            return {k: v for k, v in data.items()}
        except Exception:
            pass
    return {}


def save_roots(roots_dict: Dict):
    REF_FILE.parent.mkdir(parents=True, exist_ok=True)
    envelope = make_schema_envelope(roots_dict)
    atomic_write_json(REF_FILE, envelope)


def extract_unique_roots(surah: int) -> List[str]:
    BASE = Path(__file__).resolve().parent.parent
    s_dir = BASE / (f"২৫_সূরা_আল-ফুরকান" if surah == 25 else f"surah_{surah}")
    words_file = s_dir / "_sources" / "bahouth_words.json"
    if not words_file.exists():
        return []
    import json
    with open(words_file, "r", encoding="utf-8") as f:
        env = json.load(f)
    roots = set()
    for a in env.get("data", []):
        for w in a.get("words", []):
            r = strip_root_slashes(w.get("root_token_raw", ""))
            if r:
                roots.add(r)
    return sorted(roots)


def main():
    import json
    ap = argparse.ArgumentParser()
    ap.add_argument("--surah", type=int, default=25)
    ap.add_argument("--retry-failed", action="store_true")
    args = ap.parse_args()

    surah = args.surah

    client = BahouthClient()
    existing = load_existing_roots()
    print(f"Existing roots in reference: {len(existing)}")

    new_roots = [r for r in extract_unique_roots(surah) if r not in existing]
    print(f"New roots to harvest from Surah {surah}: {len(new_roots)}")

    if not new_roots:
        print("No new roots.")
        return

    harvested = 0
    failed_roots = []

    for i, root in enumerate(new_roots, 1):
        print(f"  [{i}/{len(new_roots)}] root='{root}' ...", end=" ", flush=True)
        try:
            verses, pag = paginate_collect(client, client.list_root_verses, root, limit=50)
            total = pag.get("total")
            if total is not None and len(verses) != total:
                print(f"TRUNCATION WARN: collected={len(verses)} vs total={total}", file=sys.stderr)
            existing[root] = {"verses": verses, "pagination": pag}
            harvested += 1
            print(f"ok ({len(verses)} verses)")
        except Exception as e:
            print(f"FAILED: {e}", file=sys.stderr)
            failed_roots.append(root)

    if harvested > 0:
        save_roots(existing)
        print(f"Saved {harvested} new roots to {REF_FILE}")

    if failed_roots:
        print(f"Failed roots ({len(failed_roots)}): {failed_roots}", file=sys.stderr)
        sys.exit(1)

    # Verify integrity: count == len(verses) for all
    mismatches = []
    for root, data in existing.items():
        cnt = data.get("pagination", {}).get("total")
        actual = len(data.get("verses", []))
        if cnt is not None and cnt != actual:
            mismatches.append((root, cnt, actual))
    if mismatches:
        print(f"INTEGRITY MISMATCHES: {mismatches}", file=sys.stderr)
    else:
        print("Integrity OK: all roots have count == len(verses)")


if __name__ == "__main__":
    main()
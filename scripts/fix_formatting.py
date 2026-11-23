#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministic Formatting Fix Engine v2.0
Project: Tafsir al-Jalalayn Class Notes (Surahs 24–114)
Author: Mufti Muhammad Muhibbullah (Muheb Anam) / Antigravity AI

Rules enforced:
1. Idempotent Section Separators:
   - Ensures every '## ' (level 2 heading) is preceded by '---', unless it's at the start of the file.
   - Never duplicates '---'.
2. Whitespace and Layout Normalization:
   - Ensures clean blank lines around major headings.
   - Strips trailing whitespace.
3. Content & Arabic Integrity:
   - Preserves all «...» quotes, Arabic text, verse keys, turath tags intact.
   - Never generates hallucinated translations or fabricated hadith citations.
4. Clean Backups:
   - Backups saved in a dedicated .backup_formatting/ directory (never cluttering git).
"""

import sys
import re
import shutil
from pathlib import Path

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = Path(r"d:\আমার গবেষণা\জালালাইন")
BACKUP_DIR = BASE_DIR / ".backup_formatting"


def format_ruku_content(text: str) -> tuple[str, bool, list[str]]:
    """
    Format a ruku markdown file idempotently.
    Returns: (new_text, changed, change_logs)
    """
    lines = text.splitlines()
    new_lines = []
    changed = False
    change_logs = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Check for Level 2 heading '## '
        if stripped.startswith("## "):
            # Check previous non-empty lines in new_lines
            prev_non_empty = None
            for p in reversed(new_lines):
                if p.strip():
                    prev_non_empty = p.strip()
                    break

            # If not start of file and previous non-empty line is NOT '---', add '---'
            if prev_non_empty is not None and prev_non_empty != "---":
                # Ensure one blank line before '---'
                while new_lines and new_lines[-1].strip() == "":
                    new_lines.pop()
                new_lines.append("")
                new_lines.append("---")
                new_lines.append("")
                changed = True
                change_logs.append(f"Added '---' separator before: {stripped[:40]}")
            else:
                # Ensure single blank line before '## ' if preceded by '---'
                if prev_non_empty == "---":
                    while new_lines and new_lines[-1].strip() == "":
                        new_lines.pop()
                    new_lines.append("")

            new_lines.append(stripped)

            # Ensure blank line after '## '
            if i + 1 < len(lines) and lines[i + 1].strip() != "":
                new_lines.append("")
                changed = True
            i += 1
            continue

        # Normal line: strip trailing whitespace
        new_lines.append(line.rstrip())
        i += 1

    # Ensure single trailing newline
    while new_lines and new_lines[-1].strip() == "":
        new_lines.pop()
    new_lines.append("")

    formatted_text = "\n".join(new_lines)
    if formatted_text != text:
        changed = True

    return formatted_text, changed, change_logs


def process_file(file_path: Path, dry_run: bool = False, create_backup: bool = True) -> bool:
    try:
        original_text = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    formatted_text, changed, logs = format_ruku_content(original_text)

    if not changed:
        return True

    print(f"[*] {file_path.parent.name}/{file_path.name}: {len(logs)} changes")
    for log in logs:
        print(f"    - {log}")

    if dry_run:
        print("    [DRY RUN - No file written]")
        return True

    if create_backup:
        rel_path = file_path.relative_to(BASE_DIR)
        backup_path = BACKUP_DIR / rel_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)

    file_path.write_text(formatted_text, encoding="utf-8")
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Deterministic Formatting Fix Engine")
    parser.add_argument("--file", type=str, help="Single file to process")
    parser.add_argument("--surahs", nargs="+", help="Specific surah folders to process (e.g., 24 25)")
    parser.add_argument("--all", action="store_true", help="Process all ruku files")
    parser.add_argument("--dry-run", action="store_true", help="Dry run without modifying files")
    parser.add_argument("--no-backup", action="store_true", help="Do not create backup files")

    args = parser.parse_args()

    target_files = []
    if args.file:
        f = Path(args.file)
        if not f.is_absolute():
            f = BASE_DIR / f
        target_files.append(f)
    elif args.surahs:
        bn_digits = "০১২৩৪৫৬৭৮৯"
        en_digits = "0123456789"
        en2bn = str.maketrans(en_digits, bn_digits)
        for s in args.surahs:
            s_bn = str(s).translate(en2bn)
            matched = list(BASE_DIR.glob(f"*{s}_*")) + list(BASE_DIR.glob(f"*{s_bn}_*"))
            for md in set(matched):
                if md.is_dir():
                    target_files.extend(sorted(md.glob("রুকু*.md")))
    elif args.all:
        for p in BASE_DIR.iterdir():
            if p.is_dir() and p.name not in ["00_প্রজেক্ট_তথ্য", "web", "scripts", ".git", ".backup_formatting"]:
                target_files.extend(sorted(p.glob("রুকু*.md")))
    else:
        print("Usage: python scripts/fix_formatting.py [--file FILE | --surahs 24 25 | --all] [--dry-run]")
        sys.exit(1)

    print(f"Total target ruku files: {len(target_files)}")
    modified_count = 0
    for tf in target_files:
        orig = tf.read_text(encoding="utf-8")
        _, changed, _ = format_ruku_content(orig)
        if changed:
            process_file(tf, dry_run=args.dry_run, create_backup=not args.no_backup)
            modified_count += 1

    print(f"\nProcessing complete! Modified: {modified_count} / {len(target_files)} files.")


if __name__ == "__main__":
    main()

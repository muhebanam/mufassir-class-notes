import os
import sys
from pathlib import Path

sys.path.insert(0, '00_প্রজেক্ট_তথ্য')
import audit_ruku

surahs_to_check = [
    '৩০_সূরা_আর-রূম', '৩১_সূরা_লুকমান', '৩২_সূরা_আস-সাজদাহ', '৩৩_সূরা_আল-আহযাব',
    '৩৪_সূরা_সাবা', '৩৫_সূরা_ফাতির', '৩৬_সূরা_ইয়াসীন', '৩৭_সূরা_আস-সাফফাত',
    '৩৮_সূরা_সোয়াদ', '৩৯_সূরা_আয-যুমার', '৪০_সূরা_গাফির', '৪১_সূরা_ফুসসিলাত',
    '৪২_সূরা_আশ-শূরা', '৪৩_সূরা_আয-যুখরুফ', '৪৪_সূরা_আদ-দুখান', '৪৫_সূরা_আল-জাসিয়াহ'
]

total_files = 0
total_passed = 0
total_failed = 0

for s_dir in surahs_to_check:
    p = Path(s_dir)
    md_files = sorted([f for f in p.glob('*.md') if not f.name.startswith('00_')])
    passed = 0
    failed = 0
    err_reasons = {}
    for md in md_files:
        ok, errs, warns = audit_ruku.audit_file(md, json_report=True)
        if ok:
            passed += 1
            total_passed += 1
        else:
            failed += 1
            total_failed += 1
            for e in errs:
                cat = e.split(':')[0]
                err_reasons[cat] = err_reasons.get(cat, 0) + 1
    total_files += len(md_files)
    print(f"{s_dir}: total={len(md_files)}, passed={passed}, failed={failed}")
    if err_reasons:
        print("   sample errors:", err_reasons)

print(f"\nGRAND TOTAL (Surahs 30-45): {total_files} rukus, {total_passed} passed, {total_failed} failed.")

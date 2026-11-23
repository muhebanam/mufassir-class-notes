import sys, re
from pathlib import Path

sys.path.append(r'd:\আমার গবেষণা\জালালাইন\00_প্রজেক্ট_তথ্য')
from audit_ruku import audit_file

surah_dirs = [
    (30, "৩০_সূরা_আর-রূম", 6),
    (31, "৩১_সূরা_লুকমান", 4),
    (32, "৩২_সূরা_আস-সাজদাহ", 3),
    (33, "৩৩_সূরা_আল-আহযাব", 9),
    (34, "৩৪_সূরা_সাবা", 6),
    (35, "৩৫_সূরা_ফাতির", 5),
    (36, "৩৬_সূরা_ইয়াসীন", 5),
    (37, "৩৭_সূরা_আস-সাফফাত", 5),
    (38, "৩৮_সূরা_সোয়াদ", 5),
    (39, "৩৯_সূরা_আয-যুমার", 8),
    (40, "৪০_সূরা_গাফির", 9),
    (41, "৪১_সূরা_ফুসসিলাত", 6),
    (42, "৪২_সূরা_আশ-শূরা", 5),
    (43, "৪৩_সূরা_আয-যুখরুফ", 7),
    (44, "৪৪_সূরা_আদ-দুখান", 3),
    (45, "৪৫_সূরা_আল-জাসিয়াহ", 4),
]

BENGALI_DIGITS = "০১২৩৪৫৬৭৮৯"
def to_bn_pad(n: int) -> str:
    return "".join(BENGALI_DIGITS[int(c)] for c in f"{n:02d}")

all_files = []
for s_num, s_dir, num_rukus in surah_dirs:
    dir_path = Path(s_dir)
    for r in range(1, num_rukus + 1):
        bn_r = to_bn_pad(r)
        matching = list(dir_path.glob(f"রুকু-{bn_r}_*.md"))
        if not matching:
            print(f"ERROR: Missing file for Surah {s_num} Ruku {r:02d}")
            sys.exit(1)
        all_files.append((s_num, r, matching[0]))

print(f"Total files collected for Juz 21-25: {len(all_files)} (Expected: 90)")

audit_passed = 0
audit_failed = 0
placeholder_errors = 0

for s_num, r_num, fpath in all_files:
    txt = fpath.read_text(encoding='utf-8')
    
    # 1. Structural audit via audit_ruku
    ok, errs, warns = audit_file(fpath, json_report=True)
    if not ok:
        print(f"[AUDIT FAIL] S{s_num} R{r_num:02d} ({fpath.name}): {errs}")
        audit_failed += 1
    else:
        audit_passed += 1

    # 2. Strict placeholder check
    has_trans_ph = bool(re.search(r'\(আয়াত [০-৯\d]+-এর প্রামাণ্য বঙ্গানুবাদ\)', txt))
    has_muf_ph = bool(re.search(r'কুরআনিক শব্দরূপ ও আভিধানিক অর্থ', txt))
    has_irab_stub = "প্রযোজ্য নয় — এই রুকুর আয়াতসমূহের" in txt

    if has_trans_ph or has_muf_ph or has_irab_stub:
        print(f"[PLACEHOLDER FAIL] S{s_num} R{r_num:02d} ({fpath.name}): trans={has_trans_ph}, muf={has_muf_ph}, irab={has_irab_stub}")
        placeholder_errors += 1

print("\n" + "="*50)
print(f"AUDIT SUMMARY (Juz 21 - Juz 25):")
print(f"Total rukus checked: {len(all_files)}")
print(f"audit_ruku PASSED: {audit_passed} / {len(all_files)}")
print(f"audit_ruku FAILED: {audit_failed}")
print(f"Placeholder Errors: {placeholder_errors}")
print("="*50)

if audit_failed == 0 and placeholder_errors == 0:
    print("[SUCCESS] 100% of all 90 rukus across Juz 21 to Juz 25 achieved Gold Standard!")
else:
    print("[FAILURE] Some files need attention.")
    sys.exit(1)

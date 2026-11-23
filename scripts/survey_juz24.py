import re
from pathlib import Path

BENGALI_DIGITS = "০১২৩৪৫৬৭৮৯"
def to_bn_pad(n: int) -> str:
    s = f"{n:02d}"
    return "".join(BENGALI_DIGITS[int(c)] for c in s)

files = []
# Surah 39 rukus 4 to 8
s39_dir = Path("৩৯_সূরা_আয-যুমার")
for r in range(4, 9):
    bn_r = to_bn_pad(r)
    p = list(s39_dir.glob(f"রুকু-{bn_r}_*.md"))
    if p: files.append((39, r, p[0]))

# Surah 40 rukus 1 to 9
s40_dir = Path("৪০_সূরা_গাফির")
for r in range(1, 10):
    bn_r = to_bn_pad(r)
    p = list(s40_dir.glob(f"রুকু-{bn_r}_*.md"))
    if p: files.append((40, r, p[0]))

# Surah 41 rukus 1 to 5
s41_dir = Path("৪১_সূরা_ফুসসিলাত")
for r in range(1, 6):
    bn_r = to_bn_pad(r)
    p = list(s41_dir.glob(f"রুকু-{bn_r}_*.md"))
    if p: files.append((41, r, p[0]))

print(f"Total files found for Juz 24: {len(files)} (expected 19)")
for s, r, f in files:
    txt = f.read_text(encoding='utf-8')
    has_trans_ph = bool(re.search(r'\(আয়াত [০-৯\d]+-এর প্রামাণ্য বঙ্গানুবাদ\)', txt))
    has_muf_ph = bool(re.search(r'কুরআনিক শব্দরূপ ও আভিধানিক অর্থ', txt))
    has_irab_stub = "প্রযোজ্য নয় — এই রুকুর আয়াতসমূহের" in txt
    print(f"S{s} R{r:02d} ({f.name}): trans_ph={has_trans_ph}, muf_ph={has_muf_ph}, irab_stub={has_irab_stub}")

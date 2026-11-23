import re
from pathlib import Path

BENGALI_DIGITS = "০১২৩৪৫৬৭৮৯"
def to_bn_pad(n: int) -> str:
    s = f"{n:02d}"
    return "".join(BENGALI_DIGITS[int(c)] for c in s)

files = []

# Surah 41 ruku 6
s41_dir = Path("৪১_সূরা_ফুসসিলাত")
p = list(s41_dir.glob(f"রুকু-{to_bn_pad(6)}_*.md"))
if p: files.append((41, 6, p[0]))

# Surah 42 rukus 1 to 5
s42_dir = Path("৪২_সূরা_আশ-শূরা")
for r in range(1, 6):
    p = list(s42_dir.glob(f"রুকু-{to_bn_pad(r)}_*.md"))
    if p: files.append((42, r, p[0]))

# Surah 43 rukus 1 to 7
s43_dir = Path("৪৩_সূরা_আয-যুখরুফ")
for r in range(1, 8):
    p = list(s43_dir.glob(f"রুকু-{to_bn_pad(r)}_*.md"))
    if p: files.append((43, r, p[0]))

# Surah 44 rukus 1 to 3
s44_dir = Path("৪৪_সূরা_আদ-দুখান")
for r in range(1, 4):
    p = list(s44_dir.glob(f"রুকু-{to_bn_pad(r)}_*.md"))
    if p: files.append((44, r, p[0]))

# Surah 45 rukus 1 to 4
s45_dir = Path("৪৫_সূরা_আল-জাসিয়াহ")
for r in range(1, 5):
    p = list(s45_dir.glob(f"রুকু-{to_bn_pad(r)}_*.md"))
    if p: files.append((45, r, p[0]))

print(f"Total files found for Juz 25: {len(files)} (expected 20)")
for s, r, f in files:
    txt = f.read_text(encoding='utf-8')
    has_trans_ph = bool(re.search(r'\(আয়াত [০-৯\d]+-এর প্রামাণ্য বঙ্গানুবাদ\)', txt))
    has_muf_ph = bool(re.search(r'কুরআনিক শব্দরূপ ও আভিধানিক অর্থ', txt))
    has_irab_stub = "প্রযোজ্য নয় — এই রুকুর আয়াতসমূহের" in txt
    print(f"S{s} R{r:02d} ({f.name}): trans_ph={has_trans_ph}, muf_ph={has_muf_ph}, irab_stub={has_irab_stub}")

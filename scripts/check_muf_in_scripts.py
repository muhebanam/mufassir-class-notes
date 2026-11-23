import re, os

scripts = (
    [(39, r, f'00_প্রজেক্ট_তথ্য/build_surah39_r0{r}.py') for r in range(4, 9)] +
    [(40, r, f'00_প্রজেক্ট_তথ্য/build_surah40_r0{r}.py') for r in range(1, 10)] +
    [(41, r, f'00_প্রজেক্ট_তথ্য/build_surah41_r0{r}.py') for r in range(1, 6)]
)

for s, r, sc in scripts:
    if not os.path.exists(sc): continue
    with open(sc, 'r', encoding='utf-8', errors='ignore') as f:
        txt = f.read()
    # Check if table has mufradat
    m = re.findall(r'\|\s*শব্দ\s*\|\s*মূলধাতু\s*\|', txt)
    has_muf = len(m) > 0
    # Also check section 13 or glossaries
    has_sec13 = "## ১৩. পরিভাষাকোষ" in txt
    print(f"S{s} R{r:02d}: has_muf_table={has_muf}, has_glossary={has_sec13}")

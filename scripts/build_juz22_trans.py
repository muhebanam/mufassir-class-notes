import os, glob, re, json

BENGALI_DIGITS = "০১২৩৪৫৬৭৮৯"
def to_int(s: str) -> int:
    res = "".join(str(BENGALI_DIGITS.index(c)) if c in BENGALI_DIGITS else c for c in s if c in "0123456789" + BENGALI_DIGITS)
    return int(res) if res else -1

scripts = (
    [(33, r, f'00_প্রজেক্ট_তথ্য/build_surah33_r0{r}.py') for r in range(5, 10)] +
    [(34, r, f'00_প্রজেক্ট_তথ্য/build_surah34_r0{r}.py') for r in range(1, 7)] +
    [(35, r, f'00_প্রজেক্ট_তথ্য/build_surah35_r0{r}.py') for r in range(1, 6)] +
    [(36, r, f'00_প্রজেক্ট_তথ্য/build_surah36_r0{r}.py') for r in range(1, 3)]
)

juz22_trans = {}
for s_num, r_num, sc in scripts:
    with open(sc, 'r', encoding='utf-8', errors='ignore') as f:
        t = f.read()
    m_bn = re.findall(r'\*\*বঙ্গানুবাদ\s*\(([০-৯\d]+)\)\s*:\*\*\s*([^\n]+)', t)
    t_dict = {}
    for a_str, text in m_bn:
        t_dict[to_int(a_str)] = text.strip()
    if s_num not in juz22_trans: juz22_trans[s_num] = {}
    juz22_trans[s_num][r_num] = t_dict
    print(f"Surah {s_num} Ruku {r_num:02d}: {len(t_dict)} ayahs extracted")

with open('scripts/juz22_trans.json', 'w', encoding='utf-8') as f:
    json.dump(juz22_trans, f, ensure_ascii=False, indent=2)

print("\nAll Juz 22 translations saved to scripts/juz22_trans.json")

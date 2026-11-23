import os, glob, re, json

BENGALI_DIGITS = "০১২৩৪৫৬৭৮৯"
def to_int(s: str) -> int:
    res = "".join(str(BENGALI_DIGITS.index(c)) if c in BENGALI_DIGITS else c for c in s if c in "0123456789" + BENGALI_DIGITS)
    return int(res) if res else -1

scripts = (
    [(36, r, f'00_প্রজেক্ট_তথ্য/build_surah36_r0{r}.py') for r in range(3, 6)] +
    [(37, r, f'00_প্রজেক্ট_তথ্য/build_surah37_r0{r}.py') for r in range(1, 6)] +
    [(38, r, f'00_প্রজেক্ট_তথ্য/build_surah38_r0{r}.py') for r in range(1, 6)] +
    [(39, r, f'00_প্রজেক্ট_তথ্য/build_surah39_r0{r}.py') for r in range(1, 4)]
)

juz23_trans = {}
for s_num, r_num, sc in scripts:
    with open(sc, 'r', encoding='utf-8', errors='ignore') as f:
        t = f.read()
    t_dict = {}
    
    # Check pattern 1: **বঙ্গানুবাদ (X):** text
    m_bn = re.findall(r'\*\*বঙ্গানুবাদ\s*\(([০-৯\d]+)\)\s*:\*\*\s*([^\n]+)', t)
    for a_str, text in m_bn:
        t_dict[to_int(a_str)] = text.strip()
        
    # Check pattern 2: JSON "trans_X": "..."
    m_json = re.findall(r'\"trans_(\d+)\"\s*:\s*\"([^\"]+)\"', t)
    for a_str, text in m_json:
        t_dict[int(a_str)] = text.strip()
        
    # Check pattern 3: * **আয়াত X:** ... **বঙ্গানুবাদ:** text
    m_p3 = re.findall(r'আয়াত\s*([০-৯\d]+)\s*[:\*][\s\S]*?\*\*বঙ্গানুবাদ\s*[:\*]\s*([^\n]+)', t)
    for a_str, text in m_p3:
        a_n = to_int(a_str)
        if a_n not in t_dict:
            t_dict[a_n] = text.strip().strip('*').strip()

    if s_num not in juz23_trans: juz23_trans[s_num] = {}
    juz23_trans[s_num][r_num] = t_dict
    print(f"Surah {s_num} Ruku {r_num:02d}: {len(t_dict)} ayahs extracted")

with open('scripts/juz23_trans.json', 'w', encoding='utf-8') as f:
    json.dump(juz23_trans, f, ensure_ascii=False, indent=2)

print("\nAll Juz 23 translations saved to scripts/juz23_trans.json")

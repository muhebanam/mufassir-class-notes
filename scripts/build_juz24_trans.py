import os, glob, re, json

BENGALI_DIGITS = "০১২৩৪৫৬৭৮৯"
def to_int(s: str) -> int:
    res = "".join(str(BENGALI_DIGITS.index(c)) if c in BENGALI_DIGITS else c for c in s if c in "0123456789" + BENGALI_DIGITS)
    return int(res) if res else -1

scripts = (
    [(39, r, f'00_প্রজেক্ট_তথ্য/build_surah39_r0{r}.py') for r in range(4, 9)] +
    [(40, r, f'00_প্রজেক্ট_তথ্য/build_surah40_r0{r}.py') for r in range(1, 10)] +
    [(41, r, f'00_প্রজেক্ট_তথ্য/build_surah41_r0{r}.py') for r in range(1, 6)]
)

juz24_trans = {}
for s_num, r_num, sc in scripts:
    if not os.path.exists(sc):
        print(f"NOT FOUND: {sc}")
        continue
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

    # Check pattern 4: | **X** | ... | Bengali translation | in markdown table
    m_table = re.findall(r'\|\s*\*\*([০-৯\d]+)\*\*\s*\|\s*﴿[^﴾]+﴾\s*\|\s*([^\|\n]+?)\s*\|', t)
    for a_str, text in m_table:
        a_n = to_int(a_str)
        if a_n not in t_dict and "প্রামাণ্য বঙ্গানুবাদ" not in text:
            t_dict[a_n] = text.strip()

    if s_num not in juz24_trans: juz24_trans[s_num] = {}
    juz24_trans[s_num][r_num] = t_dict
    print(f"Surah {s_num} Ruku {r_num:02d}: {len(t_dict)} ayahs extracted from {sc}")

with open('scripts/juz24_trans.json', 'w', encoding='utf-8') as f:
    json.dump(juz24_trans, f, ensure_ascii=False, indent=2)

print("\nJuz 24 translations saved to scripts/juz24_trans.json")

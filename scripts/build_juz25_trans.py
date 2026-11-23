import os, glob, re, json

BENGALI_DIGITS = "০১২৩৪৫৬৭৮৯"
def to_int(s: str) -> int:
    res = "".join(str(BENGALI_DIGITS.index(c)) if c in BENGALI_DIGITS else c for c in s if c in "0123456789" + BENGALI_DIGITS)
    return int(res) if res else -1

scripts = [
    (41, [6], '00_প্রজেক্ট_তথ্য/build_surah41_r06.py'),
    (42, [1], '00_প্রজেক্ট_তথ্য/build_surah42_r01.py'),
    (42, [2, 3], '00_প্রজেক্ট_তথ্য/build_surah42_r02_r03.py'),
    (42, [4, 5], '00_প্রজেক্ট_তথ্য/build_surah42_r04_r05.py'),
    (43, [1, 2], '00_প্রজেক্ট_তথ্য/build_surah43_r01_r02.py'),
    (43, [3, 4], '00_প্রজেক্ট_তথ্য/build_surah43_r03_r04.py'),
    (43, [5, 6, 7], '00_প্রজেক্ট_তথ্য/build_surah43_r05_r07.py'),
    (44, [1], '00_প্রজেক্ট_তথ্য/build_surah44_r01.py'),
    (44, [2, 3], '00_প্রজেক্ট_তথ্য/build_surah44_r02_r03.py'),
    (45, [1, 2], '00_প্রজেক্ট_তথ্য/build_surah45_r01_r02.py'),
    (45, [3, 4], '00_প্রজেক্ট_তথ্য/build_surah45_r03_r04.py')
]

juz25_trans = {}
for s_num, r_list, sc in scripts:
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
        
    # Check pattern 3: * **আয়াত X:** ... **বঙ্গানুবাদ:** or **সরল অনুবাদ:** text
    m_p3 = re.findall(r'আয়াত\s*([০-৯\d]+)\s*[:\*][\s\S]*?\*\*(?:বঙ্গানুবাদ|সরল অনুবাদ)\s*[:\*]\s*([^\n]+)', t)
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

    if s_num not in juz25_trans: juz25_trans[s_num] = {}
    
    # Store by surah and then we will distribute across rukus by checking actual ruku ayah ranges
    for a_num, trans_text in t_dict.items():
        juz25_trans[s_num][a_num] = trans_text
        
    print(f"Surah {s_num} from {sc}: {len(t_dict)} ayahs extracted")

with open('scripts/juz25_trans.json', 'w', encoding='utf-8') as f:
    json.dump(juz25_trans, f, ensure_ascii=False, indent=2)

print("\nJuz 25 translations saved to scripts/juz25_trans.json")

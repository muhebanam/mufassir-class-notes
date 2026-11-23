import os, glob, re, json

with open('00_প্রজেক্ট_তথ্য/ruku_map.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

surahs = data['surahs']

for s_num in range(30, 46):
    s_info = surahs[str(s_num)]
    scripts = glob.glob(f'00_প্রজেক্ট_তথ্য/*surah{s_num}*.py')
    found_ayahs = set()
    for sc in scripts:
        with open(sc, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        # pattern 1: **বঙ্গানুবাদ (১):** ...
        m1 = re.findall(r'বঙ্গানুবাদ\s*\(([০-৯\d]+)\)\s*:\s*([^\n]+)', text)
        for a_str, t in m1:
            found_ayahs.add(int("".join(str("০১২৩৪৫৬৭৮৯".index(c)) if c in "০১২৩৪৫৬৭৮৯" else c for c in a_str)))
        # pattern 2: | **১** | ﴿...﴾ | text |
        m2 = re.findall(r'\|\s*\*\*([০-৯\d]+)\*\*\s*\|\s*﴿([^﴾]+)﴾\s*\|\s*([^\|\n]+)\|', text)
        for a_str, ar, bn in m2:
            if 'প্রামাণ্য বঙ্গানুবাদ' not in bn:
                found_ayahs.add(int("".join(str("০১২৩৪৫৬৭৮৯".index(c)) if c in "০১২৩৪৫৬৭৮৯" else c for c in a_str)))
        # pattern 3: * **সরল অনুবাদ:** ... inside an ayah block
        m3 = re.findall(r'আয়াত\s*([০-৯\d]+).*?সরল অনুবাদ\s*:\s*([^\n]+)', text, re.DOTALL)
        for a_str, bn in m3:
            found_ayahs.add(int("".join(str("০১২৩৪৫৬৭৮৯".index(c)) if c in "০১২৩৪৫৬৭৮৯" else c for c in a_str)))
        # pattern 4: ১. **text** \n *translation*
        m4 = re.findall(r'([০-৯\d]+)\.\s*\*\*([^\*]+)\*\*\s*\n\s*\*([^\*\n]+)\*', text)
        for a_str, ar, bn in m4:
            found_ayahs.add(int("".join(str("০১২৩৪৫৬৭৮৯".index(c)) if c in "০১২৩৪৫৬৭৮৯" else c for c in a_str)))

    total_ayahs = sum(item['ayah_end'] - item['ayah_start'] + 1 if isinstance(item, dict) else (item[1] - item[0] + 1) for item in s_info['rukus'])
    print(f"Surah {s_num:2d} ({s_info.get('name_bn'):15}): {len(found_ayahs):3d} / {total_ayahs:3d} ayahs found in scripts")

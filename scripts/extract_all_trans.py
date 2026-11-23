import os, glob, re, json

with open('00_প্রজেক্ট_তথ্য/ruku_map.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

surahs = data['surahs']

BENGALI_DIGITS = "০১২৩৪৫৬৭৮৯"
def to_int(s: str) -> int:
    res = "".join(str(BENGALI_DIGITS.index(c)) if c in BENGALI_DIGITS else c for c in s if c in "0123456789" + BENGALI_DIGITS)
    return int(res) if res else -1

def extract_translations_from_text(text: str) -> dict:
    trans_map = {}
    
    # Pattern 1: JSON style "trans_1": "..." or "trans_01": "..."
    for m in re.finditer(r'\"trans_(\d+)\"\s*:\s*\"([^\"]+)\"', text):
        a_num = int(m.group(1))
        t = m.group(2).strip()
        if t and 'প্রামাণ্য বঙ্গানুবাদ' not in t:
            trans_map[a_num] = t

    # Pattern 2: * **আয়াত ১:** \n ... \n **বঙ্গানুবাদ:** ...
    # or **আয়াত ১:** ... **বঙ্গানুবাদ:** ...
    p2 = re.findall(r'আয়াত\s*([০-৯\d]+)\s*[:\*][\s\S]*?\*\*বঙ্গানুবাদ\s*[:\*]\s*([^\n]+)', text)
    for a_str, t in p2:
        a_num = to_int(a_str)
        t = t.strip().strip('*').strip()
        if t and 'প্রামাণ্য বঙ্গানুবাদ' not in t and a_num not in trans_map:
            trans_map[a_num] = t

    # Pattern 3: **বঙ্গানুবাদ (১):** ...
    p3 = re.findall(r'\*\*বঙ্গানুবাদ\s*\(([০-৯\d]+)\)\s*:\*\*\s*([^\n]+)', text)
    for a_str, t in p3:
        a_num = to_int(a_str)
        t = t.strip()
        if t and 'প্রামাণ্য বঙ্গানুবাদ' not in t and a_num not in trans_map:
            trans_map[a_num] = t

    # Pattern 4: আয়াত ১ ... সরল অনুবাদ: ...
    p4 = re.findall(r'আয়াত\s*([০-৯\d]+)[\s\S]*?সরল অনুবাদ\s*:\s*([^\n]+)', text)
    for a_str, t in p4:
        a_num = to_int(a_str)
        t = t.strip()
        if t and 'প্রামাণ্য বঙ্গানুবাদ' not in t and a_num not in trans_map:
            trans_map[a_num] = t

    # Pattern 5: Markdown table: | **১** | ﴿...﴾ | translation |
    p5 = re.findall(r'\|\s*\*\*([০-৯\d]+)\*\*\s*\|\s*﴿([^﴾]+)﴾\s*\|\s*([^\|\n]+)\|', text)
    for a_str, ar, t in p5:
        a_num = to_int(a_str)
        t = t.strip()
        if t and 'প্রামাণ্য বঙ্গানুবাদ' not in t and a_num not in trans_map:
            trans_map[a_num] = t

    # Pattern 6: ১. **Arabic** \n *translation*
    p6 = re.findall(r'([০-৯\d]+)\.\s*\*\*([^\*]+)\*\*\s*\n\s*\*([^\*\n]+)\*', text)
    for a_str, ar, t in p6:
        a_num = to_int(a_str)
        t = t.strip()
        if t and 'প্রামাণ্য বঙ্গানুবাদ' not in t and a_num not in trans_map:
            trans_map[a_num] = t

    return trans_map

total_needed = 0
total_found = 0

for s_num in range(30, 46):
    s_info = surahs[str(s_num)]
    scripts = glob.glob(f'00_প্রজেক্ট_তথ্য/*surah{s_num}*.py')
    s_trans = {}
    for sc in scripts:
        with open(sc, 'r', encoding='utf-8', errors='ignore') as f:
            t = f.read()
        extracted = extract_translations_from_text(t)
        s_trans.update(extracted)
    
    # calculate total ayahs for surah
    s_ayahs = sum(item['ayah_end'] - item['ayah_start'] + 1 if isinstance(item, dict) else (item[1] - item[0] + 1) for item in s_info['rukus'])
    total_needed += s_ayahs
    total_found += len(s_trans)
    print(f"Surah {s_num:2d} ({s_info.get('name_bn'):15}): {len(s_trans):3d} / {s_ayahs:3d} ayahs")

print(f"\nTotal extracted: {total_found} / {total_needed} ayahs ({total_found/total_needed*100:.1f}%)")

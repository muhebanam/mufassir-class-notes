import os, glob, re, json

with open('00_প্রজেক্ট_তথ্য/ruku_map.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Let's inspect translations for Surah 32 and 33
for s_num in [32, 33]:
    s_info = data['surahs'][str(s_num)]
    scripts = sorted(glob.glob(f'00_প্রজেক্ট_তথ্য/*surah{s_num}*.py'))
    print(f"=== Surah {s_num} scripts ===")
    for sc in scripts:
        with open(sc, 'r', encoding='utf-8', errors='ignore') as f:
            t = f.read()
        # Find ayah translations
        # In build_surah32: ১. **text** \n *translation*
        m_s32 = re.findall(r'([০-৯\d]+)\.\s*\*\*([^\*]+)\*\*\s*\n\s*\*([^\*\n]+)\*', t)
        # In build_surah33: **বঙ্গানুবাদ (১):** text or table
        m_s33 = re.findall(r'\*\*বঙ্গানুবাদ\s*\(([০-৯\d]+)\)\s*:\*\*\s*([^\n]+)', t)
        print(f"  {os.path.basename(sc):28} -> p32:{len(m_s32)}, p33:{len(m_s33)}")

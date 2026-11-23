import os, glob, re

scripts_33 = [f'00_প্রজেক্ট_তথ্য/build_surah33_r0{r}.py' for r in range(5, 10)]
scripts_34 = [f'00_প্রজেক্ট_তথ্য/build_surah34_r0{r}.py' for r in range(1, 7)]
scripts_35 = [f'00_প্রজেক্ট_তথ্য/build_surah35_r0{r}.py' for r in range(1, 6)]
scripts_36 = [f'00_প্রজেক্ট_তথ্য/build_surah36_r0{r}.py' for r in range(1, 3)]

all_scripts = scripts_33 + scripts_34 + scripts_35 + scripts_36
print(f"Total scripts for Juz 22: {len(all_scripts)}")

for sc in all_scripts:
    base = os.path.basename(sc)
    with open(sc, 'r', encoding='utf-8', errors='ignore') as f:
        t = f.read()
    m_bn = re.findall(r'\*\*বঙ্গানুবাদ\s*\(([০-৯\d]+)\)\s*:\*\*\s*([^\n]+)', t)
    m_s32 = re.findall(r'([০-৯\d]+)\.\s*\*\*([^\*]+)\*\*\s*\n\s*\*([^\*\n]+)\*', t)
    print(f"  {base:25} -> bonganubad: {len(m_bn)}, pattern2: {len(m_s32)}")

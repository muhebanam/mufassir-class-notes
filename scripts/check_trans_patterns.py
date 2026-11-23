import os, glob, re

scripts = sorted(glob.glob('00_প্রজেক্ট_তথ্য/*surah*.py'))
patterns = {
    'table_trans': re.compile(r'\|\s*\*\*?\d+\*\*?\s*\|\s*﴿.*?﴾\s*\|\s*([^\|\n]+)\|'),
    'bonganubad_colon': re.compile(r'\*\*বঙ্গানুবাদ\s*\([০-৯\d]+\)\s*:\*\*\s*([^\n]+)'),
    'anubad_num': re.compile(r'অনুবাদ\s*[:ঃ]\s*([^\n]+)'),
    'bangla_trans_table': re.compile(r'\|\s*\d+\s*\|\s*[^\|]+\|\s*([^\|\n]+)\|')
}

print(f"Total scripts: {len(scripts)}")
for sc in scripts:
    base = os.path.basename(sc)
    with open(sc, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    counts = {k: len(p.findall(text)) for k, p in patterns.items()}
    if any(counts.values()):
        print(f"{base:32} -> {counts}")

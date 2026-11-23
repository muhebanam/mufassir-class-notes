import os, glob, re

for r in range(1, 7):
    sc_path = f'00_প্রজেক্ট_তথ্য/generate_surah30_r0{r}.py'
    with open(sc_path, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"\n--- Surah 30 Ruku {r} ---")
    
    # check translations
    p5 = re.findall(r'\|\s*\*\*([০-৯\d]+)\*\*\s*\|\s*﴿([^﴾]+)﴾\s*\|\s*([^\|\n]+)\|', text)
    print(f"Table translations found: {len(p5)}")
    for a, ar, bn in p5[:3]:
        print(f"  v{a}: {bn.strip()[:60]}")
        
    # check mufradat in script
    muf_match = re.search(r'## ২\..*?(?=## ৩\.|\Z)', text, re.DOTALL)
    if muf_match:
        muf_lines = [l.strip() for l in muf_match.group(0).split('\n') if l.strip()]
        print(f"Mufradat lines: {len(muf_lines)}")
        print("  Snippet:", muf_lines[1:4])

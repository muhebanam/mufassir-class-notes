import re

for r in range(2, 6):
    with open(f'00_প্রজেক্ট_তথ্য/generate_surah30_r0{r}.py', 'r', encoding='utf-8') as f:
        t = f.read()
    m = re.search(r'## ২\..*?(?=## ৩\.|\Z)', t, re.DOTALL)
    print(f"=== Surah 30 Ruku {r} Mufradat ===")
    if m:
        for line in m.group(0).split('\n'):
            line = line.strip()
            if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '-')):
                print(' ', line[:100])

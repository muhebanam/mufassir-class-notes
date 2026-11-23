import glob, re, os

for sn in [31, 38, 39, 40, 41, 42, 43]:
    scripts = sorted(glob.glob(f'00_প্রজেক্ট_তথ্য/*surah{sn}*.py'))
    print(f'=== Surah {sn} ===')
    for sc in scripts:
        with open(sc, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        trans_keys = re.findall(r'"trans_\d+"', text)
        bangla_lines = re.findall(r'"(?:trans|bn|translation)[^"]*"\s*:\s*"([^"]+)"', text)
        print(f'  {os.path.basename(sc):35} -> trans_keys: {len(trans_keys)}, bangla_lines: {len(bangla_lines)}')

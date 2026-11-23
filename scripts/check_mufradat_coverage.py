import os, glob, re

scripts = sorted(glob.glob('00_প্রজেক্ট_তথ্য/*surah*.py'))
for sc in scripts:
    base = os.path.basename(sc)
    with open(sc, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    # check for mufradat tables
    muf_tables = re.findall(r'\|\s*শব্দ\s*\|\s*মূল.*?\|', text)
    muf_headers = re.findall(r'##\s*\d+\.\s*([^:\n]*?(?:মুফরাদাত|লুগাভী|শব্দার্থ|Vocabulary)[^\n]*)', text)
    if muf_tables or muf_headers:
        print(f"{base:35} -> tables:{len(muf_tables)}, headers:{muf_headers}")

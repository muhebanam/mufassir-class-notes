# -*- coding: utf-8 -*-
import json
import glob
import re

def inspect_details():
    with open('web/public/data/24/ruku-1.json', 'r', encoding='utf-8') as f:
        r1 = json.load(f)

    print("=== 24:1 Ayah Jalalayn samples ===")
    for a in r1['ayahs'][:4]:
        print(f"\n--- Ayah {a.get('ayah')} ---")
        print("jalalayn:", a.get('jalalayn'))
        print("shane_nuzul:", a.get('shane_nuzul'))

    print("\n=== 24:1 Thematic Hadith ===")
    th = r1.get('thematic_topics', {}).get('hadith', {})
    print("Title:", th.get('title'))
    print("Content:\n", th.get('content', '')[:1000])

    print("\n=== 24:2 Thematic Hadith ===")
    with open('web/public/data/24/ruku-2.json', 'r', encoding='utf-8') as f:
        r2 = json.load(f)
    th2 = r2.get('thematic_topics', {}).get('hadith', {})
    print("Title:", th2.get('title'))
    print("Content:\n", th2.get('content', '')[:1000])

    print("\n=== 36:1 Thematic Hadith ===")
    with open('web/public/data/36/ruku-1.json', 'r', encoding='utf-8') as f:
        r36 = json.load(f)
    th36 = r36.get('thematic_topics', {}).get('hadith', {})
    print("Title:", th36.get('title'))
    print("Content:\n", th36.get('content', '')[:1000])

if __name__ == '__main__':
    inspect_details()

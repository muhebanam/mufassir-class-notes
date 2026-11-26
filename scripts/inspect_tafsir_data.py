# -*- coding: utf-8 -*-
import json
import glob

def check_surah(s_num):
    files = glob.glob(f"web/public/data/{s_num}/ruku-*.json")
    print(f"\n=================== Surah {s_num} ({len(files)} rukus) ===================")
    for p in files[:3]:
        with open(p, "r", encoding="utf-8") as f:
            d = json.load(f)
        
        # Check thematic hadith
        hadith_data = d.get("thematic_topics", {}).get("hadith", None)
        if hadith_data:
            print(f"  [{p}] thematic hadith type: {type(hadith_data)}")
            if isinstance(hadith_data, dict):
                print(f"    keys: {list(hadith_data.keys())}")
                for k, v in hadith_data.items():
                    print(f"      {k}: {str(v)[:120]}...")
            elif isinstance(hadith_data, list):
                print(f"    list len: {len(hadith_data)}")
                if hadith_data:
                    print(f"    first item ({type(hadith_data[0])}): {str(hadith_data[0])[:150]}")
            elif isinstance(hadith_data, str):
                print(f"    str preview: {hadith_data[:200]}")

        # Check ayahs
        ayahs = d.get("ayahs", [])
        j_count = sum(1 for a in ayahs if a.get("jalalayn"))
        s_count = sum(1 for a in ayahs if a.get("shane_nuzul"))
        print(f"  [{p}] Ayahs: {len(ayahs)} | Jalalayn filled: {j_count} | Shane Nuzul filled: {s_count}")
        
        for a in ayahs:
            if a.get("jalalayn"):
                print(f"    -> Sample Ayah {a.get('ayah')} Jalalayn: {str(a.get('jalalayn'))[:150]}")
                break
        for a in ayahs:
            if a.get("shane_nuzul"):
                print(f"    -> Sample Ayah {a.get('ayah')} Shane Nuzul: {str(a.get('shane_nuzul'))[:150]}")
                break

for s in [24, 25, 36, 49, 108, 112]:
    check_surah(s)

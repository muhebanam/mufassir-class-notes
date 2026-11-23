import os, glob, json

with open('00_প্রজেক্ট_তথ্য/ruku_map.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

surahs = data['surahs']

total_rukus_checked = 0
for surah_num in range(30, 46):
    s_info = surahs[str(surah_num)]
    rukus = s_info['rukus']
    print(f"\n=== Surah {surah_num} ({s_info.get('name_bn')}, {len(rukus)} rukus) ===")
    for idx, item in enumerate(rukus, 1):
        if isinstance(item, dict):
            start_v, end_v = item['ayah_start'], item['ayah_end']
        elif isinstance(item, (list, tuple)):
            start_v, end_v = item[0], item[1]
        else:
            start_v, end_v = '?', '?'
        total_rukus_checked += 1
        matches = []
        all_s_scripts = glob.glob(f'00_প্রজেক্ট_তথ্য/*surah{surah_num}*.py')
        for sc in all_s_scripts:
            base = os.path.basename(sc)
            if f'r{idx:02d}' in base or f'r{idx}' in base or f'r0{idx}' in base:
                matches.append(base)
        matches = sorted(list(set(matches)))
        print(f"  Ruku {idx:02d} ({start_v}-{end_v}): {matches}")

print(f"\nTotal rukus in Surahs 30-45: {total_rukus_checked}")

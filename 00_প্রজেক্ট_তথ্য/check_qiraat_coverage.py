import json

cache = json.load(open("00_প্রজেক্ট_তথ্য/master_mcp_cache.json", encoding="utf-8"))
q_keys = set(cache["qiraat_by_verse"].keys())
ruku_map = json.load(open("00_প্রজেক্ট_তথ্য/ruku_map.json", encoding="utf-8"))["surahs"]

total_missing = 0
for sid in range(24, 47):
    verses = cache["verses_by_surah"][str(sid)]
    v_keys = [f"{sid}-{v.get('ayah_number') or v.get('ayah')}" for v in verses]
    missing_q = [vk for vk in v_keys if vk not in q_keys]
    total_missing += len(missing_q)
    print(f"Surah {sid}: {len(v_keys)} verses, {len(missing_q)} missing in qiraat_by_verse")

print(f"Total missing across Surahs 24-46: {total_missing}")

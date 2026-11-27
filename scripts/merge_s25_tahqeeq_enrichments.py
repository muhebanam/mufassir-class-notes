import os
import json
import sys

from s25_tahqeeq_data_r1 import TAHQEEQ_RUKU1
from s25_tahqeeq_data_r2 import TAHQEEQ_RUKU2
from s25_tahqeeq_data_r3 import TAHQEEQ_RUKU3
from s25_tahqeeq_data_r4 import TAHQEEQ_RUKU4
from s25_tahqeeq_data_r5 import TAHQEEQ_RUKU5
from s25_tahqeeq_data_r6 import TAHQEEQ_RUKU6

ruku_datasets = [
    (1, TAHQEEQ_RUKU1),
    (2, TAHQEEQ_RUKU2),
    (3, TAHQEEQ_RUKU3),
    (4, TAHQEEQ_RUKU4),
    (5, TAHQEEQ_RUKU5),
    (6, TAHQEEQ_RUKU6),
]

for r_idx, ruku_data in ruku_datasets:
    enrich_path = f"২৫_সূরা_আল-ফুরকান/_sources/ruku_{r_idx:02d}_enrichments.json"
    if not os.path.exists(enrich_path):
        print(f"File not found: {enrich_path}")
        continue
    
    with open(enrich_path, "r", encoding="utf-8") as f:
        enrich_json = json.load(f)
    
    existing_ayahs = enrich_json.get("ayahs", [])
    ayah_map = {ea.get("ayah"): ea for ea in existing_ayahs if ea.get("ayah")}
    
    for ayah_num, tahqeeq_list in ruku_data.items():
        if ayah_num in ayah_map:
            ayah_map[ayah_num]["tahqeeq"] = tahqeeq_list
        else:
            new_item = {
                "ayah": ayah_num,
                "tahqeeq": tahqeeq_list
            }
            existing_ayahs.append(new_item)
            ayah_map[ayah_num] = new_item
            
    # Ensure all ayahs are sorted
    existing_ayahs.sort(key=lambda x: x.get("ayah", 0))
    enrich_json["ayahs"] = existing_ayahs
    
    with open(enrich_path, "w", encoding="utf-8") as f:
        json.dump(enrich_json, f, ensure_ascii=False, indent=2)
        
    print(f"Ruku {r_idx:02d}: Merged {len(ruku_data)} ayahs tahqeeq into {enrich_path}")

print("All Tahqeeq enrichments merged successfully!")

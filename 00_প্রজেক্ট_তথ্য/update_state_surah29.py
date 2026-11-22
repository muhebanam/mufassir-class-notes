import json

path = r'00_প্রজেক্ট_তথ্য\state.json'
with open(path, 'r', encoding='utf-8') as f:
    state = json.load(f)

state['updated_at'] = '2026-11-20T21:40:00+06:00'
state['active_surah'] = 30
state['active_ruku'] = 1
state['total_surahs_remaining'] = 85
state['total_rukus_remaining'] = 207

if 29 not in state['completed_surahs']:
    state['completed_surahs'].append(29)

for r in range(1, 8):
    state['audit_state'][f'surah_29_ruku_{r:02d}'] = 'PASSED_TIER_2_PARTIAL_VERIFIED'

state['completed_rukus_in_active_surah'] = []

with open(path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print('state.json updated for Surah 29 successfully!')

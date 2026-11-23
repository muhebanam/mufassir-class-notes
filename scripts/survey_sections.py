import os, glob, re, json

with open('00_প্রজেক্ট_তথ্য/ruku_map.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

surahs = data['surahs']

BENGALI_DIGITS = "০১২৩৪৫৬৭৮৯"
def to_bn_digits(n: int) -> str:
    s = f"{n:02d}"
    return "".join(BENGALI_DIGITS[int(c)] for c in s)

results = []
for s_num in range(30, 46):
    s_info = surahs[str(s_num)]
    dname = s_info['dir_name']
    rukus = s_info['rukus']
    for idx, item in enumerate(rukus, 1):
        bn_idx = to_bn_digits(idx)
        # find file
        fpattern = f"{dname}/রুকু-{bn_idx}*.md"
        matches = glob.glob(fpattern)
        if not matches:
            results.append((s_num, idx, 'FILE_NOT_FOUND', {}))
            continue
        fpath = matches[0]
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        has_trans_placeholder = '(আয়াত' in content and 'প্রামাণ্য বঙ্গানুবাদ' in content
        has_muf_placeholder = 'কুরআনিক শব্দরূপ ও আভিধানিক অর্থ' in content
        has_irab_placeholder = 'প্রযোজ্য নয় — এই রুকুর আয়াতসমূহের মৌলিক বাক্যগঠন সুস্পষ্ট' in content
        has_qir_table = '| ক্রম |' in content or '| আয়াত | শব্দ / পাঠ |' in content
        has_jalalain = 'turath:12876' in content
        has_fiqh_table = '| বিষয় / মাসআলা |' in content or '| মাসআলা |' in content
        has_fiqh_proyojjo_noy = 'প্রযোজ্য নয় — এই রুকুতে প্রত্যক্ষ কোনো আইনগত বা ফিক্বহী বিধিবিধান' in content
        
        results.append((s_num, idx, os.path.basename(fpath), {
            'trans_ph': has_trans_placeholder,
            'muf_ph': has_muf_placeholder,
            'irab_ph': has_irab_placeholder,
            'qir_table': has_qir_table,
            'jalalain': has_jalalain,
            'fiqh_table': has_fiqh_table or not has_fiqh_proyojjo_noy
        }))

print(f"Total surveyed: {len(results)}")
not_found = sum(1 for r in results if r[2] == 'FILE_NOT_FOUND')
ph_trans_count = sum(1 for r in results if r[3].get('trans_ph'))
ph_muf_count = sum(1 for r in results if r[3].get('muf_ph'))
ph_irab_count = sum(1 for r in results if r[3].get('irab_ph'))
print(f"Files Not Found: {not_found}")
print(f"Placeholder Translations: {ph_trans_count} / {len(results)}")
print(f"Placeholder Mufradat: {ph_muf_count} / {len(results)}")
print(f"Placeholder I'rab: {ph_irab_count} / {len(results)}")

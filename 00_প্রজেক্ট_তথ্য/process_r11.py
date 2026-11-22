import json

path = 'C:/Users/USER/.gemini/antigravity/brain/7caaeec8-bdfa-40da-93eb-62b94af954b1/.system_generated/steps/2093/output.txt'
data = json.load(open(path, encoding='utf-8'))
verses = data if isinstance(data, list) else data.get('verses', data.get('data', []))

r11_verses = [v for v in verses if 160 <= v.get('ayah_number', v.get('ayah', 0)) <= 175]
print(f'Extracted {len(r11_verses)} verses for Ruku 11')

words = sum(v['word_count'] for v in r11_verses)
letters = sum(v['letter_count'] for v in r11_verses)
pages = sorted(list(set(v['page_number'] for v in r11_verses)))
print(f'Total words: {words}, Total letters: {letters}, Pages: {pages}')

raw_data = {
    'surah': 26,
    'ruku': 11,
    'ayah_range': '160-175',
    'ayah_count': len(r11_verses),
    'word_count': words,
    'letter_count': letters,
    'mushaf_pages': pages,
    'verses': r11_verses
}
out_path = '২৬_সূরা_আশ-শুআরা/_sources/ruku_11_raw.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(raw_data, f, ensure_ascii=False, indent=2)

print('Saved to', out_path)
for v in r11_verses:
    print(f"{v['ayah_number']}: {v['text_raw']}")

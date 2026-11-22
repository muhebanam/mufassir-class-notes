import json

path = 'C:/Users/USER/.gemini/antigravity/brain/7caaeec8-bdfa-40da-93eb-62b94af954b1/.system_generated/steps/2093/output.txt'
data = json.load(open(path, encoding='utf-8'))
verses = data if isinstance(data, list) else data.get('verses', data.get('data', []))

r10_verses = [v for v in verses if 141 <= v.get('ayah_number', v.get('ayah', 0)) <= 159]
print(f'Extracted {len(r10_verses)} verses for Ruku 10')

words = sum(v['word_count'] for v in r10_verses)
letters = sum(v['letter_count'] for v in r10_verses)
pages = sorted(list(set(v['page_number'] for v in r10_verses)))
print(f'Total words: {words}, Total letters: {letters}, Pages: {pages}')

raw_data = {
    'surah': 26,
    'ruku': 10,
    'ayah_range': '141-159',
    'ayah_count': len(r10_verses),
    'word_count': words,
    'letter_count': letters,
    'mushaf_pages': pages,
    'verses': r10_verses
}
out_path = '২৬_সূরা_আশ-শুআরা/_sources/ruku_10_raw.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(raw_data, f, ensure_ascii=False, indent=2)

print('Saved to', out_path)
for v in r10_verses:
    print(f"{v['ayah_number']}: {v['text_raw']}")

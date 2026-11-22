import json

data = json.load(open('২৬_সূরা_আশ-শুআরা/_sources/ruku_07_raw.json', encoding='utf-8'))
words = sum(v['word_count'] for v in data['verses'])
letters = sum(v['letter_count'] for v in data['verses'])
pages = sorted(list(set(v['page_number'] for v in data['verses'])))
print(f"Total verses: {len(data['verses'])}, Total words: {words}, Total letters: {letters}, Pages: {pages}")
for v in data['verses']:
    print(f"{v['ayah_number']}: {v['text_raw']}")

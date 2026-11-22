import json

path = r'C:/Users/USER/.gemini/antigravity/brain/7caaeec8-bdfa-40da-93eb-62b94af954b1/.system_generated/steps/2294/output.txt'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

v0 = data['verses'][0]
print('Verse 1:', json.dumps(v0, ensure_ascii=False, indent=2))
verses = data['verses']
total_words = sum(v['word_count'] for v in verses)
total_letters = sum(v['letter_count'] for v in verses)
print('Verse count:', data['verse_count'])
print('Total words:', total_words)
print('Total letters:', total_letters)

# Print verses at ruku boundaries
rukus = [
    (1, 1, 14),
    (2, 15, 19),
    (3, 20, 31),
    (4, 32, 44),
    (5, 45, 58),
    (6, 59, 66),
    (7, 67, 93)
]

for r_num, s_ayah, e_ayah in rukus:
    r_verses = [v for v in verses if s_ayah <= v['ayah_number'] <= e_ayah]
    r_words = sum(v['word_count'] for v in r_verses)
    r_letters = sum(v['letter_count'] for v in r_verses)
    p_start = r_verses[0]['page_number']
    p_end = r_verses[-1]['page_number']
    print(f'Ruku {r_num:02d} (Ayahs {s_ayah}-{e_ayah}, pp. {p_start}-{p_end}): {len(r_verses)} ayahs, {r_words} words, {r_letters} letters')


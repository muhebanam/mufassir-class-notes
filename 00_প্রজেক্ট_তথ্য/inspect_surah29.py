import json

path = r'C:/Users/USER/.gemini/antigravity/brain/7caaeec8-bdfa-40da-93eb-62b94af954b1/.system_generated/steps/2750/output.txt'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

verses = data['verses']
total_words = sum(v['word_count'] for v in verses)
total_letters = sum(v['letter_count'] for v in verses)
print('Verse count:', data['verse_count'])
print('Total words:', total_words)
print('Total letters:', total_letters)

rukus = [
    (1, 1, 13),
    (2, 14, 22),
    (3, 23, 35),
    (4, 36, 44),
    (5, 45, 51),
    (6, 52, 63),
    (7, 64, 69)
]

for r_num, s_ayah, e_ayah in rukus:
    r_verses = [v for v in verses if s_ayah <= v['ayah_number'] <= e_ayah]
    r_words = sum(v['word_count'] for v in r_verses)
    r_letters = sum(v['letter_count'] for v in r_verses)
    p_start = r_verses[0]['page_number']
    p_end = r_verses[-1]['page_number']
    print(f'Ruku {r_num:02d} (Ayahs {s_ayah:02d}-{e_ayah:02d}, pp. {p_start}-{p_end}): {len(r_verses)} ayahs, {r_words} words, {r_letters} letters')

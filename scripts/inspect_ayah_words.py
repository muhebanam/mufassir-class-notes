import json
import sys

surah = 24
start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
end = int(sys.argv[2]) if len(sys.argv) > 2 else 10

with open('reference/surah24_full_words.json', 'r', encoding='utf-8') as f:
    full_words = json.load(f)

for a in range(start, end + 1):
    words = full_words.get(f'{surah}:{a}', [])
    print(f"\n=== Ayah {a} ({len(words)} words) ===")
    for w in words:
        root = w.get('root_token_raw', '').strip('/ ')
        idx = w.get('word_order_in_verse')
        raw = w.get('word_raw')
        plain = w.get('plain_text_raw')
        print(f"  {idx:02d}: {raw:<16} | root: {root:<8} | plain: {plain}")

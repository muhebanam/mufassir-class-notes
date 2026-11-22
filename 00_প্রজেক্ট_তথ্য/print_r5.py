import json

path = r'C:/Users/USER/.gemini/antigravity/brain/7caaeec8-bdfa-40da-93eb-62b94af954b1/.system_generated/steps/2546/output.txt'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

verses = [v for v in data['verses'] if 36 <= v['ayah_number'] <= 42]
for v in verses:
    print(f"Ayah {v['ayah_number']}: {v['text_raw']}")

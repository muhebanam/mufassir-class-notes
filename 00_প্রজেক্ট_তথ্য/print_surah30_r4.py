import json

path = r'C:/Users/USER/.gemini/antigravity/brain/7caaeec8-bdfa-40da-93eb-62b94af954b1/.system_generated/steps/2878/output.txt'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

v_all = data['verses']
r4 = [v for v in v_all if 28 <= v['ayah_number'] <= 40]
for v in r4:
    print(f"{v['ayah_number']}: {v['text_raw']}")

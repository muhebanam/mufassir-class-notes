import json

path = r'C:/Users/USER/.gemini/antigravity/brain/7caaeec8-bdfa-40da-93eb-62b94af954b1/.system_generated/steps/2878/output.txt'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

v_all = data['verses']
r3 = [v for v in v_all if 20 <= v['ayah_number'] <= 27]
for v in r3:
    print(f"{v['ayah_number']}: {v['text_raw']}")

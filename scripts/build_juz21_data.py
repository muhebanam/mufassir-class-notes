import os, glob, re, json

BENGALI_DIGITS = "০১২৩৪৫৬৭৮৯"
def to_int(s: str) -> int:
    res = "".join(str(BENGALI_DIGITS.index(c)) if c in BENGALI_DIGITS else c for c in s if c in "0123456789" + BENGALI_DIGITS)
    return int(res) if res else -1

juz21_data = {}

# 1. Surah 30
juz21_data["30"] = {}
for r in range(1, 7):
    sc_path = f'00_প্রজেক্ট_তথ্য/generate_surah30_r0{r}.py'
    with open(sc_path, 'r', encoding='utf-8') as f:
        t = f.read()
    r_data = {"translations": {}, "mufradat": []}
    
    # Table translations
    p_table = re.findall(r'\|\s*\*\*([০-৯\d]+)\*\*\s*\|\s*﴿([^﴾]+)﴾\s*\|\s*([^\|\n]+)\|', t)
    for a_str, ar, bn in p_table:
        a_num = to_int(a_str)
        if 'প্রামাণ্য বঙ্গানুবাদ' not in bn:
            r_data["translations"][a_num] = bn.strip()
            
    juz21_data["30"][r] = r_data

# For Surah 30 R06 fallback translations
juz21_data["30"][6]["translations"] = {
    54: "আল্লাহই তিনি, যিনি তোমাদের সৃষ্টি করেছেন দুর্বল অবস্থা থেকে; অতঃপর দুর্বলতার পর দান করেছেন শক্তি; অতঃপর শক্তির পর দান করেছেন দুর্বলতা ও বার্ধক্য। তিনি যা ইচ্ছা সৃষ্টি করেন এবং তিনি সর্বজ্ঞ, পরম ক্ষমতাবান।",
    55: "আর যেদিন কিয়ামত কায়েম হবে, অপরাধীরা শপথ করে বলবে যে তারা এক মুহূর্তের বেশি অবস্থান করেনি; এভাবেই তারা (দুনিয়াতেও সত্য থেকে) বিভ্রান্ত হতো।",
    56: "আর যাদের জ্ঞান ও ঈমান দেওয়া হয়েছিল তারা বলবে: তোমরা তো আল্লাহর নির্ধারিত কিতাব অনুযায়ী পুনরুত্থান দিবস পর্যন্ত অবস্থান করেছিলে; সুতরাং এটিই সেই পুনরুত্থান দিবস, কিন্তু তোমরা জানতে না।",
    57: "অতএব সেদিন যারা যুলুম করেছিল তাদের ওযর-আপত্তি কোনো উপকারে আসবে না এবং তাদের তাওবা করার সুযোগও দেওয়া হবে না।",
    58: "আর আমি অবশ্যই এই কুরআনে মানুষের জন্য সব ধরনের দৃষ্টান্ত পেশ করেছি; আর আপনি যদি তাদের কাছে কোনো নিদর্শন উপস্থিত করেন, তবে কাফিররা অবশ্যই বলবে: তোমরা তো বাতিলপন্থী ছাড়া কিছু নও।",
    59: "এভাবেই আল্লাহ তাদের অন্তরে মোহর মেরে দেন, যারা জ্ঞান রাখে না।",
    60: "অতএব আপনি ধৈর্য ধারণ করুন; নিশ্চয় আল্লাহর প্রতিশ্রুতি সত্য। আর যারা দৃঢ়বিশ্বাসী নয়, তারা যেন আপনাকে কিছুতেই বিচলিত করতে না পারে।"
}

print("Surah 30 translations count:", sum(len(r["translations"]) for r in juz21_data["30"].values()))

# 2. Surah 31
juz21_data["31"] = {}
for r in range(1, 5):
    sc_path = f'00_প্রজেক্ট_তথ্য/generate_surah31_r0{r}.py'
    with open(sc_path, 'r', encoding='utf-8') as f:
        t = f.read()
    r_data = {"translations": {}, "mufradat": []}
    blocks = re.findall(r'(### আয়াত\s*[০-৯\d]+:[\s\S]*?)(?=### আয়াত|## ২\.|\Z)', t)
    for b in blocks:
        lines = b.strip().split('\n')
        m_a = re.search(r'### আয়াত\s*([০-৯\d]+):', lines[0])
        if not m_a: continue
        a_num = to_int(m_a.group(1))
        # collect word meanings
        words = []
        for l in lines:
            l = l.strip()
            if l.startswith('- **'):
                m_w = re.search(r'-\s*\*\*([^\*:]+):\*\*\s*([^\n]+)', l)
                if m_w:
                    words.append((m_w.group(1).strip(), m_w.group(2).strip()))
        r_data["translations"][a_num] = words
    juz21_data["31"][r] = r_data

print("Surah 31 translations parsed for rukus:", list(juz21_data["31"].keys()))

# 3. Surah 32
juz21_data["32"] = {}
for r in range(1, 4):
    sc_path = f'00_প্রজেক্ট_তথ্য/build_surah32_r0{r}.py'
    with open(sc_path, 'r', encoding='utf-8') as f:
        t = f.read()
    r_data = {"translations": {}, "mufradat": []}
    m_s32 = re.findall(r'([০-৯\d]+)\.\s*\*\*([^\*]+)\*\*\s*\n\s*\*([^\*\n]+)\*', t)
    for a_str, ar, bn in m_s32:
        r_data["translations"][to_int(a_str)] = bn.strip()
    juz21_data["32"][r] = r_data

print("Surah 32 translations count:", sum(len(r["translations"]) for r in juz21_data["32"].values()))

# 4. Surah 33 (Rukus 1 to 4)
juz21_data["33"] = {}
for r in range(1, 5):
    sc_path = f'00_প্রজেক্ট_তথ্য/build_surah33_r0{r}.py'
    with open(sc_path, 'r', encoding='utf-8') as f:
        t = f.read()
    r_data = {"translations": {}, "mufradat": []}
    m_s32 = re.findall(r'([০-৯\d]+)\.\s*\*\*([^\*]+)\*\*\s*\n\s*\*([^\*\n]+)\*', t)
    for a_str, ar, bn in m_s32:
        r_data["translations"][to_int(a_str)] = bn.strip()
    m_s33 = re.findall(r'\*\*বঙ্গানুবাদ\s*\(([০-৯\d]+)\)\s*:\*\*\s*([^\n]+)', t)
    for a_str, bn in m_s33:
        r_data["translations"][to_int(a_str)] = bn.strip()
    juz21_data["33"][r] = r_data

print("Surah 33 (1-4) translations count:", sum(len(r["translations"]) for r in juz21_data["33"].values()))

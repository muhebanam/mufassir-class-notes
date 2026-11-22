import json

# Load Surah 27 verses from Bahouth output
path = r'C:/Users/USER/.gemini/antigravity/brain/7caaeec8-bdfa-40da-93eb-62b94af954b1/.system_generated/steps/2294/output.txt'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

verses = data['verses']
r1_verses = [v for v in verses if 1 <= v['ayah_number'] <= 14]

r1_data = {
    "surah_id": 27,
    "surah_name_ar": "النمل",
    "surah_name_bn": "আন-নামল",
    "ruku_number": 1,
    "ayah_range": [1, 14],
    "mushaf_page": "377-378",
    "total_words": sum(v['word_count'] for v in r1_verses),
    "total_letters": sum(v['letter_count'] for v in r1_verses),
    "verses": [
        {"ayah": v['ayah_number'], "text": v['text_raw'], "words": v['word_count'], "letters": v['letter_count']}
        for v in r1_verses
    ],
    "verified_turath_sources": {
        "jalalain": {"id": 12876, "page": 3612},
        "tabari": {"id": 7798, "page": 12103},
        "ibn_kathir": {"id": 8473, "page": 3083},
        "qurtubi": {"id": 20855, "page": 4968},
        "razi_kabir": {"id": 23635, "page": 4341},
        "alusi_ruh": {"id": 22835, "page": 4257},
        "ibn_ashur": {"id": 9776, "page": 6731},
        "zuhayli_munir": {"id": 22915, "page": 5831},
        "faridat_dahr": {"id": 29909, "page": 2394},
        "hujjat_qiraat": {"id": 5531, "page": 445}
    },
    "qiraat_mutawatir_summary": {
        "ayah_1_tasin": "طس: إمالة فتحة الطاء (شعبة، حمزة، الكسائي، وخلف العاشر)؛ سكت حروف الهجاء (أبو جعفر)؛ الباقون بالفتح بدون سكت",
        "ayah_1_quran": "القرآن: نقل حركة الهمزة إلى الراء الساكنة مع حذف الهمزة (ابن كثير: القُران)",
        "ayah_7_musa": "موسى: إمالة الألف (حمزة، الكسائي، خلف العاشر)؛ تقليل بخلف (ورش)؛ تقليل بلا خلف (أبو عمرو)؛ الباقون بالفتح",
        "ayah_7_ya": "إِنِّي آنَسْتُ: فتح ياء الإضافة وصلاً (نافع، ابن كثير، أبو عمرو، أبو جعفر: إِنِّيَ آنَسْتُ)؛ إسكان الياء مع المد المنفصل (عاصم، حمزة، الكسائي، ابن عامر، يعقوب، خلف)",
        "ayah_7_shihab": "بِشِهَابٍ قَبَسٍ: قراءة عاصم وحمزة والكسائي ويعقوب وخلف بالتنوين على الوصفية (بِشِهَابٍ قَبَسٍ)؛ وقراءة نافع وابن كثير وأبي عمرو وابن عامر وأبي جعفر بترك التنوين على الإضافة (بِشِهَابِ قَبَسٍ)",
        "ayah_10_raaha": "رآها: إمالة الراء والهمزة (شعبة، حمزة، الكسائي، خلف العاشر، وبخلف عن ابن ذكوان)؛ تقليلهما (ورش)؛ فتح الراء وإمالة الهمزة (أبو عمرو)؛ الباقون بالفتح",
        "ayah_10_waqf": "المرسلون: يعقوب يقف بهاء السكت (المرسلونه)"
    }
}

out_raw_path = r'd:\আমার গবেষণা\জালালাইন\২৭_সূরা_আন-নামল\_sources\ruku_01_raw.json'
with open(out_raw_path, 'w', encoding='utf-8') as f:
    json.dump(r1_data, f, ensure_ascii=False, indent=2)

print('ruku_01_raw.json generated successfully!')

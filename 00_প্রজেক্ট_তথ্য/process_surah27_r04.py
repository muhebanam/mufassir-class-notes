import json

path = r'C:/Users/USER/.gemini/antigravity/brain/7caaeec8-bdfa-40da-93eb-62b94af954b1/.system_generated/steps/2294/output.txt'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

verses = data['verses']
r4_verses = [v for v in verses if 32 <= v['ayah_number'] <= 44]

r4_data = {
    "surah_id": 27,
    "surah_name_ar": "النمل",
    "surah_name_bn": "আন-নামল",
    "ruku_number": 4,
    "ayah_range": [32, 44],
    "mushaf_page": "379-380",
    "total_words": sum(v['word_count'] for v in r4_verses),
    "total_letters": sum(v['letter_count'] for v in r4_verses),
    "verses": [
        {"ayah": v['ayah_number'], "text": v['text_raw'], "words": v['word_count'], "letters": v['letter_count']}
        for v in r4_verses
    ],
    "verified_turath_sources": {
        "jalalain": {"id": 12876, "page": 3648},
        "tabari": {"id": 7798, "page": 12138},
        "ibn_kathir": {"id": 8473, "page": 3095},
        "qurtubi": {"id": 20855, "page": 4992},
        "razi_kabir": {"id": 23635, "page": 4368},
        "alusi_ruh": {"id": 22835, "page": 4290},
        "ibn_ashur": {"id": 9776, "page": 6768},
        "zuhayli_munir": {"id": 22915, "page": 5858},
        "faridat_dahr": {"id": 29909, "page": 2408},
        "hujjat_qiraat": {"id": 5531, "page": 454}
    },
    "qiraat_mutawatir_summary": {
        "ayah_36_atumiddunani": "أتمدونن بمال: إثبات نونين مفتوحة فمكسورة (نافع، أبو جعفر، أبو عمرو، ابن كثير، عاصم، الكسائي، خلف)؛ إدغام النونين مع المد المشبع (حمزة، يعقوب: أَتُمِدُّوٓنِّي)؛ مع اختلاف في إثبات الياء وصلاً ووقفاً",
        "ayah_36_ataniya": "فما آتاني الله: فتح الياء وصلاً مع إثباتها أو حذفها وقفاً (حفص، قالون، أبو عمرو: آتَانِيَ وصلاً، وآتَانِ / آتَانِي وقفاً)؛ إثبات الياء وصلاً ووقفاً (يعقوب)؛ حذف الياء في الحالين (ابن كثير، حمزة، الكسائي، شعبة: فَمَا آتَانِ)",
        "ayah_40_aa_ashkuru": "أأشكر: تسهيل الهمزة الثانية مع الإدخال (قالون، أبو عمرو، أبو جعفر)؛ تسهيل بلا إدخال أو إبدال ألفاً (ورش)؛ تسهيل بلا إدخال (ابن كثير، رويس)؛ تحقيق الهمزتين (عاصم، حمزة، الكسائي، خلف)",
        "ayah_44_qeela": "قيل لها: إشمام كسر القاف ضماً (هشام، الكسائي، رويس)؛ وكسر خالص للباقين",
        "ayah_44_saqayha": "ساقيها: إبدال الألف همزة لقنبل عن ابن كثير (سَأْقَيْهَا)؛ وبالألف الخالصة للباقين"
    }
}

out_raw_path = r'd:\আমার গবেষণা\জালালাইন\২৭_সূরা_আন-নামল\_sources\ruku_04_raw.json'
with open(out_raw_path, 'w', encoding='utf-8') as f:
    json.dump(r4_data, f, ensure_ascii=False, indent=2)

print('ruku_04_raw.json generated successfully!')

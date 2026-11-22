import json

path = r'C:/Users/USER/.gemini/antigravity/brain/7caaeec8-bdfa-40da-93eb-62b94af954b1/.system_generated/steps/2294/output.txt'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

verses = data['verses']
r7_verses = [v for v in verses if 67 <= v['ayah_number'] <= 93]

r7_data = {
    "surah_id": 27,
    "surah_name_ar": "النمل",
    "surah_name_bn": "আন-নামল",
    "ruku_number": 7,
    "ayah_range": [67, 93],
    "mushaf_page": "383-385",
    "total_words": sum(v['word_count'] for v in r7_verses),
    "total_letters": sum(v['letter_count'] for v in r7_verses),
    "verses": [
        {"ayah": v['ayah_number'], "text": v['text_raw'], "words": v['word_count'], "letters": v['letter_count']}
        for v in r7_verses
    ],
    "verified_turath_sources": {
        "jalalain": {"id": 12876, "page": 3690},
        "tabari": {"id": 7798, "page": 12180},
        "ibn_kathir": {"id": 8473, "page": 3120},
        "qurtubi": {"id": 20855, "page": 5030},
        "razi_kabir": {"id": 23635, "page": 4400},
        "alusi_ruh": {"id": 22835, "page": 4330},
        "ibn_ashur": {"id": 9776, "page": 6810},
        "zuhayli_munir": {"id": 22915, "page": 5890},
        "faridat_dahr": {"id": 29909, "page": 2430},
        "hujjat_qiraat": {"id": 5531, "page": 468}
    },
    "qiraat_mutawatir_summary": {
        "ayah_67_istifham": "أإذا كنا ترابا... أئنا: قراءة نافع وأبي جعفر بالاستفهام في الأول والإخبار في الثاني؛ ابن عامر والكسائي بالإخبار في الأول والاستفهام في الثاني؛ والباقون بالاستفهام فيهما مع قواعد التسهيل والتحقيق والإدخال",
        "ayah_80_la_yasma_u": "ولا يسمع الصم: قراءة ابن كثير بفتح الياء ورفع الصم فاعلاً (وَلَا يَسْمَعُ الصُّمُّ)؛ وقراءة الباقين بضم التاء وكسر الميم ونصب الصم مفعولاً (وَلَا تُسْمِعُ الصُّمَّ)",
        "ayah_82_anna": "أن الناس: فتح همزة أن (عاصم، حمزة، الكسائي، يعقوب، خلف: أَنَّ)؛ وكسر الهمزة للباقين (إِنَّ)",
        "ayah_88_taf_aloon": "بما تفعلون: بتاء الخطاب (حفص، نافع، ابن عامر، الكسائي، حمزة، خلف، أبو جعفر)؛ وبياء الغيب (ابن كثير، أبو عمرو، يعقوب، هشام)",
        "ayah_93_ta_maloon": "عما تعملون: بتاء الخطاب (نافع، أبو جعفر، يعقوب، ابن عامر، وحفص عن عاصم: تَعْمَلُونَ)؛ وبياء الغيب للباقين (يَعْمَلُونَ)"
    }
}

out_raw_path = r'd:\আমার গবেষণা\জালালাইন\২৭_সূরা_আন-নামল\_sources\ruku_07_raw.json'
with open(out_raw_path, 'w', encoding='utf-8') as f:
    json.dump(r7_data, f, ensure_ascii=False, indent=2)

print('ruku_07_raw.json generated successfully!')

import json

path = r'C:/Users/USER/.gemini/antigravity/brain/7caaeec8-bdfa-40da-93eb-62b94af954b1/.system_generated/steps/2294/output.txt'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

verses = data['verses']
r6_verses = [v for v in verses if 59 <= v['ayah_number'] <= 66]

r6_data = {
    "surah_id": 27,
    "surah_name_ar": "النمل",
    "surah_name_bn": "আন-নামল",
    "ruku_number": 6,
    "ayah_range": [59, 66],
    "mushaf_page": "382-383",
    "total_words": sum(v['word_count'] for v in r6_verses),
    "total_letters": sum(v['letter_count'] for v in r6_verses),
    "verses": [
        {"ayah": v['ayah_number'], "text": v['text_raw'], "words": v['word_count'], "letters": v['letter_count']}
        for v in r6_verses
    ],
    "verified_turath_sources": {
        "jalalain": {"id": 12876, "page": 3675},
        "tabari": {"id": 7798, "page": 12165},
        "ibn_kathir": {"id": 8473, "page": 3110},
        "qurtubi": {"id": 20855, "page": 5018},
        "razi_kabir": {"id": 23635, "page": 4388},
        "alusi_ruh": {"id": 22835, "page": 4315},
        "ibn_ashur": {"id": 9776, "page": 6795},
        "zuhayli_munir": {"id": 22915, "page": 5878},
        "faridat_dahr": {"id": 29909, "page": 2422},
        "hujjat_qiraat": {"id": 5531, "page": 462}
    },
    "qiraat_mutawatir_summary": {
        "ayah_59_yushrikun": "أما يشركون: بياء الغيب (أبو عمرو، عاصم، يعقوب: يُشْرِكُونَ)؛ وبتاء الخطاب للباقين (تُشْرِكُونَ)",
        "ayah_62_tadhakkarun": "قليلاً ما تذكرون: بتاء الخطاب وتخفيف الذال (حفص، حمزة، الكسائي، خلف: تَذَكَّرُونَ)؛ بتاء الخطاب وتشديد الذال (نافع، ابن كثير، ابن ذكوان، أبو جعفر، رويس: تَذَّكَّرُونَ)؛ وبياء الغيب مع التشديد (أبو عمرو، هشام، روح: يَذَّكَّرُونَ)",
        "ayah_63_arriyaah": "الرياح: قراءة ابن كثير وحمزة والكسائي وخلف بالإفراد (الرِّيحَ)؛ وقراءة الباقين بالجمع (الرِّيَاحَ)",
        "ayah_63_bushran": "بشراً: بباء مضمومة وسكون الشين (عاصم: بُشْرًا)؛ بنون مضمومة وسكون الشين (ابن عامر: نُشْرًا)؛ بنون مفتوحة وسكون الشين (حمزة، الكسائي، خلف: نَشْرًا)؛ وبضم النون والشين (الباقون: نُشُرًا)",
        "ayah_66_iddaraka": "بل ادارك: قراءة ابن كثير وأبي عمرو وأبي جعفر ويعقوب بهمزة قطع وإسكان الدال (بَلْ أَدْرَكَ عِلْمُهُمْ)؛ وقراءة الباقين بهمزة وصل وتشديد الدال بعدها ألف (بَلِ ادَّارَكَ عِلْمُهُمْ)"
    }
}

out_raw_path = r'd:\আমার গবেষণা\জালালাইন\২৭_সূরা_আন-নামল\_sources\ruku_06_raw.json'
with open(out_raw_path, 'w', encoding='utf-8') as f:
    json.dump(r6_data, f, ensure_ascii=False, indent=2)

print('ruku_06_raw.json generated successfully!')

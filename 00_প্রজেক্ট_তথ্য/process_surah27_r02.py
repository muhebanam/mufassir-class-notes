import json

path = r'C:/Users/USER/.gemini/antigravity/brain/7caaeec8-bdfa-40da-93eb-62b94af954b1/.system_generated/steps/2294/output.txt'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

verses = data['verses']
r2_verses = [v for v in verses if 15 <= v['ayah_number'] <= 19]

r2_data = {
    "surah_id": 27,
    "surah_name_ar": "النمل",
    "surah_name_bn": "আন-নামল",
    "ruku_number": 2,
    "ayah_range": [15, 19],
    "mushaf_page": "378",
    "total_words": sum(v['word_count'] for v in r2_verses),
    "total_letters": sum(v['letter_count'] for v in r2_verses),
    "verses": [
        {"ayah": v['ayah_number'], "text": v['text_raw'], "words": v['word_count'], "letters": v['letter_count']}
        for v in r2_verses
    ],
    "verified_turath_sources": {
        "jalalain": {"id": 12876, "page": 3625},
        "tabari": {"id": 7798, "page": 12115},
        "ibn_kathir": {"id": 8473, "page": 3087},
        "qurtubi": {"id": 20855, "page": 4975},
        "razi_kabir": {"id": 23635, "page": 4350},
        "alusi_ruh": {"id": 22835, "page": 4268},
        "ibn_ashur": {"id": 9776, "page": 6745},
        "zuhayli_munir": {"id": 22915, "page": 5840},
        "faridat_dahr": {"id": 29909, "page": 2398},
        "hujjat_qiraat": {"id": 5531, "page": 447}
    },
    "qiraat_mutawatir_summary": {
        "ayah_17_idgham": "وحشر لسليمان: إدغام الراء في اللام إدغاماً كبيراً للسوسي عن أبي عمرو (وَحُشِلِّسُلَيْمَانَ)",
        "ayah_18_waad": "على واد النمل: إثبات الياء الزائدة وقفا ليعقوب والكسائي (وَادِي)؛ وحذفها وصلاً ووقفاً للباقين (وَادِ)",
        "ayah_18_yahqimanna": "لا يحطمنكم: قراءة رويس عن يعقوب بنون التوكيد الخفيفة الساكنة (لَا يَحْطِمَنْكُمْ)؛ وقراءة الباقين بنون التوكيد الثقيلة المشددة (لَا يَحْطِمَنَّكُمْ)",
        "ayah_19_awzini": "أوزعني أن أشكر: فتح ياء الإضافة وصلاً لورش والبزي عن ابن كثير (أَوْزِعْنِيَ أَنْ)؛ وإسكانها مع المد المنفصل للباقين",
        "ayah_19_tardahu": "ترضاه: إمالة الألف لحمزة والكسائي وخلف العاشر؛ وتقليلها لورش؛ وصلة هاء الضمير لابن كثير (تَرْضَاهُو)"
    }
}

out_raw_path = r'd:\আমার গবেষণা\জালালাইন\২৭_সূরা_আন-নামল\_sources\ruku_02_raw.json'
with open(out_raw_path, 'w', encoding='utf-8') as f:
    json.dump(r2_data, f, ensure_ascii=False, indent=2)

print('ruku_02_raw.json generated successfully!')

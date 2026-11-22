import json

path = r'C:/Users/USER/.gemini/antigravity/brain/7caaeec8-bdfa-40da-93eb-62b94af954b1/.system_generated/steps/2294/output.txt'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

verses = data['verses']
r5_verses = [v for v in verses if 45 <= v['ayah_number'] <= 58]

r5_data = {
    "surah_id": 27,
    "surah_name_ar": "النمل",
    "surah_name_bn": "আন-নামল",
    "ruku_number": 5,
    "ayah_range": [45, 58],
    "mushaf_page": "381-382",
    "total_words": sum(v['word_count'] for v in r5_verses),
    "total_letters": sum(v['letter_count'] for v in r5_verses),
    "verses": [
        {"ayah": v['ayah_number'], "text": v['text_raw'], "words": v['word_count'], "letters": v['letter_count']}
        for v in r5_verses
    ],
    "verified_turath_sources": {
        "jalalain": {"id": 12876, "page": 3662},
        "tabari": {"id": 7798, "page": 12152},
        "ibn_kathir": {"id": 8473, "page": 3102},
        "qurtubi": {"id": 20855, "page": 5005},
        "razi_kabir": {"id": 23635, "page": 4378},
        "alusi_ruh": {"id": 22835, "page": 4302},
        "ibn_ashur": {"id": 9776, "page": 6782},
        "zuhayli_munir": {"id": 22915, "page": 5868},
        "faridat_dahr": {"id": 29909, "page": 2415},
        "hujjat_qiraat": {"id": 5531, "page": 458}
    },
    "qiraat_mutawatir_summary": {
        "ayah_49_lanubayyitannahu": "لنبيتنه... لنقولن: قراءة حمزة والكسائي وخلف العاشر بتاء الخطاب (لَتُبَيِّتُنَّهُ... لَتَقُولُنَّ)؛ وقراءة الباقين بنون المتكلمين (لَنُبَيِّتَنَّهُ... لَنَقُولَنَّ)",
        "ayah_49_mahlika": "مهلك: فتح الميم وكسر اللام (حفص: مَهْلِكَ)؛ فتح الميم واللام (شعبة: مَهْلَكَ)؛ ضم الميم وفتح اللام (الباقون: مُهْلَكَ)",
        "ayah_51_anna": "أنا دمرناهم: فتح الهمزة (عاصم، حمزة، الكسائي، يعقوب، خلف: أَنَّا)؛ وكسر الهمزة للباقين (إِنَّا)",
        "ayah_55_ainnakum": "أئنكم لتأتون: تسهيل الهمزة الثانية مع الإدخال وبدونه؛ وتحقيق الهمزتين لعاصم وحمزة والكسائي وخلف",
        "ayah_57_qaddarnaha": "قدرناها: تخفيف الدال لشعبة عن عاصم (قَدَرْنَاهَا)؛ وتشديد الدال للباقين (قَدَّرْنَاهَا)"
    }
}

out_raw_path = r'd:\আমার গবেষণা\জালালাইন\২৭_সূরা_আন-নামল\_sources\ruku_05_raw.json'
with open(out_raw_path, 'w', encoding='utf-8') as f:
    json.dump(r5_data, f, ensure_ascii=False, indent=2)

print('ruku_05_raw.json generated successfully!')

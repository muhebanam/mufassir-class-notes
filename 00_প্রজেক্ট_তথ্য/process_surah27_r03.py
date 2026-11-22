import json

path = r'C:/Users/USER/.gemini/antigravity/brain/7caaeec8-bdfa-40da-93eb-62b94af954b1/.system_generated/steps/2294/output.txt'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

verses = data['verses']
r3_verses = [v for v in verses if 20 <= v['ayah_number'] <= 31]

r3_data = {
    "surah_id": 27,
    "surah_name_ar": "النمل",
    "surah_name_bn": "আন-নামল",
    "ruku_number": 3,
    "ayah_range": [20, 31],
    "mushaf_page": "378-379",
    "total_words": sum(v['word_count'] for v in r3_verses),
    "total_letters": sum(v['letter_count'] for v in r3_verses),
    "sajdah_ayah": 25,
    "verses": [
        {"ayah": v['ayah_number'], "text": v['text_raw'], "words": v['word_count'], "letters": v['letter_count']}
        for v in r3_verses
    ],
    "verified_turath_sources": {
        "jalalain": {"id": 12876, "page": 3635},
        "tabari": {"id": 7798, "page": 12125},
        "ibn_kathir": {"id": 8473, "page": 3090},
        "qurtubi": {"id": 20855, "page": 4982},
        "razi_kabir": {"id": 23635, "page": 4358},
        "alusi_ruh": {"id": 22835, "page": 4278},
        "ibn_ashur": {"id": 9776, "page": 6755},
        "zuhayli_munir": {"id": 22915, "page": 5848},
        "faridat_dahr": {"id": 29909, "page": 2402},
        "hujjat_qiraat": {"id": 5531, "page": 450}
    },
    "qiraat_mutawatir_summary": {
        "ayah_20_maliya": "ما لي لا أرى: فتح ياء الإضافة (ابن كثير، هشام، عاصم، الكسائي: مَا لِيَ)؛ وإسكانها للباقين (مَا لِيْ)",
        "ayah_22_makatha": "فمكث: فتح الكاف (عاصم، وروح عن يعقوب: فَمَكَثَ)؛ وضم الكاف للباقين (فَمَكُثَ)",
        "ayah_22_saba": "من سبإ: فتح الهمزة بغير تنوين (البزي، وأبو عمرو: مِنْ سَبَأَ)؛ إسكان الهمزة (قنبل: مِنْ سَبْءٍ)؛ كسر الهمزة مع التنوين للباقين (مِنْ سَبَإٍ)",
        "ayah_25_alla_yasjudu": "ألا يسجدوا: تخفيف اللام (الكسائي، أبو جعفر، رويس: أَلَا يَا اسْجُدُوا)؛ وتشديد اللام للباقين (أَلَّا يَسْجُدُوا)",
        "ayah_25_tukhfoona": "ما تخفون وما تعلنون: بتاء الخطاب (حفص، والكسائي: تُخْفُونَ وَتُعْلِنُونَ)؛ وبياء الغيب للباقين (يُخْفُونَ وَيُعْلِنُونَ)",
        "ayah_28_fa_alqih": "فألقه إليهم: إسكان الهاء (أبو عمرو، عاصم، حمزة، أبو جعفر: فَأَلْقِهْ)؛ قصر الهاء بكسرة خفيفة (قالون، يعقوب: فَأَلْقِهِ)؛ إشباع كسر الهاء وصلة (ورش، ابن كثير، ابن ذكوان، الكسائي، خلف العاشر: فَأَلْقِهِۦٓ)"
    }
}

out_raw_path = r'd:\আমার গবেষণা\জালালাইন\২৭_সূরা_আন-নামল\_sources\ruku_03_raw.json'
with open(out_raw_path, 'w', encoding='utf-8') as f:
    json.dump(r3_data, f, ensure_ascii=False, indent=2)

print('ruku_03_raw.json generated successfully!')

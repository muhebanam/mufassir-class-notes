#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expand Tahqeeq for Surah 24 Ruku 4 (Ayahs 27-34) to Maximum Words.
Adds all substantive words with full morphological precision.
"""

import json

null = None

NEW_WORDS_RUKU4 = {
    27: [
        {
            "word": "تَدْخُلُوا",
            "meaning_bn": "তোমরা প্রবেশ করো না",
            "word_type": "فعل",
            "prefix_suffix_note": "নাহীসূচক لَا যোগে মাযযূম ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "مضارع معروف مجزوم بلا الناهية",
                "bab": "نَصَرَ",
                "jins": "صحيح",
                "root": "(د . خ . ل)",
                "masdar": "اَلدُّخُولُ",
                "masdar_meaning": "প্রবেশ করা; ভেতরে যাওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "لَا النَّاهِيَة এর কারণে মাযযূম বি হাযফিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "অনুমতি ও সালাম ছাড়া অন্যের গৃহে প্রবেশ সম্পূর্ণ নিষিদ্ধ।",
            "classical_notes": []
        },
        {
            "word": "بُيُوتًا",
            "meaning_bn": "এমন কোনো গৃহে বা ঘরে",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف يائي",
                "root": "(ب . ي . ت)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: بَيْتٌ | বহুবচন: بُيُوتٌ"
            },
            "taleel_or_irab": "تَدْخُلُوا ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "মানুষের ব্যক্তিগত বাসগৃহ যার গোপনীয়তা অলঙ্ঘনীয়।",
            "classical_notes": []
        },
        {
            "word": "أَهْلِهَا",
            "meaning_bn": "গৃহবাসীদের ওপর / ঘরের বাসিন্দাদের প্রতি",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(أ . ه . ل)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: أَهْلٌ | বহুবচন: أَهْلُونَ / آهَالٍ"
            },
            "taleel_or_irab": "عَلَى হরফে জারের কারণে মাজরূর বিল কাসরাহ; هَا যমীরটি মুযাফ ইলাইহি।",
            "lexical_depth_bn": "প্রবেশের পূর্বে গৃহবাসীদের শান্তিময় সালাম দেওয়া ইসলামী শিষ্টাচার।",
            "classical_notes": []
        }
    ],
    28: [
        {
            "word": "أَحَدًا",
            "meaning_bn": "কাউকে বা কোনো ব্যক্তিকে",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "مهموز الفاء",
                "root": "(أ . ح . د)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: أَحَدٌ | বহুবচন: آحَادٌ"
            },
            "taleel_or_irab": "تَجِدُوا ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "অনুমতি দেওয়ার মতো কেউ ঘরে না থাকলে সেখানে প্রবেশ নিষিদ্ধ।",
            "classical_notes": []
        },
        {
            "word": "يُؤْذَنَ",
            "meaning_bn": "তোমাদেরকে অনুমতি দেওয়া না হয়",
            "word_type": "فعل",
            "prefix_suffix_note": "হাত্তা (حَتَّى) এর পর মানসূব ফে'লে মুযারে মাঝহূল",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع مجهول",
                "bab": "سَمِعَ",
                "jins": "مهموز الفاء",
                "root": "(أ . ذ . ن)",
                "masdar": "اَلْإِذْنُ",
                "masdar_meaning": "অনুমতি দেওয়া; সম্মতি প্রকাশ করা",
                "singular_plural": null
            },
            "taleel_or_irab": "حَتَّى-এর পর أَنْ مُضْمَرَة দ্বারা মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "গৃহকর্তার সুস্পষ্ট সম্মতি ছাড়া অন্যের ঘরে প্রবেশ অবৈধ।",
            "classical_notes": []
        },
        {
            "word": "قِيلَ",
            "meaning_bn": "তোমাদের বলা হয়",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মাঝহূল",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "ماضي مجهول",
                "bab": "نَصَرَ",
                "jins": "أجوف واوي",
                "root": "(ق . و . ل)",
                "masdar": "اَلْقَوْلُ",
                "masdar_meaning": "বলা; নির্দেশ দেওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "মূলত قُوِلَ ছিল; কাসরার কারণে ওয়াও ইয়া-তে রূপান্তরিত হয়ে قِيلَ হয়েছে (مبني للمجهول)।",
            "lexical_depth_bn": "যদি ঘরের লোক ফিরে যেতে বলে তবে মনঃক্ষুণ্ণ না হয়ে ফিরে যাওয়া ওয়াজিব।",
            "classical_notes": []
        },
        {
            "word": "عَلِيمٌ",
            "meaning_bn": "তোমাদের যাবতীয় কাজের সম্যক পরিজ্ঞাত",
            "word_type": "اسم",
            "prefix_suffix_note": "খবর হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ع . ل . م)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: عَلِيمٌ | বহুবচন: عُلَمَاءُ"
            },
            "taleel_or_irab": "اللَّهُ মুবতাদার খবর হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "মানুষ অন্তরে ও প্রকাশ্যে যা করে আল্লাহ তা সম্পূর্ণ জানেন।",
            "classical_notes": []
        }
    ],
    29: [
        {
            "word": "تَدْخُلُوا",
            "meaning_bn": "তোমরা প্রবেশ করো",
            "word_type": "فعل",
            "prefix_suffix_note": "আন (أَنْ) দ্বারা মানসূব ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "مضارع معروف",
                "bab": "نَصَرَ",
                "jins": "صحيح",
                "root": "(د . خ . ل)",
                "masdar": "اَلدُّخُولُ",
                "masdar_meaning": "প্রবেশ করা",
                "singular_plural": null
            },
            "taleel_or_irab": "أَنْ মাসদারিয়্যাহ দ্বারা মানসূব বি হাযফিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "অনাবাসিক উন্মুক্ত স্থানে প্রবেশের শিথিলতা।",
            "classical_notes": []
        },
        {
            "word": "بُيُوتًا",
            "meaning_bn": "এমন গৃহ বা স্থানে",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف يائي",
                "root": "(ب . ي . ت)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: بَيْتٌ | বহুবচন: بُيُوتٌ"
            },
            "taleel_or_irab": "تَدْخُلُوا ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "যেমন: সরাইখানা, বাণিজ্য কেন্দ্র, গুদাম ইত্যাদি সাধারণ স্থান।",
            "classical_notes": []
        },
        {
            "word": "يَعْلَمُ",
            "meaning_bn": "আল্লাহ সম্যক জানেন ও দেখেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "سَمِعَ",
                "jins": "صحيح",
                "root": "(ع . ل . م)",
                "masdar": "اَلْعِلْمُ",
                "masdar_meaning": "জানা; সম্যক পরিজ্ঞাত হওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ; ফা'ইল যমীর হলো مستتر (تقديره هو)।",
            "lexical_depth_bn": "জনসাধারণের চলাচলের স্থানেও নিয়তের পবিত্রতা বজায় রাখার তাগিদ।",
            "classical_notes": []
        }
    ],
    30: [
        {
            "word": "قُلْ",
            "meaning_bn": "আপনি বলে দিন",
            "word_type": "فعل",
            "prefix_suffix_note": "আমর হাজির মুযাক্কার ওয়াহিদ",
            "morphology": {
                "sighah": "واحد مذكر حاضر",
                "bahas": "أمر حاضر معروف",
                "bab": "نَصَرَ",
                "jins": "أجوف واوي",
                "root": "(ق . و . ل)",
                "masdar": "اَلْقَوْلُ",
                "masdar_meaning": "বলা; ঘোষণা করা",
                "singular_plural": null
            },
            "taleel_or_irab": "আমর হিসেবে মাবনী আলাস সুকূন; মূলত قُولْ ছিল, التقاء الساكنين এর কারণে ওয়াও বিলুপ্ত হয়েছে।",
            "lexical_depth_bn": "রাসূলুল্লাহ ﷺ-কে মুমিনদের প্রতি পর্দার মূলনীতি প্রচারের নির্দেশ।",
            "classical_notes": []
        },
        {
            "word": "لِلْمُؤْمِنِينَ",
            "meaning_bn": "মুমিন পুরুষদেরকে",
            "word_type": "اسم",
            "prefix_suffix_note": "লাম হরফে জার সহ মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "مهموز الفاء",
                "root": "(أ . م . ن)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: مُؤْمِنٌ | বহুবচন: مُؤْمِنُونَ"
            },
            "taleel_or_irab": "لِ হরফে জারের মাজরূর হিসেবে মাজরূর বিল ইয়া (جمع مذكر سالم)।",
            "lexical_depth_bn": "দৃষ্টির সংযম প্রথমে পুরুষদের ওপর অপরিহার্য করা হয়েছে।",
            "classical_notes": []
        },
        {
            "word": "خَبِيرٌ",
            "meaning_bn": "পুঙ্খানুপুঙ্খ সম্যক অবগত",
            "word_type": "اسم",
            "prefix_suffix_note": "খবর হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(خ . ب . ر)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: خَبِيرٌ | বহুবচন: خُبَرَاءُ"
            },
            "taleel_or_irab": "إِنَّ اللَّهَ-এর খবর হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "চোখের চোরা চাহনি ও অন্তরের গোপন খেয়ানত সম্পর্কেও আল্লাহ পুরোপুরি ওয়াকিবহাল।",
            "classical_notes": []
        }
    ],
    31: [
        {
            "word": "قُلْ",
            "meaning_bn": "আপনি বলে দিন",
            "word_type": "فعل",
            "prefix_suffix_note": "আমর হাজির মুযাক্কার ওয়াহিদ",
            "morphology": {
                "sighah": "واحد مذكر حاضر",
                "bahas": "أمر حاضر معروف",
                "bab": "نَصَرَ",
                "jins": "أجوف واوي",
                "root": "(ق . و . ل)",
                "masdar": "اَلْقَوْلُ",
                "masdar_meaning": "বলা; নির্দেশ দেওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "আমর হিসেবে মাবনী আলাস সুকূন; ফা'ইল যমীর হলো مستتر (تقديره أنت)।",
            "lexical_depth_bn": "মুসলিম নারীদের পবিত্রতা ও পর্দার বিধানের ঘোষণা।",
            "classical_notes": []
        },
        {
            "word": "لِلْمُؤْمِنَاتِ",
            "meaning_bn": "বিশ্বাসী মুমিন নারীদেরকে",
            "word_type": "اسم",
            "prefix_suffix_note": "লাম হরফে জার সহ মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "مهموز الفاء",
                "root": "(أ . م . ن)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: مُؤْمِنَةٌ | বহুবচন: مُؤْمِنَاتٌ"
            },
            "taleel_or_irab": "لِ হরফে জারের কারণে মাজরূর বিল কাসরাহ (جمع مؤنث سالم)।",
            "lexical_depth_bn": "পর্দা মুমিন নারীর অনন্য সম্মান ও আত্মমর্যাদার প্রতীক।",
            "classical_notes": []
        },
        {
            "word": "أَبْصَارِهِنَّ",
            "meaning_bn": "তাদের নিজ নিজ দৃষ্টিসমূহ",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ب . ص . ر)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: بَصَرٌ | বহুবচন: أَبْصَارٌ"
            },
            "taleel_or_irab": "مِنْ হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ; هِنَّ যমীরটি মুযাফ ইলাইহি।",
            "lexical_depth_bn": "পরপুরুষের প্রতি কামুক দৃষ্টিপাত থেকে নারীদের চোখকে অবনত রাখা।",
            "classical_notes": []
        },
        {
            "word": "فُرُوجَهُنَّ",
            "meaning_bn": "তাদের নিজ নিজ লজ্জাস্থানসমূহ",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ف . ر . ج)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: فَرْجٌ | বহুবচন: فُرُوجٌ"
            },
            "taleel_or_irab": "يَحْفَظْنَ ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ; هُنَّ যমীরটি মুযাফ ইলাইহি।",
            "lexical_depth_bn": "যাবতীয় ব্যভিচার, অনাবৃত অবস্থা ও সমকামী বিকৃতি থেকে সর্বতোভাবে হেফাজত।",
            "classical_notes": []
        },
        {
            "word": "ظَهَرَ",
            "meaning_bn": "যা নিজে থেকেই প্রকাশ পেয়ে যায়",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "فَتَحَ",
                "jins": "صحيح",
                "root": "(ظ . ه . ر)",
                "masdar": "اَلظُّهُورُ",
                "masdar_meaning": "প্রকাশ পাওয়া; দৃশ্যমান হওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলাল ফাতহ; ফা'ইল যমীর مستتر (تقديره هو)। مَا موصولة-এর সিলাহ।",
            "lexical_depth_bn": "ইবনে আব্বাস (রা.)-এর মতে: অনিচ্ছাকৃতভাবে উন্মুক্ত হওয়া যেমন মুখমণ্ডল ও দুই হাতের তালু অথবা বাইরের চাদর।",
            "classical_notes": []
        },
        {
            "word": "وَلْيَضْرِبْنَ",
            "meaning_bn": "এবং তারা যেন অবশ্যই টেনে ফেলে দেয়",
            "word_type": "فعل",
            "prefix_suffix_note": "লামে আমর সহ ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مؤنث غائب",
                "bahas": "مضارع معروف مجزوم بلام الأمر",
                "bab": "ضَرَبَ",
                "jins": "صحيح",
                "root": "(ض . ر . ب)",
                "masdar": "اَلضَّرْبُ",
                "masdar_meaning": "টেনে দেওয়া; আঘাত করা; ঢেকে ফেলা",
                "singular_plural": null
            },
            "taleel_or_irab": "لام الأمر এর কারণে মাযযূম হওয়ার কথা থাকলেও نون النسوة যুক্ত থাকায় مَبْنِيٌّ عَلَى السُّكُونِ فِي مَحَلِّ جَزْمٍ।",
            "lexical_depth_bn": "বক্ষদেশ ও গ্রীবা ওড়না দিয়ে সুদৃঢ়ভাবে আবৃত করার অলঙ্ঘনীয় ফরয বিধান।",
            "classical_notes": [
                {
                    "scholar_or_book": "মুফরাদাতুল কুরআন (ইমাম রাগেব)",
                    "note": "الضرب এখানে কোনো কিছুকে অন্য বস্তুর ওপর দৃঢ়ভাবে চেপে বসানো বা ফেলা বোঝায়; ওড়নাকে গ্রীবা ও বক্ষের ওপর সুসংহত করা।"
                }
            ]
        },
        {
            "word": "آبَائِهِنَّ",
            "meaning_bn": "তাদের নিজ নিজ পিতাগণ",
            "word_type": "اسم",
            "prefix_suffix_note": "মুযাফ ইলাইহি হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "নাقص واوي",
                "root": "(أ . ب . و)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: أَبٌ | বহুবচন: آبَاءٌ"
            },
            "taleel_or_irab": "মা'তূফ হিসেবে মাজরূর বিল কাসরাহ; هِنَّ যমীরটি মুযাফ ইলাইহি।",
            "lexical_depth_bn": "মাহরাম পুরুষদের তালিকা যাদের সামনে সাধারণ গৃহস্থালি সাজসজ্জা প্রকাশ বৈধ।",
            "classical_notes": []
        },
        {
            "word": "أَبْنَائِهِنَّ",
            "meaning_bn": "তাদের নিজ নিজ পুত্রসন্তানগণ",
            "word_type": "اسم",
            "prefix_suffix_note": "মা'তূফ হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "ناقص واوي",
                "root": "(ب . ن . و)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: اِبْنٌ | বহুবচন: أَبْنَاءٌ"
            },
            "taleel_or_irab": "মা'তূফ হিসেবে মাজরূর বিল কাসরাহ; هِنَّ মুযাফ ইলাইহি।",
            "lexical_depth_bn": "নিজের ঔরসজাত সন্তান যাদের সাথে বিবাহ চিরতরে হারাম।",
            "classical_notes": []
        },
        {
            "word": "إِخْوَانِهِنَّ",
            "meaning_bn": "তাদের নিজ নিজ সহোদর ভাইগণ",
            "word_type": "اسم",
            "prefix_suffix_note": "মা'তূফ হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "নাقص واوي",
                "root": "(أ . خ . و)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: أَخٌ | বহুবচন: إِخْوَانٌ"
            },
            "taleel_or_irab": "মা'তূফ হিসেবে মাজরূর বিল কাসরাহ; هِنَّ মুযাফ ইলাইহি।",
            "lexical_depth_bn": "আপন ভাই যাদের সাথে রক্তসম্পর্কীয় অকাট্য মাহরামীয়াত রয়েছে।",
            "classical_notes": []
        },
        {
            "word": "نِسَائِهِنَّ",
            "meaning_bn": "তাদের সমমনা মুসলিম নারীগণ",
            "word_type": "اسم",
            "prefix_suffix_note": "মা'তূফ হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "নাقص واوي",
                "root": "(ن . س . و)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: امْرَأَةٌ | বহুবচন: نِسَاءٌ"
            },
            "taleel_or_irab": "মা'তূফ হিসেবে মাজরূর বিল কাসরাহ; هِنَّ মুযাফ ইলাইহি।",
            "lexical_depth_bn": "সচ্চরিত্রা মুসলিম নারী যাদের সামনে রূপ প্রকাশ নিরাপদ।",
            "classical_notes": []
        },
        {
            "word": "مَلَكَتْ",
            "meaning_bn": "মালিকানাধীন হয়েছে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "واحد مؤنث غائب",
                "bahas": "ماضي معروف",
                "bab": "ضَرَبَ",
                "jins": "صحيح",
                "root": "(م . ل . ك)",
                "masdar": "اَلْمِلْكُ",
                "masdar_meaning": "মালিকানা অর্জন করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলাল ফাতহ; أَيْمَانُهُنَّ হলো এর ফা'ইল।",
            "lexical_depth_bn": "শরীয়তসম্মত দাস-দাসী যাদের সাথে অবাধ পারিবারিক সম্পর্ক ছিল।",
            "classical_notes": []
        },
        {
            "word": "أَيْمَانُهُنَّ",
            "meaning_bn": "তাদের ডান হাত / অধীনস্থ দাস-দাসী",
            "word_type": "اسم",
            "prefix_suffix_note": "ফা'ইল হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ي . م . ن)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: يَمِينٌ | বহুবচন: أَيْمَانٌ"
            },
            "taleel_or_irab": "مَلَكَتْ ক্রিয়ার ফা'ইল হিসেবে মারফূ বিয যম্মাহ; هُنَّ মুযাফ ইলাইহি।",
            "lexical_depth_bn": "মালিকানা চুক্তি নির্দেশক পরিভাষা।",
            "classical_notes": []
        },
        {
            "word": "التَّابِعِينَ",
            "meaning_bn": "এমন অনুগত অধীনস্থ ব্যক্তিগণ",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল ইয়া",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ت . ب . ع)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: تَابِعٌ | বহুবচন: تَابِعُونَ"
            },
            "taleel_or_irab": "ما'তূফ হিসেবে মাজরূর বিল ইয়া (جمع مذكر سالم)।",
            "lexical_depth_bn": "যাদের খাদ্যের বিনিময়ে সেবা নেওয়া হতো এবং যাদের যৌন বাসনা নিঃশেষিত।",
            "classical_notes": []
        },
        {
            "word": "يَظْهَرُوا",
            "meaning_bn": "তারা এখনো অবগত বা সজাগ হয়নি",
            "word_type": "فعل",
            "prefix_suffix_note": "লম (لَمْ) যোগে মাযযূম ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف مجزوم بلم",
                "bab": "فَتَحَ",
                "jins": "صحيح",
                "root": "(ظ . ه . ر)",
                "masdar": "اَلظُّهُورُ",
                "masdar_meaning": "অবগত হওয়া; প্রকাশ পাওয়া; চেনা",
                "singular_plural": null
            },
            "taleel_or_irab": "لَمْ হরফের কারণে মাযযূম বি হাযফিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "ছোট বাচ্চারা যারা এখনো নারীদের রূপ বা গোপনীয় বিষয়ের অনুভূতি লাভ করেনি।",
            "classical_notes": []
        },
        {
            "word": "يَضْرِبْنَ",
            "meaning_bn": "তারা সজোরে চরণ নিক্ষেপ করবে না",
            "word_type": "فعل",
            "prefix_suffix_note": "নাহীসূচক لَا যোগে ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مؤنث غائب",
                "bahas": "مضارع معروف مجزوم بلا الناهية",
                "bab": "ضَرَبَ",
                "jins": "صحيح",
                "root": "(ض . ر . ب)",
                "masdar": "اَلضَّرْبُ",
                "masdar_meaning": "আঘাত করা; পদধ্বনি সৃষ্টি করা",
                "singular_plural": null
            },
            "taleel_or_irab": "لَا النَّاهِيَة-এর পর নূনে নিসওয়ার কারণে مَبْنِيٌّ عَلَى السُّكُونِ فِي مَحَلِّ جَزْمٍ।",
            "lexical_depth_bn": "পায়ে পরা মল বা নূপুরের আওয়াজ তুলে পরপুরুষের দৃষ্টি আকর্ষণ করা হারাম।",
            "classical_notes": []
        },
        {
            "word": "بِأَرْجُلِهِنَّ",
            "meaning_bn": "তাদের পা দ্বারা",
            "word_type": "اسم",
            "prefix_suffix_note": "বা হরফে জার সহ মাজরূর এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ر . ج . ل)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: رِجْلٌ | বহুবচন: أَرْجُلٌ"
            },
            "taleel_or_irab": "بِ হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ; هِنَّ মুযাফ ইলাইহি।",
            "lexical_depth_bn": "চলার গতি ও পদধ্বনিতে শালীনতা রক্ষার নির্দেশ।",
            "classical_notes": []
        },
        {
            "word": "يُعْلَمَ",
            "meaning_bn": "যাতে জানা যায় বা প্রকাশ পায়",
            "word_type": "فعل",
            "prefix_suffix_note": "লামে কায় (لِـ) দ্বারা মানসূব ফে'লে মুযারে মাঝহূল",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع مجهول",
                "bab": "سَمِعَ",
                "jins": "صحيح",
                "root": "(ع . ل . م)",
                "masdar": "اَلْعِلْمُ",
                "masdar_meaning": "জানা যাওয়া; প্রকাশিত হওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "لَامُ كَيْ-এর পর أَنْ مُضْمَرَة দ্বারা মানসূব বিল ফাতহাহ (مبني للمجهول)।",
            "lexical_depth_bn": "অলংকারের ঝংকার বাজিয়ে পুরুষদের দৃষ্টি আকৃষ্ট করার চেষ্টা প্রতিহতকরণ।",
            "classical_notes": []
        },
        {
            "word": "يُخْفِينَ",
            "meaning_bn": "যা তারা গোপন করে রেখেছে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "جمع مؤنث غائب",
                "bahas": "مضارع معروف",
                "bab": "إِفْعَالٌ",
                "jins": "নাقص يائي",
                "root": "(خ . ف . ي)",
                "masdar": "اَلْإِخْفَاءُ",
                "masdar_meaning": "গোপন রাখা; ঢেকে রাখা",
                "singular_plural": null
            },
            "taleel_or_irab": "নূনে নিসওয়া যুক্ত থাকায় مَبْنِيٌّ عَلَى السُّكُونِ فِي مَحَلِّ رَفْعٍ; ن হলো ফা'ইল।",
            "lexical_depth_bn": "পোশাকের নিচে আবৃত অলংকার।",
            "classical_notes": []
        },
        {
            "word": "تُفْلِحُونَ",
            "meaning_bn": "তোমরা চূড়ান্ত সফলতা ও মুক্তি অর্জন করতে পারো",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "مضارع معروف",
                "bab": "إِفْعَالٌ",
                "jins": "صحيح",
                "root": "(ف . ل . ح)",
                "masdar": "اَلْفَلَاحُ",
                "masdar_meaning": "সফলতা অর্জন করা; মুক্তি লাভ করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বি সুবূতিন নূন; لَعَلَّكُمْ-এর খবর হিসেবে মহলে রফ' এ রয়েছে।",
            "lexical_depth_bn": "পবিত্রতা ও তওবার পথই দুনিয়া ও আখেরাতের চিরন্তন সফলতার একমাত্র চাবিকাঠি।",
            "classical_notes": [
                {
                    "scholar_or_book": "মুফরাদাতুল কুরআন (ইমাম রাগেব)",
                    "note": "الفلاح হলো এমন সার্বিক মুক্তি ও বিজয় যার মধ্যে পার্থিব শান্তি ও পরকালীন জান্নাতের অনন্ত নিয়ামত উভয়ই সন্নিবেশিত।"
                }
            ]
        }
    ],
    32: [
        {
            "word": "فُقَرَاءَ",
            "meaning_bn": "নিঃস্ব ও অসচ্ছল",
            "word_type": "اسم",
            "prefix_suffix_note": "খবর হিসেবে মানসূব",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ف . ق . ر)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: فَقِيرٌ | বহুবচন: فُقَرَاءُ"
            },
            "taleel_or_irab": "يَكُونُوا ক্রিয়ার খবর হিসেবে মানসূব বিল ফাতহাহ (غَيْرُ مُنْصَرِف)।",
            "lexical_depth_bn": "আর্থিক অসচ্ছলতার ভয় যেন যুবক-যুবতীদের বিবাহ বন্ধনে আবদ্ধ হওয়া থেকে বিরত না রাখে।",
            "classical_notes": []
        },
        {
            "word": "فَضْلِهِ",
            "meaning_bn": "আল্লাহর নিজস্ব অনুগ্রহ ও দান",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ف . ض . ل)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: فَضْلٌ | বহুবচন: فُضُولٌ"
            },
            "taleel_or_irab": "مِنْ হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ; هِ যমীরটি মুযাফ ইলাইহি।",
            "lexical_depth_bn": "বিবাহের পবিত্র বরকতে আল্লাহ বান্দাকে স্বাবলম্বী করার জামিনদার হন।",
            "classical_notes": []
        },
        {
            "word": "عَلِيمٌ",
            "meaning_bn": "বান্দার অভাব ও নিয়ত সম্পর্কে সম্পূর্ণ অবগত",
            "word_type": "اسم",
            "prefix_suffix_note": "দ্বিতীয় খবর হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ع . ل . م)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: عَلِيمٌ | বহুবচন: عُلَمَاءُ"
            },
            "taleel_or_irab": "اللَّهُ মুবতাদার দ্বিতীয় খবর হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "আল্লাহর জ্ঞান ও প্রাচুর্য চিরন্তন।",
            "classical_notes": []
        }
    ],
    33: [
        {
            "word": "يَجِدُونَ",
            "meaning_bn": "তারা জোগাড় করতে পারে না / পায় না",
            "word_type": "فعل",
            "prefix_suffix_note": "নাফীসূচক لَا যোগে ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "ضَرَبَ",
                "jins": "مثال واوي",
                "root": "(و . ج . د)",
                "masdar": "اَلْوِجْدَانُ",
                "masdar_meaning": "পাওয়া; সামর্থ্য থাকা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বি সুবূতিন নূন; মূলত يَوْجِدُونَ ছিল, হরকত ও বাবের কারণে ওয়াও বিলুপ্ত হয়েছে।",
            "lexical_depth_bn": "মোহর বা বিবাহের আর্থিক ও পারিবারিক সামর্থ্যহীনতা।",
            "classical_notes": []
        },
        {
            "word": "نِكَاحًا",
            "meaning_bn": "বিবাহের উপকরণ বা বিবাহের ব্যয়",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ن . ك . ح)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: نِكَاحٌ | বহুবচন: أَنْكِحَةٌ"
            },
            "taleel_or_irab": "يَجِدُونَ ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "বিবাহের ব্যয়ভার যতদিন না জোটে ততদিন রোজা ও সংযমের মাধ্যমে আত্মরক্ষা করার নির্দেশ।",
            "classical_notes": []
        },
        {
            "word": "يَبْتَغُونَ",
            "meaning_bn": "তারা লিখিত মুক্তিচুক্তি কামনা করে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "اِفْتِعَالٌ",
                "jins": "নাقص يائي",
                "root": "(ب . غ . ي)",
                "masdar": "اَلْاِبْتِغَاءُ",
                "masdar_meaning": "কামনা করা; অন্বেষণ করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বি সুবূতিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "দাস-দাসী যখন অর্থের বিনিময়ে মুক্তির আবেদন জানায়।",
            "classical_notes": []
        },
        {
            "word": "الْكِتَابَ",
            "meaning_bn": "মুক্তির আনুষ্ঠানিক চুক্তিপত্র (মুকাতাবাত)",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ك . ت . ب)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: كِتَابٌ | বহুবচন: كُتُبٌ"
            },
            "taleel_or_irab": "يَبْتَغُونَ ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "ইসলামে দাসপ্রথা বিলুপ্তির অন্যতম মাইলফলক আইনি চুক্তি 'কিতাবাত'।",
            "classical_notes": [
                {
                    "scholar_or_book": "মুফরাদাতুল কুরআন (ইমাম রাগেব)",
                    "note": "المكاتبة হলো দাস ও মনিবের মাঝে নির্দিষ্ট অর্থ পরিশোধের বিনিময়ে স্বাধীনতার লিখিত চুক্তি।"
                }
            ]
        },
        {
            "word": "عَلِمْتُمْ",
            "meaning_bn": "তোমরা যদি জানতে পারো বা নিশ্চিত হও",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "ماضي معروف",
                "bab": "سَمِعَ",
                "jins": "صحيح",
                "root": "(ع . ل . م)",
                "masdar": "اَلْعِلْمُ",
                "masdar_meaning": "জানা; নিশ্চিত হওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "إِنْ শるので ফে'লে মাযী মাবনী আলাস সুকূন; تُمْ হলো ফা'ইল।",
            "lexical_depth_bn": "দাসের মাঝে উপার্জনক্ষমতা, সততা ও দ্বীনদারির উপস্থিতি থাকা।",
            "classical_notes": []
        },
        {
            "word": "وَآتُوهُمْ",
            "meaning_bn": "এবং তোমরা তাদেরকে অর্থ সাহায্য দাও",
            "word_type": "فعل",
            "prefix_suffix_note": "আমর হাজির মুযাক্কার জামা'",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "أمر حاضر معروف",
                "bab": "إِفْعَالٌ",
                "jins": "مهموز الفاء ناقص يائي",
                "root": "(أ . ت . ي)",
                "masdar": "اَلْإِيتَاءُ",
                "masdar_meaning": "প্রদান করা; দান করা",
                "singular_plural": null
            },
            "taleel_or_irab": "আমর হিসেবে মাবনী আলা হাযফিন নূন; ওয়াও ফা'ইল; هُمْ মাফ'ঊলে বিহি।",
            "lexical_depth_bn": "মুকাতাব দাসকে মুক্তিপণ পরিশোধে যাকাত ও সাধারণ তহবিল থেকে আর্থিক সহায়তা দেওয়ার নির্দেশ।",
            "classical_notes": []
        },
        {
            "word": "مَالِ",
            "meaning_bn": "আল্লাহর প্রদত্ত সম্পদ থেকে",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف واوي",
                "root": "(م . و . ل)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: مَالٌ | বহুবচন: أَمْوَالٌ"
            },
            "taleel_or_irab": "مِنْ হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ; اللَّهِ মুযাফ ইলাইহি।",
            "lexical_depth_bn": "সম্পদ মানুষের নিজস্ব নয়, বরং আল্লাহর দেওয়া আমানত।",
            "classical_notes": []
        },
        {
            "word": "فَتَيَاتِكُمْ",
            "meaning_bn": "তোমাদের অধীনস্থ তরুণী দাসীদের",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব বিল কাসরাহ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "নাقص يائي",
                "root": "(ف . ت . ي)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: فَتَاةٌ | বহুবচন: فَتَيَاتٌ"
            },
            "taleel_or_irab": "تُكْرِهُوا ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল কাসরাহ (جمع مؤنث سالم); كُمْ মুযাফ ইলাইহি।",
            "lexical_depth_bn": "জাহেলি যুগে মুনাফিক সর্দাররা দাসীদের জোরপূর্বক পতিতাবৃত্তিতে নামাত; ইসলাম তা চিরতরে নিষিদ্ধ ঘোষণা করে।",
            "classical_notes": []
        },
        {
            "word": "عَرَضَ",
            "meaning_bn": "ক্ষণস্থায়ী ও নশ্বর পার্থিব স্বার্থ",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ع . ر . ض)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: عَرَضٌ | বহুবচন: أَعْرَاضٌ"
            },
            "taleel_or_irab": "لِتَبْتَغُوا ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ; الْحَيَاةِ মুযাফ ইলাইহি।",
            "lexical_depth_bn": "সামান্য বৈষয়িক অর্থের লোভে নারীর সম্ভ্রমকে পণ্য বানানোর বিরুদ্ধে কঠোর তিরস্কার।",
            "classical_notes": [
                {
                    "scholar_or_book": "মুফরাদাতুল কুরআন (ইমাম রাগেব)",
                    "note": "العَرَض হলো এমন নশ্বর বস্তু যা দ্রুত নিঃশেষ হয়ে যায়; দুনিয়ার যাবতীয় ভোগ্যসামগ্রী ক্ষণস্থায়ী হওয়ার কারণে তাকে عرض বলা হয়েছে।"
                }
            ]
        },
        {
            "word": "يُكْرِهْهُنَّ",
            "meaning_bn": "তাদেরকে জোরজবরদস্তি করে",
            "word_type": "فعل",
            "prefix_suffix_note": "শার্তের ফে'লে মুযারে মাযযূম",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "إِفْعَالٌ",
                "jins": "صحيح",
                "root": "(ك . ر . ه)",
                "masdar": "اَلْإِكْرَاهُ",
                "masdar_meaning": "জবরদস্তি করা; বাধ্য করা",
                "singular_plural": null
            },
            "taleel_or_irab": "مَنْ শারতিয়্যাহ দ্বারা মাযযূম বিস সুকূন; هُنَّ যমীরটি মাফ'ঊলে বিহি।",
            "lexical_depth_bn": "জুলুমের শিকার নারীর দায়মুক্তি ও ক্ষমা ঘোষণা।",
            "classical_notes": []
        },
        {
            "word": "غَفُورٌ",
            "meaning_bn": "পরম ক্ষমাশীল",
            "word_type": "اسم",
            "prefix_suffix_note": "প্রথম খবর হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(غ . ف . ر)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: غَفُورٌ | বহুবচন: غُفُرٌ"
            },
            "taleel_or_irab": "إِنَّ اللَّهَ-এর প্রথম খবর হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "মজলুম নারীর ওপর কোনো পাপ বর্তাবে না, আল্লাহ তাদের ক্ষমা করবেন।",
            "classical_notes": []
        },
        {
            "word": "رَحِيمٌ",
            "meaning_bn": "অসীম করুণাময়",
            "word_type": "اسم",
            "prefix_suffix_note": "দ্বিতীয় খবর হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ر . ح . م)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: رَحِيمٌ | বহুবচন: رُحَمَاءُ"
            },
            "taleel_or_irab": "দ্বিতীয় খবর হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "অসহায়দের প্রতি আল্লাহর অনন্ত রহমত।",
            "classical_notes": []
        }
    ],
    34: [
        {
            "word": "أَنْزَلْنَا",
            "meaning_bn": "আমরা সুস্পষ্টভাবে অবতীর্ণ করেছি",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "جمع متكلم",
                "bahas": "ماضي معروف",
                "bab": "إِفْعَالٌ",
                "jins": "صحيح",
                "root": "(ن . ز . ل)",
                "masdar": "اَلْإِنْزَالُ",
                "masdar_meaning": "অবতীর্ণ করা; নাযিল করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলাস সুকূন; نا হলো ফা'ইল।",
            "lexical_depth_bn": "কুরআনের সার্বিক নৈতিক ও পারিবারিক বিধানাবলীর অবতরণ।",
            "classical_notes": []
        },
        {
            "word": "آيَاتٍ",
            "meaning_bn": "সুস্পষ্ট বহু নিদর্শন ও বিধিমালা",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব বিল কাসরাহ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "مهموز الفاء ناقص يائي",
                "root": "(أ . ي . ي)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: آيَةٌ | বহুবচন: آيَاتٌ"
            },
            "taleel_or_irab": "أَنْزَلْنَا ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল কাসরাহ (جمع مؤنث سالم)।",
            "lexical_depth_bn": "সামাজিক ন্যায়বিচার ও পারিবারিক পবিত্রতার ঐশী কানুন।",
            "classical_notes": []
        }
    ]
}

def merge_and_sort(existing_list, new_items, ayah_words):
    def word_rank(w_obj):
        w_text = w_obj["word"].strip()
        for idx, aw in enumerate(ayah_words):
            raw = aw["word_raw"].strip()
            plain = aw["plain_text_raw"].strip()
            if w_text in raw or raw in w_text or w_text in plain or plain in w_text:
                return idx
        return 999
        
    combined = list(existing_list)
    existing_words = {w["word"].strip() for w in existing_list}
    for item in new_items:
        if item["word"].strip() not in existing_words:
            combined.append(item)
            existing_words.add(item["word"].strip())
            
    combined.sort(key=word_rank)
    return combined

def main():
    with open("reference/surah24_full_words.json", "r", encoding="utf-8") as f:
        full_words = json.load(f)
        
    with open("web/public/data/24/ruku-4.json", "r", encoding="utf-8") as f:
        ruku4 = json.load(f)
        
    total_added = 0
    total_words = 0
    for a in ruku4.get("ayahs", []):
        v = a.get("ayah")
        ayah_w = full_words.get(f"24:{v}", [])
        existing = a.get("tahqeeq", [])
        new_w = NEW_WORDS_RUKU4.get(v, [])
        merged = merge_and_sort(existing, new_w, ayah_w)
        added = len(merged) - len(existing)
        total_added += added
        total_words += len(merged)
        a["tahqeeq"] = merged
        print(f"Ayah {v:02d}: {len(existing)} -> {len(merged)} words (+{added})")
        
    with open("web/public/data/24/ruku-4.json", "w", encoding="utf-8") as f:
        json.dump(ruku4, f, ensure_ascii=False, indent=2)
        
    print(f"\n[SUCCESS] Ruku 4 expanded: +{total_added} words, total {total_words} words across Ayahs 27-34.")

if __name__ == "__main__":
    main()

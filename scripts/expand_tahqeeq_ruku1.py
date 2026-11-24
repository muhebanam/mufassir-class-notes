#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expand Tahqeeq for Surah 24 Ruku 1 (Ayahs 1-10) to Maximum Words.
Adds all substantive words while preserving existing in-depth classical notes.
"""

import json

null = None

NEW_WORDS_RUKU1 = {
    1: [
        {
            "word": "وَأَنْزَلْنَا",
            "meaning_bn": "এবং আমরা অবতীর্ণ করেছি",
            "word_type": "فعل",
            "prefix_suffix_note": "ওয়াও হরফে আতফ সহ ফে'লে মাযী",
            "morphology": {
                "sighah": "جمع متكلم",
                "bahas": "ماضي معروف",
                "bab": "إِفْعَالٌ",
                "jins": "صحيح",
                "root": "(ن . ز . ل)",
                "masdar": "اَلْإِنْزَالُ",
                "masdar_meaning": "নাযিল করা; অবতীর্ণ করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলাস সুকূন; ফা'ইল যমীর হলো না (نَا)।",
            "lexical_depth_bn": "পুনরায় ইনযাল উল্লেখ করে আয়াতের বিধানাবলির সম্মান ও মহত্ত্ব প্রকাশ করা হয়েছে।",
            "classical_notes": []
        }
    ],
    2: [
        {
            "word": "كُلَّ",
            "meaning_bn": "প্রত্যেককে",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "مضاعف ثلاثي",
                "root": "(ك . ل . ل)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: كُلٌّ | বহুবচন: أَكْلَالٌ"
            },
            "taleel_or_irab": "فَاجْلِدُوا ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ; وَاحِدٍ হলো মুযাফ ইলাইহি।",
            "lexical_depth_bn": "শাস্তি প্রয়োগে ব্যভিচারী ও ব্যভিচারিণীর প্রত্যেকেই যে সমানভাবে দণ্ডনীয় তা ঘোষণা করা হয়েছে।",
            "classical_notes": []
        },
        {
            "word": "وَاحِدٍ",
            "meaning_bn": "একজনকে / একক ব্যক্তিকে",
            "word_type": "اسم",
            "prefix_suffix_note": "মুযাফ ইলাইহি হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "مثال واوي",
                "root": "(و . ح . د)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: وَاحِدٌ | বহুবচন: وُحْدَانٌ"
            },
            "taleel_or_irab": "كُلَّ শব্দের মুযাফ ইলাইহি হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "প্রত্যেক অপরাধীর জন্য পৃথকভাবে স্বতন্ত্র এক শত বেত্রাঘাত প্রযোজ্য।",
            "classical_notes": []
        },
        {
            "word": "تَأْخُذْكُمْ",
            "meaning_bn": "তোমাদেরকে পেয়ে না বসে / আচ্ছন্ন না করে",
            "word_type": "فعل",
            "prefix_suffix_note": "নাফী/নাহীসূচক لَا যোগে মাযযূম ফে'লে মুযারে",
            "morphology": {
                "sighah": "واحد مؤنث غائب",
                "bahas": "مضارع معروف مجزوم بلا الناهية",
                "bab": "نَصَرَ",
                "jins": "مهموز الفاء",
                "root": "(أ . خ . ذ)",
                "masdar": "اَلْأَخْذُ",
                "masdar_meaning": "পাকড়াও করা; বশীভূত করা; পেয়ে বসা",
                "singular_plural": null
            },
            "taleel_or_irab": "لَا النَّاهِيَة এর কারণে মাযযূম বিস সুকূন; كُمْ যমীরটি মাফ'ঊলে বিহি; رَأْفَةٌ হলো এর ফা'ইল।",
            "lexical_depth_bn": "আল্লাহর হদ্দ কায়েম করার ক্ষেত্রে মানুষের স্বাভাবিক দুর্বলতা বা অন্ধ মায়াকে প্রশ্রয় দিতে নিষেধ করা হয়েছে।",
            "classical_notes": [
                {
                    "scholar_or_book": "মুফরাদাতুল কুরআন (ইমাম রাগেব)",
                    "note": "الأخذ অর্থ কোনো বস্তুকে সম্পূর্ণ নিজের আয়ত্তে নেওয়া; এখানে অন্ধ অনুভূতির প্রভাব মানব বিবেককে বশীভূত করা বোঝানো হয়েছে।"
                }
            ]
        },
        {
            "word": "دِينِ",
            "meaning_bn": "আল্লাহর অকাট্য বিধান ও দণ্ডবিধিতে",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف يائي",
                "root": "(د . ي . ن)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: دِينٌ | বহুবচন: أَدْيَانٌ"
            },
            "taleel_or_irab": "فِي হরফে জারের কারণে মাজরূর বিল কাসরাহ; لفظ الجلالة (اللَّهِ) হলো মুযাফ ইলাইহি।",
            "lexical_depth_bn": "এখানে দীন অর্থ কেবল আধ্যাত্মিক ধর্ম নয়, বরং আল্লাহর শরীয়তী বিচারব্যবস্থা ও শাস্তিবিধান।",
            "classical_notes": [
                {
                    "scholar_or_book": "তাফসীরে কাশশাফ (যমখশারী)",
                    "note": "دين الله দ্বারা আল্লাহর হুকুম, বিচার ও শাস্তি বাস্তবায়ন বোঝানো হয়েছে; অর্থাৎ আল্লাহর নির্ধারিত হদ্দে কোনো করুণা প্রদর্শন বৈধ নয়।"
                }
            ]
        },
        {
            "word": "تُؤْمِنُونَ",
            "meaning_bn": "তোমরা দৃঢ় ঈমান রাখো",
            "word_type": "فعل",
            "prefix_suffix_note": "শার্তের জওয়াবের দিকে প্রত্যাবর্তিত ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "مضارع معروف",
                "bab": "إِفْعَالٌ",
                "jins": "مهموز الفاء",
                "root": "(أ . م . ن)",
                "masdar": "اَلْإِيمَانُ",
                "masdar_meaning": "ঈমান আনা; আন্তরিক বিশ্বাস স্থাপন করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বি সুবূতিন নূন; كُنْتُمْ-এর খবর হিসেবে মহলে নাসব-এ রয়েছে।",
            "lexical_depth_bn": "হদ্দ বাস্তবায়নে আন্তরিক হওয়া প্রকৃত ঈমানের আবশ্যকীয় প্রমাণ।",
            "classical_notes": []
        },
        {
            "word": "الْيَوْمِ",
            "meaning_bn": "মহাদিবস বা পরকাল",
            "word_type": "اسم",
            "prefix_suffix_note": "মা'তূফ হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف واوي",
                "root": "(ي . و . م)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: يَوْمٌ | বহুবচন: أَيَّامٌ"
            },
            "taleel_or_irab": "اللَّهِ শব্দের ওপর মা'তূফ হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "হিসাব ও প্রতিফল দিবস, যে দিবসের জওয়াবদিহির ভয় মানুষকে শরীয়তের অনুগত রাখে।",
            "classical_notes": []
        },
        {
            "word": "الْآخِرِ",
            "meaning_bn": "সর্বশেষ ও চিরন্তন",
            "word_type": "اسم",
            "prefix_suffix_note": "সিফাত হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "مهموز الفاء",
                "root": "(أ . خ . ر)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: آخِرٌ | বহুবচন: أَوَاخِرُ"
            },
            "taleel_or_irab": "الْيَوْمِ শব্দের সিফাত (نعت) হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "দুনিয়ার পরকালীন সর্বশেষ স্থায়ী অনন্ত জীবন।",
            "classical_notes": []
        },
        {
            "word": "وَلْيَشْهَدْ",
            "meaning_bn": "এবং তাদের যেন প্রত্যক্ষ করে বা উপস্থিত থাকে",
            "word_type": "فعل",
            "prefix_suffix_note": "লামে আমর সহ ফে'লে মুযারে",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف مجزوم بلام الأمر",
                "bab": "سَمِعَ",
                "jins": "صحيح",
                "root": "(ش . ه . د)",
                "masdar": "اَلشَّهَادَةُ",
                "masdar_meaning": "প্রত্যক্ষ করা; সাক্ষী হওয়া; উপস্থিত থাকা",
                "singular_plural": null
            },
            "taleel_or_irab": "لام الأمر এর কারণে মাযযূম বিস সুকূন; طَائِفَةٌ হলো এর ফা'ইল।",
            "lexical_depth_bn": "হদ্দ জনসমক্ষে কার্যকর করার নির্দেশ যাতে তা সমাজের অন্যদের জন্য কার্যকর সতর্কবাণী হয়।",
            "classical_notes": [
                {
                    "scholar_or_book": "মুফরাদাতুল কুরআন (ইমাম রাগেব)",
                    "note": "الشهود অর্থ সশরীরে উপস্থিত থেকে স্বচক্ষে কোনো ঘটনা অবলোকন করা।"
                }
            ]
        },
        {
            "word": "عَذَابَهُمَا",
            "meaning_bn": "তাদের দুজনের পার্থিব শাস্তি",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ع . ذ . ب)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: عَذَابٌ | বহুবচন: أَعْذِبَةٌ"
            },
            "taleel_or_irab": "يَشْهَدْ ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ; هُمَا যমীরটি মুযাফ ইলাইহি।",
            "lexical_depth_bn": "ব্যভিচারের নির্ধারিত দৈহিক শাস্তি (বেত্রাঘাত)।",
            "classical_notes": []
        },
        {
            "word": "طَائِفَةٌ",
            "meaning_bn": "মুমিনদের একটি দল",
            "word_type": "اسم",
            "prefix_suffix_note": "ফা'ইল হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف واوي",
                "root": "(ط . و . ف)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: طَائِفَةٌ | বহুবচন: طَوَائِفُ"
            },
            "taleel_or_irab": "يَشْهَدْ ক্রিয়ার ফা'ইল হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "ফুকাহাদের মতে কমপক্ষে তিনজন বা চারজন মুমিনের একদল উপস্থিত থাকা সুন্নাত।",
            "classical_notes": [
                {
                    "scholar_or_book": "মুফরাদাতুল কুরআন (ইমাম রাগেব)",
                    "note": "الطائفة হলো মানুষের একটি দল যা বিশেষ উদ্দেশ্যে পরিবেষ্টন করে বা সমবেত হয়।"
                }
            ]
        },
        {
            "word": "الْمُؤْمِنِينَ",
            "meaning_bn": "বিশ্বাসী মুমিন সমাজ",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল ইয়া",
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
            "taleel_or_irab": "مِنْ হরফে জারের মাজরূর হিসেবে মাজরূর বিল ইয়া (جمع مذكر سالم)।",
            "lexical_depth_bn": "ন্যায় ও অনুশাসনের সাক্ষী হিসেবে ঈমানদারদের উপস্থিতির গুরুত্ব।",
            "classical_notes": []
        }
    ],
    3: [
        {
            "word": "الزَّانِي",
            "meaning_bn": "ব্যভিচারী পুরুষ",
            "word_type": "اسم",
            "prefix_suffix_note": "মুবতাদা হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "ناقص يائي",
                "root": "(ز . ن . ي)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: زَانٍ | বহুবচন: زُنَاةٌ"
            },
            "taleel_or_irab": "মুবতাদা হিসেবে মারফূ বিয যম্মাহ মুকাদ্দারা আলাল ইয়া।",
            "lexical_depth_bn": "যে ব্যক্তি অবৈধ যৌনাচারে লিপ্ত হয় এবং তওবা ছাড়া সেই পাপে অবিচল থাকে।",
            "classical_notes": []
        },
        {
            "word": "وَالزَّانِيَةُ",
            "meaning_bn": "এবং ব্যভিচারিণী নারী",
            "word_type": "اسم",
            "prefix_suffix_note": "দ্বিতীয় মুবতাদা হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "ناقص يائي",
                "root": "(ز . ن . ي)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: زَانِيَةٌ | বহুবচন: زَوَانٍ"
            },
            "taleel_or_irab": "দ্বিতীয় জুমলার মুবতাদা হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "পাপী নারীর সাথেও কোনো খাঁটি মুমিনের বিবাহ সঙ্গত নয়।",
            "classical_notes": []
        },
        {
            "word": "يَنْكِحُهَا",
            "meaning_bn": "তাকে বিবাহ করে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ এবং মাফ'ঊল",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "ضَرَبَ",
                "jins": "صحيح",
                "root": "(ن . ك . ح)",
                "masdar": "اَلنِّكَاحُ",
                "masdar_meaning": "বিবাহ করা; বিবাহবন্ধনে আবদ্ধ হওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ; হَا যমীরটি মানসূব মাফ'ঊলে বিহি; زَانٍ হলো ফা'ইল।",
            "lexical_depth_bn": "কুফু বা সমতা এবং সামাজিক পবিত্রতা রক্ষার কঠোর দিকনির্দেশনা।",
            "classical_notes": []
        },
        {
            "word": "زَانٍ",
            "meaning_bn": "ব্যভিচারী পুরুষ ছাড়া",
            "word_type": "اسم",
            "prefix_suffix_note": "ফা'ইল হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "ناقص يائي",
                "root": "(ز . ن . ي)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: زَانٍ | বহুবচন: زُنَاةٌ"
            },
            "taleel_or_irab": "يَنْكِحُهَا-এর ফা'ইল হিসেবে মারফূ বিয যম্মাহ মুকাদ্দারা আলাল ইয়া মাহযূফাহ (মূলত زَانِيٌ ছিল)।",
            "lexical_depth_bn": "পাপী চরিত্রবানদের সাথে খাপ খায় না, বরং সমমনা পাপীর সাথেই মেলে।",
            "classical_notes": []
        },
        {
            "word": "مُشْرِكٌ",
            "meaning_bn": "অথবা কোনো মুশরিক",
            "word_type": "اسم",
            "prefix_suffix_note": "মা'তূফ হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ش . ر . ك)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: مُشْرِكٌ | বহুবচন: مُشْرِكُونَ"
            },
            "taleel_or_irab": "زَانٍ শব্দের ওপর أَوْ দ্বারা মা'তূফ হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "আল্লাহর সাথে অংশীদার স্থাপনকারী অপবিত্র সত্তা।",
            "classical_notes": []
        }
    ],
    4: [
        {
            "word": "يَأْتُوا",
            "meaning_bn": "তারা উপস্থিত না করে / না নিয়ে আসে",
            "word_type": "فعل",
            "prefix_suffix_note": "লম (لَمْ) যোগে মাযযূম ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف مجزوم بلم",
                "bab": "ضَرَبَ",
                "jins": "مهموز الفاء ناقص يائي",
                "root": "(أ . ت . ي)",
                "masdar": "اَلْإِتْيَانُ",
                "masdar_meaning": "উপস্থিত করা; নিয়ে আসা; হাজির করা",
                "singular_plural": null
            },
            "taleel_or_irab": "لَمْ হরফের কারণে মাযযূম বি হাযফিন নূন (মূলত يَأْتُونَ ছিল); ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "অপবাদের দাবির সপক্ষে সরাসরি স্বচক্ষে দেখা চারজন চাক্ষুষ সাক্ষী হাজির করার আইনি বাধ্যবাধকতা।",
            "classical_notes": []
        },
        {
            "word": "بِأَرْبَعَةِ",
            "meaning_bn": "চারজন পুরুষ দ্বারা",
            "word_type": "اسم",
            "prefix_suffix_note": "বা হরফে জার সহ মাজরূর এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ر . ب . ع)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: أَرْبَعَةٌ | বহুবচন: أَرْبَعَاتٌ"
            },
            "taleel_or_irab": "بِ হরফে জারের কারণে মাজরূর বিল কাসরাহ; شُهَدَاءَ হলো মুযাফ ইলাইহি।",
            "lexical_depth_bn": "ইসলামী দণ্ডবিধিতে যেনতেন অপবাদ রোধে কঠোরতম প্রমাণ হিসেবে চারজন ন্যায়পরায়ণ সাক্ষীর শর্ত।",
            "classical_notes": []
        },
        {
            "word": "جَلْدَةً",
            "meaning_bn": "বেত্রাঘাত",
            "word_type": "اسم",
            "prefix_suffix_note": "তাময়ীয হিসেবে মানসূব",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ج . ل . د)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: جَلْدَةٌ | বহুবচন: جَلَدَاتٌ"
            },
            "taleel_or_irab": "ثَمَانِينَ সংখ্যার তাময়ীয (تَمْيِيز) হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "অপবাদকারী (কাযিফ)-এর জন্য নির্ধারিত আশিটি বেত্রাঘাত।",
            "classical_notes": []
        },
        {
            "word": "شَهَادَةً",
            "meaning_bn": "কোনো সাক্ষ্য",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ش . ه . د)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: شَهَادَةٌ | বহুবচন: شَهَادَاتٌ"
            },
            "taleel_or_irab": "تَقْبَلُوا ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "অপবাদকারীর নাগরিক ও আইনি সাক্ষ্য প্রদানের অধিকার চিরতরে বাতিল করার শাস্তি।",
            "classical_notes": []
        },
        {
            "word": "أَبَدًا",
            "meaning_bn": "কখনোই নয় / চিরকালের জন্য",
            "word_type": "اسم",
            "prefix_suffix_note": "যরফ হিসেবে মানসূব",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "مهموز الفاء",
                "root": "(أ . ب . د)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: أَبَدٌ | বহুবচন: آبَادٌ"
            },
            "taleel_or_irab": "ভবিষ্যতকালীন যরফিজ জামান হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "আইনিভাবে তার সাক্ষ্য গ্রহণযোগ্যতা আজীবনের জন্য রহিত হয়ে যায়।",
            "classical_notes": []
        }
    ],
    5: [
        {
            "word": "بَعْدِ",
            "meaning_bn": "পরবর্তী সময়ে",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ب . ع . د)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: بَعْدٌ | বহুবচন: أَبْعَادٌ"
            },
            "taleel_or_irab": "مِنْ হরফে জারের কারণে মাজরূর বিল কাসরাহ; ذَلِكَ হলো মুযাফ ইলাইহি।",
            "lexical_depth_bn": "অপরাধ সংঘটনের পর আন্তরিক অনুশোচনা ও সংশোধনের অবকাশ নির্দেশক।",
            "classical_notes": []
        }
    ],
    6: [
        {
            "word": "يَرْمُونَ",
            "meaning_bn": "অপবাদ দেয়",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "ضَرَبَ",
                "jins": "ناقص يائي",
                "root": "(ر . م . ي)",
                "masdar": "اَلرَّمْيُ",
                "masdar_meaning": "নিক্ষেপ করা; ব্যভিচারের অপবাদ দেওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বি সুবূতিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "স্বামীর পক্ষ থেকে নিজ স্ত্রীর ওপর পরকীয়া বা ব্যভিচারের অভিযোগ আরোপ।",
            "classical_notes": []
        },
        {
            "word": "شُهَدَاءُ",
            "meaning_bn": "অন্য কোনো সাক্ষী",
            "word_type": "اسم",
            "prefix_suffix_note": "ইসম হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ش . ه . د)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: شَهِيدٌ | বহুবচন: شُهَدَاءُ"
            },
            "taleel_or_irab": "يَكُن-এর মুআখখার ইসম হিসেবে মারফূ বিয যম্মাহ (غَيْرُ مُنْصَرِف)।",
            "lexical_depth_bn": "স্বামী ছাড়া অন্য কোনো নিরপেক্ষ চাক্ষুষ সাক্ষীর অনুপস্থিতি।",
            "classical_notes": []
        },
        {
            "word": "أَنْفُسُهُمْ",
            "meaning_bn": "কেবল তারা নিজেরা ছাড়া",
            "word_type": "اسم",
            "prefix_suffix_note": "ফা'ইল বা মুসতাসনা হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ن . ف . س)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: نَفْسٌ | বহুবচন: أَنْفُسٌ"
            },
            "taleel_or_irab": "إِلَّا-এর পর বাদাল বা মুসতাসনা হিসেবে মারফূ বিয যম্মাহ; هُمْ যমীরটি মুযাফ ইলাইহি।",
            "lexical_depth_bn": "স্বামী নিজেই একমাত্র প্রত্যক্ষদর্শী সাক্ষী হওয়ায় লি'আনের বিশেষ বিধান প্রযোজ্য হয়েছে।",
            "classical_notes": []
        },
        {
            "word": "فَشَهَادَةُ",
            "meaning_bn": "সুতরাং সাক্ষ্য হবে",
            "word_type": "اسم",
            "prefix_suffix_note": "মুবতাদা হিসেবে মারফূ এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ش . ه . د)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: شَهَادَةٌ | বহুবচন: شَهَادَاتٌ"
            },
            "taleel_or_irab": "মুবতাদা হিসেবে মারফূ বিয যম্মাহ; أَحَدِهِمْ হলো মুযাফ ইলাইহি।",
            "lexical_depth_bn": "লি'আনে স্বামীর পক্ষ থেকে শপথের আইনি প্রক্রিয়া।",
            "classical_notes": []
        },
        {
            "word": "أَحَدِهِمْ",
            "meaning_bn": "তাদের একজনের",
            "word_type": "اسم",
            "prefix_suffix_note": "মুযাফ ইলাইহি হিসেবে মাজরূর",
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
            "taleel_or_irab": "شَهَادَةُ শব্দের মুযাফ ইলাইহি হিসেবে মাজরূর বিল কাসরাহ; هِمْ যমীরটি মুযাফ ইলাইহি।",
            "lexical_depth_bn": "অভিযোগকারী স্বামী যার দায়িত্ব প্রথমে কসম খাওয়া।",
            "classical_notes": []
        },
        {
            "word": "شَهَادَاتٍ",
            "meaning_bn": "চারবার সাক্ষ্য বা কসম",
            "word_type": "اسم",
            "prefix_suffix_note": "মুযাফ ইলাইহি হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ش . ه . د)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: شَهَادَةٌ | বহুবচন: شَهَادَاتٌ"
            },
            "taleel_or_irab": "أَرْبَعُ শব্দের মুযাফ ইলাইহি হিসেবে মাজরূর বিল কাসরাহ (جمع مؤنث سالم)।",
            "lexical_depth_bn": "চারজন সাক্ষীর সমতুল্য হিসেবে চারবার আল্লাহর নামে কসম করা।",
            "classical_notes": []
        }
    ],
    7: [
        {
            "word": "الْكَاذِبِينَ",
            "meaning_bn": "মিথ্যুকদের অন্তর্ভুক্ত",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল ইয়া",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ك . ذ . ب)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: كَاذِبٌ | বহুবচন: كَاذِبُونَ"
            },
            "taleel_or_irab": "مِنْ হরফে জারের কারণে মাজরূর বিল ইয়া (جمع مذكر سالم)।",
            "lexical_depth_bn": "মিথ্যা অপবাদ দিলে নিজের ওপর আল্লাহর চিরন্তন লা'নত ডেকে নেওয়া।",
            "classical_notes": []
        }
    ],
    8: [
        {
            "word": "أَرْبَعَ",
            "meaning_bn": "চারবার",
            "word_type": "اسم",
            "prefix_suffix_note": "নায়েবে মাসদার হিসেবে মানসূব এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ر . ب . ع)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: أَرْبَعَةٌ | বহুবচন: أَرْبَعَاتٌ"
            },
            "taleel_or_irab": "تَشْهَدَ ক্রিয়ার নায়েবে মাফ'ঊলে মুতলাক হিসেবে মানসূব বিল ফাতহাহ; شَهَادَاتٍ হলো মুযাফ ইলাইহি।",
            "lexical_depth_bn": "স্বামীর চার কসমের বিপরীতে স্ত্রীর নিজের নির্দোষিতার সমর্থনে চার কসম।",
            "classical_notes": []
        },
        {
            "word": "شَهَادَاتٍ",
            "meaning_bn": "সাক্ষ্য বা শপথ",
            "word_type": "اسم",
            "prefix_suffix_note": "মুযাফ ইলাইহি হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ش . ه . د)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: شَهَادَةٌ | বহুবচন: شَهَادَاتٌ"
            },
            "taleel_or_irab": "أَرْبَعَ শব্দের মুযাফ ইলাইহি হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "আল্লাহর পবিত্র নামের শপথ দ্বারা স্ত্রীর আত্মপক্ষ সমর্থন।",
            "classical_notes": []
        },
        {
            "word": "الْكَاذِبِينَ",
            "meaning_bn": "নিশ্চয়ই সে (স্বামী) মিথ্যাবাদীদের একজন",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল ইয়া",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ك . ذ . ب)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: كَاذِبٌ | বহুবচন: كَاذِبُونَ"
            },
            "taleel_or_irab": "مِنْ হরফে জারের মাজরূর হিসেবে মাজরূর বিল ইয়া।",
            "lexical_depth_bn": "স্বামী যে মিথ্যারোপ করেছে তা দৃঢ়ভাবে খণ্ডন করা।",
            "classical_notes": []
        }
    ],
    9: [
        {
            "word": "وَالْخَامِسَةَ",
            "meaning_bn": "এবং পঞ্চমবারে এই শপথ করবে যে",
            "word_type": "اسم",
            "prefix_suffix_note": "মানসূব বিল ফাতহাহ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(خ . م . س)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: خَامِسَةٌ | বহুবচন: خَوَامِسُ"
            },
            "taleel_or_irab": "أَرْبَعَ شَهَادَاتٍ-এর ওপর মা'তূফ অথবা উহ্য ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "স্ত্রীর জন্য চূড়ান্ত সতর্কবাণী—পঞ্চমবারে নিজের ওপর আল্লাহর গযব কামনা।",
            "classical_notes": []
        },
        {
            "word": "الصَّادِقِينَ",
            "meaning_bn": "যদি সে সত্যবাদীদের দলভুক্ত হয়",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল ইয়া",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ص . د . ق)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: صَادِقٌ | বহুবচন: صَادِقُونَ"
            },
            "taleel_or_irab": "مِنْ হরফে জারের মাজরূর হিসেবে মাজরূর বিল ইয়া (جمع مذكر سالم)।",
            "lexical_depth_bn": "সত্যবাদীর বিরুদ্ধে মিথ্যা আত্মপক্ষ সমর্থনের চরম পরিণতি আল্লাহর ক্রোধ।",
            "classical_notes": []
        }
    ],
    10: [
        {
            "word": "وَرَحْمَتُهُ",
            "meaning_bn": "এবং তাঁর অপরিসীম দয়া ও করুণা",
            "word_type": "اسم",
            "prefix_suffix_note": "মা'তূফ হিসেবে মারফূ এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ر . ح . م)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: رَحْمَةٌ | বহুবচন: رَحَمَاتٌ"
            },
            "taleel_or_irab": "فَضْلُ শব্দের ওপর মা'তূফ হিসেবে মারফূ বিয যম্মাহ; هُ যমীরটি মুযাফ ইলাইহি।",
            "lexical_depth_bn": "আল্লাহর রহমত ও অনুগ্রহ না থাকলে মানুষ তাৎক্ষণিক ধ্বংস হয়ে যেত।",
            "classical_notes": []
        }
    ]
}

def merge_and_sort(existing_list, new_items, ayah_words):
    # build a word-to-index mapping from ayah_words
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
        
    with open("web/public/data/24/ruku-1.json", "r", encoding="utf-8") as f:
        ruku1 = json.load(f)
        
    total_added = 0
    total_words = 0
    for a in ruku1.get("ayahs", []):
        v = a.get("ayah")
        ayah_w = full_words.get(f"24:{v}", [])
        existing = a.get("tahqeeq", [])
        new_w = NEW_WORDS_RUKU1.get(v, [])
        merged = merge_and_sort(existing, new_w, ayah_w)
        added = len(merged) - len(existing)
        total_added += added
        total_words += len(merged)
        a["tahqeeq"] = merged
        print(f"Ayah {v:02d}: {len(existing)} -> {len(merged)} words (+{added})")
        
    with open("web/public/data/24/ruku-1.json", "w", encoding="utf-8") as f:
        json.dump(ruku1, f, ensure_ascii=False, indent=2)
        
    print(f"\n[SUCCESS] Ruku 1 expanded: +{total_added} words, total {total_words} words across Ayahs 1-10.")

if __name__ == "__main__":
    main()

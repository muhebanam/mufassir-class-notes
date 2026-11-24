#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expand Tahqeeq for Surah 24 Ruku 3 (Ayahs 21-26) to Maximum Words.
Adds all substantive words with full morphological precision.
"""

import json

null = None

NEW_WORDS_RUKU3 = {
    21: [
        {
            "word": "آمَنُوا",
            "meaning_bn": "যারা খাঁটি ঈমান এনেছো",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "إِفْعَالٌ",
                "jins": "مهموز الفاء",
                "root": "(أ . م . ن)",
                "masdar": "اَلْإِيمَانُ",
                "masdar_meaning": "ঈমান আনা; বিশ্বাস স্থাপন করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলায যম্ম; ওয়াও হলো ফা'ইল। الَّذِينَ-এর সিলাহ।",
            "lexical_depth_bn": "মুমিনদের সরাসরি সম্বোধন করে শয়তানের চক্রান্ত থেকে সতর্কবার্তা।",
            "classical_notes": []
        },
        {
            "word": "تَتَّبِعُوا",
            "meaning_bn": "তোমরা অনুসরণ করো না / পেছনে চলো না",
            "word_type": "فعل",
            "prefix_suffix_note": "নাহীসূচক لَا যোগে মাযযূম ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "مضارع معروف مجزوم بلا الناهية",
                "bab": "اِفْتِعَالٌ",
                "jins": "صحيح",
                "root": "(ت . ب . ع)",
                "masdar": "اَلْاِتِّبَاعُ",
                "masdar_meaning": "অনুসরণ করা; পদাঙ্ক অনুসরণ করা",
                "singular_plural": null
            },
            "taleel_or_irab": "لَا النَّاهِيَة এর কারণে মাযযূম বি হাযফিন নূন (মূলত تَتَّبِعُونَ ছিল); ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "শয়তানের প্রতারণাপূর্ণ প্ররোচনার কোনো ধাপে পা না বাড়ানোর আদেশ।",
            "classical_notes": []
        },
        {
            "word": "يَأْمُرُ",
            "meaning_bn": "সে প্ররোচিত করে ও নির্দেশ দেয়",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "نَصَرَ",
                "jins": "مهموز الفاء",
                "root": "(أ . م . ر)",
                "masdar": "اَلْأَمْرُ",
                "masdar_meaning": "আদেশ করা; প্ররোচিত করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ; ফা'ইল যমীর হলো مستتر (تقديره هو যা শয়তানের দিকে ফিরে)।",
            "lexical_depth_bn": "শয়তান মানুষকে পাপ ও অশ্লীলতার দিকে ক্রমাগত তাড়িত করে।",
            "classical_notes": []
        },
        {
            "word": "فَضْلُ",
            "meaning_bn": "আল্লাহর অপরিসীম অনুগ্রহ",
            "word_type": "اسم",
            "prefix_suffix_note": "মুবতাদা হিসেবে মারফূ এবং মুযাফ",
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
            "taleel_or_irab": "لَوْلَا-এর পর মুবতাদা হিসেবে মারফূ বিয যম্মাহ; خبر محذوف تقديره موجود।",
            "lexical_depth_bn": "শয়তানের ফাঁদ থেকে আত্মরক্ষায় আল্লাহর তাওফীকই একমাত্র উপায়।",
            "classical_notes": []
        },
        {
            "word": "وَرَحْمَتُهُ",
            "meaning_bn": "এবং তাঁর পরম দয়া",
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
            "lexical_depth_bn": "আত্মশুদ্ধি ও গুনাহমুক্ত জীবন পরিচালনায় ঐশী করুণার গুরুত্ব।",
            "classical_notes": []
        },
        {
            "word": "أَحَدٍ",
            "meaning_bn": "তোমাদের কোনো একজন মানুষও",
            "word_type": "اسم",
            "prefix_suffix_note": "ফা'ইল হিসেবে মাজরূর লাফযান মারফূ মহল্লান",
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
            "taleel_or_irab": "مِنْ জাইদাহ (অতিরিক্ত)-এর কারণে মাজরূর লাফযান, কিন্তু زَكَى ক্রিয়ার ফা'ইল হিসেবে মারফূ মহল্লান।",
            "lexical_depth_bn": "মানুষ নিজ শক্তিবলে কখনো পূর্ণ পবিত্র হতে পারে না, যদি না আল্লাহ অনুগ্রহ করেন।",
            "classical_notes": []
        },
        {
            "word": "يَشَاءُ",
            "meaning_bn": "যাকে তিনি ইচ্ছা করেন বা মনোনীত করেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "ضَرَبَ",
                "jins": "أجوف يائي مهموز اللام",
                "root": "(ش . ي . أ)",
                "masdar": "اَلْمَشِيئَةُ",
                "masdar_meaning": "ইচ্ছা করা; মনস্থ করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ; ফা'ইল যমীর হলো مستتر (تقديره هو)। مَنْ-এর সিলাহ।",
            "lexical_depth_bn": "হেদায়াত ও আত্মশুদ্ধি দানের ক্ষেত্রে আল্লাহর একচ্ছত্র সার্বভৌম কর্তৃত্ব।",
            "classical_notes": []
        },
        {
            "word": "سَمِيعٌ",
            "meaning_bn": "বান্দার সর্বাবস্থার সম্যক শ্রবণকারী",
            "word_type": "اسم",
            "prefix_suffix_note": "প্রথম খবর হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(س . م . ع)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: سَمِيعٌ | বহুবচন: سُمَعَاءُ"
            },
            "taleel_or_irab": "لفظ الجلالة (اللَّهُ) মুবতাদার প্রথম খবর হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "মুখনিঃসৃত প্রতিটি কথা ও প্রার্থনা তিনি সরাসরি শোনেন।",
            "classical_notes": []
        },
        {
            "word": "عَلِيمٌ",
            "meaning_bn": "অন্তরের গূঢ় রহস্যের পুঙ্খানুপুঙ্খ জ্ঞানী",
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
            "taleel_or_irab": "দ্বিতীয় খবর হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "কার অন্তরে খাঁটি ঈমান আর কার অন্তরে মুনাফিকি রয়েছে তা সম্যক পরিজ্ঞাত।",
            "classical_notes": []
        }
    ],
    22: [
        {
            "word": "الْفَضْلِ",
            "meaning_bn": "মর্যাদা, শ্রেষ্ঠত্ব ও আর্থিক সচ্ছলতা",
            "word_type": "اسم",
            "prefix_suffix_note": "মুযাফ ইলাইহি হিসেবে মাজরূর",
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
            "taleel_or_irab": "أُولُو শব্দের মুযাফ ইলাইহি হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "হযরত আবু বকর সিদ্দীক (রা.)-এর অনন্য ঈমানী শ্রেষ্ঠত্ব ও দানশীলতার প্রতি বিশেষ ইঙ্গিত।",
            "classical_notes": []
        },
        {
            "word": "يُؤْتُوا",
            "meaning_bn": "তারা প্রদান করবে / সাহায্য অব্যাহত রাখবে",
            "word_type": "فعل",
            "prefix_suffix_note": "আন (أَنْ) দ্বারা মানসূব ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "إِفْعَالٌ",
                "jins": "مهموز الفاء ناقص يائي",
                "root": "(أ . ت . ي)",
                "masdar": "اَلْإِيتَاءُ",
                "masdar_meaning": "প্রদান করা; দান করা",
                "singular_plural": null
            },
            "taleel_or_irab": "أَنْ মাসদারিয়্যাহ দ্বারা মানসূব বি হাযফিন নূন (মূলত يُؤْتُونَ ছিল); ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "ব্যক্তিগত মনোমালিন্যের কারণে আত্মীয়দের আর্থিক সহায়তা বন্ধ না করার তাগিদ।",
            "classical_notes": []
        },
        {
            "word": "وَالْمَسَاكِينَ",
            "meaning_bn": "এবং অভাবগ্রস্ত মিসকীনদের",
            "word_type": "اسم",
            "prefix_suffix_note": "মা'তূফ হিসেবে মানসূব বিল ইয়া",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(س . ك . ن)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: مِسْكِينٌ | বহুবচন: مَسَاكِينُ"
            },
            "taleel_or_irab": "أُولِي الْقُرْبَى-এর ওপর মা'তূফ হিসেবে মানসূব বিল ইয়া (جمع تكسير)।",
            "lexical_depth_bn": "সমাজে অসহায় ও দরিদ্র শ্রেণির মানবিক সহায়তার অধিকার।",
            "classical_notes": []
        },
        {
            "word": "وَالْمُهَاجِرِينَ",
            "meaning_bn": "এবং আল্লাহর রাহে হিজরতকারীদের",
            "word_type": "اسم",
            "prefix_suffix_note": "মা'তূফ হিসেবে মানসূব বিল ইয়া",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ه . ج . ر)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: مُهَاجِرٌ | বহুবচন: مُهَاجِرُونَ"
            },
            "taleel_or_irab": "মা'তূফ হিসেবে মানসূব বিল ইয়া (جمع مذكر سالم)।",
            "lexical_depth_bn": "মিস্তাহ ইবনে উসাসা (রা.)-এর মতো মুহাজির সাহাবী যিনি অপবাদে ভুলবশত জড়িয়ে পড়েছিলেন।",
            "classical_notes": []
        },
        {
            "word": "سَبِيلِ",
            "meaning_bn": "আল্লাহর পথ ও সন্তুষ্টির উদ্দেশ্যে",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(س . ب . ل)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: سَبِيلٌ | বহুবচন: سُبُلٌ"
            },
            "taleel_or_irab": "فِي হরফে জারের কারণে মাজরূর বিল কাসরাহ; اللَّهِ হলো মুযাফ ইলাইহি।",
            "lexical_depth_bn": "হিজরত ও জিহাদের পবিত্র পথ।",
            "classical_notes": []
        },
        {
            "word": "تُحِبُّونَ",
            "meaning_bn": "তোমরা কি এটি পছন্দ করো না",
            "word_type": "فعل",
            "prefix_suffix_note": "ইসতিফহাম তানকীরী সহ ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "مضارع معروف",
                "bab": "إِفْعَالٌ",
                "jins": "مضاعف ثلاثي",
                "root": "(ح . ب . ب)",
                "masdar": "اَلْإِحْبَابُ",
                "masdar_meaning": "ভালোবাসা; পছন্দ করা; কামনা করা",
                "singular_plural": null
            },
            "taleel_or_irab": "أَلَا التحضيضية-এর পর ফে'লে মুযারে মারফূ বি সুবূতিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "আল্লাহর ক্ষমা পাওয়ার আকাঙ্ক্ষায় মানুষের ভুলত্রুটি ক্ষমা করে দেওয়ার ঐশী প্ররোচনা।",
            "classical_notes": [
                {
                    "scholar_or_book": "তাফসীরে কাশশাফ (যমখশারী)",
                    "note": "আবু বকর (রা.) এই আয়াত শুনে সাথে সাথে বলে উঠেন: 'হ্যাঁ, আল্লাহর কসম! আমি চাই আল্লাহ আমাকে ক্ষমা করুন' এবং মিস্তাহর ভাতা পুনরায় চালু করেন।"
                }
            ]
        },
        {
            "word": "يَغْفِرَ",
            "meaning_bn": "তিনি তোমাদের ক্ষমা করে দেবেন",
            "word_type": "فعل",
            "prefix_suffix_note": "আন (أَنْ) দ্বারা মানসূব ফে'লে মুযারে",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "ضَرَبَ",
                "jins": "صحيح",
                "root": "(غ . ف . ر)",
                "masdar": "اَلْمَغْفِرَةُ",
                "masdar_meaning": "ক্ষমা করা; মার্জনা করা",
                "singular_plural": null
            },
            "taleel_or_irab": "أَنْ মাসদারিয়্যাহ দ্বারা মানসূব বিল ফাতহাহ; لفظ الجلالة (اللَّهُ) হলো ফা'ইল।",
            "lexical_depth_bn": "বান্দার গুনাহ ঢেকে দেওয়া ও মার্জনা করা।",
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
            "taleel_or_irab": "اللَّهُ মুবতাদার প্রথম খবর হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "যে রব বান্দার ত্রুটি বারবার মার্জনা করেন।",
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
            "lexical_depth_bn": "বান্দার প্রতি চিরন্তন দয়ার ফল্গুধারা।",
            "classical_notes": []
        }
    ],
    23: [
        {
            "word": "يَرْمُونَ",
            "meaning_bn": "অপবাদ দেয় বা কলঙ্ক রটায়",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "ضَرَبَ",
                "jins": "ناقص يائي",
                "root": "(ر . م . ي)",
                "masdar": "اَلرَّمْيُ",
                "masdar_meaning": "অপবাদ দেওয়া; কটুবাণী নিক্ষেপ করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বি সুবূতিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "সতী-সাধ্বী নিষ্পাপ নারীদের ওপর কুৎসা আরোপ।",
            "classical_notes": []
        },
        {
            "word": "الْمُحْصَنَاتِ",
            "meaning_bn": "পবিত্র ও সতী-সাধ্বী নারীদের",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব বিল কাসরাহ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ح . ص . ن)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: مُحْصَنَةٌ | বহুবচন: مُحْصَنَاتٌ"
            },
            "taleel_or_irab": "يَرْمُونَ ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল কাসরাহ (جمع مؤنث سالم)।",
            "lexical_depth_bn": "চারিত্রিক নিষ্কলুষতা ও বিবাহের পবিত্র দুর্গে সুরক্ষিত নারী।",
            "classical_notes": []
        },
        {
            "word": "الْمُؤْمِنَاتِ",
            "meaning_bn": "বিশ্বাসী মুমিন নারীগণকে",
            "word_type": "اسم",
            "prefix_suffix_note": "দ্বিতীয় সিফাত হিসেবে মানসূব বিল কাসরাহ",
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
            "taleel_or_irab": "الْمُحْصَنَاتِ শব্দের দ্বিতীয় সিফাত হিসেবে মানসূব বিল কাসরাহ।",
            "lexical_depth_bn": "যাদের অন্তরে আল্লাহর ভয় ও ঈমানের নুর সদা জাগ্রত।",
            "classical_notes": []
        },
        {
            "word": "الدُّنْيَا",
            "meaning_bn": "পার্থিব জীবনে অভিশপ্ত",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ মুকাদ্দারা",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "ناقص واوي",
                "root": "(د . ن . و)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: دُنْيَا | বহুবচন: دُنًى"
            },
            "taleel_or_irab": "فِي হরফে জারের কারণে মাজরূর বিল কাসরাহ মুকাদ্দারা আলাল আলিফ।",
            "lexical_depth_bn": "দুনিয়াতে হদ্দ, লাঞ্ছনা ও আল্লাহর করুণা থেকে বিতাড়ন।",
            "classical_notes": []
        },
        {
            "word": "وَالْآخِرَةِ",
            "meaning_bn": "এবং পরকালে চিরস্থায়ী লা'নতপ্রাপ্ত",
            "word_type": "اسم",
            "prefix_suffix_note": "মা'তূফ হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "مهموز الفاء",
                "root": "(أ . خ . ر)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: آخِرَةٌ | বহুবচন: أُوَاخِرُ"
            },
            "taleel_or_irab": "الدُّنْيَا শব্দের ওপর মা'তূফ হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "আখেরাতে অনন্তকালের শাস্তি।",
            "classical_notes": []
        },
        {
            "word": "عَذَابٌ",
            "meaning_bn": "ভয়াবহ শাস্তি",
            "word_type": "اسم",
            "prefix_suffix_note": "মুবতাদা মুআখখার হিসেবে মারফূ",
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
            "taleel_or_irab": "لَهُمْ জার-মাজরূরের পর মুবতাদা মুআখখার হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "অপবাদের পাপীদের জন্য নির্ধারিত দণ্ড।",
            "classical_notes": []
        },
        {
            "word": "عَظِيمٌ",
            "meaning_bn": "মহা তীব্র ও অবর্ণনীয়",
            "word_type": "اسم",
            "prefix_suffix_note": "সিফাত হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ع . ظ . م)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: عَظِيمٌ | বহুবচন: عُظَمَاءُ"
            },
            "taleel_or_irab": "عَذَابٌ শব্দের সিফাত হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "জাহান্নামের গভীরতম অগ্নির শাস্তি।",
            "classical_notes": []
        }
    ],
    24: [
        {
            "word": "يَوْمَ",
            "meaning_bn": "যে মহাদিবসে",
            "word_type": "اسم",
            "prefix_suffix_note": "যরফিজ জামান হিসেবে মানসূব",
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
            "taleel_or_irab": "যরফিজ জামান হিসেবে মানসূব বিল ফাতহাহ (عَذَابٌ عَظِيمٌ-এর সাথে সম্পর্কিত)।",
            "lexical_depth_bn": "কিয়ামত দিবসের বিচার যখন সব গোপনীয়তা প্রকাশ পেয়ে যাবে।",
            "classical_notes": []
        },
        {
            "word": "وَأَيْدِيهِمْ",
            "meaning_bn": "এবং তাদের নিজ নিজ হাতসমূহ",
            "word_type": "اسم",
            "prefix_suffix_note": "মা'তূফ হিসেবে মারফূ এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "নাقص يائي",
                "root": "(ي . د . ي)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: يَدٌ | বহুবচন: أَيْدٍ"
            },
            "taleel_or_irab": "أَلْسِنَتُهُمْ শব্দের ওপর মা'তূফ হিসেবে মারফূ বিয যম্মাহ মুকাদ্দারা; هِمْ যমীরটি মুযাফ ইলাইহি।",
            "lexical_depth_bn": "হাত কথা বলবে এবং অপরাধের বর্ণনা দেবে।",
            "classical_notes": []
        },
        {
            "word": "وَأَرْجُلُهُمْ",
            "meaning_bn": "এবং তাদের পা-সমূহ",
            "word_type": "اسم",
            "prefix_suffix_note": "মা'তূফ হিসেবে মারফূ এবং মুযাফ",
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
            "taleel_or_irab": "মা'তূফ হিসেবে মারফূ বিয যম্মাহ; هُمْ যমীরটি মুযাফ ইলাইহি।",
            "lexical_depth_bn": "পায়ের পদচিহ্ন ও চলাচল সাক্ষ্য হিসেবে দাঁড়িয়ে যাবে।",
            "classical_notes": []
        },
        {
            "word": "يَعْمَلُونَ",
            "meaning_bn": "তারা যা কিছু আমল বা অপকর্ম করত",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "سَمِعَ",
                "jins": "صحيح",
                "root": "(ع . م . ل)",
                "masdar": "اَلْعَمَلُ",
                "masdar_meaning": "কাজ করা; আমল করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বি সুবূতিন নূন; كَانُوا-এর খবর হিসেবে মহলে নাসব-এ রয়েছে।",
            "lexical_depth_bn": "মানুষের সমস্ত গোপন ও প্রকাশ্য কাজের নিখুঁত প্রতিফল।",
            "classical_notes": []
        }
    ],
    25: [
        {
            "word": "يَعْلَمُونَ",
            "meaning_bn": "তারা চূড়ান্তভাবে জানতে পারবে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "سَمِعَ",
                "jins": "صحيح",
                "root": "(ع . ل . م)",
                "masdar": "اَلْعِلْمُ",
                "masdar_meaning": "জানা; স্পষ্ট উপলব্ধি করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বি সুবূতিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "পরকালে সত্য উদ্ভাসিত হলে কাফির ও মুনাফিকদের অনুতাপ।",
            "classical_notes": []
        },
        {
            "word": "الْحَقُّ",
            "meaning_bn": "তিনিই চিরন্তন সত্য সত্তা",
            "word_type": "اسم",
            "prefix_suffix_note": "খবর হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "مضاعف ثلاثي",
                "root": "(ح . ق . ق)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: حَقٌّ | বহুবচন: حُقُوقٌ"
            },
            "taleel_or_irab": "هُوَ যমীরের খবর হিসেবে মারফূ বিয যম্মাহ (أَنَّ-এর খবর)।",
            "lexical_depth_bn": "আল্লাহ তা'আলার পবিত্র আসমাউল হুসনার অন্যতম—যাঁর অস্তিত্ব, ওয়াদা ও বিচার চিরন্তন সত্য।",
            "classical_notes": [
                {
                    "scholar_or_book": "মুফরাদাতুল কুরআন (ইমাম রাগেব)",
                    "note": "الحق হলো এমন অবিচল বাস্তবতা যাতে কোনো মিথ্যার সংমিশ্রণ হতে পারে না; আল্লাহ স্বয়ং আল-হাক্ক।"
                }
            ]
        },
        {
            "word": "الْمُبِينُ",
            "meaning_bn": "যাঁর সত্যতা ও ন্যায়বিচার সুপ্রভাত",
            "word_type": "اسم",
            "prefix_suffix_note": "সিফাত হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف يائي",
                "root": "(ب . ي . ن)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: مُبِينٌ | বহুবচন: مُبِينُونَ"
            },
            "taleel_or_irab": "الْحَقُّ শব্দের সিফাত হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "যা সত্যকে সম্পূর্ণরূপে উন্মোচন ও প্রকাশ করে।",
            "classical_notes": []
        }
    ],
    26: [
        {
            "word": "لِلْخَبِيثِينَ",
            "meaning_bn": "দুশ্চরিত্র অপবিত্র পুরুষদের জন্য",
            "word_type": "اسم",
            "prefix_suffix_note": "লাম হরফে জার সহ মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(خ . ب . ث)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: خَبِيثٌ | বহুবচন: خَبِيثُونَ"
            },
            "taleel_or_irab": "لِ হরফে জারের কারণে মাজরূর বিল ইয়া (جمع مذكر سالم); شبه جملة খবর হিসেবে মারফূ।",
            "lexical_depth_bn": "খারাপ কথা বা খারাপ নারী কেবল অসৎ মানুষের সাথেই সামঞ্জস্যপূর্ণ।",
            "classical_notes": []
        },
        {
            "word": "وَالْخَبِيثُونَ",
            "meaning_bn": "এবং অপবিত্র পুরুষেরা",
            "word_type": "اسم",
            "prefix_suffix_note": "মুবতাদা হিসেবে মারফূ বিল ওয়াও",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(خ . ب . ث)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: خَبِيثٌ | বহুবচন: خَبِيثُونَ"
            },
            "taleel_or_irab": "মুবতাদা হিসেবে মারফূ বিল ওয়াও (جمع مذكر سالم)।",
            "lexical_depth_bn": "চরিত্রহীনদের স্বভাব ও ঝোঁক অসৎ চরিত্রের প্রতিই থাকে।",
            "classical_notes": []
        },
        {
            "word": "لِلطَّيِّبِينَ",
            "meaning_bn": "পবিত্র ও সচ্চরিত্র পুরুষদের জন্য",
            "word_type": "اسم",
            "prefix_suffix_note": "লাম হরফে জার সহ মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف يائي",
                "root": "(ط . ي . ب)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: طَيِّبٌ | বহুবচন: طَيِّبُونَ"
            },
            "taleel_or_irab": "لِ হরফে জারের মাজরূর হিসেবে মাজরূর বিল ইয়া; شبه جملة খবর।",
            "lexical_depth_bn": "পবিত্র নারী ও পবিত্র বাক্য সৎ চরিত্রবান মানুষদেরই ভূষণ।",
            "classical_notes": []
        },
        {
            "word": "وَالطَّيِّبُونَ",
            "meaning_bn": "এবং পবিত্র ও চরিত্রবান পুরুষেরা",
            "word_type": "اسم",
            "prefix_suffix_note": "মুবতাদা হিসেবে মারফূ বিল ওয়াও",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف يائي",
                "root": "(ط . ي . ب)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: طَيِّبٌ | বহুবচন: طَيِّبُونَ"
            },
            "taleel_or_irab": "মুবতাদা হিসেবে মারফূ বিল ওয়াও (جمع مذكر سالم)।",
            "lexical_depth_bn": "রাসূলুল্লাহ ﷺ ও হযরত আয়েশা (রা.) উভয়ই পবিত্রতম মর্যাদায় অধিষ্ঠিত।",
            "classical_notes": []
        },
        {
            "word": "يَقُولُونَ",
            "meaning_bn": "যা অপবাদকারীরা রটায় ও বলে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "نَصَرَ",
                "jins": "أجوف واوي",
                "root": "(ق . و . ل)",
                "masdar": "اَلْقَوْلُ",
                "masdar_meaning": "বলা; অপবাদ দেওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বি সুবূতিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "কুৎসাকারীদের যাবতীয় ভিত্তিহীন মিথ্যাচার থেকে আয়েশা (রা.) পুতপবিত্র।",
            "classical_notes": []
        },
        {
            "word": "رِزْقٌ",
            "meaning_bn": "মর্যাদাপূর্ণ জীবিকা ও জান্নাতের নেয়ামত",
            "word_type": "اسم",
            "prefix_suffix_note": "মা'তূফ হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ر . ز . ق)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: رِزْقٌ | বহুবচন: أَرْزَاقٌ"
            },
            "taleel_or_irab": "مَغْفِرَةٌ শব্দের ওপর মা'তূফ হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "জান্নাতের সুউচ্চ সম্মান ও অবিনশ্বর অনুগ্রহ।",
            "classical_notes": []
        },
        {
            "word": "كَرِيمٌ",
            "meaning_bn": "সম্মানজনক ও মর্যাদাপূর্ণ",
            "word_type": "اسم",
            "prefix_suffix_note": "সিফাত হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ك . ر . م)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: كَرِيمٌ | বহুবচন: كِرَامٌ"
            },
            "taleel_or_irab": "رِزْقٌ শব্দের সিফাত (نعت) হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "যে নেয়ামতে কোনো কষ্ট বা খোঁটা নেই, কেবল সম্মান ও সন্তুষ্টি।",
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
        
    with open("web/public/data/24/ruku-3.json", "r", encoding="utf-8") as f:
        ruku3 = json.load(f)
        
    total_added = 0
    total_words = 0
    for a in ruku3.get("ayahs", []):
        v = a.get("ayah")
        ayah_w = full_words.get(f"24:{v}", [])
        existing = a.get("tahqeeq", [])
        new_w = NEW_WORDS_RUKU3.get(v, [])
        merged = merge_and_sort(existing, new_w, ayah_w)
        added = len(merged) - len(existing)
        total_added += added
        total_words += len(merged)
        a["tahqeeq"] = merged
        print(f"Ayah {v:02d}: {len(existing)} -> {len(merged)} words (+{added})")
        
    with open("web/public/data/24/ruku-3.json", "w", encoding="utf-8") as f:
        json.dump(ruku3, f, ensure_ascii=False, indent=2)
        
    print(f"\n[SUCCESS] Ruku 3 expanded: +{total_added} words, total {total_words} words across Ayahs 21-26.")

if __name__ == "__main__":
    main()

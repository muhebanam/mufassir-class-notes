#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expand Tahqeeq for Surah 24 Ruku 5 (Ayahs 35-43) to Maximum Words.
Ayatun Noor, Deep Ocean Darknesses, Universal Glorification, and Storm Metaphors.
"""

import json

null = None

NEW_WORDS_RUKU5 = {
    35: [
        {
            "word": "نُورُ",
            "meaning_bn": "জ্যোতির্ময় ও পথপ্রদর্শক",
            "word_type": "اسم",
            "prefix_suffix_note": "খবর হিসেবে মারফূ এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف واوي",
                "root": "(ن . و . ر)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: نُورٌ | বহুবচন: أَنْوَارٌ"
            },
            "taleel_or_irab": "لفظ الجلالة (اللَّهُ) মুবতাদার খবর হিসেবে মারফূ বিয যম্মাহ; السَّمَاوَاتِ হলো মুযাফ ইলাইহি।",
            "lexical_depth_bn": "আল্লাহ নভোমণ্ডল ও ভূমণ্ডলের আদি ও অনন্ত সত্যের আলোকবর্তিকা এবং সঠিক পথের দিশারী।",
            "classical_notes": [
                {
                    "scholar_or_book": "মুফরাদাতুল কুরআন (ইমাম রাগেব)",
                    "note": "النور হলো এমন আলোকচ্ছটা যা নিজে দৃশ্যমান এবং অপরাপর বস্তুকে দৃশ্যমান করে; রূপকার্থে জ্ঞান, প্রজ্ঞা ও ঐশী হেদায়াতকে নূর বলা হয়।"
                }
            ]
        },
        {
            "word": "السَّمَاوَاتِ",
            "meaning_bn": "আকাশমণ্ডলী",
            "word_type": "اسم",
            "prefix_suffix_note": "মুযাফ ইলাইহি হিসেবে মাজরূর বিল কাসরাহ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "ناقص واوي",
                "root": "(س . م . و)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: سَمَاءٌ | বহুবচন: سَمَاوَاتٌ"
            },
            "taleel_or_irab": "نُورُ শব্দের মুযাফ ইলাইহি হিসেবে মাজরূর বিল কাসরাহ (جمع مؤنث سالم)।",
            "lexical_depth_bn": "সাত আসমানের বিশালতা ও নভোমণ্ডলীয় জগৎ।",
            "classical_notes": []
        },
        {
            "word": "وَالْأَرْضِ",
            "meaning_bn": "এবং সমগ্র ভূমণ্ডল",
            "word_type": "اسم",
            "prefix_suffix_note": "মা'তূফ হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "مهموز الفاء",
                "root": "(أ . ر . ض)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: أَرْضٌ | বহুবচন: أَرَاضٍ"
            },
            "taleel_or_irab": "السَّمَاوَاتِ শব্দের ওপর মা'তূফ হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "মানবজাতির আবাসভূমি এই পৃথিবী।",
            "classical_notes": []
        },
        {
            "word": "كَوْكَبٌ",
            "meaning_bn": "উজ্জ্বল নক্ষত্র বা গ্রহ",
            "word_type": "اسم",
            "prefix_suffix_note": "খবর হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "رباعي مجرد",
                "root": "(ك . و . ك . ب)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: كَوْكَبٌ | বহুবচন: كَوَاكِبُ"
            },
            "taleel_or_irab": "كَأَنَّهَا-এর খবর হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "কাঁচের পাত্রটি এত স্বচ্ছ ও পরিচ্ছন্ন যেন এক দীপ্তিমান মুক্তাতুল্য তারকা।",
            "classical_notes": []
        },
        {
            "word": "يُوقَدُ",
            "meaning_bn": "যা প্রজ্বলিত করা হয়",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মাঝহূল",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع مجهول",
                "bab": "إِفْعَالٌ",
                "jins": "مثال واوي",
                "root": "(و . ق . د)",
                "masdar": "اَلْإِيقَادُ",
                "masdar_meaning": "প্রজ্বলিত করা; জ্বালানো",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মাঝহূল মারফূ বিয যম্মাহ; নায়েবে ফা'ইল হলো যমীর مستتر (যা প্রদীপের দিকে ফিরে)।",
            "lexical_depth_bn": "অগ্নিশিখা যা বরকতময় তেলের সাহায্যে আলো বিকিরণ করে।",
            "classical_notes": []
        },
        {
            "word": "مُبَارَكَةٍ",
            "meaning_bn": "বরকতময় ও কল্যাণময়",
            "word_type": "اسم",
            "prefix_suffix_note": "সিফাত হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ب . ر . ك)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: مُبَارَكَةٌ | বহুবচন: مُبَارَكَاتٌ"
            },
            "taleel_or_irab": "شَجَرَةٍ শব্দের প্রথম সিফাত হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "যেই জলপাই গাছের ফল, তেল ও কাঠে রয়েছে অফুরন্ত কল্যাণ ও রোগমুক্তি।",
            "classical_notes": []
        },
        {
            "word": "شَرْقِيَّةٍ",
            "meaning_bn": "কেবল পূর্বমুখী নয়",
            "word_type": "اسم",
            "prefix_suffix_note": "সিফাত হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ش . ر . ق)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: شَرْقِيَّةٌ | বহুবচন: شَرْقِيَّاتٌ"
            },
            "taleel_or_irab": "لا نافيه-এর পর সিফাত হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "গাছটি এমন উন্মুক্ত ময়দানে অবস্থিত যেখানে সূর্যোদয় থেকে সূর্যাস্ত সারাদিন রোদ পড়ে, ফলে এর তেল সর্বোচ্চ পরিশোধিত।",
            "classical_notes": []
        },
        {
            "word": "غَرْبِيَّةٍ",
            "meaning_bn": "এবং কেবল পশ্চিমমুখীও নয়",
            "word_type": "اسم",
            "prefix_suffix_note": "মা'তূফ হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(غ . ر . ب)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: غَرْبِيَّةٌ | বহুবচন: غَرْبِيَّاتٌ"
            },
            "taleel_or_irab": "মা'তূফ হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "মধ্যবর্তী অবস্থানে থাকায় এর তেলেও থাকে পরম স্বচ্ছতা ও চমৎকার ঔজ্জ্বল্য।",
            "classical_notes": []
        },
        {
            "word": "يَكَادُ",
            "meaning_bn": "উপক্রম হয় বা প্রায় হয়ে যায়",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মা'রূফ (মুকারাবাহ)",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "فَعَلَ",
                "jins": "أجوف واوي",
                "root": "(ك . و . د)",
                "masdar": "اَلْكَوْدُ",
                "masdar_meaning": "উপক্রম হওয়া; কাছাকাছি পৌঁছানো",
                "singular_plural": null
            },
            "taleel_or_irab": "أَفْعَالُ الْمُقَارَبَة এর অন্তর্ভুক্ত; মারফূ বিয যম্মাহ; زَيْتُهَا হলো এর ইসম।",
            "lexical_depth_bn": "তেলের তীব্র স্বচ্ছতা এমন যে আগুন স্পর্শ ছাড়াই যেন তা জ্বলে ওঠার উপক্রম।",
            "classical_notes": []
        },
        {
            "word": "يُضِيءُ",
            "meaning_bn": "স্বয়ং আলো বিকিরণ করে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "إِفْعَالٌ",
                "jins": "أجوف واوي مهموز اللام",
                "root": "(ض . و . أ)",
                "masdar": "اَلْإِضَاءَةُ",
                "masdar_meaning": "আলোকিত করা; আলো বিকিরণ করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ; يَكَادُ-এর খবর হিসেবে মহলে নাসব-এ রয়েছে।",
            "lexical_depth_bn": "ফিতরাত ও ঐশী হেদায়াতের আলোর চরম মেলবন্ধন।",
            "classical_notes": []
        },
        {
            "word": "يَهْدِي",
            "meaning_bn": "তিনি পথপ্রদর্শন করেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "ضَرَبَ",
                "jins": "নাقص يائي",
                "root": "(ه . د . ي)",
                "masdar": "اَلْهِدَايَةُ",
                "masdar_meaning": "হেদায়াত দেওয়া; সঠিক পথ দেখানো",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ মুকাদ্দারা আলাল ইয়া; لفظ الجلالة (اللَّهُ) হলো ফা'ইল।",
            "lexical_depth_bn": "যার অন্তরে সত্য গ্রহণের আগ্রহ থাকে আল্লাহ তাকে তাঁর নূরের দিকে পরিচালিত করেন।",
            "classical_notes": []
        },
        {
            "word": "الْأَمْثَالَ",
            "meaning_bn": "বহু প্রজ্ঞাপূর্ণ দৃষ্টান্তসমূহ",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(م . ث . ل)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: مَثَلٌ | বহুবচন: أَمْثَالٌ"
            },
            "taleel_or_irab": "يَضْرِبُ ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "অদৃশ্য সত্যকে মানুষের বোধগম্য করার জন্য দৃশ্যমান রূপকের উপস্থাপন।",
            "classical_notes": []
        }
    ],
    36: [
        {
            "word": "بُيُوتٍ",
            "meaning_bn": "এমন গৃহসমূহে (মসজিদসমূহে)",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ",
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
            "taleel_or_irab": "فِي হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "জমিনে আল্লাহর ঘর অর্থাৎ মসজিদসমূহ যেখানে ঐশী নূরের চর্চা হয়।",
            "classical_notes": [
                {
                    "scholar_or_book": "তাফসীরে কাশশাফ (যমখশারী)",
                    "note": "অধিকাংশ মুফাসসিরের মতে 'বুয়ূত' দ্বারা মসজিদসমূহ উদ্দেশ্য; যা ইবাদত ও তাযকীয়ার জন্য বিশেষভাবে নির্মিত।"
                }
            ]
        },
        {
            "word": "أَذِنَ",
            "meaning_bn": "আল্লাহ নির্দেশ ও অনুমতি দিয়েছেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "سَمِعَ",
                "jins": "مهموز الفاء",
                "root": "(أ . ذ . ن)",
                "masdar": "اَلْإِذْنُ",
                "masdar_meaning": "অনুমতি দেওয়া; নির্দেশ দেওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলাল ফাতহ; لفظ الجلالة (اللَّهُ) হলো ফা'ইল।",
            "lexical_depth_bn": "মসজিদের মর্যাদা রক্ষা ও তাকে অপবিত্রতা থেকে মুক্ত রাখার ঐশী হুকুম।",
            "classical_notes": []
        },
        {
            "word": "وَيُذْكَرَ",
            "meaning_bn": "এবং যাতে স্মরণ করা হয়",
            "word_type": "فعل",
            "prefix_suffix_note": "মা'তূফ হিসেবে মানসূব ফে'লে মুযারে মাঝহূল",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع مجهول",
                "bab": "نَصَرَ",
                "jins": "صحيح",
                "root": "(ذ . ك . ر)",
                "masdar": "اَلذِّكْرُ",
                "masdar_meaning": "স্মরণ করা; যিকির করা",
                "singular_plural": null
            },
            "taleel_or_irab": "تُرْفَعَ শব্দের ওপর মা'তূফ হিসেবে মানসূব বিল ফাতহাহ (مبني للمجهول); اسْمُهُ হলো নায়েবে ফা'ইল।",
            "lexical_depth_bn": "নামাজ, তিলাওয়াত ও তাসবীহের মাধ্যমে আল্লাহর মহিমা প্রকাশ।",
            "classical_notes": []
        },
        {
            "word": "يُسَبِّحُ",
            "meaning_bn": "পবিত্রতা ও মহিমা ঘোষণা করে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "تَفْعِيلٌ",
                "jins": "صحيح",
                "root": "(س . ب . ح)",
                "masdar": "اَلتَّسْبِيحُ",
                "masdar_meaning": "তাসবীহ পাঠ করা; পবিত্রতা ঘোষণা করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ; পরবর্তী আয়াতে উল্লিখিত رِجَالٌ হলো এর ফা'ইল।",
            "lexical_depth_bn": "প্রতিটি সকাল ও সন্ধ্যায় একনিষ্ঠচিত্তে আল্লাহর ইবাদতে রত থাকা।",
            "classical_notes": []
        }
    ],
    37: [
        {
            "word": "رِجَالٌ",
            "meaning_bn": "এমন কিছু নিষ্ঠাবান পুরুষ",
            "word_type": "اسم",
            "prefix_suffix_note": "ফা'ইল হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ر . ج . ل)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: رَجُلٌ | বহুবচন: رِجَالٌ"
            },
            "taleel_or_irab": "পূর্ববর্তী আয়াতের يُسَبِّحُ ক্রিয়ার ফা'ইল হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "খাঁটি ঈমানদার পুরুষ যাদের পৌরুষ আল্লাহর আনুগত্যে প্রতিষ্ঠিত।",
            "classical_notes": [
                {
                    "scholar_or_book": "মুফরাদাতুল কুরআন (ইমাম রাগেব)",
                    "note": "الرجل হলো পূর্ণবয়স্ক পুরুষ; কুরআনে বহু স্থানে رِجَالٌ শব্দ দিয়ে ঈমানের পরাকাষ্ঠা ও দৃঢ় সংকল্পসম্পন্ন মুমিনদের সম্মানসূচক সম্বোধন করা হয়েছে।"
                }
            ]
        },
        {
            "word": "تُلْهِيهِمْ",
            "meaning_bn": "তাদেরকে উদাসীন বা গাফেল করে না",
            "word_type": "فعل",
            "prefix_suffix_note": "নাফীসূচক لَا যোগে ফে'লে মুযারে",
            "morphology": {
                "sighah": "واحد مؤنث غائب",
                "bahas": "مضارع معروف",
                "bab": "إِفْعَالٌ",
                "jins": "ناقص واوي",
                "root": "(ل . ه . و)",
                "masdar": "اَلْإِلْهَاءُ",
                "masdar_meaning": "উদাসীন করা; অন্যমনস্ক করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ মুকাদ্দারা; تِجَارَةٌ হলো এর ফা'ইল; هِمْ মাফ'ঊলে বিহি।",
            "lexical_depth_bn": "ব্যবসা-বাণিজ্য ও জাগতিক লাভক্ষতির ব্যস্ততা তাদের নামাজের সময় গাফেল করতে পারে না।",
            "classical_notes": []
        },
        {
            "word": "يَخَافُونَ",
            "meaning_bn": "তারা গভীর শঙ্কা ও ভয় পোষণ করে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "سَمِعَ",
                "jins": "أجوف واوي",
                "root": "(خ . و . ف)",
                "masdar": "اَلْخَوْفُ",
                "masdar_meaning": "ভয় করা; শঙ্কিত থাকা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বি সুবূতিন নূন; ওয়াও হলো ফা'ইল। জুমলাটি رِجَالٌ-এর সিফাত।",
            "lexical_depth_bn": "কিয়ামতের কঠিন দিনের হিসাবের ভয় যা মুমিনকে পাপমুক্ত রাখে।",
            "classical_notes": []
        },
        {
            "word": "الْقُلُوبُ",
            "meaning_bn": "মানুষের অন্তরসমূহ উলটপালট হয়ে যাবে",
            "word_type": "اسم",
            "prefix_suffix_note": "ফা'ইল হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ق . ل . ب)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: قَلْبٌ | বহুবচন: قُلُوبٌ"
            },
            "taleel_or_irab": "تَتَقَلَّبُ ক্রিয়ার ফা'ইল হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "কিয়ামতের চরম আতঙ্কে অন্তরের বিচলিত ও ভীতসন্ত্রস্ত অবস্থা।",
            "classical_notes": []
        }
    ],
    38: [
        {
            "word": "أَحْسَنَ",
            "meaning_bn": "সর্বোত্তম প্রতিদান",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ح . س . ن)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: أَحْسَنُ | বহুবচন: أَحَاسِنُ"
            },
            "taleel_or_irab": "يَجْزِيَهُمُ ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ; مَا موصولة হলো মুযাফ ইলাইহি।",
            "lexical_depth_bn": "আল্লাহ নেক কাজের দশগুণ থেকে সাতশত গুণ বা তারও অধিক উত্তম বদলা দান করবেন।",
            "classical_notes": []
        },
        {
            "word": "وَيَزِيدَهُم",
            "meaning_bn": "এবং তিনি তাদের আরও বাড়িয়ে দেবেন",
            "word_type": "فعل",
            "prefix_suffix_note": "মা'তূফ হিসেবে মানসূব ফে'লে মুযারে",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "ضَرَبَ",
                "jins": "أجوف يائي",
                "root": "(ز . ي . د)",
                "masdar": "اَلزِّيَادَةُ",
                "masdar_meaning": "বৃদ্ধি করা; বাড়িয়ে দেওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "يَجْزِيَهُمُ শব্দের ওপর মা'তূফ হিসেবে মানসূব বিল ফাতহাহ; هُمْ যমীরটি মাফ'ঊলে বিহি।",
            "lexical_depth_bn": "আমলের নির্ধারিত বদলার বাইরে আল্লাহর নিজস্ব অনুগ্রহ থেকে অতিরিক্ত দান।",
            "classical_notes": []
        },
        {
            "word": "يَرْزُقُ",
            "meaning_bn": "তিনি রিজিক দান করেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "نَصَرَ",
                "jins": "صحيح",
                "root": "(ر . ز . ق)",
                "masdar": "اَلرِّزْقُ",
                "masdar_meaning": "রিজিক দেওয়া; অনুগ্রহ করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ; ফা'ইল যমীর হলো مستتر (تقديره هو)।",
            "lexical_depth_bn": "আল্লাহর অফুরন্ত ধনভাণ্ডার যা হিসাবের ঊর্ধ্বে অবারিত।",
            "classical_notes": []
        }
    ],
    39: [
        {
            "word": "أَعْمَالُهُمْ",
            "meaning_bn": "কাফিরদের যাবতীয় আমল ও কর্ম",
            "word_type": "اسم",
            "prefix_suffix_note": "মুবতাদা হিসেবে মারফূ এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ع . م . ل)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: عَمَلٌ | বহুবচন: أَعْمَالٌ"
            },
            "taleel_or_irab": "মুবতাদা হিসেবে মারফূ বিয যম্মাহ; هُمْ যমীরটি মুযাফ ইলাইহি। كَسَرَابٍ হলো এর খবর।",
            "lexical_depth_bn": "ঈমানহীন ভালো কাজ কিয়ামতের দিন মরীচিকার মতো শূন্য ও মূল্যহীন প্রমাণিত হবে।",
            "classical_notes": []
        },
        {
            "word": "يَحْسَبُهُ",
            "meaning_bn": "তাকে ধারণা করে বা ভেবে বসে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ সহ মাফ'ঊল",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "حَسِبَ",
                "jins": "صحيح",
                "root": "(ح . س . ب)",
                "masdar": "اَلْحُسْبَانُ",
                "masdar_meaning": "ধারণা করা; অনুমান করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ; هُ যমীরটি প্রথম মাফ'ঊলে বিহি; الظَّمْآنُ হলো এর ফা'ইল।",
            "lexical_depth_bn": "মরুভূমিতে পিপাসার্ত পথিকের মরিচীকায় পানি দেখার মতো কাফিরের বৃথা আশা।",
            "classical_notes": []
        },
        {
            "word": "وَجَدَ",
            "meaning_bn": "সে দেখতে পেল বা উপস্থিত পেল",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "ضَرَبَ",
                "jins": "مثال واوي",
                "root": "(و . ج . د)",
                "masdar": "اَلْوِجْدَانُ",
                "masdar_meaning": "উপস্থিত পাওয়া; প্রত্যক্ষ করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলাল ফাতহ; ফা'ইল যমীর مستتر (تقديره هو)।",
            "lexical_depth_bn": "মৃত্যুর পর কাফির দেখবে তার কোনো সঞ্চয় নেই, বরং সামনে কেবল আল্লাহ বিচারক হিসেবে উপস্থিত।",
            "classical_notes": []
        },
        {
            "word": "فَوَفَّاهُ",
            "meaning_bn": "অতঃপর তিনি তাকে পূর্ণ প্রতিদান দিলেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী সহ মাফ'ঊল যমীর",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "تَفْعِيلٌ",
                "jins": "لفيف مفروق",
                "root": "(و . ف . ي)",
                "masdar": "اَلتَّوْفِيَةُ",
                "masdar_meaning": "পূর্ণ পাওনা মিটিয়ে দেওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলাল ফাতহ মুকাদ্দার; هُ যমীরটি মাফ'ঊলে বিহি।",
            "lexical_depth_bn": "আল্লাহ প্রতিটি কর্মের সূক্ষ্মাতিসূক্ষ্ম হিসাব পূর্ণরূপে চুকিয়ে দেবেন।",
            "classical_notes": []
        },
        {
            "word": "سَرِيعُ",
            "meaning_bn": "অতি দ্রুত হিসাব গ্রহণকারী",
            "word_type": "اسم",
            "prefix_suffix_note": "খবর হিসেবে মারফূ এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(س . ر . ع)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: سَرِيعٌ | বহুবচন: سِرَاعٌ"
            },
            "taleel_or_irab": "اللَّهُ মুবতাদার খবর হিসেবে মারফূ বিয যম্মাহ; الْحِسَابِ হলো মুযাফ ইলাইহি।",
            "lexical_depth_bn": "সমগ্র সৃষ্টির হিসাব এক নিমেষেই গ্রহণ করতে আল্লাহ সম্পূর্ণ সক্ষম।",
            "classical_notes": []
        }
    ],
    40: [
        {
            "word": "بَحْرٍ",
            "meaning_bn": "মহাসমুদ্রের অগাধ জলরাশি",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ب . ح . ر)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: بَحْرٌ | বহুবচন: بِحَارٌ / أَبْحُرٌ"
            },
            "taleel_or_irab": "فِي হরফে জারের কারণে মাজরূর বিল কাসরাহ; لُجِّيٍّ হলো এর সিফাত।",
            "lexical_depth_bn": "কাফিরের কুফর ও গোমরাহীর উপমা সমুদ্রের অতল অন্ধকারের সাথে।",
            "classical_notes": []
        },
        {
            "word": "أَخْرَجَ",
            "meaning_bn": "সে যখন বের করে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "إِفْعَالٌ",
                "jins": "صحيح",
                "root": "(خ . ر . ج)",
                "masdar": "اَلْإِخْرَاجُ",
                "masdar_meaning": "বের করা; মেলে ধরা",
                "singular_plural": null
            },
            "taleel_or_irab": "إِذَا যরফের পর ফে'লে মাযী মাবনী আলাল ফাতহ; يَدَهُ হলো এর মাফ'ঊলে বিহি।",
            "lexical_depth_bn": "গাঢ় অন্ধকারের তীব্রতা বোঝাতে হাতের রূপক ব্যবহার।",
            "classical_notes": []
        },
        {
            "word": "يَرَاهَا",
            "meaning_bn": "সে তা দেখতে পায় না",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মাযযূম সহ মাফ'ঊল",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف مجزوم بلم",
                "bab": "فَتَحَ",
                "jins": "مهموز العين ناقص يائي",
                "root": "(ر . أ . ي)",
                "masdar": "اَلرُّؤْيَةُ",
                "masdar_meaning": "দেখা; প্রত্যক্ষ করা",
                "singular_plural": null
            },
            "taleel_or_irab": "لَمْ হরফের কারণে মাযযূম বি হাযফি হারফিল ইল্লাহ (মূলত يَرَاهَا ছিল); هَا যমীরটি মাফ'ঊলে বিহি।",
            "lexical_depth_bn": "এত নিশ্ছিদ্র অন্ধকার যে নিজের হাত পর্যন্ত দেখতে অক্ষম।",
            "classical_notes": []
        },
        {
            "word": "يَجْعَلِ",
            "meaning_bn": "তিনি নির্ধারণ বা দান করেন না",
            "word_type": "فعل",
            "prefix_suffix_note": "লম (لَمْ) যোগে মাযযূম ফে'লে মুযারে",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف مجزوم بلم",
                "bab": "فَتَحَ",
                "jins": "صحيح",
                "root": "(ج . ع . ل)",
                "masdar": "اَلْجَعْلُ",
                "masdar_meaning": "নির্ধারণ করা; দেওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "لَمْ হরফের কারণে মাযযূম বিস সুকূন; মিলানোর সুবিধার্থে সুকূন কাসরাহ হয়েছে (يَجْعَلِ اللَّهُ)।",
            "lexical_depth_bn": "আল্লাহ যাকে হেদায়াতের নূর না দেন বিশ্বজগতের কেউ তাকে আলোর সন্ধান দিতে পারে না।",
            "classical_notes": []
        }
    ],
    41: [
        {
            "word": "يُسَبِّحُ",
            "meaning_bn": "মহিমা ও পবিত্রতা ঘোষণা করে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "تَفْعِيلٌ",
                "jins": "صحيح",
                "root": "(س . ب . ح)",
                "masdar": "اَلتَّسْبِيحُ",
                "masdar_meaning": "তাসবীহ পাঠ করা; পবিত্রতা ঘোষণা করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ; مَنْ হলো এর ফা'ইল।",
            "lexical_depth_bn": "নভোমণ্ডল ও ভূমণ্ডলের প্রতিটি সৃষ্টবস্তু স্ব স্ব ভাষায় মহান রবের প্রশংসাগীতি গায়।",
            "classical_notes": []
        },
        {
            "word": "الطَّيْرُ",
            "meaning_bn": "উড্ডয়নশীল বিহঙ্গকুল / পাখিরা",
            "word_type": "اسم",
            "prefix_suffix_note": "মা'তূফ হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف يائي",
                "root": "(ط . ي . ر)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: طَائِرٌ | বহুবচন: طَيْرٌ / طُيُورٌ"
            },
            "taleel_or_irab": "مَنْ শব্দের ওপর মা'তূফ হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "আকাশে ডানা মেলে ওড়া পাখিরাও মহান আল্লাহর অনুগত সৃষ্টি।",
            "classical_notes": []
        },
        {
            "word": "صَلَاتَهُ",
            "meaning_bn": "তার নিজ নিজ ইবাদতের রীতি",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "নাقص واوي",
                "root": "(ص . ل . و)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: صَلَاةٌ | বহুবচন: صَلَوَاتٌ"
            },
            "taleel_or_irab": "عَلِمَ ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ; هُ যমীরটি মুযাফ ইলাইহি।",
            "lexical_depth_bn": "প্রতিটি প্রাণীর নিজস্ব সহজাত প্রার্থনা ও বশ্যতা পদ্ধতি রয়েছে।",
            "classical_notes": [
                {
                    "scholar_or_book": "মুফরাদাতুল কুরআন (ইমাম রাগেব)",
                    "note": "الصلاة মূলত দোয়া, বশ্যতা ও ইবাদত; সৃষ্টিজগতের প্রতিটি উপাদান আল্লাহর বিধিবদ্ধ নিয়মে নিজ সালাত ও তাসবীহ অবগত।"
                }
            ]
        },
        {
            "word": "يَفْعَلُونَ",
            "meaning_bn": "তারা যা কিছু করে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "فَتَحَ",
                "jins": "صحيح",
                "root": "(ف . ع . ل)",
                "masdar": "اَلْفِعْلُ",
                "masdar_meaning": "সম্পাদন করা; করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বি সুবূতিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "সৃষ্টির প্রতিটি কর্ম ও গতিবিধির পূর্ণ বিবরণ আল্লাহর নখদর্পণে।",
            "classical_notes": []
        }
    ],
    42: [
        {
            "word": "مُلْكُ",
            "meaning_bn": "একচ্ছত্র সার্বভৌম রাজত্ব ও কর্তৃত্ব",
            "word_type": "اسم",
            "prefix_suffix_note": "মুবতাদা মুআখখার হিসেবে মারফূ এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(م . ل . ك)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: مُلْكٌ | বহুবচন: أَمْلَاكٌ"
            },
            "taleel_or_irab": "لِلَّهِ যার-মাজরূরের পর মুবতাদা মুআখখার হিসেবে মারফূ বিয যম্মাহ; السَّمَاوَاتِ হলো মুযাফ ইলাইহি।",
            "lexical_depth_bn": "বিশ্বজগতের দৃশ্য-অদৃশ্য সকল রাজত্বের নিরঙ্কুশ মালিকানা একমাত্র আল্লাহর।",
            "classical_notes": []
        },
        {
            "word": "السَّمَاوَاتِ",
            "meaning_bn": "নভোমণ্ডলসমূহের",
            "word_type": "اسم",
            "prefix_suffix_note": "মুযাফ ইলাইহি হিসেবে মাজরূর বিল কাসরাহ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "নাقص واوي",
                "root": "(س . م . و)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: سَمَاءٌ | বহুবচন: سَمَاوَاتٌ"
            },
            "taleel_or_irab": "مُلْكُ শব্দের মুযাফ ইলাইহি হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "উর্ধ্বজগতের সৃষ্টি।",
            "classical_notes": []
        },
        {
            "word": "وَالْأَرْضِ",
            "meaning_bn": "এবং ভূমণ্ডলের",
            "word_type": "اسم",
            "prefix_suffix_note": "মা'তূফ হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "مهموز الفاء",
                "root": "(أ . ر . ض)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: أَرْضٌ | বহুবচন: أَرَاضٍ"
            },
            "taleel_or_irab": "মা'তূফ হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "নিখিল বিশ্বের সার্বভৌমত্ব।",
            "classical_notes": []
        }
    ],
    43: [
        {
            "word": "يَجْعَلُهُ",
            "meaning_bn": "তিনি তাকে পরিণত করেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ সহ মাফ'ঊল",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "فَتَحَ",
                "jins": "صحيح",
                "root": "(ج . ع . ل)",
                "masdar": "اَلْجَعْلُ",
                "masdar_meaning": "পরিণত করা; বানানো",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ; هُ যমীরটি প্রথম মাফ'ঊলে বিহি; رُكَامًا দ্বিতীয় মাফ'ঊল।",
            "lexical_depth_bn": "মেঘমালাকে স্তূপীকৃত ঘন ঘন মেঘে রূপান্তর করার প্রাকৃতিক কৌশল।",
            "classical_notes": []
        },
        {
            "word": "يَخْرُجُ",
            "meaning_bn": "বের হয়ে প্রবাহিত হয়",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "نَصَرَ",
                "jins": "صحيح",
                "root": "(خ . ر . ج)",
                "masdar": "اَلْخُرُوجُ",
                "masdar_meaning": "বের হওয়া; নির্গত হওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ; الْوَدْقُ-এর অবস্থা প্রকাশক হাল হিসেবে রয়েছে।",
            "lexical_depth_bn": "মেঘের ছিদ্রপথ দিয়ে বৃষ্টির বিন্দুর ধারা বর্ষণ।",
            "classical_notes": []
        },
        {
            "word": "يُنَزِّلُ",
            "meaning_bn": "তিনি ক্রমাগত অবতীর্ণ করেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "تَفْعِيلٌ",
                "jins": "صحيح",
                "root": "(ن . ز . ل)",
                "masdar": "اَلتَّنْزِيلُ",
                "masdar_meaning": "ধারাবাহিকভাবে বর্ষণ করা বা নামানো",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ; ফা'ইল যমীর مستتر (تقديره هو)।",
            "lexical_depth_bn": "আকাশ থেকে বরফ ও শিলাবৃষ্টি বর্ষণ।",
            "classical_notes": []
        },
        {
            "word": "جِبَالٍ",
            "meaning_bn": "পাহাড়সম পুঞ্জীভূত মেঘ",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ج . ب . ل)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: جَبَلٌ | বহুবচন: جِبَالٌ"
            },
            "taleel_or_irab": "مِنْ হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "আধুনিক আবহাওয়াবিজ্ঞান সমর্থিত কিউমুলোনিম্বাস মেঘ যা আকাশে বিশাল বরফাবৃত পাহাড়ের মতো দেখায়।",
            "classical_notes": [
                {
                    "scholar_or_book": "মুফরাদাতুল কুরআন (ইমাম রাগেব)",
                    "note": "الجبل হলো বিশাল উচ্চতাসম্পন্ন পাহাড়; রূপকার্থে আকাশে মেঘের সুউচ্চ স্তূপকে جبال বলা হয়েছে।"
                }
            ]
        },
        {
            "word": "يُصِيبُ",
            "meaning_bn": "তিনি তা নিক্ষেপ করেন বা আঘাত হানেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফা হরফে আতফ সহ ফে'লে মুযারে",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "إِفْعَالٌ",
                "jins": "أجوف واوي",
                "root": "(ص . و . ب)",
                "masdar": "اَلْإِصَابَةُ",
                "masdar_meaning": "আঘাত করা; বর্ষণ করা; পতিত করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ; ফা'ইল যমীর مستتر (تقديره هو)।",
            "lexical_depth_bn": "শিলাবৃষ্টির মাধ্যমে ফসলাদির ক্ষয়ক্ষতি সাধন।",
            "classical_notes": []
        },
        {
            "word": "يَصْرِفُهُ",
            "meaning_bn": "তিনি তা ফিরিয়ে দেন বা রক্ষা করেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ সহ মাফ'ঊল",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "ضَرَبَ",
                "jins": "صحيح",
                "root": "(ص . ر . ف)",
                "masdar": "اَلصَّرْفُ",
                "masdar_meaning": "ফিরিয়ে নেওয়া; সরিয়ে দেওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ; هُ যমীরটি মাফ'ঊলে বিহি।",
            "lexical_depth_bn": "প্রাকৃতিক দুর্যোগ থেকেও যাকে ইচ্ছা বাঁচিয়ে নেওয়ার ঐশী নিয়ন্ত্রণ।",
            "classical_notes": []
        },
        {
            "word": "يَذْهَبُ",
            "meaning_bn": "ছিনিয়ে নিয়ে যায় বা ঝলসে দেয়",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "فَتَحَ",
                "jins": "صحيح",
                "root": "(ذ . ه . ب)",
                "masdar": "اَلذَّهَابُ",
                "masdar_meaning": "নিয়ে যাওয়া; বিলুপ্ত করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ; يَكَادُ-এর খবর হিসেবে মহলে নাসব-এ রয়েছে।",
            "lexical_depth_bn": "বিদ্যুতের তীব্র ঝলকানি যা চোখের দৃষ্টিশক্তি ছিনিয়ে নেওয়ার উপক্রম হয়।",
            "classical_notes": []
        },
        {
            "word": "بِالْأَبْصَارِ",
            "meaning_bn": "মানুষের দৃষ্টিশক্তিসমূহকে",
            "word_type": "اسم",
            "prefix_suffix_note": "বা হরফে জার সহ মাজরূর",
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
            "taleel_or_irab": "بِ হরফে জারের মাধ্যমে يَذْهَبُ ক্রিয়ার تعدية হয়েছে; মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "আল্লাহর প্রাকৃতিক নিদর্শনাবলীর প্রচণ্ড ক্ষমতা ও মহিমা।",
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
        
    with open("web/public/data/24/ruku-5.json", "r", encoding="utf-8") as f:
        ruku5 = json.load(f)
        
    total_added = 0
    total_words = 0
    for a in ruku5.get("ayahs", []):
        v = a.get("ayah")
        ayah_w = full_words.get(f"24:{v}", [])
        existing = a.get("tahqeeq", [])
        new_w = NEW_WORDS_RUKU5.get(v, [])
        merged = merge_and_sort(existing, new_w, ayah_w)
        added = len(merged) - len(existing)
        total_added += added
        total_words += len(merged)
        a["tahqeeq"] = merged
        print(f"Ayah {v:02d}: {len(existing)} -> {len(merged)} words (+{added})")
        
    with open("web/public/data/24/ruku-5.json", "w", encoding="utf-8") as f:
        json.dump(ruku5, f, ensure_ascii=False, indent=2)
        
    print(f"\n[SUCCESS] Ruku 5 expanded: +{total_added} words, total {total_words} words across Ayahs 35-43.")

if __name__ == "__main__":
    main()

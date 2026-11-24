#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expand Tahqeeq for Surah 24 Rukus 7, 8, and 9 (Ayahs 53-64) to Maximum Words.
Covers all substantive words with full morphological precision.
"""

import json

null = None

NEW_WORDS_RUKU7 = {
    53: [
        {
            "word": "أَمَرْتَهُمْ",
            "meaning_bn": "আপনি যদি তাদের নির্দেশ দেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী সহ মাফ'ঊল যমীর",
            "morphology": {
                "sighah": "واحد مذكر حاضر",
                "bahas": "ماضي معروف",
                "bab": "نَصَرَ",
                "jins": "مهموز الفاء",
                "root": "(أ . م . ر)",
                "masdar": "اَلْأَمْرُ",
                "masdar_meaning": "আদেশ করা; নির্দেশ দেওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "لَئِنْ শるので ফে'লে মাযী মাবনী আলাস সুকূন; تَ হলো ফা'ইল; هُمْ মাফ'ঊলে বিহি।",
            "lexical_depth_bn": "মুনাফিকরা রসূলকে সন্তুষ্ট করতে ভণ্ডামিপূর্ণ শর্ত জুড়ে দিত।",
            "classical_notes": []
        },
        {
            "word": "تُقْسِمُوا",
            "meaning_bn": "তোমরা শপথ করো না",
            "word_type": "فعل",
            "prefix_suffix_note": "নাহীসূচক لَا যোগে মাযযূম ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "مضارع معروف مجزوم بلا الناهية",
                "bab": "إِفْعَالٌ",
                "jins": "صحيح",
                "root": "(ق . س . م)",
                "masdar": "اَلْإِقْسَامُ",
                "masdar_meaning": "কসম খাওয়া; শপথ করা",
                "singular_plural": null
            },
            "taleel_or_irab": "لَا النَّاهِيَة এর কারণে মাযযূম বি হাযফিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "মিথ্যা কসমের প্রদর্শন বন্ধ করার নির্দেশ।",
            "classical_notes": []
        },
        {
            "word": "خَبِيرٌ",
            "meaning_bn": "সম্যক অবগত ও পরিজ্ঞাত",
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
            "lexical_depth_bn": "আল্লাহ অন্তরের উদ্দেশ্য ও বাহ্যিক আমল সবই জানেন।",
            "classical_notes": []
        },
        {
            "word": "تَعْمَلُونَ",
            "meaning_bn": "তোমরা যা কিছু আমল বা কর্ম করো",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "مضارع معروف",
                "bab": "سَمِعَ",
                "jins": "صحيح",
                "root": "(ع . م . ل)",
                "masdar": "اَلْعَمَلُ",
                "masdar_meaning": "কাজ করা; আমল করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বি সুবূতিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "মানুষের কর্মের উপযুক্ত প্রতিফল প্রস্তুত রাখা হয়েছে।",
            "classical_notes": []
        }
    ],
    54: [
        {
            "word": "الرَّسُولَ",
            "meaning_bn": "আল্লাহর মহান রাসূলের",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ر . س . ل)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: رَسُولٌ | বহুবচন: رُسُلٌ"
            },
            "taleel_or_irab": "أَطِيعُوا ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "আল্লাহর আনুগত্য ও রাসূলের আনুগত্য পরস্পর অবিচ্ছেদ্য।",
            "classical_notes": []
        },
        {
            "word": "حُمِّلْتُمْ",
            "meaning_bn": "তোমাদের ওপর যে আনুগত্যের বোঝা অর্পণ করা হয়েছে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মাঝহূল",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "ماضي مجهول",
                "bab": "تَفْعِيلٌ",
                "jins": "صحيح",
                "root": "(ح . م . ل)",
                "masdar": "اَلتَّحْمِيلُ",
                "masdar_meaning": "বোঝা বা দায়িত্ব চাপানো",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাঝহূল মাবনী আলাস সুকূন; تُمْ হলো নায়েবে ফা'ইল।",
            "lexical_depth_bn": "উম্মতের ওপর শরীয়তের হুকুম মেনে চলার ব্যক্তিগত দায়ভার।",
            "classical_notes": []
        },
        {
            "word": "تُطِيعُوهُ",
            "meaning_bn": "তোমরা যদি তাঁর পূর্ণ আনুগত্য করো",
            "word_type": "فعل",
            "prefix_suffix_note": "শার্তে মাযযূম ফে'লে মুযারে সহ মাফ'ঊল",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "مضارع معروف",
                "bab": "إِفْعَالٌ",
                "jins": "أجوف واوي",
                "root": "(ط . و . ع)",
                "masdar": "اَلْإِطَاعَةُ",
                "masdar_meaning": "আনুগত্য করা; হুকুম মানা",
                "singular_plural": null
            },
            "taleel_or_irab": "إِنْ শারতিয়্যাহ দ্বারা মাযযূম বি হাযফিন নূন; ওয়াও ফা'ইল; هُ মাফ'ঊলে বিহি।",
            "lexical_depth_bn": "রাসূলের সুন্নাহর নিঃশর্ত অনুসরণের মাধ্যমেই হেদায়াত লাভ সম্ভব।",
            "classical_notes": []
        },
        {
            "word": "الْمُبِينُ",
            "meaning_bn": "স্পষ্ট ও বিশদ প্রকাশকারী",
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
            "taleel_or_irab": "الْبَلَاغُ শব্দের সিফাত হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "রিসালাতের বার্তা সম্পূর্ণ উন্মোচনকারী।",
            "classical_notes": []
        }
    ],
    55: [
        {
            "word": "آمَنُوا",
            "meaning_bn": "তোমাদের মধ্যে যারা খাঁটি ঈমান এনেছে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "إِفْعَالٌ",
                "jins": "مهموز الفاء",
                "root": "(أ . م . ن)",
                "masdar": "اَلْإِيمَانُ",
                "masdar_meaning": "ঈমান আনা; আন্তরিক বিশ্বাস স্থাপন করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলায যম্ম; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "খেলাফত ও রাজনৈতিক বিজয়ের প্রথম ও প্রধান পূর্বশর্ত ঈমান।",
            "classical_notes": []
        },
        {
            "word": "وَعَمِلُوا",
            "meaning_bn": "এবং যারা নিষ্ঠার সাথে আমল করেছে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "سَمِعَ",
                "jins": "صحيح",
                "root": "(ع . م . ل)",
                "masdar": "اَلْعَمَلُ",
                "masdar_meaning": "কাজ করা; আমল করা",
                "singular_plural": null
            },
            "taleel_or_irab": "মা'তূফ হিসেবে মাবনী আলায যম্ম; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "ঈমানের বাস্তব প্রতিফলন নেক আমল।",
            "classical_notes": []
        },
        {
            "word": "الصَّالِحَاتِ",
            "meaning_bn": "যাবতীয় সৎ ও গঠনমূলক কর্মসমূহ",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব বিল কাসরাহ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ص . ل . ح)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: صَالِحَةٌ | বহুবচন: صَالِحَاتٌ"
            },
            "taleel_or_irab": "عَمِلُوا ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল কাসরাহ (جمع مؤنث سالم)।",
            "lexical_depth_bn": "আল্লাহর সন্তুষ্টিমূলক কল্যাণকর কাজ।",
            "classical_notes": []
        },
        {
            "word": "الْأَرْضِ",
            "meaning_bn": "এই ভূমণ্ডলে / পৃথিবীতে",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ",
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
            "taleel_or_irab": "فِي হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "জমিনের বুকে ইসলামী শাসন ও ন্যায়বিচার প্রতিষ্ঠা।",
            "classical_notes": []
        },
        {
            "word": "اسْتَخْلَفَ",
            "meaning_bn": "তিনি যেমন পূর্ববর্তীদের খিলাফত ও কর্তৃত্ব দিয়েছিলেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "اِسْتِفْعَالٌ",
                "jins": "صحيح",
                "root": "(خ . ل . ف)",
                "masdar": "اَلْاِسْتِخْلَافُ",
                "masdar_meaning": "স্থলাভিষিক্ত করা; প্রতিনিধিত্ব দেওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলাল ফাতহ; ফা'ইল যমীর مستتر।",
            "lexical_depth_bn": "দাউদ ও সুলাইমান (আ.) এবং বনী ইসরাঈলের নেককারদের শাসনক্ষমতা দান।",
            "classical_notes": []
        },
        {
            "word": "دِينَهُمُ",
            "meaning_bn": "তাদের মনোনীত পূর্ণাঙ্গ জীবনব্যবস্থাকে",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব এবং মুযাফ",
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
            "taleel_or_irab": "لَيُمَكِّنَنَّ ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ; هُمُ মুযাফ ইলাইহি।",
            "lexical_depth_bn": "ইসলামকে অন্যান্য মতবাদের ওপর বিজয়ী ও সুপ্রতিষ্ঠিত করা।",
            "classical_notes": []
        },
        {
            "word": "خَوْفِهِمْ",
            "meaning_bn": "তাদের চরম ভীতিকর ও অনিরাপদ অবস্থার পর",
            "word_type": "اسم",
            "prefix_suffix_note": "মুযাফ ইলাইহি হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف واوي",
                "root": "(خ . و . ف)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: خَوْفٌ | বহুবচন: مَخَاوِفُ"
            },
            "taleel_or_irab": "بَعْدِ শব্দের মুযাফ ইলাইহি হিসেবে মাজরূর বিল কাসরাহ; هِمْ মুযাফ ইলাইহি।",
            "lexical_depth_bn": "মক্কার সূচনালগ্নে সাহাবীদের যে সার্বক্ষণিক শত্রুভীতি ছিল তা দূর করার সুসংবাদ।",
            "classical_notes": []
        },
        {
            "word": "يَعْبُدُونَنِي",
            "meaning_bn": "তারা একান্তভাবে কেবল আমারই ইবাদত করবে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ সহ মাফ'ঊল",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "نَصَرَ",
                "jins": "صحيح",
                "root": "(ع . ب . د)",
                "masdar": "اَلْعِبَادَةُ",
                "masdar_meaning": "ইবাদত করা; বন্দেগি করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বি সুবূতিন নূন; ওয়াও ফা'ইল; نِي হলো নূনে বেকায়া ও ইয়া মাফ'ঊলে বিহি। হাল হিসেবে ব্যবহৃত।",
            "lexical_depth_bn": "খেলাফত ও নিরাপত্তার মূল লক্ষ্যই হলো খাঁটি তাওহীদের ভিত্তিতে আল্লাহর উপাসনা কায়েম করা।",
            "classical_notes": []
        },
        {
            "word": "يُشْرِكُونَ",
            "meaning_bn": "তারা কোনো কিছুকে শরিক করবে না",
            "word_type": "فعل",
            "prefix_suffix_note": "নাফীসূচক لَا যোগে ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "إِفْعَالٌ",
                "jins": "صحيح",
                "root": "(ش . ر . ك)",
                "masdar": "اَلْإِشْرَاكُ",
                "masdar_meaning": "অংশীদার স্থাপন করা; শিরক করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বি সুবূতিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "শিরকমুক্ত নিষ্কলুষ ঈমানের অপরিহার্য শর্ত।",
            "classical_notes": []
        },
        {
            "word": "كَفَرَ",
            "meaning_bn": "যে ব্যক্তি অকৃতজ্ঞতা বা কুফরি করবে",
            "word_type": "فعل",
            "prefix_suffix_note": "শার্তে ফে'লে মাযী",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "نَصَرَ",
                "jins": "صحيح",
                "root": "(ك . ف . ر)",
                "masdar": "اَلْكُفْرُ",
                "masdar_meaning": "অস্বীকার করা; কুফরি করা; অকৃতজ্ঞ হওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "مَنْ শারতিয়্যাহর পর ফে'লে মাযী মাবনী আলাল ফাতহ।",
            "lexical_depth_bn": "খেলাফতের নেয়ামত লাভের পর তার মর্যাদা না রেখে বিদ্রোহ করা।",
            "classical_notes": []
        },
        {
            "word": "الْفَاسِقُونَ",
            "meaning_bn": "তারাই প্রকৃতপক্ষে চূড়ান্ত সত্যত্যাগী ও পাপাচারী",
            "word_type": "اسم",
            "prefix_suffix_note": "খবর হিসেবে মারফূ বিল ওয়াও",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ف . س . ق)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: فَاسِقٌ | বহুবচন: فَاسِقُونَ"
            },
            "taleel_or_irab": "أُولَئِكَ মুবতাদার খবর হিসেবে মারফূ বিল ওয়াও (جمع مذكر سالم)।",
            "lexical_depth_bn": "আল্লাহর আনুগত্যের গণ্ডি থেকে বের হয়ে যাওয়া চরম অবাধ্য দল।",
            "classical_notes": []
        }
    ],
    56: [
        {
            "word": "الصَّلَاةَ",
            "meaning_bn": "নিয়মিত নামাজ",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব",
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
            "taleel_or_irab": "أَقِيمُوا ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "শরীয়তের শ্রেষ্ঠতম ইবাদত যা আত্মাকে নিষ্কলুষ রাখে।",
            "classical_notes": []
        },
        {
            "word": "الزَّكَاةَ",
            "meaning_bn": "ফরযকৃত যাকাত",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "নাقص واوي",
                "root": "(ز . ك . و)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: زَكَاةٌ | বহুবচন: زَكَوَاتٌ"
            },
            "taleel_or_irab": "آتُوا ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "অর্থনৈতিক ভারসাম্য ও সমাজের বঞ্চিতদের অধিকার আদায়ের স্তম্ভ।",
            "classical_notes": []
        },
        {
            "word": "الرَّسُولَ",
            "meaning_bn": "আল্লাহর প্রেরিত রাসূলের",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ر . س . ل)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: رَسُولٌ | বহুবচন: رُسُلٌ"
            },
            "taleel_or_irab": "أَطِيعُوا ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "রহমত পাওয়ার অপরিহার্য চাবিকাঠি রাসূলের সুন্নাহর আনুগত্য।",
            "classical_notes": []
        }
    ],
    57: [
        {
            "word": "تَحْسَبَنَّ",
            "meaning_bn": "আপনি কখনোই মনে করবেন না",
            "word_type": "فعل",
            "prefix_suffix_note": "নূনে সাকীলাহ সহ ফে'লে মুযারে",
            "morphology": {
                "sighah": "واحد مذكر حاضر",
                "bahas": "مضارع معروف مؤكد بنون التوكيد الثقيلة",
                "bab": "حَسِبَ",
                "jins": "صحيح",
                "root": "(ح . س . ب)",
                "masdar": "اَلْحُسْبَانُ",
                "masdar_meaning": "ধারণা করা; মনে করা",
                "singular_plural": null
            },
            "taleel_or_irab": "لَا النَّاهِيَة-এর পর নূনে তা'কীদের কারণে مَبْنِيٌّ عَلَى الْفَتْحِ فِي مَحَلِّ جَزْمٍ।",
            "lexical_depth_bn": "কাফিররা যে কোনোভাবেই আল্লাহর পাকড়াও থেকে বাঁচতে পারবে না তার দৃঢ় ঘোষণা।",
            "classical_notes": []
        },
        {
            "word": "كَفَرُوا",
            "meaning_bn": "যারা সত্যকে অস্বীকার ও কুফরি করেছে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "نَصَرَ",
                "jins": "صحيح",
                "root": "(ك . ف . ر)",
                "masdar": "اَلْكُفْرُ",
                "masdar_meaning": "কুফরি করা; প্রত্যাখ্যান করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলায যম্ম; ওয়াও হলো ফা'ইল। الَّذِينَ-এর সিলাহ।",
            "lexical_depth_bn": "ইসলামের বিরুদ্ধে চক্রান্তকারী শত্রুসমাজ।",
            "classical_notes": []
        },
        {
            "word": "النَّارُ",
            "meaning_bn": "জাহান্নামের লেলিহান অগ্নি",
            "word_type": "اسم",
            "prefix_suffix_note": "খবর হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف واوي",
                "root": "(ن . و . ر)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: نَارٌ | বহুবচন: نِيرَانٌ"
            },
            "taleel_or_irab": "مَأْوَاهُمُ মুবতাদার খবর হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "কাফিরদের অবধারিত শেষ ঠিকানা।",
            "classical_notes": []
        }
    ],
    58: [
        {
            "word": "آمَنُوا",
            "meaning_bn": "হে ঈমানদারগণ",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "إِفْعَالٌ",
                "jins": "مهموز الفاء",
                "root": "(أ . م . ن)",
                "masdar": "اَلْإِيمَانُ",
                "masdar_meaning": "ঈমান আনা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলায যম্ম; الَّذِينَ-এর সিলাহ।",
            "lexical_depth_bn": "পারিবারিক শিষ্টাচারের বিধানাবলীর সূচনা।",
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
                "masdar_meaning": "মালিকানা থাকা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলাল ফাতহ; أَيْمَانُكُمْ হলো ফা'ইল।",
            "lexical_depth_bn": "অধীনস্থ ভৃত্য ও খাদেমদের ক্ষেত্রে প্রযোজ্য নিয়ম।",
            "classical_notes": []
        },
        {
            "word": "أَيْمَانُكُمْ",
            "meaning_bn": "তোমাদের অধীনস্থ দাস-দাসী ও ভৃত্যগণ",
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
            "taleel_or_irab": "مَلَكَتْ ক্রিয়ার ফা'ইল হিসেবে মারফূ বিয যম্মাহ; كُمْ মুযাফ ইলাইহি।",
            "lexical_depth_bn": "পারিবারিক সেবায় নিয়োজিত ব্যক্তিরা।",
            "classical_notes": []
        },
        {
            "word": "مَرَّاتٍ",
            "meaning_bn": "দিনে তিনবার",
            "word_type": "اسم",
            "prefix_suffix_note": "মুযাফ ইলাইহি হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "مضاعف ثلاثي",
                "root": "(م . ر . ر)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: مَرَّةٌ | বহুবচন: مَرَّاتٌ"
            },
            "taleel_or_irab": "ثَلَاثَ সংখ্যার মুযাফ ইলাইহি হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "তিনটি বিশেষ সময়ে কক্ষে প্রবেশের পূর্বে অনুমতি চাওয়ার আবশ্যকতা।",
            "classical_notes": []
        },
        {
            "word": "الْفَجْرِ",
            "meaning_bn": "ভোরের ফজরের সালাত",
            "word_type": "اسم",
            "prefix_suffix_note": "মুযাফ ইলাইহি হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ف . ج . ر)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: فَجْرٌ | বহুবচন: فُجُورٌ"
            },
            "taleel_or_irab": "صَلَاةِ শব্দের মুযাফ ইলাইহি হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "প্রথম গোপনীয় সময়—ঘুম থেকে ওঠার পূর্বমুহূর্ত।",
            "classical_notes": []
        },
        {
            "word": "تَضَعُونَ",
            "meaning_bn": "তোমরা খুলে রেখে দাও",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "مضارع معروف",
                "bab": "فَتَحَ",
                "jins": "مثال واوي",
                "root": "(و . ض . ع)",
                "masdar": "اَلْوَضْعُ",
                "masdar_meaning": "খোলা; রেখে দেওয়া; নামিয়ে রাখা",
                "singular_plural": null
            },
            "taleel_or_irab": "حِينَ যরফের পর ফে'লে মুযারে মারফূ বি সুবূতিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "দুপুরের বিশ্রামের সময় অতিরিক্ত পোশাক খুলে হালকা হওয়া।",
            "classical_notes": []
        },
        {
            "word": "ثِيَابَكُمْ",
            "meaning_bn": "তোমাদের পরিধেয় পোশাক-আশাক",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف واوي",
                "root": "(ث . و . ب)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: ثَوْبٌ | বহুবচন: ثِيَابٌ"
            },
            "taleel_or_irab": "تَضَعُونَ ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ; كُمْ মুযাফ ইলাইহি।",
            "lexical_depth_bn": "পোশাক পরিবর্তনের মুহূর্তে সতর্কতা।",
            "classical_notes": []
        },
        {
            "word": "الظَّهِيرَةِ",
            "meaning_bn": "দুপুরের দ্বিপ্রহরের সময়",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ظ . ه . ر)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: ظَهِيرَةٌ | বহুবচন: ظَهَائِرُ"
            },
            "taleel_or_irab": "مِنْ হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "দ্বিতীয় গোপনীয় সময়—তপ্ত দ্বিপ্রহরে কায়লুলা বা দুপুরের বিশ্রামের কাল।",
            "classical_notes": []
        },
        {
            "word": "الْعِشَاءِ",
            "meaning_bn": "রাতের এশার সালাতের পর",
            "word_type": "اسم",
            "prefix_suffix_note": "মুযাফ ইলাইহি হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "নাقص واوي",
                "root": "(ع . ش . و)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: عِشَاءٌ | বহুবচন: أَعْشِيَةٌ"
            },
            "taleel_or_irab": "صَلَاةِ শব্দের মুযাফ ইলাইহি হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "তৃতীয় গোপনীয় সময়—রাতের ঘুমের প্রস্তুতি ও শয়নকাল।",
            "classical_notes": []
        },
        {
            "word": "جُنَاحٌ",
            "meaning_bn": "কোনো প্রকার দোষ বা অপরাধ",
            "word_type": "اسم",
            "prefix_suffix_note": "লাইসা-এর ইসম হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ج . ن . ح)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: جُنَاحٌ | বহুবচন: أَجْنِحَةٌ"
            },
            "taleel_or_irab": "لَيْسَ ক্রিয়ার মুআখখার ইসম হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "উক্ত তিন সময় ব্যতীত অন্য সময়ে ঘরে বিনা অনুমতিতে স্বাভাবিক চলাচলে কোনো পাপ নেই।",
            "classical_notes": []
        },
        {
            "word": "يُبَيِّنُ",
            "meaning_bn": "তিনি স্পষ্টরূপে বুঝিয়ে দেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "تَفْعِيلٌ",
                "jins": "أجوف يائي",
                "root": "(ب . ي . ن)",
                "masdar": "اَلتَّبْيِينُ",
                "masdar_meaning": "সুস্পষ্ট করা; বর্ণনা করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ; اللَّهُ হলো ফা'ইল।",
            "lexical_depth_bn": "মানবজীবনের প্রতি ক্ষেত্রের নিখুঁত আচরণবিধি বয়ান।",
            "classical_notes": []
        },
        {
            "word": "الْآيَاتِ",
            "meaning_bn": "সুস্পষ্ট বিধান ও শিক্ষাসমূহ",
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
            "taleel_or_irab": "يُبَيِّنُ ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল কাসরাহ (جمع مؤنث سالم)।",
            "lexical_depth_bn": "পারিবারিক শিষ্টাচারের অলঙ্ঘনীয় ঐশী বিধান।",
            "classical_notes": []
        },
        {
            "word": "عَلِيمٌ",
            "meaning_bn": "বান্দার সার্বিক প্রয়োজন ও দুর্বলতা সম্পর্কে পূর্ণ জ্ঞানী",
            "word_type": "اسم",
            "prefix_suffix_note": "প্রথম খবর হিসেবে মারফূ",
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
            "taleel_or_irab": "اللَّهُ মুবতাদার প্রথম খবর হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "মানুষের জীবনের সকল সূক্ষ্ম চাহিদার জ্ঞান।",
            "classical_notes": []
        },
        {
            "word": "حَكِيمٌ",
            "meaning_bn": "বিধানে পরম প্রজ্ঞাময়",
            "word_type": "اسم",
            "prefix_suffix_note": "দ্বিতীয় খবর হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ح . ك . م)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: حَكِيمٌ | বহুবচন: حُكَمَاءُ"
            },
            "taleel_or_irab": "দ্বিতীয় খবর হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "প্রতিটি নির্দেশের পেছনে অন্তর্নিহিত অপার সামাজিক প্রজ্ঞা।",
            "classical_notes": []
        }
    ]
}

NEW_WORDS_RUKU8 = {
    59: [
        {
            "word": "بَلَغَ",
            "meaning_bn": "যখন উপনীত হয় বা পৌঁছায়",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "نَصَرَ",
                "jins": "صحيح",
                "root": "(ب . ل . غ)",
                "masdar": "اَلْبُلُوغُ",
                "masdar_meaning": "উপনীত হওয়া; পৌঁছানো",
                "singular_plural": null
            },
            "taleel_or_irab": "إِذَا যরফের পর ফে'লে মাযী মাবনী আলাল ফাতহ; الْأَطْفَالُ হলো এর ফা'ইল।",
            "lexical_depth_bn": "বয়ঃসন্ধির সীমারেখায় পদার্পণ করা।",
            "classical_notes": []
        },
        {
            "word": "الْحُلُمَ",
            "meaning_bn": "সাবালকত্ব ও বয়ঃসন্ধিকালের যৌন পরিপক্বতা",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ح . ل . م)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: حُلُمٌ | বহুবচন: أَحْلَامٌ"
            },
            "taleel_or_irab": "بَلَغَ ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "শরীয়তের দৃষ্টিতে শারীরিক সাবালকত্ব লাভ।",
            "classical_notes": []
        },
        {
            "word": "اسْتَأْذَنَ",
            "meaning_bn": "অনুমতি প্রার্থনা করেছিল",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "اِسْتِفْعَالٌ",
                "jins": "مهموز الفاء",
                "root": "(أ . ذ . ن)",
                "masdar": "اَلْاِسْتِئْذَانُ",
                "masdar_meaning": "অনুমতি চাওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলাল ফাতহ; الَّذِينَ হলো ফা'ইল।",
            "lexical_depth_bn": "বড়দের মতো নিয়মিত অনুমতি নিয়ে প্রবেশের শিষ্টাচার।",
            "classical_notes": []
        },
        {
            "word": "يُبَيِّنُ",
            "meaning_bn": "তিনি স্পষ্টরূপে বুঝিয়ে দেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "تَفْعِيلٌ",
                "jins": "أجوف يائي",
                "root": "(ب . ي . ن)",
                "masdar": "اَلتَّبْيِينُ",
                "masdar_meaning": "স্পষ্ট করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ; اللَّهُ হলো ফা'ইল।",
            "lexical_depth_bn": "পারিবারিক নীতিমালার বিশদ ব্যাখ্যা।",
            "classical_notes": []
        },
        {
            "word": "آيَاتِهِ",
            "meaning_bn": "তাঁর স্পষ্ট নিদর্শন ও আদেশাবলি",
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
            "taleel_or_irab": "يُبَيِّنُ ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল কাসরাহ (جمع مؤنث سالم); هِ মুযাফ ইলাইহি।",
            "lexical_depth_bn": "আল্লাহর প্রতিটি নির্দেশ মানুষের পবিত্রতার সহায়ক।",
            "classical_notes": []
        }
    ],
    60: [
        {
            "word": "النِّسَاءِ",
            "meaning_bn": "বৃদ্ধা নারীদের মধ্য থেকে",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ",
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
            "taleel_or_irab": "مِنْ হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "বার্ধক্যে উপনীত নারীদের জন্য পর্দার সাধারণ বিধানে ছাড়।",
            "classical_notes": []
        },
        {
            "word": "نِكَاحًا",
            "meaning_bn": "বিবাহের কোনো আগ্রহ বা আশা",
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
            "taleel_or_irab": "يَرْجُونَ ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "বার্ধক্যের কারণে যাদের প্রতি পুরুষের কামোদ্দীপক দৃষ্টি আকর্ষণ হয় না।",
            "classical_notes": []
        },
        {
            "word": "جُنَاحٌ",
            "meaning_bn": "কোনো প্রকার পাপ বা ত্রুটি",
            "word_type": "اسم",
            "prefix_suffix_note": "লাইসা-এর ইসম হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ج . ن . ح)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: جُنَاحٌ | বহুবচন: أَجْنِحَةٌ"
            },
            "taleel_or_irab": "لَيْسَ ক্রিয়ার মুআখখার ইসম হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "বাহিরের অতিরিক্ত চাদর খুলে রাখা বৃদ্ধাদের জন্য অনুমোদিত।",
            "classical_notes": []
        },
        {
            "word": "يَضَعْنَ",
            "meaning_bn": "তারা যেন খুলে রাখে / সরিয়ে রাখে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مؤنث غائب",
                "bahas": "مضارع معروف",
                "bab": "فَتَحَ",
                "jins": "مثال واوي",
                "root": "(و . ض . ع)",
                "masdar": "اَلْوَضْعُ",
                "masdar_meaning": "খুলে রাখা; শিথিল করা",
                "singular_plural": null
            },
            "taleel_or_irab": "أَنْ মাসদারিয়্যাহর পর নূনে নিসওয়ার কারণে মাবনী আলাস সুকূন ফী মাহাল্লি নাসব।",
            "lexical_depth_bn": "মাথার ওপরের চাদর বা ওড়না কিছুটা শিথিল করার অনুমতি।",
            "classical_notes": []
        },
        {
            "word": "ثِيَابَهُنَّ",
            "meaning_bn": "তাদের বাহ্যিক অতিরিক্ত পোশাক",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف واوي",
                "root": "(ث . و . ب)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: ثَوْبٌ | বহুবচন: ثِيَابٌ"
            },
            "taleel_or_irab": "يَضَعْنَ ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ; هُنَّ মুযাফ ইলাইহি।",
            "lexical_depth_bn": "ইবনে আব্বাস ও ইবনে মাসউদ (রা.)-এর মতে: জিলবাব বা বড় চাদর, সতর অনাবৃত করা নয়।",
            "classical_notes": []
        },
        {
            "word": "زِينَةٍ",
            "meaning_bn": "রূপ ও সাজসজ্জা দিয়ে",
            "word_type": "اسم",
            "prefix_suffix_note": "বা হরফে জার সহ মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "مثال واوي",
                "root": "(ز . ي . ن)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: زِينَةٌ | বহুবচন: زِينَاتٌ"
            },
            "taleel_or_irab": "بِ হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "অলংকার বা আকর্ষণীয় সাজসজ্জা প্রদর্শন থেকে বিরত থাকার শর্ত।",
            "classical_notes": []
        },
        {
            "word": "خَيْرٌ",
            "meaning_bn": "অধিকতর উত্তম ও কল্যাণকর",
            "word_type": "اسم",
            "prefix_suffix_note": "খবর হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف يائي",
                "root": "(خ . ي . ر)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: خَيْرٌ | বহুবচন: خِيَارٌ"
            },
            "taleel_or_irab": "وَأَنْ يَسْتَعْفِفْنَ মাসদারে মুআউওয়াল মুবতাদার খবর হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "বৃদ্ধাবস্থায়ও পূর্ণ পর্দা বজায় রাখা অধিকতর মর্যাদার প্রতীক।",
            "classical_notes": []
        },
        {
            "word": "سَمِيعٌ",
            "meaning_bn": "বান্দার সর্বাবস্থা শ্রবণকারী",
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
            "taleel_or_irab": "اللَّهُ মুবতাদার প্রথম খবর হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "সকল কথা ও প্রার্থনার সর্বদ্রষ্টা।",
            "classical_notes": []
        },
        {
            "word": "عَلِيمٌ",
            "meaning_bn": "অন্তরের গূঢ় নিয়ত সম্পর্কে পরিজ্ঞাত",
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
            "lexical_depth_bn": "পর্দা পালনের পেছনের আন্তরিকতার সাক্ষী।",
            "classical_notes": []
        }
    ],
    61: [
        {
            "word": "أَنْفُسِكُمْ",
            "meaning_bn": "তোমাদের নিজেদের আত্মীয়দের ওপর",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ এবং মুযাফ",
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
            "taleel_or_irab": "عَلَى হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ; كُمْ মুযাফ ইলাইহি।",
            "lexical_depth_bn": "পারিবারিক পারস্পরিক খাবার গ্রহণের ক্ষেত্রে কোনো সংকীর্ণতা না থাকা।",
            "classical_notes": []
        },
        {
            "word": "تَأْكُلُوا",
            "meaning_bn": "তোমরা আহার গ্রহণ করো বা খাও",
            "word_type": "فعل",
            "prefix_suffix_note": "আন (أَنْ) দ্বারা মানসূব ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "مضارع معروف",
                "bab": "نَصَرَ",
                "jins": "مهموز الفاء",
                "root": "(أ . ك . ل)",
                "masdar": "اَلْأَكْلُ",
                "masdar_meaning": "খাওয়া; আহার গ্রহণ করা",
                "singular_plural": null
            },
            "taleel_or_irab": "أَنْ মাসদারিয়্যাহ দ্বারা মানসূব বি হাযফিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "আত্মীয়-স্বজনের ঘরে আতিথেয়তা গ্রহণ ও হৃদ্যতাপূর্ণ মেলবন্ধন।",
            "classical_notes": []
        },
        {
            "word": "بُيُوتِكُمْ",
            "meaning_bn": "তোমাদের নিজ নিজ গৃহ থেকে",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ এবং মুযাফ",
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
            "taleel_or_irab": "مِنْ হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ; كُمْ মুযাফ ইলাইহি।",
            "lexical_depth_bn": "সন্তান ও স্বামী-স্ত্রীর নিজস্ব বাড়ি।",
            "classical_notes": []
        },
        {
            "word": "صَدِيقِكُمْ",
            "meaning_bn": "তোমাদের অন্তরঙ্গ ও বিশ্বস্ত বন্ধুদের ঘর থেকে",
            "word_type": "اسم",
            "prefix_suffix_note": "মুযাফ ইলাইহি হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ص . د . ق)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: صَدِيقٌ | বহুবচন: أَصْدِقَاءُ"
            },
            "taleel_or_irab": "মা'তূফ হিসেবে মাজরূর বিল কাসরাহ; كُمْ মুযাফ ইলাইহি।",
            "lexical_depth_bn": "যে বন্ধুত্বের মাঝে কোনো সংকোচ বা কুণ্ঠা থাকে না।",
            "classical_notes": [
                {
                    "scholar_or_book": "মুফরাদাতুল কুরআন (ইমাম রাগেব)",
                    "note": "الصديق হলো যে অন্তরের সততা ও একনিষ্ঠতায় ভালোবাসে; এমন অকৃত্রিম বন্ধুর ঘরে স্বাভাবিকভাবে খাওয়ার অনুমতি ইসলাম দিয়েছে।"
                }
            ]
        },
        {
            "word": "جَمِيعًا",
            "meaning_bn": "সকলে একসাথে সমবেত হয়ে",
            "word_type": "اسم",
            "prefix_suffix_note": "হাল হিসেবে মানসূব",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ج . م . ع)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: جَمِيعٌ | বহুবচন: أَجْمَعُونَ"
            },
            "taleel_or_irab": "تَأْكُلُوا ক্রিয়ার হাল (حال) হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "একসাথে বসে খাওয়া বরকতময়।",
            "classical_notes": []
        },
        {
            "word": "دَخَلْتُمْ",
            "meaning_bn": "তোমরা যখন কোনো গৃহে প্রবেশ করো",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "ماضي معروف",
                "bab": "نَصَرَ",
                "jins": "صحيح",
                "root": "(د . خ . ل)",
                "masdar": "اَلدُّخُولُ",
                "masdar_meaning": "প্রবেশ করা",
                "singular_plural": null
            },
            "taleel_or_irab": "إِذَا যরফের পর ফে'লে মাযী মাবনী আলাস সুকূন; تُمْ হলো ফা'ইল।",
            "lexical_depth_bn": "ঘরে প্রবেশের সাথে সাথে শান্তি ও দোয়ার ঘোষণা দেওয়া।",
            "classical_notes": []
        },
        {
            "word": "فَسَلِّمُوا",
            "meaning_bn": "তোমরা অভিবাদন ও সালাম পেশ করো",
            "word_type": "فعل",
            "prefix_suffix_note": "ফা জাযা সহ আমর হাজির মুযাক্কার জামা'",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "أمر حاضر معروف",
                "bab": "تَفْعِيلٌ",
                "jins": "صحيح",
                "root": "(س . ل . م)",
                "masdar": "اَلتَّسْلِيمُ",
                "masdar_meaning": "সালাম দেওয়া; অভিবাদন জানানো",
                "singular_plural": null
            },
            "taleel_or_irab": "আমর হিসেবে মাবনী আলা হাযফিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "ঘরে লোক থাকুক বা না থাকুক আসসালামু আলাইনা ওয়া আলা ইবাদিল্লাহিস সালিহীন বলা।",
            "classical_notes": []
        },
        {
            "word": "تَحِيَّةً",
            "meaning_bn": "ঐশী কল্যাণময় অভিবাদনস্বরূপ",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে মুতলাক হিসেবে মানসূব",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "مضاعف / ناقص يائي",
                "root": "(ح . ي . ي)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: تَحِيَّةٌ | বহুবচন: تَحِيَّاتٌ"
            },
            "taleel_or_irab": "سَلِّمُوا ক্রিয়ার নায়েবে মাফ'ঊলে মুতলাক হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "ইসলামী অভিবাদন সালাম যা দোয়া ও নিরাপত্তার বার্তা বহন করে।",
            "classical_notes": [
                {
                    "scholar_or_book": "মুফরাদাতুল কুরআন (ইমাম রাগেব)",
                    "note": "التحية হলো অন্যের কল্যাণ ও দীর্ঘ জীবনের প্রার্থনা করা; ইসলামের সালাম হলো সর্বোচ্চ বরকতময় তাহিয়্যাহ।"
                }
            ]
        },
        {
            "word": "مُبَارَكَةً",
            "meaning_bn": "আল্লাহর নিকট থেকে অবধারিত বরকতপূর্ণ",
            "word_type": "اسم",
            "prefix_suffix_note": "সিফাত হিসেবে মানসূব",
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
            "taleel_or_irab": "تَحِيَّةً শব্দের প্রথম সিফাত হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "সালামের বরকতে ঘরে শান্তি ও ঐশী অনুকম্পা নাযিল হয়।",
            "classical_notes": []
        },
        {
            "word": "طَيِّبَةً",
            "meaning_bn": "পবিত্র ও পরম তৃপ্তিদায়ক",
            "word_type": "اسم",
            "prefix_suffix_note": "দ্বিতীয় সিফাত হিসেবে মানসূব",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف يائي",
                "root": "(ط . ي . ب)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: طَيِّبَةٌ | বহুবচন: طَيِّبَاتٌ"
            },
            "taleel_or_irab": "تَحِيَّةً শব্দের দ্বিতীয় সিফাত হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "শ্রবণে আনন্দদায়ক ও আত্মিক প্রশান্তিদায়ক কথা।",
            "classical_notes": []
        }
    ],
    62: [
        {
            "word": "الْمُؤْمِنُونَ",
            "meaning_bn": "প্রকৃত মুমিন ও বিশ্বস্ত ব্যক্তিগণ",
            "word_type": "اسم",
            "prefix_suffix_note": "মুবতাদা হিসেবে মারফূ বিল ওয়াও",
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
            "taleel_or_irab": "إِنَّمَا-এর পর মুবতাদা হিসেবে মারফূ বিল ওয়াও (جمع مذكر سالم)।",
            "lexical_depth_bn": "যাঁদের আনুগত্য দ্বিধাহীন ও আদর্শবাদী।",
            "classical_notes": []
        },
        {
            "word": "آمَنُوا",
            "meaning_bn": "যারা একনিষ্ঠভাবে ঈমান এনেছে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "إِفْعَالٌ",
                "jins": "مهموز الفاء",
                "root": "(أ . م . ن)",
                "masdar": "اَلْإِيمَانُ",
                "masdar_meaning": "ঈমান আনা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলায যম্ম; ওয়াও হলো ফা'ইল। الَّذِينَ-এর সিলাহ।",
            "lexical_depth_bn": "আল্লাহ ও রাসূলের সাথে দৃঢ় অঙ্গীকার।",
            "classical_notes": []
        },
        {
            "word": "يَذْهَبُوا",
            "meaning_bn": "তারা প্রস্থান করে না বা চলে যায় না",
            "word_type": "فعل",
            "prefix_suffix_note": "লম (لَمْ) যোগে মাযযূম ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف مجزوم بلم",
                "bab": "فَتَحَ",
                "jins": "صحيح",
                "root": "(ذ . ه . ب)",
                "masdar": "اَلذَّهَابُ",
                "masdar_meaning": "চলে যাওয়া; প্রস্থান করা",
                "singular_plural": null
            },
            "taleel_or_irab": "لَمْ হরফের কারণে মাযযূম বি হাযফিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "দলনেতার সম্মতি ছাড়া কোনো সাংগঠনিক বৈঠক বা জিহাদ ত্যাগ না করা।",
            "classical_notes": []
        },
        {
            "word": "شَأْنِهِمْ",
            "meaning_bn": "তাদের কোনো ব্যক্তিগত জরুরত বা প্রয়োজনে",
            "word_type": "اسم",
            "prefix_suffix_note": "মুযাফ ইলাইহি হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "مهموز العين",
                "root": "(ش . أ . ن)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: شَأْنٌ | বহুবচন: شُؤُونٌ"
            },
            "taleel_or_irab": "بَعْضِ শব্দের মুযাফ ইলাইহি হিসেবে মাজরূর বিল কাসরাহ; هِمْ মুযাফ ইলাইহি।",
            "lexical_depth_bn": "ব্যক্তিগত জরুরি প্রয়োজনে দলনেতার নিকট ছুটির আর্জি পেশ করার নিয়ম।",
            "classical_notes": []
        },
        {
            "word": "فَأْذَنْ",
            "meaning_bn": "আপনি তাদের অনুমতি দিন",
            "word_type": "فعل",
            "prefix_suffix_note": "আমর হাজির মুযাক্কার ওয়াহিদ",
            "morphology": {
                "sighah": "واحد مذكر حاضر",
                "bahas": "أمر حاضر معروف",
                "bab": "سَمِعَ",
                "jins": "مهموز الفاء",
                "root": "(أ . ذ . ن)",
                "masdar": "اَلْإِذْنُ",
                "masdar_meaning": "অনুমতি দেওয়া; সম্মতি প্রকাশ করা",
                "singular_plural": null
            },
            "taleel_or_irab": "আমর হিসেবে মাবনী আলাস সুকূন; ফা'ইল যমীর হলো مستتر (تقديره أنت)।",
            "lexical_depth_bn": "নেতার বিচক্ষণতা ও অনুমোদনের অধিকার।",
            "classical_notes": []
        },
        {
            "word": "شِئْتَ",
            "meaning_bn": "আপনি যাদের জন্য সমীচীন মনে করেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "واحد مذكر حاضر",
                "bahas": "ماضي معروف",
                "bab": "ضَرَبَ",
                "jins": "أجوف يائي مهموز اللام",
                "root": "(ش . ي . أ)",
                "masdar": "اَلْمَشِيئَةُ",
                "masdar_meaning": "ইচ্ছা করা; বিবেচনা করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলাস সুকূন; تَ হলো ফা'ইল।",
            "lexical_depth_bn": "নেতার প্রজ্ঞার ওপর সিদ্ধান্ত ছেড়ে দেওয়া।",
            "classical_notes": []
        },
        {
            "word": "وَاسْتَغْفِرْ",
            "meaning_bn": "এবং তাদের জন্য ক্ষমা প্রার্থনা করুন",
            "word_type": "فعل",
            "prefix_suffix_note": "আমর হাজির মুযাক্কার ওয়াহিদ",
            "morphology": {
                "sighah": "واحد مذكر حاضر",
                "bahas": "أمر حاضر معروف",
                "bab": "اِسْتِفْعَالٌ",
                "jins": "صحيح",
                "root": "(غ . ف . ر)",
                "masdar": "اَلْاِسْتِغْفَارُ",
                "masdar_meaning": "ক্ষমা প্রার্থনা করা",
                "singular_plural": null
            },
            "taleel_or_irab": "আমর হিসেবে মাবনী আলাস সুকূন; ফা'ইল যমীর مستتر।",
            "lexical_depth_bn": "সামষ্টিক কাজ থেকে ব্যক্তিগত কারণে পিছিয়ে পড়ায় যে আধ্যাত্মিক ক্ষতি হয় তা পূরণে রাসূলের দোয়া।",
            "classical_notes": []
        },
        {
            "word": "غَفُورٌ",
            "meaning_bn": "মহাপরাক্রমশালী ক্ষমাশীল",
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
            "lexical_depth_bn": "বান্দার সীমাবদ্ধতা মার্জনাকারী।",
            "classical_notes": []
        },
        {
            "word": "رَحِيمٌ",
            "meaning_bn": "পরম দয়ালু ও স্নেহশীল",
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
            "lexical_depth_bn": "ঈমানদারদের প্রতি মহান প্রতিপালকের করুণা।",
            "classical_notes": []
        }
    ]
}

NEW_WORDS_RUKU9 = {
    63: [
        {
            "word": "تَجْعَلُوا",
            "meaning_bn": "তোমরা গণ্য করো না বা পরিগণিত করো না",
            "word_type": "فعل",
            "prefix_suffix_note": "নাহীসূচক لَا যোগে মাযযূম ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "مضارع معروف مجزوم بلا الناهية",
                "bab": "فَتَحَ",
                "jins": "صحيح",
                "root": "(ج . ع . ل)",
                "masdar": "اَلْجَعْلُ",
                "masdar_meaning": "বানানো; সাব্যস্ত করা; গণ্য করা",
                "singular_plural": null
            },
            "taleel_or_irab": "لَا النَّاهِيَة এর কারণে মাযযূম বি হাযফিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "রাসূলুল্লাহ ﷺ-এর সাথে সাধারণ মানুষের মতো আচরণ না করার কঠোর সতর্কবাণী।",
            "classical_notes": []
        },
        {
            "word": "الرَّسُولِ",
            "meaning_bn": "আল্লাহর প্রেরিত রাসূলের",
            "word_type": "اسم",
            "prefix_suffix_note": "মুযাফ ইলাইহি হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ر . س . ل)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: رَسُولٌ | বহুবচন: رُسُلٌ"
            },
            "taleel_or_irab": "دُعَاءَ শব্দের মুযাফ ইলাইহি হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "রাসূলের অনন্য সুউচ্চ সম্মান ও মর্যাদা রক্ষা প্রতিটি মুমিনের ফরয দায়িত্ব।",
            "classical_notes": []
        },
        {
            "word": "تُصِيبَهُمْ",
            "meaning_bn": "তাদের ওপর নিপতিত হয় বা আক্রান্ত করে",
            "word_type": "فعل",
            "prefix_suffix_note": "আন (أَنْ) দ্বারা মানসূব ফে'লে মুযারে",
            "morphology": {
                "sighah": "واحد مؤنث غائب",
                "bahas": "مضارع معروف",
                "bab": "إِفْعَالٌ",
                "jins": "أجوف واوي",
                "root": "(ص . و . ب)",
                "masdar": "اَلْإِصَابَةُ",
                "masdar_meaning": "আক্রান্ত করা; নিপতিত হওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "أَنْ মাসদারিয়্যাহ দ্বারা মানসূব বিল ফাতহাহ; فِتْنَةٌ হলো এর ফা'ইল; هُمْ মাফ'ঊলে বিহি।",
            "lexical_depth_bn": "রাসূলের আদর্শ লঙ্ঘনের তাৎক্ষণিক শাস্তি দুনিয়াতেই গোমরাহী ও ফিতনায় নিমজ্জিত হওয়া।",
            "classical_notes": []
        },
        {
            "word": "عَذَابٌ",
            "meaning_bn": "কঠিন আযাব বা শাস্তি",
            "word_type": "اسم",
            "prefix_suffix_note": "ফা'ইল হিসেবে মারফূ",
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
            "taleel_or_irab": "দ্বিতীয় تُصِيبَهُمْ ক্রিয়ার ফা'ইল হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "সুন্নাহ অমান্য করার পরকালীন পরিণতি জাহান্নামের আগুন।",
            "classical_notes": []
        },
        {
            "word": "أَلِيمٌ",
            "meaning_bn": "মর্মন্তুদ ও যন্ত্রণাদায়ক",
            "word_type": "اسم",
            "prefix_suffix_note": "সিফাত হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(أ . ل . م)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: أَلِيمٌ | বহুবচন: أُلَمَاءُ"
            },
            "taleel_or_irab": "عَذَابٌ শব্দের সিফাত (نعت) হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "এমন শাস্তি যা অন্তর ও দেহকে ছিন্নভিন্ন করে দেয়।",
            "classical_notes": []
        }
    ],
    64: [
        {
            "word": "السَّمَاوَاتِ",
            "meaning_bn": "নভোমণ্ডলে যা কিছু রয়েছে",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ",
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
            "taleel_or_irab": "فِي হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ (جمع مؤنث سالم)।",
            "lexical_depth_bn": "আকাশমণ্ডলীর সৃষ্টি ও ব্যবস্থাপনা সবই আল্লাহর নিরঙ্কুশ মালিকানাধীন।",
            "classical_notes": []
        },
        {
            "word": "وَالْأَرْضِ",
            "meaning_bn": "এবং ভূমণ্ডলে যা কিছু রয়েছে",
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
            "lexical_depth_bn": "মহাজগতের সবকিছু তাঁরই হুকুমের অধীন।",
            "classical_notes": []
        },
        {
            "word": "عَمِلُوا",
            "meaning_bn": "তারা যা কিছু আমল বা কর্ম করেছিল",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "سَمِعَ",
                "jins": "صحيح",
                "root": "(ع . م . ل)",
                "masdar": "اَلْعَمَلُ",
                "masdar_meaning": "আমল করা; কাজ করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলায যম্ম; ওয়াও হলো ফা'ইল। مَا موصولة-এর সিলাহ।",
            "lexical_depth_bn": "কিয়ামতের দিন ক্ষুদ্রাতিক্ষুদ্র আমলও প্রকাশ করে দেওয়া হবে।",
            "classical_notes": []
        },
        {
            "word": "عَلِيمٌ",
            "meaning_bn": "সবকিছু সম্পর্কে সম্যক জ্ঞানী",
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
            "lexical_depth_bn": "সূরা আন-নূরের সমাপ্তি আল্লাহর সর্বব্যাপী জ্ঞানের মহিমান্বিত ঘোষণার মাধ্যমে।",
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

def process_ruku(ruku_num, new_data_dict, full_words):
    file_path = f"web/public/data/24/ruku-{ruku_num}.json"
    with open(file_path, "r", encoding="utf-8") as f:
        doc = json.load(f)
        
    total_added = 0
    total_words = 0
    for a in doc.get("ayahs", []):
        v = a.get("ayah")
        ayah_w = full_words.get(f"24:{v}", [])
        existing = a.get("tahqeeq", [])
        new_w = new_data_dict.get(v, [])
        merged = merge_and_sort(existing, new_w, ayah_w)
        added = len(merged) - len(existing)
        total_added += added
        total_words += len(merged)
        a["tahqeeq"] = merged
        print(f"Ruku {ruku_num} Ayah {v:02d}: {len(existing)} -> {len(merged)} words (+{added})")
        
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        
    print(f"\n[SUCCESS] Ruku {ruku_num} expanded: +{total_added} words, total {total_words} words.")

def main():
    with open("reference/surah24_full_words.json", "r", encoding="utf-8") as f:
        full_words = json.load(f)
        
    process_ruku(7, NEW_WORDS_RUKU7, full_words)
    process_ruku(8, NEW_WORDS_RUKU8, full_words)
    process_ruku(9, NEW_WORDS_RUKU9, full_words)

if __name__ == "__main__":
    main()

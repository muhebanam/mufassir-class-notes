#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expand Tahqeeq for Surah 24 Ruku 6 (Ayahs 44-52) to Maximum Words.
Prophetic Arbitration, Hypocrisy, and Sam'an wa Ta'atan.
"""

import json

null = None

NEW_WORDS_RUKU6 = {
    44: [
        {
            "word": "اللَّيْلَ",
            "meaning_bn": "রাত্রিকালকে",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ل . ي . ل)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: لَيْلٌ | বহুবচন: لَيَالٍ"
            },
            "taleel_or_irab": "يُقَلِّبُ ক্রিয়ার মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "অন্ধকার রজনী যা আল্লাহ বান্দার বিশ্রামের জন্য সৃষ্টি করেছেন।",
            "classical_notes": []
        },
        {
            "word": "وَالنَّهَارَ",
            "meaning_bn": "এবং দিবসের আলোকচ্ছটাকে",
            "word_type": "اسم",
            "prefix_suffix_note": "মা'তূফ হিসেবে মানসূব",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ن . ه . ر)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: نَهَارٌ | বহুবচন: أَنْهُرٌ"
            },
            "taleel_or_irab": "اللَّيْلَ শব্দের ওপর মা'তূফ হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "কর্মচাঞ্চল্যের দিন যা মানুষের জীবিকা অন্বেষণের ক্ষেত্র।",
            "classical_notes": []
        },
        {
            "word": "الْأَبْصَارِ",
            "meaning_bn": "অন্তর্দৃষ্টিসম্পন্ন চক্ষুষ্মান ব্যক্তিদের",
            "word_type": "اسم",
            "prefix_suffix_note": "মুযাফ ইলাইহি হিসেবে মাজরূর",
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
            "taleel_or_irab": "أُولِي শব্দের মুযাফ ইলাইহি হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "যাঁরা বাহ্যিক সৃষ্টির পরিবর্তনের মাঝে স্রষ্টার অনন্ত কুদরত দেখতে পান।",
            "classical_notes": []
        }
    ],
    45: [
        {
            "word": "خَلَقَ",
            "meaning_bn": "তিনি সৃষ্টি করেছেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "نَصَرَ",
                "jins": "صحيح",
                "root": "(خ . ل . ق)",
                "masdar": "اَلْخَلْقُ",
                "masdar_meaning": "সৃষ্টি করা; অস্তিত্বে আনয়ন করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলাল ফাতহ; ফা'ইল হলো لفظ الجلالة (اللَّهُ)।",
            "lexical_depth_bn": "অনস্তিত্ব থেকে জীবকুলের নিখুঁত সৃষ্টি।",
            "classical_notes": []
        },
        {
            "word": "مَاءٍ",
            "meaning_bn": "একই মৌলিক উপাদান পানি থেকে",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف واوي",
                "root": "(م . و . ه)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: مَاءٌ | বহুবচন: مِيَاهٌ"
            },
            "taleel_or_irab": "مِنْ হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "জীববিজ্ঞানের আধুনিক আবিষ্কার সমর্থিত সত্য—সকল প্রাণীর মূল উপাদান পানি ও প্রোটোপ্লাজম।",
            "classical_notes": [
                {
                    "scholar_or_book": "মুফরাদাতুল কুরআন (ইমাম রাগেব)",
                    "note": "الماء হলো তরল জীবনদায়ী উপাদান; এখানে প্রাণ সৃষ্টির আদি ভিত্তি হিসেবে পানিকে উল্লেখ করা হয়েছে।"
                }
            ]
        },
        {
            "word": "يَمْشِي",
            "meaning_bn": "বিচরণ করে বা চলাফেরা করে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "ضَرَبَ",
                "jins": "নাقص يائي",
                "root": "(م . ش . ي)",
                "masdar": "اَلْمَشْيُ",
                "masdar_meaning": "হাঁটা; চলাফেরা করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ মুকাদ্দারা আলাল ইয়া; ফা'ইল যমীর مستتر (تقديره هو)। مَنْ-এর সিলাহ।",
            "lexical_depth_bn": "প্রাণীকুলের চলাচলের বিচিত্র বৈচিত্র্য।",
            "classical_notes": []
        },
        {
            "word": "بَطْنِهِ",
            "meaning_bn": "তার পেটের ওপর ভর দিয়ে (সরীসৃপ)",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ب . ط . ن)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: بَطْنٌ | বহুবচন: بُطُونٌ"
            },
            "taleel_or_irab": "عَلَى হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ; هِ যমীরটি মুযাফ ইলাইহি।",
            "lexical_depth_bn": "সাপ, কীট-পতঙ্গ ও সরীসৃপ জাতীয় প্রাণীর চলাচলের ধারা।",
            "classical_notes": []
        },
        {
            "word": "يَخْلُقُ",
            "meaning_bn": "তিনি অব্যাহতভাবে সৃষ্টি করে চলেছেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "نَصَرَ",
                "jins": "صحيح",
                "root": "(خ . ل . ق)",
                "masdar": "اَلْخَلْقُ",
                "masdar_meaning": "সৃষ্টি করা; উদ্ভাবন করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ; لفظ الجلالة (اللَّهُ) হলো ফা'ইল।",
            "lexical_depth_bn": "আল্লাহর সৃজনশীলতার কোনো সমাপ্তি নেই; তিনি যা ইচ্ছা সৃষ্টি করেন।",
            "classical_notes": []
        },
        {
            "word": "قَدِيرٌ",
            "meaning_bn": "অনন্ত সর্বশক্তিমান",
            "word_type": "اسم",
            "prefix_suffix_note": "খবর হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ق . د . ر)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: قَدِيرٌ | বহুবচন: قُدَرَاءُ"
            },
            "taleel_or_irab": "إِنَّ اللَّهَ-এর খবর হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "যাবতীয় সৃষ্টির ওপর আল্লাহর সার্বভৌম কুদরতের পূর্ণ নিয়ন্ত্রণ।",
            "classical_notes": []
        }
    ],
    46: [
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
            "lexical_depth_bn": "কুরআনের দ্ব্যর্থহীন দিকনির্দেশনা ও হেদায়াতগ্রন্থের অবতরণ।",
            "classical_notes": []
        },
        {
            "word": "آيَاتٍ",
            "meaning_bn": "বহু সুস্পষ্ট আয়াত ও নিদর্শনাবলি",
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
            "lexical_depth_bn": "সত্য ও মিথ্যার পার্থক্যকারী সুস্পষ্ট দলীলমালা।",
            "classical_notes": []
        },
        {
            "word": "مُبَيِّنَاتٍ",
            "meaning_bn": "যা সত্যকে পূর্ণ উদ্ভাসিত করে",
            "word_type": "اسم",
            "prefix_suffix_note": "সিফাত হিসেবে মানসূব বিল কাসরাহ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف يائي",
                "root": "(ب . ي . ن)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: مُبَيِّنَةٌ | বহুবচন: مُبَيِّنَاتٌ"
            },
            "taleel_or_irab": "آيَاتٍ শব্দের সিফাত হিসেবে মানসূব বিল কাসরাহ।",
            "lexical_depth_bn": "যে আয়াত মানুষের বিবেককে আলোকিত ও সংশয়মুক্ত করে।",
            "classical_notes": []
        },
        {
            "word": "يَهْدِي",
            "meaning_bn": "তিনি পরিচালিত করেন ও হেদায়াত দেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "ضَرَبَ",
                "jins": "নাقص يائي",
                "root": "(ه . د . ي)",
                "masdar": "اَلْهِدَايَةُ",
                "masdar_meaning": "পথ দেখানো; হেদায়াত দেওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ মুকাদ্দারা; اللَّهُ হলো ফা'ইল।",
            "lexical_depth_bn": "সরল পথের সন্ধান কেবল আল্লাহর তাওফীকেই মেলে।",
            "classical_notes": []
        }
    ],
    47: [
        {
            "word": "يَقُولُونَ",
            "meaning_bn": "তারা মুখে মুখে দাবি করে বলে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "نَصَرَ",
                "jins": "أجوف واوي",
                "root": "(ق . و . ل)",
                "masdar": "اَلْقَوْلُ",
                "masdar_meaning": "বলা; দাবি করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বি সুবূতিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "মুনাফিকদের মৌখিক স্বীকৃতির অন্তঃসারশূন্যতা।",
            "classical_notes": []
        },
        {
            "word": "آمَنَّا",
            "meaning_bn": "আমরা ঈমান এনেছি",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "جمع متكلم",
                "bahas": "ماضي معروف",
                "bab": "إِفْعَالٌ",
                "jins": "مهموز الفاء",
                "root": "(أ . م . ن)",
                "masdar": "اَلْإِيمَانُ",
                "masdar_meaning": "ঈমান আনা; বিশ্বাস করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলাস সুকূন; نَا হলো ফা'ইল।",
            "lexical_depth_bn": "মুখে ঈমানের দাবি কিন্তু কাজের সময় পৃষ্ঠপ্রদর্শন।",
            "classical_notes": []
        },
        {
            "word": "وَأَطَعْنَا",
            "meaning_bn": "এবং আমরা আনুগত্য স্বীকার করেছি",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "جمع متكلم",
                "bahas": "ماضي معروف",
                "bab": "إِفْعَالٌ",
                "jins": "أجوف واوي",
                "root": "(ط . و . ع)",
                "masdar": "اَلْإِطَاعَةُ",
                "masdar_meaning": "আনুগত্য করা; হুকুম মানা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলাস সুকূন; মূলত أَطْوَعْنَا থেকে أَطَعْنَا হয়েছে।",
            "lexical_depth_bn": "বাস্তব আমলহীন ভণ্ডামিপূর্ণ আনুগত্যের মৌখিক বুলি।",
            "classical_notes": []
        },
        {
            "word": "فَرِيقٌ",
            "meaning_bn": "তাদের একটি দল বা গোষ্ঠী",
            "word_type": "اسم",
            "prefix_suffix_note": "ফা'ইল হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ف . ر . ق)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: فَرِيقٌ | বহুবচন: فُرَقَاءُ"
            },
            "taleel_or_irab": "يَتَوَلَّى ক্রিয়ার ফা'ইল হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "মুনাফিকদের সেই দল যারা বিচার সালিসের সময় মুখ ফিরিয়ে নেয়।",
            "classical_notes": []
        }
    ],
    48: [
        {
            "word": "فَرِيقٌ",
            "meaning_bn": "তাদের একদল লোক",
            "word_type": "اسم",
            "prefix_suffix_note": "মুবতাদা হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ف . ر . ق)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: فَرِيقٌ | বহুবচন: فُرَقَاءُ"
            },
            "taleel_or_irab": "إِذَا الفجائية-এর পর মুবতাদা হিসেবে মারফূ বিয যম্মাহ; مُعْرِضُونَ হলো এর খবর।",
            "lexical_depth_bn": "রাসূলের নিরপেক্ষ ফায়সালার মুখোমুখি হতে মুনাফিকদের ভীতি ও অনীহা।",
            "classical_notes": []
        }
    ],
    49: [
        {
            "word": "الْحَقُّ",
            "meaning_bn": "ন্যায়সঙ্গত অধিকার ও স্বার্থ",
            "word_type": "اسم",
            "prefix_suffix_note": "ইসম হিসেবে মারফূ",
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
            "taleel_or_irab": "يَكُن-এর মুআখখার ইসম হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "যদি নিজেদের পক্ষে রায় পাওয়ার সম্ভাবনা থাকে তবে তারা দ্রুত ছুটে আসে।",
            "classical_notes": []
        },
        {
            "word": "يَأْتُوا",
            "meaning_bn": "তারা দ্রুত ছুটে আসে",
            "word_type": "فعل",
            "prefix_suffix_note": "জওয়াফুশ শার্তে ফে'লে মুযারে মাযযূম",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "ضَرَبَ",
                "jins": "مهموز الفاء ناقص يائي",
                "root": "(أ . ت . ي)",
                "masdar": "اَلْإِتْيَانُ",
                "masdar_meaning": "আসা; দ্রুত উপস্থিত হওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "জওয়াফুশ শার্ত হিসেবে মাযযূম বি হাযফিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "স্বার্থপর সুবিধাবাদী মানসিকতার বাস্তব প্রমাণ।",
            "classical_notes": []
        }
    ],
    50: [
        {
            "word": "قُلُوبِهِمْ",
            "meaning_bn": "তাদের নিজ নিজ অন্তরে",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ এবং মুযাফ",
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
            "taleel_or_irab": "فِي হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ; هِمْ যমীরটি মুযাফ ইলাইহি।",
            "lexical_depth_bn": "মুনাফিকির ব্যাধিতে আক্রান্ত অন্তরের কলুষতা।",
            "classical_notes": []
        },
        {
            "word": "يَخَافُونَ",
            "meaning_bn": "নাকি তারা এই আশঙ্কা করে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "سَمِعَ",
                "jins": "أجوف واوي",
                "root": "(خ . و . ف)",
                "masdar": "اَلْخَوْفُ",
                "masdar_meaning": "ভয় করা; অবিচারের আশঙ্কা করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বি সুবূতিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "তারা কি ভাবে যে আল্লাহ ও তাঁর রাসূল তাদের ওপর অবিচার করবেন? নাউযুবিল্লাহ!",
            "classical_notes": []
        }
    ],
    51: [
        {
            "word": "قَوْلَ",
            "meaning_bn": "মুমিনদের একমাত্র বাক্য ও ঘোষণা",
            "word_type": "اسم",
            "prefix_suffix_note": "খবর হিসেবে মানসূব এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف واوي",
                "root": "(ق . و . ل)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: قَوْلٌ | বহুবচন: أَقْوَالٌ"
            },
            "taleel_or_irab": "كَانَ ক্রিয়ার মুকাদ্দাম খবর হিসেবে মানসূব বিল ফাতহাহ; أَنْ يَقُولُوا হলো এর মুআখখার ইসম।",
            "lexical_depth_bn": "বিচার-ফায়সালা যখনই ডাকা হোক না কেন, খাঁটি মুমিনের মুখ দিয়ে কেবল আনুগত্যের কথাই বের হয়।",
            "classical_notes": []
        },
        {
            "word": "الْمُؤْمِنِينَ",
            "meaning_bn": "প্রকৃত ঈমানদার সমাজ",
            "word_type": "اسم",
            "prefix_suffix_note": "মুযাফ ইলাইহি হিসেবে মাজরূর",
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
            "taleel_or_irab": "قَوْلَ শব্দের মুযাফ ইলাইহি হিসেবে মাজরূর বিল ইয়া (جمع مذكر سالم)।",
            "lexical_depth_bn": "যাঁরা রাসুলের বিচারকে শিরোধার্য মনে করেন।",
            "classical_notes": []
        },
        {
            "word": "دُعُوا",
            "meaning_bn": "তাদেরকে যখন আহ্বান জানানো হয়",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মাঝহূল",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "ماضي مجهول",
                "bab": "نَصَرَ",
                "jins": "নাقص واوي",
                "root": "(د . ع . و)",
                "masdar": "اَلدُّعَاءُ",
                "masdar_meaning": "আহ্বান করা; ডাকা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাঝহূল মাবনী আলায যম্ম; ওয়াও হলো নায়েবে ফা'ইল।",
            "lexical_depth_bn": "শরীয়তী ফায়সালার দিকে যখনই আহ্বান আসে।",
            "classical_notes": []
        },
        {
            "word": "لِيَحْكُمَ",
            "meaning_bn": "যাতে রাসূলুল্লাহ ﷺ বিচার নিষ্পত্তি করেন",
            "word_type": "فعل",
            "prefix_suffix_note": "লামে কায় (لِـ) সহ মানসূব ফে'লে মুযারে",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "نَصَرَ",
                "jins": "صحيح",
                "root": "(ح . ك . م)",
                "masdar": "اَلْحُكْمُ",
                "masdar_meaning": "বিচার করা; ফায়সালা করা",
                "singular_plural": null
            },
            "taleel_or_irab": "أَنْ مُضْمَرَة দ্বারা মানসূব বিল ফাতহাহ; ফা'ইল যমীর مستتر (যা রাসূলের দিকে প্রত্যাবর্তিত)।",
            "lexical_depth_bn": "ন্যায়বিচারের চূড়ান্ত আদর্শ নববী বিচারব্যবস্থা।",
            "classical_notes": []
        },
        {
            "word": "يَقُولُوا",
            "meaning_bn": "তারা সানন্দে বলবে",
            "word_type": "فعل",
            "prefix_suffix_note": "আন (أَنْ) দ্বারা মানসূব ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "نَصَرَ",
                "jins": "أجوف واوي",
                "root": "(ق . و . ل)",
                "masdar": "اَلْقَوْلُ",
                "masdar_meaning": "বলা; স্বীকার করা",
                "singular_plural": null
            },
            "taleel_or_irab": "أَنْ মাসদারিয়্যাহ দ্বারা মানসূব বি হাযফিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "হৃদয়ের গভীর থেকে স্বতঃস্ফূর্ত আত্মসমর্পণ।",
            "classical_notes": []
        },
        {
            "word": "سَمِعْنَا",
            "meaning_bn": "আমরা সর্বান্তঃকরণে শুনলাম",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "جمع متكلم",
                "bahas": "ماضي معروف",
                "bab": "سَمِعَ",
                "jins": "صحيح",
                "root": "(س . م . ع)",
                "masdar": "اَلسَّمْعُ",
                "masdar_meaning": "শোনা; মান্য করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলাস সুকূন; نَا হলো ফা'ইল।",
            "lexical_depth_bn": "মুমিনের সর্বশ্রেষ্ঠ স্লোগান: سمعنا وأطعنا (শুনলাম এবং আনুগত্য করলাম)।",
            "classical_notes": []
        },
        {
            "word": "وَأَطَعْنَا",
            "meaning_bn": "এবং আমরা বিনাবাক্যে মেনে নিলাম",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "جمع متكلم",
                "bahas": "ماضي معروف",
                "bab": "إِفْعَالٌ",
                "jins": "أجوف واوي",
                "root": "(ط . و . ع)",
                "masdar": "اَلْإِطَاعَةُ",
                "masdar_meaning": "আনুগত্য করা; আদেশ পালন করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলাস সুকূন; نَا হলো ফা'ইল।",
            "lexical_depth_bn": "শর্তহীন বশ্যতা ও আমল যা প্রকৃত মুফলিহুনদের পরিচয়।",
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
        
    with open("web/public/data/24/ruku-6.json", "r", encoding="utf-8") as f:
        ruku6 = json.load(f)
        
    total_added = 0
    total_words = 0
    for a in ruku6.get("ayahs", []):
        v = a.get("ayah")
        ayah_w = full_words.get(f"24:{v}", [])
        existing = a.get("tahqeeq", [])
        new_w = NEW_WORDS_RUKU6.get(v, [])
        merged = merge_and_sort(existing, new_w, ayah_w)
        added = len(merged) - len(existing)
        total_added += added
        total_words += len(merged)
        a["tahqeeq"] = merged
        print(f"Ayah {v:02d}: {len(existing)} -> {len(merged)} words (+{added})")
        
    with open("web/public/data/24/ruku-6.json", "w", encoding="utf-8") as f:
        json.dump(ruku6, f, ensure_ascii=False, indent=2)
        
    print(f"\n[SUCCESS] Ruku 6 expanded: +{total_added} words, total {total_words} words across Ayahs 44-52.")

if __name__ == "__main__":
    main()

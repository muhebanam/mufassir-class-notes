#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expand Tahqeeq for Surah 24 Ruku 2 (Ayahs 11-20) to Maximum Words.
Adds all substantive words with full morphological precision.
"""

import json

null = None

NEW_WORDS_RUKU2 = {
    11: [
        {
            "word": "جَاءُوا",
            "meaning_bn": "তারা নিয়ে এসেছে বা রচনা করেছে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "ضَرَبَ",
                "jins": "أجوف يائي مهموز اللام",
                "root": "(ج . ي . أ)",
                "masdar": "اَلْمَجِيءُ",
                "masdar_meaning": "আসা; নিয়ে আসা; রচনা করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলায যম্ম; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "মনগড়া অপবাদ রচনা করে সমাজে ছড়িয়ে দেওয়ার ঘৃণ্য পদক্ষেপ।",
            "classical_notes": []
        },
        {
            "word": "امْرِئٍ",
            "meaning_bn": "প্রত্যেক ব্যক্তি বা মানুষের জন্য",
            "word_type": "اسم",
            "prefix_suffix_note": "মুযাফ ইলাইহি হিসেবে মাজরূর",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "مهموز اللام",
                "root": "(م . ر . أ)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: امْرُؤٌ | বহুবচন: رِجَالٌ"
            },
            "taleel_or_irab": "كُلِّ শব্দের মুযাফ ইলাইহি হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "পাপের অংশীদারিত্বে প্রত্যেক ব্যক্তির ব্যক্তিগত অপরাধের দায়ভার।",
            "classical_notes": []
        },
        {
            "word": "اكْتَسَبَ",
            "meaning_bn": "যা সে কামাই করেছে বা অর্জন করেছে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "اِفْتِعَالٌ",
                "jins": "صحيح",
                "root": "(ك . س . ب)",
                "masdar": "اَلْاِكْتِسَابُ",
                "masdar_meaning": "উপার্জন করা; অর্জন করা; কামাই করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলাল ফাতহ; ফা'ইল যমীর হলো مستتر (تقديره هو)। জুমলাটি صلة الموصول।",
            "lexical_depth_bn": "ইফতে'আল বাবে চেষ্টা-প্রচেষ্টার মাধ্যমে অর্জিত পাপ বা পুণ্যকে বিশেষ গুরুত্বের সাথে বোঝানো হয়।",
            "classical_notes": [
                {
                    "scholar_or_book": "মুফরাদাতুল কুরআন (ইমাম রাগেব)",
                    "note": "الاكتساب হলো স্বীয় শ্রম ও ইচ্ছাকৃত প্রচেষ্টায় কোনো কিছু লাভ করা; বিশেষত অনিচ্ছাকৃত পাপ নয়, বরং সুপরিকল্পিত অপরাধে ব্যবহৃত হয়।"
                }
            ]
        },
        {
            "word": "الْإِثْمِ",
            "meaning_bn": "জঘন্য পাপ ও অপরাধ",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "مهموز الفاء",
                "root": "(أ . ث . م)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: إِثْمٌ | বহুবচন: آثَامٌ"
            },
            "taleel_or_irab": "مِنْ হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "যে অপরাধ মানুষের কল্যাণ বিলম্বিত করে এবং আল্লাহর অসন্তোষ ও শাস্তি ডেকে আনে।",
            "classical_notes": []
        },
        {
            "word": "عَظِيمٌ",
            "meaning_bn": "মহাভয়াবহ ও কঠিন",
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
            "taleel_or_irab": "عَذَابٌ শব্দের সিফাত (نعت) হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "মুনাফিক সর্দার আব্দুল্লাহ ইবনে উবাই ও তার দোসরদের জন্য জাহান্নামের মহাশাস্তি।",
            "classical_notes": []
        }
    ],
    12: [
        {
            "word": "سَمِعْتُمُوهُ",
            "meaning_bn": "তোমরা তা শুনেছিলে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী সহ মাফ'ঊল যমীর",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "ماضي معروف",
                "bab": "سَمِعَ",
                "jins": "صحيح",
                "root": "(س . م . ع)",
                "masdar": "اَلسَّمْعُ",
                "masdar_meaning": "শোনা; কর্ণপাত করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলাস সুকূন; تُمْ হলো ফা'ইল; هُ যমীরটি মানসূব মাফ'ঊলে বিহি।",
            "lexical_depth_bn": "কুৎসা প্রথম শোনার মুহূর্তেই মুমিনের প্রাথমিক প্রতিক্রিয়া কেমন হওয়া উচিত ছিল তার তাগিদ।",
            "classical_notes": []
        },
        {
            "word": "وَالْمُؤْمِنَاتُ",
            "meaning_bn": "এবং মুমিন নারীগণ",
            "word_type": "اسم",
            "prefix_suffix_note": "মা'তূফ হিসেবে মারফূ",
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
            "taleel_or_irab": "الْمُؤْمِنُونَ শব্দের ওপর মা'তূফ হিসেবে মারফূ বিয যম্মাহ (جمع مؤنث سالم)।",
            "lexical_depth_bn": "চরিত্রহরণমূলক অপপ্রচারের বিরুদ্ধে নারী-পুরুষ নির্বিশেষে ঈমানদার সমাজের ঐক্যবদ্ধ সংহতি।",
            "classical_notes": []
        },
        {
            "word": "بِأَنْفُسِهِمْ",
            "meaning_bn": "নিজেদের লোকদের প্রতি / নিজেদের ভাইদের প্রতি",
            "word_type": "اسم",
            "prefix_suffix_note": "বা হরফে জার সহ মাজরূর এবং মুযাফ",
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
            "taleel_or_irab": "بِ হরফে জারের কারণে মাজরূর বিল কাসরাহ; هِمْ যমীরটি মুযাফ ইলাইহি।",
            "lexical_depth_bn": "সমগ্র মুসলিম উম্মাহ একটি একক দেহের ন্যায়; অপর মুমিনের সম্মান রক্ষা করা নিজের সম্মান রক্ষারই নামান্তর।",
            "classical_notes": [
                {
                    "scholar_or_book": "তাফসীরে কাশশাফ (যমখশারী)",
                    "note": "بأنفسهم অর্থ بأهل دينهم وملتهم؛ মুমিনগণ পরস্পর একই দেহের অঙ্গের মতো, তাই ভাইয়ের প্রতি সুধারণা রাখা নিজের প্রতি সুধারণা রাখার শামিল।"
                }
            ]
        },
        {
            "word": "خَيْرًا",
            "meaning_bn": "উত্তম ও কল্যাণকর ধারণা",
            "word_type": "اسم",
            "prefix_suffix_note": "মাফ'ঊলে বিহি হিসেবে মানসূব",
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
            "taleel_or_irab": "ظَنَّ ক্রিয়ার দ্বিতীয় মাফ'ঊলে বিহি হিসেবে মানসূব বিল ফাতহাহ।",
            "lexical_depth_bn": "অন্য কোনো মুসলিম ভাইয়ের ব্যাপারে প্রমাণ ছাড়া কোনো অপবাদ না মেনে সর্বদা শুভধারণা (حسن الظن) পোষণ করা।",
            "classical_notes": []
        },
        {
            "word": "مُبِينٌ",
            "meaning_bn": "একান্ত সুস্পষ্ট ও প্রকাশ্য",
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
            "taleel_or_irab": "إِفْكٌ শব্দের সিফাত (نعت) হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "যার মিথ্যা ও বানোয়াট হওয়া সামান্য বিচারবুদ্ধি সম্পন্ন মানুষের কাছেও সম্পূর্ণ স্পষ্ট।",
            "classical_notes": []
        }
    ],
    13: [
        {
            "word": "جَاءُوا",
            "meaning_bn": "তারা নিয়ে এলো না কেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "ماضي معروف",
                "bab": "ضَرَبَ",
                "jins": "أجوف يائي مهموز اللام",
                "root": "(ج . ي . أ)",
                "masdar": "اَلْمَجِيءُ",
                "masdar_meaning": "উপস্থিত করা; নিয়ে আসা",
                "singular_plural": null
            },
            "taleel_or_irab": "لَوْلَا التحضيضية-এর পর ফে'লে মাযী মাবনী আলায যম্ম; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "অপবাদের দাবির সপক্ষে তাৎক্ষণিক চাক্ষুষ প্রমাণের আইনি দাবি।",
            "classical_notes": []
        },
        {
            "word": "يَأْتُوا",
            "meaning_bn": "তারা উপস্থিত করতে পারল না",
            "word_type": "فعل",
            "prefix_suffix_note": "লম (لَمْ) যোগে মাযযূম ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مذكر غائب",
                "bahas": "مضارع معروف مجزوم بلم",
                "bab": "ضَرَبَ",
                "jins": "مهموز الفاء ناقص يائي",
                "root": "(أ . ت . ي)",
                "masdar": "اَلْإِتْيَانُ",
                "masdar_meaning": "হাজির করা; উপস্থিত করা",
                "singular_plural": null
            },
            "taleel_or_irab": "لَمْ হরফের কারণে মাযযূম বি হাযফিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "আইনি প্রমাণ প্রদানে তাদের চূড়ান্ত ব্যর্থতা ও অক্ষমতা।",
            "classical_notes": []
        },
        {
            "word": "بِالشُّهَدَاءِ",
            "meaning_bn": "নির্দিষ্ট চারজন সাক্ষীকে",
            "word_type": "اسم",
            "prefix_suffix_note": "বা হরফে জার সহ মাজরূর",
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
            "taleel_or_irab": "بِ হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ।",
            "lexical_depth_bn": "আল-আলিফ ওয়াল-লাম দ্বারা পূর্বে উল্লিখিত চারজন নির্ধারিত সাক্ষীকে নির্দেশ করা হয়েছে।",
            "classical_notes": []
        },
        {
            "word": "الْكَاذِبُونَ",
            "meaning_bn": "তারাই প্রকৃতপক্ষে চরম মিথ্যুক",
            "word_type": "اسم",
            "prefix_suffix_note": "খবর হিসেবে মারফূ বিল ওয়াও",
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
            "taleel_or_irab": "فَأُولَئِكَ মুবতাদার খবর হিসেবে মারফূ বিল ওয়াও (جمع مذكر سالم)।",
            "lexical_depth_bn": "আল্লাহর আদালতে ও ইসলামী শাসনব্যবস্থায় তারা প্রমাণিত মিথ্যাবাদী ও দণ্ডযোগ্য অপরাধী।",
            "classical_notes": []
        }
    ],
    14: [
        {
            "word": "فَضْلُ",
            "meaning_bn": "আল্লাহর বিশেষ অনুগ্রহ",
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
            "taleel_or_irab": "لَوْلَا-এর পর মুবতাদা হিসেবে মারফূ বিয যম্মাহ; এর খবর মাহযূফ (موجود) থাকে।",
            "lexical_depth_bn": "আল্লাহর অবারিত দান ও ক্ষমার ছায়া যা সমাজকে অনাকাঙ্ক্ষিত শাস্তি থেকে বাঁচায়।",
            "classical_notes": []
        },
        {
            "word": "وَرَحْمَتُهُ",
            "meaning_bn": "এবং তাঁর পরম করুণা",
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
            "lexical_depth_bn": "আল্লাহর দয়া যা অনুতপ্ত ঈমানদারদের পাপের গ্লানি থেকে মুক্ত করে।",
            "classical_notes": []
        },
        {
            "word": "الدُّنْيَا",
            "meaning_bn": "পার্থিব জগতে",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ মুকাদ্দারা",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "নাقص واوي",
                "root": "(د . ن . و)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: دُنْيَا | বহুবচন: دُنًى"
            },
            "taleel_or_irab": "فِي হরফে জারের কারণে মাজরূর বিল কাসরাহ মুকাদ্দারা আলাল আলিফ।",
            "lexical_depth_bn": "নিকটবর্তী ও ক্ষণস্থায়ী ইহলৌকিক জীবনকাল।",
            "classical_notes": []
        },
        {
            "word": "الْآخِرَةِ",
            "meaning_bn": "এবং পরকালীন চিরস্থায়ী জীবনে",
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
            "lexical_depth_bn": "মৃত্যুর পরবর্তী স্থায়ী হিসাব ও প্রতিফল দিবস।",
            "classical_notes": []
        },
        {
            "word": "عَظِيمٌ",
            "meaning_bn": "চরম মহা শাস্তি",
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
            "lexical_depth_bn": "ইফকের কুৎসায় অংশগ্রহণকারীদের জন্য অবধারিত শাস্তির তীব্রতা।",
            "classical_notes": []
        }
    ],
    15: [
        {
            "word": "أَلْسِنَتِكُمْ",
            "meaning_bn": "তোমাদের নিজ নিজ জিহ্বা দ্বারা",
            "word_type": "اسم",
            "prefix_suffix_note": "বা হরফে জার সহ মাজরূর এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ل . س . ن)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: لِسَانٌ | বহুবচন: أَلْسِنَةٌ"
            },
            "taleel_or_irab": "بِ হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ; كُمْ যমীরটি মুযাফ ইলাইহি।",
            "lexical_depth_bn": "বিবেক বা প্রমাণের কোনো সংযোগ ছাড়াই কেবল মুখের কথার ওপর ভর করে কুৎসা ছড়ানো।",
            "classical_notes": []
        },
        {
            "word": "أَفْوَاهِكُمْ",
            "meaning_bn": "তোমাদের মুখ দিয়ে",
            "word_type": "اسم",
            "prefix_suffix_note": "বা হরফে জার সহ মাজরূর এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "أجوف واوي",
                "root": "(ف . و . ه)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: فَمٌ / فُوهٌ | বহুবচন: أَفْوَاهٌ"
            },
            "taleel_or_irab": "بِ হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ; كُمْ মুযাফ ইলাইহি।",
            "lexical_depth_bn": "যে কথার অন্তরে কোনো ভিত্তি নেই, কেবল মুখনিঃসৃত মিথ্যা শব্দমালা।",
            "classical_notes": []
        },
        {
            "word": "عِلْمٌ",
            "meaning_bn": "কোনো নিশ্চিত জ্ঞান বা চাক্ষুষ প্রমাণ",
            "word_type": "اسم",
            "prefix_suffix_note": "লাইসা-এর ইসম হিসেবে মারফূ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(ع . ل . م)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: عِلْمٌ | বহুবচন: عُلُومٌ"
            },
            "taleel_or_irab": "لَيْسَ ক্রিয়ার মুআখখার ইসম হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "প্রমাণহীন অনুমানের ভিত্তিতে অন্যের সম্মানহানি করার মূঢ়তা।",
            "classical_notes": []
        },
        {
            "word": "عَظِيمٌ",
            "meaning_bn": "আল্লাহর নিকট মহা গুরুতর অপরাধ",
            "word_type": "اسم",
            "prefix_suffix_note": "খবর হিসেবে মারফূ",
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
            "taleel_or_irab": "هُوَ যমীরের খবর হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "মানুষ যাকে মামুলি বা হালকা মনে করে, আল্লাহর দরবারে তা ক্ষমার অযোগ্য মহাপাপ।",
            "classical_notes": []
        }
    ],
    16: [
        {
            "word": "سَمِعْتُمُوهُ",
            "meaning_bn": "তোমরা তা শোনার সাথে সাথেই",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী সহ মাফ'ঊল যমীর",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "ماضي معروف",
                "bab": "سَمِعَ",
                "jins": "صحيح",
                "root": "(س . م . ع)",
                "masdar": "اَلسَّمْعُ",
                "masdar_meaning": "শোনা; কর্ণগোচর হওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "إِذْ যরফের পর ফে'লে মাযী মাবনী আলাস সুকূন; تُمْ ফা'ইল এবং هُ মাফ'ঊলে বিহি।",
            "lexical_depth_bn": "অপবাদ শোনামাত্রই তা নাকচ ও প্রতিহত করার নৈতিক দায়িত্ব।",
            "classical_notes": []
        },
        {
            "word": "قُلْتُمْ",
            "meaning_bn": "তোমরা অবিলম্বে বলতে",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মাযী মা'রূফ",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "ماضي معروف",
                "bab": "نَصَرَ",
                "jins": "أجوف واوي",
                "root": "(ق . و . ل)",
                "masdar": "اَلْقَوْلُ",
                "masdar_meaning": "বলা; স্পষ্ট উচ্চারণ করা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মাযী মাবনী আলাস সুকূন; تُمْ হলো ফা'ইল।",
            "lexical_depth_bn": "কুৎসিত অপবাদকে কোনোভাবেই নীরব সমর্থন না দিয়ে প্রকাশ্যে প্রতিবাদ জানানো।",
            "classical_notes": []
        },
        {
            "word": "عَظِيمٌ",
            "meaning_bn": "এক মহা অপবাদ ও মারাত্মক মিথ্যাচার",
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
            "taleel_or_irab": "بُهْتَانٌ শব্দের সিফাত (نعت) হিসেবে মারফূ বিয যম্মাহ।",
            "lexical_depth_bn": "উম্মুল মুমিনীন হযরত আয়েশা সিদ্দীকা (রা.)-এর পবিত্র চরিত্রের ওপর রটিত জঘন্য অপবাদ।",
            "classical_notes": []
        }
    ],
    17: [
        {
            "word": "لِمِثْلِهِ",
            "meaning_bn": "অনুরূপ আচরণের দিকে",
            "word_type": "اسم",
            "prefix_suffix_note": "লাম হরফে জার সহ মাজরূর এবং মুযাফ",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "صحيح",
                "root": "(م . ث . ل)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: مِثْلٌ | বহুবচন: أَمْثَالٌ"
            },
            "taleel_or_irab": "لِ হরফে জারের মাজরূর হিসেবে মাজরূর বিল কাসরাহ; هِ যমীরটি মুযাফ ইলাইহি।",
            "lexical_depth_bn": "ভবিষ্যতে কোনো মুসলমানের বিরুদ্ধে অপবাদমূলক কথায় লিপ্ত হওয়া থেকে চূড়ান্ত নিবৃত্তি।",
            "classical_notes": []
        },
        {
            "word": "أَبَدًا",
            "meaning_bn": "কখনোই নয় / চিরতরে",
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
            "lexical_depth_bn": "অনুরূপ গুনাহে জীবনে কখনো লিপ্ত না হওয়ার স্থায়ী তাগিদ।",
            "classical_notes": []
        },
        {
            "word": "مُؤْمِنِينَ",
            "meaning_bn": "যদি তোমরা প্রকৃত বিশ্বাসী মুমিন হয়ে থাকো",
            "word_type": "اسم",
            "prefix_suffix_note": "খবর হিসেবে মানসূব বিল ইয়া",
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
            "taleel_or_irab": "كُنْتُمْ ক্রিয়ার খবর হিসেবে মানসূব বিল ইয়া (جمع مذكر سالم)।",
            "lexical_depth_bn": "ঈমানের অন্যতম শর্ত হলো সহমর্মিতা ও অন্যের মানহানি না করা।",
            "classical_notes": []
        }
    ],
    18: [
        {
            "word": "الْآيَاتِ",
            "meaning_bn": "সুস্পষ্ট বিধানাবলি ও নৈতিক নির্দেশনা",
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
            "lexical_depth_bn": "পবিত্র সমাজ গঠনে আল্লাহর স্পষ্ট হেদায়াত ও সীমারেখা।",
            "classical_notes": []
        }
    ],
    19: [
        {
            "word": "آمَنُوا",
            "meaning_bn": "যারা ঈমান এনেছে",
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
            "lexical_depth_bn": "ঈমানদার নারী-পুরুষের মর্যাদা সুরক্ষায় শরীয়তের আপসহীন অবস্থান।",
            "classical_notes": []
        },
        {
            "word": "عَذَابٌ",
            "meaning_bn": "যন্ত্রণাদায়ক শাস্তি",
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
            "lexical_depth_bn": "অশ্লীলতা ও পরকীয়ার অপপ্রচারকারীদের জন্য কঠিন শাস্তির ঘোষণা।",
            "classical_notes": []
        },
        {
            "word": "الدُّنْيَا",
            "meaning_bn": "পার্থিব জীবনে (হদ্দ ও লাঞ্ছনা)",
            "word_type": "اسم",
            "prefix_suffix_note": "মাজরূর বিল কাসরাহ মুকাদ্দারা",
            "morphology": {
                "sighah": null,
                "bahas": null,
                "bab": null,
                "jins": "নাقص واوي",
                "root": "(د . ن . و)",
                "masdar": null,
                "masdar_meaning": null,
                "singular_plural": "একবচন: دُنْيَا | বহুবচন: دُنًى"
            },
            "taleel_or_irab": "فِي হরফে জারের মাজরূর হিসেবে কাসরাহ মুকাদ্দারা আলাল আলিফ।",
            "lexical_depth_bn": "দুনিয়াতে হদ্দ (বেত্রাঘাত), সামাজিক বয়কট ও সাক্ষ্যের অযোগ্যতা।",
            "classical_notes": []
        },
        {
            "word": "وَالْآخِرَةِ",
            "meaning_bn": "এবং আখেরাতে (জাহান্নামের আগুন)",
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
            "lexical_depth_bn": "তওবা ছাড়া মৃত্যুবরণ করলে পরকালের চিরস্থায়ী নারকীয় আযাব।",
            "classical_notes": []
        },
        {
            "word": "يَعْلَمُ",
            "meaning_bn": "আল্লাহ সম্যক জানেন ও অবগত আছেন",
            "word_type": "فعل",
            "prefix_suffix_note": "ফে'লে মুযারে মারফূ",
            "morphology": {
                "sighah": "واحد مذكر غائب",
                "bahas": "مضارع معروف",
                "bab": "سَمِعَ",
                "jins": "صحيح",
                "root": "(ع . ل . م)",
                "masdar": "اَلْعِلْمُ",
                "masdar_meaning": "জানা; অবগত হওয়া",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বিয যম্মাহ; ফা'ইল যমীর হলো مستتر (تقديره هو)।",
            "lexical_depth_bn": "আল্লাহ অন্তরের গূঢ় ষড়যন্ত্র ও কপটতা সবই জানেন।",
            "classical_notes": []
        },
        {
            "word": "تَعْلَمُونَ",
            "meaning_bn": "তোমরা এর পরিণতি ও ভয়াবহতা জানো না",
            "word_type": "فعل",
            "prefix_suffix_note": "নাফীসূচক لَا যোগে ফে'লে মুযারে",
            "morphology": {
                "sighah": "جمع مذكر حاضر",
                "bahas": "مضارع معروف",
                "bab": "سَمِعَ",
                "jins": "صحيح",
                "root": "(ع . ل . م)",
                "masdar": "اَلْعِلْمُ",
                "masdar_meaning": "জানা; জ্ঞান রাখা",
                "singular_plural": null
            },
            "taleel_or_irab": "ফে'লে মুযারে মারফূ বি সুবূতিন নূন; ওয়াও হলো ফা'ইল।",
            "lexical_depth_bn": "মানুষ অপবাদের সামাজিক ক্ষতি ও ঐশী ক্রোধের গভীরতা উপলব্ধি করতে পারে না।",
            "classical_notes": []
        }
    ],
    20: [
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
            "lexical_depth_bn": "অপবাদের ঘটনার পুনরাবৃত্তির সমাপ্তি টানতে আল্লাহর পরম অনুগ্রহের স্মরণ।",
            "classical_notes": []
        },
        {
            "word": "وَرَحْمَتُهُ",
            "meaning_bn": "এবং তাঁর অপার ক্ষমা ও দয়া",
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
            "lexical_depth_bn": "মুমিনদের তাওবা কবুল ও সমাজকে পবিত্র করার পেছনে আল্লাহর রহমতের প্রভাব।",
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
        
    with open("web/public/data/24/ruku-2.json", "r", encoding="utf-8") as f:
        ruku2 = json.load(f)
        
    total_added = 0
    total_words = 0
    for a in ruku2.get("ayahs", []):
        v = a.get("ayah")
        ayah_w = full_words.get(f"24:{v}", [])
        existing = a.get("tahqeeq", [])
        new_w = NEW_WORDS_RUKU2.get(v, [])
        merged = merge_and_sort(existing, new_w, ayah_w)
        added = len(merged) - len(existing)
        total_added += added
        total_words += len(merged)
        a["tahqeeq"] = merged
        print(f"Ayah {v:02d}: {len(existing)} -> {len(merged)} words (+{added})")
        
    with open("web/public/data/24/ruku-2.json", "w", encoding="utf-8") as f:
        json.dump(ruku2, f, ensure_ascii=False, indent=2)
        
    print(f"\n[SUCCESS] Ruku 2 expanded: +{total_added} words, total {total_words} words across Ayahs 11-20.")

if __name__ == "__main__":
    main()

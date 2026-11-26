import React, { useState, useRef, useEffect } from 'react';
import { ExternalLink, BookOpen, ChevronDown, Sparkles } from 'lucide-react';

const TAFSIR_CATEGORIES = [
  {
    category: 'أمهات (মৌলিক ও প্রাচীন তাফসীর)',
    books: [
      { name: 'جامع البيان (ابن جرير الطبري)', year: '৩১০ হিজরী', slug: 'tabari' },
      { name: 'تفسير القرآن العظيم (ابن كثير)', year: '৭৭৪ হিজরী', slug: 'katheer' },
      { name: 'الجامع لأحكام القرآن (القرطبي)', year: '৬৭১ হিজরী', slug: 'qurtubi' },
      { name: 'معالم التنزيل (البغوي)', year: '৫১৬ হিজরী', slug: 'baghawi' }
    ]
  },
  {
    category: 'موسوعات (বিশ্বকোষীয় তাফসীর)',
    books: [
      { name: 'مفاتيح الغيب (فخر الدين الرازي)', year: '৬০৬ হিজরী', slug: 'razi' },
      { name: 'روح المعاني (الألوسي)', year: '১২৭০ হিজরী', slug: 'alusi' }
    ]
  },
  {
    category: 'عامة وجمع الأقوال (সাধারণ ও আহকাম)',
    books: [
      { name: 'فتح القدير (الشوكاني)', year: '১২৫০ হিজরী', slug: 'shawkani' },
      { name: 'زاد المسير (ابن الجوزي)', year: '৫৯৭ হিজরী', slug: 'zad' },
      { name: 'التحرير والتنوير (ابن عاشور)', year: '১৩৯৩ হিজরী', slug: 'ibn-ashoor' }
    ]
  },
  {
    category: 'معاصرة (সমকালীন ও সহজবোধ্য)',
    books: [
      { name: 'التفسير الميسر (مجمع الملك فهد)', year: 'সমকালীন', slug: 'muyassar' },
      { name: 'المختصر في التفسير (مركز تفسير)', year: 'সমকালীন', slug: 'mukhtasar' },
      { name: 'تيسير الكريم الرحمن (السعدي)', year: '১৩৭৬ হিজরী', slug: 'saadi' },
      { name: 'أيسر التفاسير (الجزائري)', year: '১৪৩৯ হিজরী', slug: 'jazaeri' },
      { name: 'تفسير القرآن الكريم (ابن عثيمين)', year: '১৪২১ হিজরী', slug: 'othaimin' }
    ]
  },
  {
    category: 'তাফসীরুল জালালাইন',
    books: [
      { name: 'تفسير الجلالين (المحلي والسيوطي)', year: 'মূল আরবি পাঠ', slug: 'jalalayn' }
    ]
  }
];

export default function TafsirAppMenu({ surah = 24, ayahNumber = 1, compact = false }) {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="relative inline-block text-left" ref={menuRef}>
      <div className="flex items-center gap-1.5">
        {/* Main direct link to tafsir.app search for this ayah */}
        <a
          href={`https://tafsir.app/${surah}/${ayahNumber}`}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-semibold bg-emerald-50 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 hover:bg-emerald-100 transition shadow-2xs"
          title={`الباحث القرآني (tafsir.app)-এ আয়াত ${ayahNumber}-এর তাফসীর খুলুন`}
        >
          <ExternalLink className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
          <span className="font-arabic font-medium" dir="rtl">الباحث القرآني</span>
          {!compact && (
            <span className="text-[10px] font-mono text-emerald-600 dark:text-emerald-400 hidden sm:inline">(tafsir.app)</span>
          )}
        </a>

        {/* Dropdown toggle for specific classical tafsir books */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          aria-expanded={isOpen}
          className="p-1 rounded-lg border border-emerald-200 dark:border-emerald-800 bg-white dark:bg-gray-800 text-emerald-700 dark:text-emerald-300 hover:bg-emerald-50 dark:hover:bg-gray-700 transition"
          title="নির্দিষ্ট কিতাব অনুযায়ী তাফসীর বেছে নিন (তাবারী, ইবনে কাসীর, কুরতুবী, রাযী...)"
        >
          <ChevronDown className={`w-3.5 h-3.5 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
        </button>
      </div>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-80 sm:w-96 rounded-2xl bg-white dark:bg-gray-900 border border-emerald-200 dark:border-gray-700 shadow-xl z-50 p-3 max-h-[80vh] overflow-y-auto space-y-3 font-bengali">
          <div className="flex items-center justify-between pb-2 border-b border-gray-100 dark:border-gray-800">
            <div className="flex items-center gap-1.5">
              <BookOpen className="w-4 h-4 text-emerald-600" />
              <span className="text-xs font-bold text-gray-900 dark:text-gray-100">
                الباحث القرآني — কিতাবভিত্তিক তাফসীর
              </span>
            </div>
            <a
              href={`https://tafsir.app/${surah}/${ayahNumber}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-[10px] text-emerald-600 dark:text-emerald-400 hover:underline flex items-center gap-0.5"
            >
              <span>মূল সাইট</span>
              <ExternalLink className="w-2.5 h-2.5" />
            </a>
          </div>

          {TAFSIR_CATEGORIES.map((cat, idx) => (
            <div key={idx} className="space-y-1">
              <div className="text-[11px] font-bold text-gray-500 dark:text-gray-400 px-1.5 uppercase tracking-wide">
                {cat.category}
              </div>
              <div className="grid grid-cols-1 gap-1">
                {cat.books.map((b) => (
                  <a
                    key={b.slug}
                    href={`https://tafsir.app/${b.slug}/${surah}/${ayahNumber}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={() => setIsOpen(false)}
                    className="flex items-center justify-between p-2 rounded-xl hover:bg-emerald-50 dark:hover:bg-gray-800/80 transition group border border-transparent hover:border-emerald-200 dark:hover:border-gray-700"
                  >
                    <div className="text-right flex-1" dir="rtl">
                      <div className="font-arabic text-xs font-semibold text-gray-900 dark:text-gray-100 group-hover:text-emerald-700 dark:group-hover:text-emerald-300">
                        {b.name}
                      </div>
                    </div>
                    <span className="text-[10px] text-gray-400 dark:text-gray-500 font-mono ml-2 shrink-0">
                      {b.year}
                    </span>
                  </a>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

import React, { useState } from 'react';
import { GitCommit, ChevronRight, ChevronDown, Layers, BookOpen, Compass, ExternalLink } from 'lucide-react';

const SURAH_24_THEMATIC_NODES = [
  {
    ruku_id: 1,
    title: 'পারিবারিক পবিত্রতা ও ব্যভিচারের দণ্ডবিধি',
    ayah_range: '১–১০',
    color: 'emerald',
    subtopics: [
      { text: 'সূরার গুরুত্ব ও ঐশী কর্তৃত্ব ঘোষণা', ayahs: '১' },
      { text: 'যিনার শাস্তি ও ১০০ বেত্রাঘাতের বিধান', ayahs: '২–৩' },
      { text: 'অপবাদের (কযফ) শাস্তি ও শর্তাবলি', ayahs: '৪–৫' },
      { text: 'দাম্পত্য অপবাদ ও লি‘আনের বিধান', ayahs: '৬–১০' }
    ]
  },
  {
    ruku_id: 2,
    title: 'ইফকের ঐতিহাসিক ঘটনা ও অপবাদ রটনাকারীদের নিন্দা',
    ayah_range: '১১–২০',
    color: 'blue',
    subtopics: [
      { text: 'হযরত আয়েশা (রা.)-এর ওপর অপবাদ ও মুমিনদের করণীয়', ayahs: '১১–১৫' },
      { text: 'সামাজিক গুজবের ভয়াবহতা ও আল্লাহর হুশিয়ারি', ayahs: '১৬–২০' }
    ]
  },
  {
    ruku_id: 3,
    title: 'শয়তানের পদাঙ্ক বর্জন ও সামাজিক পরিশুদ্ধি',
    ayah_range: '২১–২৬',
    color: 'teal',
    subtopics: [
      { text: 'শয়তানের অনুসরণ নিষিদ্ধকরণ ও আত্মশুদ্ধি', ayahs: '২১–২২' },
      { text: 'সতী-সাধ্বী নারীদের ওপর অপবাদের চূড়ান্ত পরিণতি', ayahs: '২৩–২৬' }
    ]
  },
  {
    ruku_id: 4,
    title: 'গৃহে প্রবেশের শিষ্টাচার, দৃষ্টি সংযম ও পর্দার বিধান',
    ayah_range: '২৭–৩৪',
    color: 'indigo',
    subtopics: [
      { text: 'অনুমতি প্রার্থনা (ইস্তিজান) ও সালামের নিয়ম', ayahs: '২৭–২৯' },
      { text: 'পুরুষ ও নারীর গযযে বাসার ও মাহরাম তালিকা', ayahs: '৩০–৩১' },
      { text: 'বিবাহের সামাজিক দায়িত্ব ও পবিত্র থাকার নির্দেশ', ayahs: '৩২–৩৪' }
    ]
  },
  {
    ruku_id: 5,
    title: 'আয়াতে নূর, মসজিদের মর্যাদা ও কাফিরদের মরীচিকা',
    ayah_range: '৩৫–৪০',
    color: 'amber',
    subtopics: [
      { text: 'আল্লাহ আসমান ও জমিনের নূর (আয়াতে নূর)', ayahs: '৩৫' },
      { text: 'মসজিদসমূহে আল্লাহর যিকর ও মুমিন ব্যবসায়ীদের বৈশিষ্ট্য', ayahs: '৩৬–৩৮' },
      { text: 'কাফিরদের আমলের মরীচিকা ও অন্ধকার সদৃশ উপমা', ayahs: '৩৯–৪০' }
    ]
  },
  {
    ruku_id: 6,
    title: 'মহাজাগতিক তাসবীহ, বৃষ্টিবর্ষণ ও আল্লাহর সার্বভৌমত্ব',
    ayah_range: '৪১–৪৭',
    color: 'cyan',
    subtopics: [
      { text: 'সৃষ্টিজগতের সর্বত্র আল্লাহর তাসবীহ ও সার্বভৌমত্ব', ayahs: '৪১–৪৫' },
      { text: 'সুস্পষ্ট আয়াতসমূহ ও বিভ্রান্তদের প্রতিক্রিয়া', ayahs: '৪৬–৪৭' }
    ]
  },
  {
    ruku_id: 7,
    title: 'বিচারব্যবস্থায় রাসূলের আনুগত্য বনাম মুনাফিকদের আচরণ',
    ayah_range: '৪৮–৫৭',
    color: 'rose',
    subtopics: [
      { text: 'রাসূলের বিচারে মুনাফিকদের অনীহা ও অহংকার', ayahs: '৪৮–৫০' },
      { text: 'মুমিনদের অকুণ্ঠ আনুগত্য (‘সামি‘না ওয়া আত্বা‘না’)', ayahs: '৫১–৫৪' },
      { text: 'পৃথিবীতে খিলাফতের ঐশী প্রতিশ্রুতি ও ঈমান', ayahs: '৫৫–৫৭' }
    ]
  },
  {
    ruku_id: 8,
    title: 'পারিবারিক গোপনীয়তার শিষ্টাচার ও আত্মীয়দের সাথে আহার',
    ayah_range: '৫৮–৬১',
    color: 'violet',
    subtopics: [
      { text: 'তিনটি সংবেদনশীল সময়ে অনুমতি গ্রহণের বিধান', ayahs: '৫৮–৫৯' },
      { text: 'বয়োবৃদ্ধ নারীদের পোশাক শিথিলতা', ayahs: '৬০' },
      { text: 'আত্মীয়স্বজনদের ঘরে আহার ও সালাম আদান-প্রদান', ayahs: '৬১' }
    ]
  },
  {
    ruku_id: 9,
    title: 'সম্মিলিত কাজে রাষ্ট্রীয় শিষ্টাচার ও আল্লাহর সার্বিক জ্ঞান',
    ayah_range: '৬২–৬৪',
    color: 'emerald',
    subtopics: [
      { text: 'সম্মিলিত গুরুত্বপূর্ণ কাজে রাসূলের নিকট ছুটির শিষ্টাচার', ayahs: '৬২' },
      { text: 'রাসূলুল্লাহ (সা.)-কে ডাকার বিশেষ আদব', ayahs: '৬৩' },
      { text: 'আসমান-জমিনের ওপর আল্লাহর পূর্ণ কর্তৃত্ব ও হিসাব গ্রহণ', ayahs: '৬৪' }
    ]
  }
];

export default function MindMap({ 
  surahInfo, 
  surahMeta,
  currentRuku = 1, 
  onSelectRuku, 
  onSelectAyah,
  mode = 'surah' // 'surah' or 'ruku'
}) {
  const [expandedRukus, setExpandedRukus] = useState({ [currentRuku]: true });
  const [hoveredNode, setHoveredNode] = useState(null);

  const toggleRuku = (rId) => {
    setExpandedRukus(prev => ({
      ...prev,
      [rId]: !prev[rId]
    }));
  };

  const toBn = (num) => {
    const bn = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
    return String(num).replace(/[0-9]/g, d => bn[d]);
  };

  const colors = ['emerald', 'blue', 'teal', 'indigo', 'amber', 'cyan', 'rose', 'violet'];

  // Dynamic nodes: If Surah 24, use detailed curated nodes; otherwise generate from surahMeta/surahInfo rukus
  const isSurah24 = (surahInfo?.id === 24 || (!surahInfo && !surahMeta));
  const rawRukus = surahMeta?.rukus || surahInfo?.rukus || [];

  const thematicNodes = isSurah24
    ? SURAH_24_THEMATIC_NODES
    : (rawRukus.length > 0
        ? rawRukus.map((r, idx) => {
            const rId = r.ruku_id || (idx + 1);
            const aStart = r.ayah_start || (Array.isArray(r) ? r[0] : 1);
            const aEnd = r.ayah_end || (Array.isArray(r) ? r[1] : 1);
            const aRangeBn = r.ayah_range_bn || `${toBn(aStart)}–${toBn(aEnd)}`;
            return {
              ruku_id: rId,
              title: `রুকু ${toBn(rId)}: আয়াত ${aRangeBn}`,
              ayah_range: aRangeBn,
              color: colors[idx % colors.length],
              subtopics: [
                { text: `আয়াত ${aRangeBn}-এর বিষয়বস্তু ও পর্যালোচনা`, ayahs: aRangeBn }
              ]
            };
          })
        : SURAH_24_THEMATIC_NODES
      );

  const surahName = surahInfo?.name_bn || surahMeta?.name_bn || 'আন-নূর';
  const surahId = surahInfo?.id || surahMeta?.id || 24;
  const rukuCount = surahInfo?.ruku_count || surahMeta?.ruku_count || thematicNodes.length;
  const ayahCount = surahInfo?.ayah_count || surahMeta?.ayah_count || 0;

  return (
    <div className="w-full bg-white dark:bg-gray-800/90 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-6 shadow-xs layout-safe">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-4 mb-4 border-b border-gray-100 dark:border-gray-700">
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 rounded-xl bg-emerald-100 dark:bg-emerald-900/50 flex items-center justify-center text-emerald-700 dark:text-emerald-300">
            <Compass className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base sm:text-lg font-bold text-gray-900 dark:text-gray-100 font-bengali">
              {mode === 'surah' ? `সূরা ${surahName}-এর পূর্ণাঙ্গ বিষয়ভিত্তিক মাইন্ড ম্যাপ` : `রুকু ${toBn(currentRuku)}-এর বিষয়ভিত্তিক সংযোগ রেখা`}
            </h3>
            <p className="text-xs text-gray-500 dark:text-gray-400 font-bengali">
              {mode === 'surah' 
                ? `${toBn(rukuCount)}টি রুকু ও ${toBn(ayahCount)}টি আয়াতের বিষয়ভিত্তিক পারস্পরিক সম্পর্ক ও প্রাসঙ্গিকতা` 
                : 'বর্তমান রুকুর শাখা-প্রশাখা ও মূল বক্তব্যের প্রবাহ'}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-xs font-bengali">
          <span className="px-2.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 font-medium border border-emerald-200 dark:border-emerald-800">
            {toBn(thematicNodes.length)}টি রুকু থিম
          </span>
        </div>
      </div>

      {/* DESKTOP VIEW: SVG Connected Flow Chart (lg:block) */}
      <div className="hidden lg:block overflow-x-auto pb-4">
        <div className="min-w-[860px] relative">
          {/* Central Root Node */}
          <div className="flex items-center justify-center mb-8">
            <div className="relative px-6 py-3.5 rounded-2xl bg-gradient-to-r from-emerald-700 to-teal-800 text-white shadow-md text-center max-w-md border-2 border-emerald-500/30">
              <span className="text-xs uppercase tracking-wider text-emerald-200 font-mono">Surah Structure</span>
              <h4 className="text-xl font-bold font-bengali">সূরা {surahName} ({toBn(surahId)})</h4>
              <p className="text-xs text-emerald-100 font-bengali mt-0.5">
                রুকু: {toBn(rukuCount)}টি • মোট আয়াত: {toBn(ayahCount)}টি
              </p>
            </div>
          </div>

          {/* SVG Connector Lines */}
          <svg className="w-full h-12 -my-4 pointer-events-none" viewBox="0 0 900 48" preserveAspectRatio="none">
            <path d="M 450,0 C 450,24 150,24 150,48" fill="none" stroke="currentColor" strokeWidth="2" className="text-emerald-300 dark:text-emerald-700/60" strokeDasharray="4 4" />
            <path d="M 450,0 C 450,24 450,24 450,48" fill="none" stroke="currentColor" strokeWidth="2" className="text-emerald-500 dark:text-emerald-600" />
            <path d="M 450,0 C 450,24 750,24 750,48" fill="none" stroke="currentColor" strokeWidth="2" className="text-emerald-300 dark:text-emerald-700/60" strokeDasharray="4 4" />
          </svg>

          {/* 3-Column Thematic Grid of Rukus */}
          <div className="grid grid-cols-3 gap-4">
            {thematicNodes.map((r) => {
              const isActive = r.ruku_id === currentRuku;
              return (
                <div
                  key={r.ruku_id}
                  onMouseEnter={() => setHoveredNode(r.ruku_id)}
                  onMouseLeave={() => setHoveredNode(null)}
                  className={`p-4 rounded-xl border transition-all duration-200 ${
                    isActive
                      ? 'bg-emerald-50/70 dark:bg-emerald-950/40 border-emerald-400 dark:border-emerald-600 shadow-sm ring-2 ring-emerald-500/20'
                      : 'bg-gray-50/60 dark:bg-gray-800/60 border-gray-200 dark:border-gray-700 hover:border-emerald-300 dark:hover:border-emerald-700'
                  }`}
                >
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <button
                      onClick={() => onSelectRuku && onSelectRuku(r.ruku_id)}
                      className="text-left group flex-1"
                    >
                      <div className="flex items-center gap-1.5">
                        <span className="w-6 h-6 rounded-lg bg-emerald-600 text-white text-xs font-bold flex items-center justify-center font-mono">
                          {r.ruku_id}
                        </span>
                        <span className="text-xs font-bold text-gray-500 dark:text-gray-400 font-bengali">
                          রুকু {toBn(r.ruku_id)} (আয়াত {r.ayah_range})
                        </span>
                      </div>
                      <h5 className="font-bold text-sm text-gray-900 dark:text-gray-100 font-bengali group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors mt-1">
                        {r.title}
                      </h5>
                    </button>
                    {onSelectRuku && (
                      <button
                        onClick={() => onSelectRuku(r.ruku_id)}
                        title="এই রুকুতে যান"
                        className="p-1 rounded-md text-gray-400 hover:text-emerald-600 hover:bg-emerald-100 dark:hover:bg-emerald-900/40 transition"
                      >
                        <ExternalLink className="w-3.5 h-3.5" />
                      </button>
                    )}
                  </div>

                  {/* Subtopics list */}
                  <div className="space-y-1.5 pt-2 border-t border-gray-200/60 dark:border-gray-700/60 text-xs font-bengali text-gray-600 dark:text-gray-300">
                    {r.subtopics.map((st, sIdx) => (
                      <div key={sIdx} className="flex items-start gap-1.5 leading-snug">
                        <span className="text-emerald-600 dark:text-emerald-400 mt-0.5">•</span>
                        <span className="flex-1">{st.text}</span>
                        <span className="text-[11px] font-mono text-gray-400 dark:text-gray-500 whitespace-nowrap">
                          [{st.ayahs}]
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* MOBILE & TABLET VIEW: Collapsible Vertical Accordion Tree (<1024px) */}
      <div className="lg:hidden space-y-2.5">
        {thematicNodes.map((r) => {
          const isExpanded = !!expandedRukus[r.ruku_id];
          const isActive = r.ruku_id === currentRuku;

          return (
            <div
              key={r.ruku_id}
              className={`rounded-xl border transition-all ${
                isActive
                  ? 'border-emerald-500 dark:border-emerald-600 bg-emerald-50/40 dark:bg-emerald-950/20 shadow-2xs'
                  : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800'
              }`}
            >
              <div
                onClick={() => toggleRuku(r.ruku_id)}
                className="flex items-center justify-between p-3 cursor-pointer select-none gap-2"
              >
                <div className="flex items-center gap-2.5 flex-1 min-w-0">
                  <span className={`w-6 h-6 rounded-md text-xs font-bold flex items-center justify-center font-mono shrink-0 ${
                    isActive ? 'bg-emerald-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                  }`}>
                    {r.ruku_id}
                  </span>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400 font-bengali">
                      <span>রুকু {toBn(r.ruku_id)}</span>
                      <span>•</span>
                      <span>আয়াত {r.ayah_range}</span>
                    </div>
                    <h5 className="font-bold text-sm text-gray-900 dark:text-gray-100 font-bengali truncate">
                      {r.title}
                    </h5>
                  </div>
                </div>
                <div className="flex items-center gap-1 shrink-0">
                  {onSelectRuku && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onSelectRuku(r.ruku_id);
                      }}
                      className="px-2 py-1 rounded-lg text-xs font-bengali bg-emerald-100 dark:bg-emerald-900/40 text-emerald-700 dark:text-emerald-300 hover:bg-emerald-200"
                    >
                      অধ্যয়ন
                    </button>
                  )}
                  {isExpanded ? (
                    <ChevronDown className="w-4 h-4 text-gray-400" />
                  ) : (
                    <ChevronRight className="w-4 h-4 text-gray-400" />
                  )}
                </div>
              </div>

              {/* Collapsible Content */}
              {isExpanded && (
                <div className="px-3.5 pb-3 pt-1 border-t border-gray-100 dark:border-gray-700/60 space-y-2">
                  <div className="text-xs font-semibold text-gray-500 dark:text-gray-400 font-bengali">
                    শাখা আলোচ্য বিষয়াবলি:
                  </div>
                  <div className="space-y-1.5 pl-2 border-l-2 border-emerald-400 dark:border-emerald-600">
                    {r.subtopics.map((st, sIdx) => (
                      <div key={sIdx} className="text-xs font-bengali text-gray-700 dark:text-gray-300 flex items-start justify-between gap-2">
                        <span>{st.text}</span>
                        <span className="font-mono text-[11px] text-gray-400 shrink-0">
                          (আয়াত {st.ayahs})
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

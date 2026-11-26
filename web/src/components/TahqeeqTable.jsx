import React, { useState, useMemo } from 'react';
import { Search, BookOpen, Sparkles, Filter, ChevronDown, ChevronUp, ExternalLink } from 'lucide-react';
import MarkdownContent from './MarkdownContent';

export default function TahqeeqTable({ words = [], ayahNumber = null, compact = false }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all'); // 'all', 'فعل', 'اسم', 'حرف'
  const [expandedWordIdx, setExpandedWordIdx] = useState(null);

  const filteredWords = useMemo(() => {
    if (!words || !Array.isArray(words)) return [];
    return words.filter(item => {
      const wText = item.word || item['শব্দ'] || item['আরবি শব্দ'] || '';
      const mText = item.meaning_bn || item['কুরআনিক পরিভাষাগত অর্থ'] || item['মূল অর্থ'] || item['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র'] || '';
      const rootText = item.morphology?.root || item['মূলধাতু'] || '';
      const sText = item['সীগা / ওযন'] || item['ব্যুৎপত্তি ও সিগাহ'] || '';
      const type = item.word_type || (sText.includes('فعل') ? 'فعل' : sText.includes('اسم') ? 'اسم' : sText.includes('حرف') ? 'حرف' : '');

      const matchesSearch = !searchTerm || 
        wText.includes(searchTerm) || 
        mText.toLowerCase().includes(searchTerm.toLowerCase()) ||
        rootText.includes(searchTerm);

      const matchesType = filterType === 'all' || type === filterType;

      return matchesSearch && matchesType;
    });
  }, [words, searchTerm, filterType]);

  const toBn = (num) => {
    const bn = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
    return String(num).replace(/[0-9]/g, d => bn[d]);
  };

  if (!words || words.length === 0) {
    return (
      <div className="text-center py-6 text-gray-500 dark:text-gray-400 font-bengali text-sm italic">
        এই আয়াতের জন্য স্বতন্ত্র শাব্দিক তাহকীক সারণি প্রযোজ্য নয় বা সংকলিত হয়নি।
      </div>
    );
  }

  return (
    <div className="space-y-3 layout-safe">
      {/* Header & Search / Filter Controls */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2.5 pb-2 border-b border-gray-100 dark:border-gray-700">
        <div className="flex items-center gap-2">
          <BookOpen className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
          <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100 font-bengali">
            {ayahNumber ? `আয়াত ${toBn(ayahNumber)}-এর শাব্দিক তাহকীক` : 'শাব্দিক তাহকীক সারণি'}
            <span className="ml-2 text-xs font-normal text-emerald-700 dark:text-emerald-400 font-mono">
              ({toBn(filteredWords.length)}/{toBn(words.length)}টি শব্দ)
            </span>
          </h4>
        </div>

        {/* Filter / Search Bar */}
        <div className="flex items-center gap-2">
          <div className="relative flex-1 sm:w-48">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="শব্দ, মূলবর্ণ বা অর্থ..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-8 pr-2.5 py-1 text-xs rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 font-bengali placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-emerald-500"
            />
          </div>

          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="text-xs py-1 px-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 font-bengali focus:outline-none"
          >
            <option value="all">সকল প্রকার</option>
            <option value="فعل">فعل (ক্রিয়া)</option>
            <option value="اسم">اسم (বিশেষ্য)</option>
            <option value="حرف">حرف (অব্যয়)</option>
          </select>
        </div>
      </div>

      {/* DESKTOP / TABLET: Structured Responsive Table */}
      <div className="hidden md:block overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700 shadow-2xs">
        <table className="w-full text-left text-xs sm:text-sm border-collapse">
          <thead className="bg-emerald-50/70 dark:bg-gray-800/90 text-gray-700 dark:text-gray-300 border-b border-gray-200 dark:border-gray-700 font-bengali">
            <tr>
              <th className="px-3 py-2.5 font-bold text-center w-12">ক্রম</th>
              <th className="px-3.5 py-2.5 font-bold text-right font-arabic">শব্দ (কুরআনিক পাঠ)</th>
              <th className="px-3.5 py-2.5 font-bold">বাংলা অর্থ ও প্রকার</th>
              <th className="px-3.5 py-2.5 font-bold">সরফ: সীগাহ, বহছ ও বাব</th>
              <th className="px-3.5 py-2.5 font-bold">মূলবর্ণ, জিনস ও মাসদার</th>
              <th className="px-3.5 py-2.5 font-bold">তালীল / ইরাব ও ক্লাসিক্যাল নোট</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 dark:divide-gray-700/60 bg-white dark:bg-gray-800 font-bengali">
            {filteredWords.map((item, idx) => {
              const morph = item.morphology || {};
              const isVerb = item.word_type === 'فعل';
              const hasNotes = item.classical_notes && item.classical_notes.length > 0;

              return (
                <tr key={idx} className="hover:bg-emerald-50/30 dark:hover:bg-gray-700/30 transition-colors">
                  {/* Serial */}
                  <td className="px-3 py-2.5 text-center font-mono text-gray-400 dark:text-gray-500 font-bold">
                    {toBn(idx + 1)}
                  </td>

                  {/* Arabic Word */}
                  <td className="px-3.5 py-2.5 text-right font-arabic text-base sm:text-lg font-bold text-emerald-800 dark:text-emerald-300 whitespace-nowrap" dir="rtl">
                    <span className="font-arabic leading-relaxed" dir="rtl">
                      {item.word || item['শব্দ'] || item['আরবি শব্দ']}
                    </span>
                    {item.prefix_suffix_note && (
                      <div className="text-[11px] font-normal text-gray-500 dark:text-gray-400 font-bengali" dir="ltr">
                        {item.prefix_suffix_note}
                      </div>
                    )}
                  </td>

                  {/* Meaning & Word Type */}
                  <td className="px-3.5 py-2.5">
                    <div className="font-semibold text-gray-900 dark:text-gray-100">
                      {item.meaning_bn || item['কুরআনিক পরিভাষাগত অর্থ'] || item['মূল অর্থ'] || item['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র']}
                    </div>
                    {item.word_type && (
                      <span className="inline-block mt-1 px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-100 dark:bg-emerald-900/40 text-emerald-800 dark:text-emerald-300 font-arabic" dir="rtl">
                        {item.word_type}
                      </span>
                    )}
                  </td>

                  {/* Morphology: Sighah, Bahas, Bab */}
                  <td className="px-3.5 py-2.5 text-xs">
                    {(item['সীগা / ওযন'] || item['ব্যুৎপত্তি ও সিগাহ'] || item['কুরআনিক রূপ ও আবওয়াব']) ? (
                      <div className="font-arabic text-emerald-800 dark:text-emerald-300 font-semibold text-xs leading-relaxed" dir="rtl">
                        {item['সীগা / ওযন'] || item['ব্যুৎপত্তি ও সিগাহ'] || item['কুরআনিক রূপ ও আবওয়াব']}
                      </div>
                    ) : isVerb ? (
                      <div className="space-y-0.5">
                        <div className="font-arabic text-emerald-700 dark:text-emerald-300 font-semibold" dir="rtl">
                          {morph.sighah} • {morph.bahas}
                        </div>
                        <div className="text-gray-600 dark:text-gray-400">
                          বাব: <span className="font-arabic font-medium" dir="rtl">{morph.bab}</span>
                        </div>
                      </div>
                    ) : (
                      <div className="text-gray-600 dark:text-gray-400">
                        {morph.singular_plural ? (
                          <div className="font-arabic text-gray-700 dark:text-gray-300" dir="rtl">
                            {morph.singular_plural}
                          </div>
                        ) : (
                          <span className="italic text-gray-400">—</span>
                        )}
                      </div>
                    )}
                  </td>

                  {/* Root, Jins, Masdar */}
                  <td className="px-3.5 py-2.5 text-xs">
                    <div className="font-bold text-emerald-800 dark:text-emerald-300 font-arabic text-sm" dir="rtl">
                      {morph.root || item['মূলধাতু'] || '—'}
                    </div>
                    {morph.jins && (
                      <div className="text-gray-500 dark:text-gray-400 mt-0.5">
                        জিনস: <span className="font-arabic">{morph.jins}</span>
                      </div>
                    )}
                    {morph.masdar && (
                      <div className="text-gray-600 dark:text-gray-300 mt-0.5 font-arabic" dir="rtl">
                        {morph.masdar}
                      </div>
                    )}
                    {(item['কুরআনে মূলধাতুর মোট প্রয়োগ'] || item['কুরআনে পুনরাবৃত্তি (সূরা/কুরআন)']) && (
                      <div className="text-[10px] text-gray-500 dark:text-gray-400 mt-1 font-mono">
                        প্রয়োগ: {toBn(item['কুরআনে মূলধাতুর মোট প্রয়োগ'] || item['কুরআনে পুনরাবৃত্তি (সূরা/কুরআন)'])} বার
                      </div>
                    )}
                  </td>

                  {/* Taleel / Irab / Classical Notes */}
                  <td className="px-3.5 py-2.5 text-xs text-gray-600 dark:text-gray-300 max-w-xs">
                    {item.taleel_or_irab && (
                      <div className="leading-relaxed">
                        {item.taleel_or_irab}
                      </div>
                    )}
                    {item['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র'] && (
                      <div className="text-[11px] text-gray-600 dark:text-gray-300 leading-relaxed">
                        {item['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র']}
                      </div>
                    )}
                    {hasNotes && (
                      <div className="mt-1 pt-1 border-t border-gray-100 dark:border-gray-700/60 space-y-1">
                        {item.classical_notes.map((cn, cIdx) => (
                          <div key={cIdx} className="text-[11px] bg-amber-50/60 dark:bg-amber-950/20 p-1.5 rounded border border-amber-200/40 dark:border-amber-800/30">
                            <strong className="text-amber-800 dark:text-amber-400">{cn.scholar_or_book}:</strong>{' '}
                            <span>{cn.note}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* MOBILE VIEW: Mobile-First Card Grid (<768px) */}
      <div className="md:hidden space-y-2.5">
        {filteredWords.map((item, idx) => {
          const morph = item.morphology || {};
          const isVerb = item.word_type === 'فعل';
          const hasNotes = item.classical_notes && item.classical_notes.length > 0;
          const isExpanded = expandedWordIdx === idx;

          return (
            <div
              key={idx}
              className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-3 shadow-2xs space-y-2 font-bengali"
            >
              {/* Top Row: Arabic Word & Meaning */}
              <div className="flex items-start justify-between gap-2">
                <div>
                  <span className="font-arabic text-lg font-bold text-emerald-800 dark:text-emerald-300" dir="rtl">
                    {item.word || item['শব্দ'] || item['আরবি শব্দ']}
                  </span>
                  {item.word_type && (
                    <span className="ml-2 px-1.5 py-0.5 rounded text-[10px] font-medium bg-emerald-100 dark:bg-emerald-900/40 text-emerald-800 dark:text-emerald-300 font-arabic" dir="rtl">
                      {item.word_type}
                    </span>
                  )}
                  <p className="text-xs font-semibold text-gray-900 dark:text-gray-100 mt-0.5">
                    {item.meaning_bn || item['কুরআনিক পরিভাষাগত অর্থ'] || item['মূল অর্থ'] || item['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র']}
                  </p>
                </div>
                <span className="w-5 h-5 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-500 text-[10px] font-mono flex items-center justify-center shrink-0">
                  {toBn(idx + 1)}
                </span>
              </div>

              {/* Morphology Badges */}
              <div className="flex flex-wrap items-center gap-1.5 text-[11px]">
                {(morph.root || item['মূলধাতু']) && (
                  <span className="px-2 py-0.5 rounded-md bg-gray-100 dark:bg-gray-700 font-arabic font-semibold text-emerald-700 dark:text-emerald-300" dir="rtl">
                    মূলবর্ণ: {morph.root || item['মূলধাতু']}
                  </span>
                )}
                {(item['সীগা / ওযন'] || item['ব্যুৎপত্তি ও সিগাহ'] || item['কুরআনিক রূপ ও আবওয়াব']) && (
                  <span className="px-2 py-0.5 rounded-md bg-emerald-50 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300 font-arabic font-medium" dir="rtl">
                    {item['সীগা / ওযন'] || item['ব্যুৎপত্তি ও সিগাহ'] || item['কুরআনিক রূপ ও আবওয়াব']}
                  </span>
                )}
                {morph.bab && (
                  <span className="px-2 py-0.5 rounded-md bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                    বাব: <strong className="font-arabic">{morph.bab}</strong>
                  </span>
                )}
                {morph.jins && (
                  <span className="px-2 py-0.5 rounded-md bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                    জিনস: <strong className="font-arabic">{morph.jins}</strong>
                  </span>
                )}
                {(item['কুরআনে মূলধাতুর মোট প্রয়োগ'] || item['কুরআনে পুনরাবৃত্তি (সূরা/কুরআন)']) && (
                  <span className="px-2 py-0.5 rounded-md bg-gray-100 dark:bg-gray-700 text-gray-500 font-mono text-[10px]">
                    প্রয়োগ: {toBn(item['কুরআনে মূলধাতুর মোট প্রয়োগ'] || item['কুরআনে পুনরাবৃত্তি (সূরা/কুরআন)'])} বার
                  </span>
                )}
              </div>

              {/* Sighah / Bahas */}
              {isVerb && (
                <div className="text-xs bg-emerald-50/50 dark:bg-emerald-950/20 p-2 rounded-lg text-emerald-900 dark:text-emerald-200">
                  <div className="font-arabic font-semibold" dir="rtl">
                    {morph.sighah} • {morph.bahas}
                  </div>
                  {morph.masdar && (
                    <div className="text-[11px] text-gray-600 dark:text-gray-400 mt-0.5">
                      মাসদার: <span className="font-arabic font-medium">{morph.masdar}</span> ({morph.masdar_meaning})
                    </div>
                  )}
                </div>
              )}

              {/* Taleel & Classical Notes Toggle */}
              {(item.taleel_or_irab || item['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র'] || hasNotes) && (
                <div>
                  <button
                    onClick={() => setExpandedWordIdx(isExpanded ? null : idx)}
                    className="text-xs font-semibold text-emerald-700 dark:text-emerald-400 flex items-center gap-1 hover:underline"
                  >
                    <span>{isExpanded ? 'বিশদ ব্যাখ্যা সংক্ষেপ করুন' : 'ভাষাতাত্ত্বিক ও ক্লাসিক্যাল তথ্য দেখুন'}</span>
                    {isExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                  </button>

                  {isExpanded && (
                    <div className="mt-2 pt-2 border-t border-gray-100 dark:border-gray-700 text-xs space-y-1.5 text-gray-600 dark:text-gray-300">
                      {item.taleel_or_irab && (
                        <p className="leading-relaxed bg-gray-50 dark:bg-gray-700/40 p-2 rounded">
                          {item.taleel_or_irab}
                        </p>
                      )}
                      {item['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র'] && (
                        <div className="bg-gray-50 dark:bg-gray-700/40 p-2 rounded leading-relaxed text-[11px]">
                          <strong>ভাষাতাত্ত্বিক সূত্র:</strong> {item['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র']}
                        </div>
                      )}
                      {hasNotes && item.classical_notes.map((cn, cIdx) => (
                        <div key={cIdx} className="bg-amber-50/60 dark:bg-amber-950/20 p-2 rounded border border-amber-200/50 dark:border-amber-800/30 text-[11px]">
                          <strong className="text-amber-800 dark:text-amber-300">{cn.scholar_or_book}:</strong>{' '}
                          <span>{cn.note}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

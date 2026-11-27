import React, { useState, useMemo } from 'react';
import { Search, BookOpen, Sparkles, Filter, ChevronDown, ChevronUp, LayoutGrid, Table, BookMarked, CheckCircle2 } from 'lucide-react';
import MarkdownContent from './MarkdownContent';

export default function TahqeeqTable({ words = [], ayahNumber = null, compact = false }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all'); // 'all', 'فعل', 'اسم', 'حرف'
  const [viewLayout, setViewLayout] = useState('cards'); // 'cards' (Academic Cards - default) or 'table' (Compact Table)
  const [expandedWordIdx, setExpandedWordIdx] = useState(null);

  const cleanWord = (w) => (w || '').replace(/\*/g, '').replace(/«|»/g, '').trim();

  const filteredWords = useMemo(() => {
    if (!words || !Array.isArray(words)) return [];
    return words.filter(item => {
      const wText = cleanWord(item.word || item['শব্দ'] || item['আরবি শব্দ'] || '');
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
    <div className="space-y-4 layout-safe">
      {/* 1. Header & Controls Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-700">
        <div className="flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0" />
          <div>
            <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100 font-bengali flex items-center gap-2">
              <span>{ayahNumber ? `আয়াত ${toBn(ayahNumber)}-এর শাব্দিক তাহকীক` : 'শাব্দিক তাহকীক সারণি'}</span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-900/40 text-emerald-800 dark:text-emerald-300 font-bold font-mono">
                {toBn(filteredWords.length)}/{toBn(words.length)}টি শব্দ
              </span>
            </h4>
            <p className="text-[11px] text-gray-500 dark:text-gray-400 font-bengali">
              দারসে নেযামী ও মুকাম্মাল লুগাতুল কুরআনের মানদণ্ডে সরফী ও লুগাভী তাহকীক
            </p>
          </div>
        </div>

        {/* Action Controls: View Switcher & Search / Filter */}
        <div className="flex flex-wrap items-center gap-2">
          {/* View Mode Toggle: Cards vs Table */}
          <div className="flex items-center bg-gray-100 dark:bg-gray-700/60 p-1 rounded-xl text-xs font-semibold">
            <button
              onClick={() => setViewLayout('cards')}
              className={`flex items-center gap-1 px-2.5 py-1 rounded-lg transition-all ${
                viewLayout === 'cards'
                  ? 'bg-white dark:bg-gray-800 text-emerald-800 dark:text-emerald-300 shadow-2xs font-bold'
                  : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100'
              }`}
              title="একাডেমিক কার্ড ভিউ (পূর্বের বিস্তারিত ডিজাইন)"
            >
              <LayoutGrid className="w-3.5 h-3.5" />
              <span>কার্ড ভিউ</span>
            </button>
            <button
              onClick={() => setViewLayout('table')}
              className={`flex items-center gap-1 px-2.5 py-1 rounded-lg transition-all ${
                viewLayout === 'table'
                  ? 'bg-white dark:bg-gray-800 text-emerald-800 dark:text-emerald-300 shadow-2xs font-bold'
                  : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100'
              }`}
              title="সংক্ষিপ্ত সারণি ভিউ"
            >
              <Table className="w-3.5 h-3.5" />
              <span>সারণি</span>
            </button>
          </div>

          {/* Search Bar */}
          <div className="relative flex-1 sm:w-44">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="শব্দ, মূলবর্ণ বা অর্থ..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-8 pr-2.5 py-1 text-xs rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 font-bengali placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-emerald-500"
            />
          </div>

          {/* Word Type Filter */}
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="text-xs py-1 px-2 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 font-bengali focus:outline-none"
          >
            <option value="all">সকল প্রকার</option>
            <option value="فعل">فعل (ক্রিয়া)</option>
            <option value="اسم">اسم (বিশেষ্য)</option>
            <option value="حرف">حرف (অব্যয়)</option>
          </select>
        </div>
      </div>

      {/* 2. MAIN VIEW 1: DETAILED ACADEMIC CARDS (পূর্বের জনপ্রিয় ডিজাইন) */}
      {viewLayout === 'cards' && (
        <div className="space-y-4">
          {filteredWords.map((item, idx) => {
            const morph = item.morphology || {};
            const isVerb = item.word_type === 'فعل' || (item['সীগা / ওযন'] && item['সীগা / ওযন'].includes('فعل'));
            const wordDisplay = cleanWord(item.word || item['শব্দ'] || item['আরবি শব্দ']);
            const meaningDisplay = item.meaning_bn || item['কুরআনিক পরিভাষাগত অর্থ'] || item['মূল অর্থ'] || item['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র'];
            const rootDisplay = morph.root || item['মূলধাতু'] || '—';
            const babDisplay = morph.bab || item['কুরআনিক রূপ ও আবওয়াব'] || '—';
            const jinsDisplay = morph.jins || '—';
            const sighahParts = [morph.sighah, morph.bahas].filter(Boolean);
            const sighahDisplay = sighahParts.length > 0
              ? sighahParts.join(' • ')
              : (item['সীগা / ওযন'] || item['ব্যুৎপত্তি ও সিগাহ'] || morph.singular_plural || '—');
            const hasNotes = (item.classical_notes && item.classical_notes.length > 0) || item.taleel_or_irab || item['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র'];

            return (
              <div
                key={idx}
                className="bg-gray-50/90 dark:bg-gray-800/90 p-4 sm:p-5 rounded-2xl border border-gray-200 dark:border-gray-700/80 shadow-2xs space-y-3.5 transition-all hover:border-emerald-300 dark:hover:border-emerald-700 font-bengali"
              >
                {/* Card Top Bar: Big Arabic Word + Meaning + Type Badge + Serial */}
                <div className="flex flex-wrap items-center justify-between gap-2.5 pb-3 border-b border-gray-200/80 dark:border-gray-700">
                  <div className="flex items-center gap-3">
                    <span className="w-6 h-6 rounded-full bg-emerald-100 dark:bg-emerald-950/70 text-emerald-800 dark:text-emerald-300 text-xs font-bold font-mono flex items-center justify-center shrink-0">
                      {toBn(idx + 1)}
                    </span>
                    <span 
                      className="font-quran text-2xl sm:text-3xl font-bold text-emerald-900 dark:text-emerald-300 tracking-wide select-text" 
                      dir="rtl"
                    >
                      {wordDisplay}
                    </span>
                    {item.word_type && (
                      <span className="px-2 py-0.5 rounded-md text-[11px] font-bold bg-emerald-100 dark:bg-emerald-900/40 text-emerald-800 dark:text-emerald-300 font-arabic" dir="rtl">
                        {item.word_type}
                      </span>
                    )}
                    {item.prefix_suffix_note && (
                      <span className="text-xs text-gray-500 dark:text-gray-400 font-bengali">
                        ({item.prefix_suffix_note})
                      </span>
                    )}
                  </div>

                  <div className="font-bold text-gray-900 dark:text-gray-100 text-sm sm:text-base">
                    {meaningDisplay}
                  </div>
                </div>

                {/* Dars-e-Nizami Morphology 4-Box Grid */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs">
                  {/* Box 1: Root / মাদ্দাহ */}
                  <div className="bg-white dark:bg-gray-900/60 p-2.5 rounded-xl border border-gray-200/70 dark:border-gray-700/60 space-y-1">
                    <span className="text-[10px] text-gray-400 dark:text-gray-500 block font-bengali">
                      মূলবর্ণ (মাদ্দাহ):
                    </span>
                    <span className="font-bold text-emerald-800 dark:text-emerald-300 font-arabic text-sm block" dir="rtl">
                      {rootDisplay}
                    </span>
                  </div>

                  {/* Box 2: Jins / জিনস */}
                  <div className="bg-white dark:bg-gray-900/60 p-2.5 rounded-xl border border-gray-200/70 dark:border-gray-700/60 space-y-1">
                    <span className="text-[10px] text-gray-400 dark:text-gray-500 block font-bengali">
                      জিনস (সাত প্রকার):
                    </span>
                    <span className="font-semibold text-gray-800 dark:text-gray-200 font-arabic text-xs block" dir="rtl">
                      {jinsDisplay}
                    </span>
                  </div>

                  {/* Box 3: Bab / বাব */}
                  <div className="bg-white dark:bg-gray-900/60 p-2.5 rounded-xl border border-gray-200/70 dark:border-gray-700/60 space-y-1">
                    <span className="text-[10px] text-gray-400 dark:text-gray-500 block font-bengali">
                      বাব / আবওয়াব:
                    </span>
                    <span className="font-semibold text-gray-800 dark:text-gray-200 font-arabic text-xs block" dir="rtl">
                      {babDisplay}
                    </span>
                  </div>

                  {/* Box 4: Sighah & Bahas / ওযন */}
                  <div className="bg-white dark:bg-gray-900/60 p-2.5 rounded-xl border border-gray-200/70 dark:border-gray-700/60 space-y-1">
                    <span className="text-[10px] text-gray-400 dark:text-gray-500 block font-bengali">
                      সীগাহ ও বহছ / ওযন:
                    </span>
                    <span className="font-semibold text-emerald-700 dark:text-emerald-300 font-arabic text-xs block leading-relaxed" dir="rtl">
                      {sighahDisplay}
                    </span>
                  </div>
                </div>

                {/* Additional Row: Masdar & Quranic Frequency (if present) */}
                {(morph.masdar || item['কুরআনে মূলধাতুর মোট প্রয়োগ'] || item['কুরআনে পুনরাবৃত্তি (সূরা/কুরআন)']) && (
                  <div className="flex flex-wrap items-center gap-2 pt-1 text-xs">
                    {morph.masdar && (
                      <div className="px-2.5 py-1 rounded-lg bg-emerald-50/70 dark:bg-emerald-950/30 text-emerald-900 dark:text-emerald-200 border border-emerald-200/60 dark:border-emerald-800/40">
                        <span className="text-gray-500 dark:text-gray-400">মাসদার: </span>
                        <strong className="font-arabic font-bold">{morph.masdar}</strong>
                        {morph.masdar_meaning && <span className="ml-1 text-[11px]">({morph.masdar_meaning})</span>}
                      </div>
                    )}
                    {(item['কুরআনে মূলধাতুর মোট প্রয়োগ'] || item['কুরআনে পুনরাবৃত্তি (সূরা/কুরআন)']) && (
                      <div className="px-2.5 py-1 rounded-lg bg-gray-100 dark:bg-gray-700/60 text-gray-700 dark:text-gray-300 font-mono text-[11px]">
                        কুরআনে মোট প্রয়োগ: <strong>{toBn(item['কুরআনে মূলধাতুর মোট প্রয়োগ'] || item['কুরআনে পুনরাবৃত্তি (সূরা/কুরআন)'])}</strong> বার
                      </div>
                    )}
                  </div>
                )}

                {/* Taleel & Classical Scholarly Notes */}
                {hasNotes && (
                  <div className="pt-2 border-t border-gray-200/60 dark:border-gray-700/60 space-y-2 text-xs">
                    {item.taleel_or_irab && (
                      <div className="p-2.5 rounded-xl bg-white dark:bg-gray-900/50 border border-gray-200/70 dark:border-gray-700/60 leading-relaxed text-gray-700 dark:text-gray-300 bn-justify">
                        <strong className="text-emerald-800 dark:text-emerald-400 mr-1.5">তালীল / ইরাব:</strong>
                        <span>{item.taleel_or_irab}</span>
                      </div>
                    )}

                    {item['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র'] && (
                      <div className="p-2.5 rounded-xl bg-white dark:bg-gray-900/50 border border-gray-200/70 dark:border-gray-700/60 leading-relaxed text-gray-700 dark:text-gray-300 bn-justify">
                        <strong className="text-gray-800 dark:text-gray-200 mr-1.5">ভাষাতাত্ত্বিক সূত্র:</strong>
                        <span>{item['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র']}</span>
                      </div>
                    )}

                    {item.classical_notes && item.classical_notes.map((cn, cIdx) => (
                      <div key={cIdx} className="p-2.5 rounded-xl bg-amber-50/70 dark:bg-amber-950/20 border border-amber-200/50 dark:border-amber-800/30 text-[11px] leading-relaxed bn-justify">
                        <strong className="text-amber-900 dark:text-amber-300 font-bold mr-1.5">
                          {cn.scholar_or_book}:
                        </strong>
                        <span className="text-amber-950 dark:text-amber-200">{cn.note}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* 3. MAIN VIEW 2: COMPACT STRUCTURED TABLE (সারণি ভিউ) */}
      {viewLayout === 'table' && (
        <div className="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700 shadow-2xs">
          <table className="w-full text-left text-xs sm:text-sm border-collapse">
            <thead className="bg-emerald-50/80 dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-b border-gray-200 dark:border-gray-700 font-bengali">
              <tr>
                <th className="px-3 py-2.5 font-bold text-center w-12">ক্রম</th>
                <th className="px-3.5 py-2.5 font-bold text-right font-arabic">শব্দ (কুরআনিক পাঠ)</th>
                <th className="px-3.5 py-2.5 font-bold">বাংলা অর্থ ও প্রকার</th>
                <th className="px-3.5 py-2.5 font-bold">সরফ: সীগাহ, বহছ ও বাব</th>
                <th className="px-3.5 py-2.5 font-bold">মূলবর্ণ, জিনস ও মাসদার</th>
                <th className="px-3.5 py-2.5 font-bold">তালীল / ইরাব ও তথ্যসূত্র</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 dark:divide-gray-700/60 bg-white dark:bg-gray-800 font-bengali">
              {filteredWords.map((item, idx) => {
                const morph = item.morphology || {};
                const isVerb = item.word_type === 'فعل';
                const wordDisplay = cleanWord(item.word || item['শব্দ'] || item['আরবি শব্দ']);
                const meaningDisplay = item.meaning_bn || item['কুরআনিক পরিভাষাগত অর্থ'] || item['মূল অর্থ'] || item['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র'];
                const rootDisplay = morph.root || item['মূলধাতু'] || '—';
                const babDisplay = morph.bab || item['কুরআনিক রূপ ও আবওয়াব'] || '';
                const tableSighahParts = [morph.sighah, morph.bahas].filter(Boolean);
                const sighahDisplay = tableSighahParts.length > 0
                  ? tableSighahParts.join(' • ')
                  : (item['সীগা / ওযন'] || item['ব্যুৎপত্তি ও সিগাহ'] || morph.singular_plural || '—');

                return (
                  <tr key={idx} className="hover:bg-emerald-50/30 dark:hover:bg-gray-700/30 transition-colors">
                    <td className="px-3 py-2.5 text-center font-mono text-gray-400 dark:text-gray-500 font-bold">
                      {toBn(idx + 1)}
                    </td>

                    <td className="px-3.5 py-2.5 text-right font-arabic text-base sm:text-lg font-bold text-emerald-800 dark:text-emerald-300 whitespace-nowrap" dir="rtl">
                      <span className="font-arabic leading-relaxed" dir="rtl">
                        {wordDisplay}
                      </span>
                    </td>

                    <td className="px-3.5 py-2.5">
                      <div className="font-semibold text-gray-900 dark:text-gray-100">
                        {meaningDisplay}
                      </div>
                      {item.word_type && (
                        <span className="inline-block mt-1 px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-100 dark:bg-emerald-900/40 text-emerald-800 dark:text-emerald-300 font-arabic" dir="rtl">
                          {item.word_type}
                        </span>
                      )}
                    </td>

                    <td className="px-3.5 py-2.5 text-xs">
                      <div className="font-arabic text-emerald-800 dark:text-emerald-300 font-semibold text-xs leading-relaxed" dir="rtl">
                        {sighahDisplay}
                      </div>
                      {babDisplay && (
                        <div className="text-gray-600 dark:text-gray-400 mt-0.5">
                          বাব: <span className="font-arabic font-medium">{babDisplay}</span>
                        </div>
                      )}
                    </td>

                    <td className="px-3.5 py-2.5 text-xs">
                      <div className="font-bold text-emerald-800 dark:text-emerald-300 font-arabic text-sm" dir="rtl">
                        {rootDisplay}
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
                    </td>

                    <td className="px-3.5 py-2.5 text-xs text-gray-600 dark:text-gray-300 max-w-xs leading-relaxed">
                      {item.taleel_or_irab || item['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র'] || '—'}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

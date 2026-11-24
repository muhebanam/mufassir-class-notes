import React, { useState, useMemo } from 'react';
import { 
  Languages, LayoutGrid, Table, Copy, Check, Sparkles, 
  Eye, Info, ChevronRight, Palette
} from 'lucide-react';
import { parseWordByWord } from '../utils/wordByWordParser';
import WordInspectorModal from './WordInspectorModal';

export default function WordByWordSection({
  ayah,
  arabicFontSize = 28,
  bengaliFontSize = 16,
  arabicLineHeight = 2.2
}) {
  const [viewMode, setViewMode] = useState('tiles'); // 'tiles' or 'table'
  const [showPosColors, setShowPosColors] = useState(false);
  const [selectedWord, setSelectedWord] = useState(null);
  const [copied, setCopied] = useState(false);

  // Parse word-by-word data safely via our central adapter
  const parsedData = useMemo(() => {
    return parseWordByWord(ayah);
  }, [ayah?.word_translation, ayah?.tahqeeq, ayah?.mufradat, ayah?.ayah]);

  const toBn = (num) => {
    const bn = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
    return String(num).replace(/[0-9]/g, d => bn[d]);
  };

  const handleCopy = () => {
    if (!parsedData.words || parsedData.words.length === 0) return;
    const formatted = parsedData.words
      .map(w => `[${w.arabic}: ${w.meaning_bn}]`)
      .join(' ');
    const fullText = `${formatted}\n(সূরা ${ayah?.surah || ''}, আয়াত ${ayah?.ayah || ''} — শব্দানুগ অনুবাদ)`;

    navigator.clipboard.writeText(fullText).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  if (!parsedData.isAvailable || parsedData.words.length === 0) {
    return (
      <div className="p-4 rounded-2xl bg-gray-50/70 dark:bg-gray-800/60 border border-gray-200/70 dark:border-gray-700 text-center font-bengali text-xs text-gray-500 dark:text-gray-400 space-y-1">
        <p className="font-semibold text-gray-700 dark:text-gray-300">
          এই আয়াতের পূর্ণাঙ্গ বঙ্গানুবাদ উপরে প্রদর্শিত হয়েছে।
        </p>
        <p className="text-[11px] text-gray-400">
          শব্দে শব্দে ইন্টারলিনিয়ার ম্যাপিং পরবর্তী সংস্করণে ক্রমান্বয়ে যুক্ত হবে।
        </p>
      </div>
    );
  }

  const words = parsedData.words;

  // Helper for POS color coding
  const getPosClasses = (pos) => {
    if (!showPosColors || !pos) {
      return 'border-gray-200/80 dark:border-gray-700/80 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 hover:border-emerald-400 dark:hover:border-emerald-500';
    }
    if (pos === 'فعل') {
      return 'border-emerald-300 dark:border-emerald-700 bg-emerald-50/60 dark:bg-emerald-950/30 text-emerald-950 dark:text-emerald-100 hover:border-emerald-500 ring-1 ring-emerald-400/20';
    }
    if (pos === 'اسم') {
      return 'border-blue-300 dark:border-blue-700 bg-blue-50/60 dark:bg-blue-950/30 text-blue-950 dark:text-blue-100 hover:border-blue-500 ring-1 ring-blue-400/20';
    }
    if (pos === 'حرف') {
      return 'border-amber-300 dark:border-amber-700 bg-amber-50/60 dark:bg-amber-950/30 text-amber-950 dark:text-amber-100 hover:border-amber-500 ring-1 ring-amber-400/20';
    }
    return 'border-gray-200/80 dark:border-gray-700/80 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100';
  };

  return (
    <div className="bg-gradient-to-br from-white via-emerald-50/20 to-teal-50/20 dark:from-gray-800 dark:via-gray-800/90 dark:to-gray-850 rounded-2xl sm:rounded-3xl border border-emerald-200/60 dark:border-gray-700 p-4 sm:p-5 shadow-xs space-y-4 layout-safe">
      {/* 1. Header Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-2.5 pb-3 border-b border-gray-100 dark:border-gray-700/80 font-bengali">
        {/* Title and Count */}
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-emerald-100 dark:bg-emerald-900/50 flex items-center justify-center text-emerald-700 dark:text-emerald-300">
            <Languages className="w-4 h-4" />
          </div>
          <div>
            <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100">
              শব্দানুগ অনুবাদ (শব্দে শব্দে অর্থ)
            </h4>
            <span className="text-[11px] text-gray-500 dark:text-gray-400 font-mono">
              মোট {toBn(words.length)}টি শব্দ • শব্দে ক্লিক করে বিস্তারিত তাহকীক দেখুন
            </span>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-1.5 sm:gap-2">
          {/* POS Color Toggle */}
          <button
            onClick={() => setShowPosColors(!showPosColors)}
            className={`flex items-center gap-1 px-2.5 py-1 rounded-xl text-xs font-semibold border transition ${
              showPosColors
                ? 'bg-emerald-100 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-300 border-emerald-300 dark:border-emerald-700'
                : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 border-gray-200 dark:border-gray-700 hover:bg-gray-50'
            }`}
            title="ব্যাকরণগত পদ রঙীন করুন (اسم / فعل / حرف)"
          >
            <Palette className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">ব্যাকরণ রং</span>
          </button>

          {/* Dual View Switcher (Tiles vs Table) */}
          <div className="flex items-center bg-gray-100 dark:bg-gray-700/70 p-0.5 rounded-xl border border-gray-200/60 dark:border-gray-600">
            <button
              onClick={() => setViewMode('tiles')}
              className={`p-1.5 rounded-lg text-xs font-semibold transition ${
                viewMode === 'tiles'
                  ? 'bg-white dark:bg-gray-800 text-emerald-700 dark:text-emerald-300 shadow-2xs'
                  : 'text-gray-500 dark:text-gray-400 hover:text-gray-900'
              }`}
              title="টাইল ভিউ (Interlinear Tiles)"
            >
              <LayoutGrid className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => setViewMode('table')}
              className={`p-1.5 rounded-lg text-xs font-semibold transition ${
                viewMode === 'table'
                  ? 'bg-white dark:bg-gray-800 text-emerald-700 dark:text-emerald-300 shadow-2xs'
                  : 'text-gray-500 dark:text-gray-400 hover:text-gray-900'
              }`}
              title="ছক / টেবিল ভিউ (Structured Table)"
            >
              <Table className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Copy Button */}
          <button
            onClick={handleCopy}
            className="flex items-center gap-1 px-2.5 py-1 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 text-xs font-semibold text-gray-700 dark:text-gray-300 transition"
            title="সম্পূর্ণ শব্দানুগ অনুবাদ কপি করুন"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
            <span className="hidden sm:inline">{copied ? 'কপি হয়েছে' : 'কপি'}</span>
          </button>
        </div>
      </div>

      {/* POS Color Legend (Visible only when color coding is on) */}
      {showPosColors && (
        <div className="flex flex-wrap items-center gap-3 text-xs font-bengali px-1 text-gray-600 dark:text-gray-300">
          <span className="font-semibold text-gray-400">পদের নির্দেশিকা:</span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
            <span>ক্রিয়া (فعل)</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-500" />
            <span>বিশেষ্য (اسم)</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500" />
            <span>অব্যয় (حرف)</span>
          </span>
        </div>
      )}

      {/* 2. MODE A: Interlinear Word Tiles (dir="rtl") */}
      {viewMode === 'tiles' ? (
        <div className="flex flex-wrap items-stretch gap-2.5 sm:gap-3" dir="rtl">
          {words.map((w) => {
            const posClass = getPosClasses(w.pos);
            const isSelected = selectedWord?.id === w.id;

            return (
              <div
                key={w.id}
                onClick={() => setSelectedWord(w)}
                className={`group relative flex flex-col items-center justify-between p-2.5 sm:p-3 rounded-2xl border transition-all duration-150 cursor-pointer select-none min-w-[70px] sm:min-w-[85px] max-w-[170px] shadow-2xs hover:shadow-sm hover:-translate-y-0.5 ${posClass} ${
                  isSelected ? 'ring-2 ring-emerald-500 dark:ring-emerald-400 border-emerald-500' : ''
                }`}
                title={w.hasDeepTahqeeq ? "ক্লিক করে বিস্তারিত তাহকীক দেখুন" : "ক্লিক করে শব্দার্থ দেখুন"}
              >
                {/* Academic Tahqeeq Indicator Dot */}
                {w.hasDeepTahqeeq && (
                  <span 
                    className="absolute top-1.5 right-1.5 w-1.5 h-1.5 rounded-full bg-emerald-500 dark:bg-emerald-400 ring-2 ring-white dark:ring-gray-800" 
                    title="গভীর তাহকীক উপলব্ধ"
                  />
                )}

                {/* Top: Arabic Word */}
                <div 
                  className="font-quran font-bold text-center leading-relaxed text-emerald-900 dark:text-emerald-200 group-hover:text-emerald-700 dark:group-hover:text-emerald-300 transition-colors"
                  dir="rtl"
                  style={{ 
                    fontSize: `${Math.max(18, arabicFontSize - 6)}px`,
                    lineHeight: 2.1
                  }}
                >
                  {w.arabic}
                </div>

                {/* Bottom: Bengali Meaning */}
                <div 
                  className="font-bengali text-center leading-snug break-words pt-1.5 border-t border-gray-100 dark:border-gray-700/60 w-full text-gray-700 dark:text-gray-300 font-medium"
                  dir="ltr"
                  style={{ fontSize: `${Math.max(11, bengaliFontSize - 3)}px` }}
                >
                  {w.meaning_bn}
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        /* 3. MODE B: Structured Table View */
        <div className="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700 shadow-2xs">
          <table className="w-full text-left text-xs sm:text-sm border-collapse font-bengali">
            <thead className="bg-emerald-50/70 dark:bg-gray-800/90 text-gray-700 dark:text-gray-300 border-b border-gray-200 dark:border-gray-700">
              <tr>
                <th className="px-3 py-2.5 text-center font-bold w-12">ক্রম</th>
                <th className="px-3.5 py-2.5 text-right font-bold w-36 font-arabic">আরবি শব্দ</th>
                <th className="px-3.5 py-2.5 font-bold">শব্দানুগ বাংলা অর্থ</th>
                <th className="px-3.5 py-2.5 font-bold w-28">পদ / মূলবর্ণ</th>
                <th className="px-3 py-2.5 text-center font-bold w-20">তাহকীক</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 dark:divide-gray-700/60 bg-white dark:bg-gray-800">
              {words.map((w) => (
                <tr 
                  key={w.id} 
                  onClick={() => setSelectedWord(w)}
                  className="hover:bg-emerald-50/40 dark:hover:bg-gray-700/30 transition-colors cursor-pointer"
                >
                  <td className="px-3 py-2.5 text-center font-mono text-gray-400 font-bold">
                    {toBn(w.id)}
                  </td>
                  <td className="px-3.5 py-2.5 text-right font-arabic font-bold text-base text-emerald-800 dark:text-emerald-300 whitespace-nowrap table-cell-arabic" dir="rtl">
                    {w.arabic}
                  </td>
                  <td className="px-3.5 py-2.5 font-medium text-gray-800 dark:text-gray-200">
                    {w.meaning_bn}
                  </td>
                  <td className="px-3.5 py-2.5 text-xs text-gray-500 dark:text-gray-400">
                    {w.pos && (
                      <span className="font-arabic font-medium block" dir="rtl">
                        {w.pos}
                      </span>
                    )}
                    {w.root && (
                      <span className="font-arabic text-emerald-700 dark:text-emerald-400 block font-semibold" dir="rtl">
                        {w.root}
                      </span>
                    )}
                    {!w.pos && !w.root && <span className="text-gray-400">—</span>}
                  </td>
                  <td className="px-3 py-2.5 text-center">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setSelectedWord(w);
                      }}
                      className="px-2 py-1 rounded-lg bg-emerald-100 dark:bg-emerald-900/50 text-emerald-800 dark:text-emerald-300 hover:bg-emerald-200 text-xs font-semibold transition"
                    >
                      বিশ্লেষণ
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* 4. Click-to-Tahqeeq Word Inspector Modal */}
      {selectedWord && (
        <WordInspectorModal
          word={selectedWord}
          ayahNumber={ayah?.ayah}
          onClose={() => setSelectedWord(null)}
        />
      )}
    </div>
  );
}

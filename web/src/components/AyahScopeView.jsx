import React, { useState, useEffect } from 'react';
import { 
  BookOpen, ChevronLeft, ChevronRight, Copy, Check, 
  Columns, AlignLeft, Volume2, Sparkles, Scale, Maximize2, Minimize2,
  Bookmark, Share2, Languages
} from 'lucide-react';
import MarkdownContent, { normalizeQuranBrackets } from './MarkdownContent';
import TahqeeqTable from './TahqeeqTable';
import QiraatTable from './QiraatTable';

export default function AyahScopeView({
  ayah,
  surahInfo,
  rukuInfo,
  onPrevAyah,
  onNextAyah,
  onSelectAyah,
  arabicFontSize = 28,
  bengaliFontSize = 16,
  arabicLineHeight = 2.2,
  splitView = true,
  onToggleSplitView
}) {
  const [copied, setCopied] = useState(false);

  // Reset local state whenever ayah changes
  useEffect(() => {
    setCopied(false);
  }, [ayah?.surah, ayah?.ruku, ayah?.ayah]);

  const toBn = (num) => {
    const bn = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
    return String(num).replace(/[0-9]/g, d => bn[d]);
  };

  // Zero Data Leakage Validation Guard
  if (!ayah || !rukuInfo) {
    return (
      <div className="max-w-4xl mx-auto py-16 text-center space-y-3 font-bengali">
        <div className="w-8 h-8 border-3 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
        <p className="text-gray-500 text-sm">আয়াত ডাটা লোড হচ্ছে...</p>
      </div>
    );
  }

  // Guard: Confirm ayah belongs to current ruku
  if (ayah.ayah < rukuInfo.ayah_start || ayah.ayah > rukuInfo.ayah_end) {
    return (
      <div className="max-w-2xl mx-auto my-12 p-6 rounded-2xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800 text-center font-bengali">
        <p className="text-amber-800 dark:text-amber-300 font-semibold text-sm">
          আয়াত {toBn(ayah.ayah)} বর্তমান রুকু {toBn(rukuInfo.ruku_id)}-এর সীমার ({toBn(rukuInfo.ayah_start)}–{toBn(rukuInfo.ayah_end)}) অন্তর্ভুক্ত নয়।
        </p>
        <button
          onClick={() => onSelectAyah && onSelectAyah(rukuInfo.ayah_start)}
          className="mt-3 px-4 py-2 rounded-xl bg-emerald-600 text-white text-xs font-bold"
        >
          রুকুর প্রথম আয়াতে ফিরে যান
        </button>
      </div>
    );
  }

  const handleCopyAyah = () => {
    const copyText = `${ayah.text_uthmani}\n\nঅনুবাদ: ${ayah.translation}\n(সূরা ${surahInfo?.name_bn || 'আন-নূর'}, আয়াত ${ayah.ayah})`;
    navigator.clipboard.writeText(copyText).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  const tahqeeqWords = ayah.tahqeeq || ayah.mufradat || [];
  const qiraatList = ayah.qiraat || [];

  const hasPrev = ayah.ayah > (rukuInfo.ayah_start || 1);
  const hasNext = ayah.ayah < (rukuInfo.ayah_end || 64);

  return (
    <div 
      key={`${ayah.surah}-${ayah.ruku}-${ayah.ayah}`} 
      className="w-full max-w-6xl mx-auto px-3 sm:px-6 py-4 sm:py-6 space-y-5 sm:space-y-6 layout-safe"
    >
      {/* 1. Ayah Action & Navigation Top Bar */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-3 sm:p-4 shadow-2xs flex flex-wrap items-center justify-between gap-3">
        {/* Breadcrumb info */}
        <div className="flex items-center gap-2 text-xs sm:text-sm font-bengali">
          <span className="font-bold text-gray-900 dark:text-gray-100">
            সূরা {surahInfo?.name_bn || 'আন-নূর'}
          </span>
          <span className="text-gray-400">•</span>
          <span className="text-gray-600 dark:text-gray-300">
            রুকু {toBn(rukuInfo.ruku_id)}
          </span>
          <span className="text-gray-400">•</span>
          <span className="px-2.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-900/40 text-emerald-800 dark:text-emerald-300 font-bold font-mono">
            আয়াত {toBn(ayah.ayah)}
          </span>
        </div>

        {/* Action Controls & Prev/Next */}
        <div className="flex items-center gap-2">
          {/* Split view toggle (desktop only) */}
          <button
            onClick={onToggleSplitView}
            title={splitView ? "স্ট্যাকড ভিউতে পরিবর্তন করুন" : "স্প্লিট ভিউতে পরিবর্তন করুন"}
            className="hidden lg:flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700 text-xs font-bengali text-gray-700 dark:text-gray-300 transition"
          >
            <Columns className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            <span>{splitView ? 'ডুয়াল স্প্লিট' : 'একক কলাম'}</span>
          </button>

          {/* Copy Ayah */}
          <button
            onClick={handleCopyAyah}
            title="আয়াত ও অনুবাদ কপি করুন"
            className="p-2 rounded-xl border border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-300 transition"
          >
            {copied ? <Check className="w-4 h-4 text-emerald-600" /> : <Copy className="w-4 h-4" />}
          </button>

          {/* Prev Ayah */}
          <button
            onClick={onPrevAyah}
            disabled={!hasPrev}
            className={`p-2 rounded-xl border flex items-center justify-center transition ${
              hasPrev 
                ? 'border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700' 
                : 'border-gray-100 dark:border-gray-800 text-gray-300 dark:text-gray-600 cursor-not-allowed'
            }`}
            title="পূর্ববর্তী আয়াত"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>

          {/* Next Ayah */}
          <button
            onClick={onNextAyah}
            disabled={!hasNext}
            className={`p-2 rounded-xl border flex items-center justify-center transition ${
              hasNext 
                ? 'border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700' 
                : 'border-gray-100 dark:border-gray-800 text-gray-300 dark:text-gray-600 cursor-not-allowed'
            }`}
            title="পরবর্তী আয়াত"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* 2. Main Ayah Display Block (Uthmani Text + বঙ্গানুবাদ + শব্দানুগ অনুবাদ সেকশন) */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl sm:rounded-3xl border border-gray-200 dark:border-gray-700 p-5 sm:p-7 shadow-xs space-y-5">
        {/* Arabic Ayah with End Symbol */}
        <div 
          className="uthmani-text leading-loose text-right font-quran select-text" 
          dir="rtl"
          style={{ 
            fontSize: `${arabicFontSize}px`,
            lineHeight: `${arabicLineHeight}`
          }}
        >
          <span>{ayah.text_uthmani}</span>
          <span className="ayah-end-symbol text-emerald-700 dark:text-emerald-400 font-mono text-2xl mx-1.5" dir="rtl">
            ۝{toBn(ayah.ayah)}
          </span>
        </div>

        {/* Simple Ayah Text if available */}
        {ayah.text_simple && (
          <div className="text-right font-arabic text-sm text-gray-500 dark:text-gray-400 pt-2 border-t border-gray-100 dark:border-gray-700/60" dir="rtl">
            {ayah.text_simple}
          </div>
        )}

        {/* সহজি ও প্রামাণিক বঙ্গানুবাদ (Fluent Bengali Translation) */}
        <div className="bg-emerald-50/50 dark:bg-emerald-950/20 p-4 rounded-xl border border-emerald-100 dark:border-emerald-900/40 text-gray-900 dark:text-gray-100 font-bengali leading-relaxed">
          <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-800 dark:text-emerald-400 mb-1">
            <AlignLeft className="w-3.5 h-3.5" />
            <span>সহজ ও প্রামাণিক বঙ্গানুবাদ:</span>
          </div>
          <div className="text-sm sm:text-base font-medium">
            <span className="text-emerald-700 dark:text-emerald-400 font-bold mr-1.5">({toBn(ayah.ayah)})</span>
            {ayah.translation || "অনুবাদ প্রস্তুত করা হচ্ছে..."}
          </div>
        </div>

        {/* শব্দানুগ অনুবাদ সেকশন (Word-by-Word Translation Section) */}
        {ayah.word_translation && (
          <div className="bg-gradient-to-r from-amber-50/60 via-emerald-50/40 to-teal-50/60 dark:from-gray-800 dark:via-gray-800/90 dark:to-gray-850 p-4 sm:p-5 rounded-2xl border border-amber-200/60 dark:border-amber-800/40 space-y-3 font-bengali shadow-2xs">
            <div className="flex items-center justify-between gap-2 pb-2 border-b border-amber-200/50 dark:border-gray-700">
              <div className="flex items-center gap-2">
                <Languages className="w-4 h-4 text-amber-700 dark:text-amber-400" />
                <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100">
                  শব্দানুগ অনুবাদ (শব্দে শব্দে অর্থ)
                </h4>
              </div>
              <span className="text-[11px] font-semibold text-amber-800 dark:text-amber-300 bg-amber-100/70 dark:bg-amber-950/60 px-2.5 py-0.5 rounded-full border border-amber-200/80 dark:border-amber-800/60 font-mono">
                {toBn(tahqeeqWords.length || 0)}টি শব্দ
              </span>
            </div>

            {/* Word by word formatted markdown text */}
            <div className="text-xs sm:text-sm text-gray-800 dark:text-gray-200 leading-loose">
              <MarkdownContent content={ayah.word_translation} />
            </div>

            {/* Interactive Word Chips (Quick Word-Meaning Badges) */}
            {tahqeeqWords && tahqeeqWords.length > 0 && (
              <div className="pt-2 border-t border-amber-200/40 dark:border-gray-700/60">
                <span className="text-[11px] font-semibold text-gray-500 dark:text-gray-400 block mb-2">
                  প্রতিটি শব্দের সরাসরি অর্থ-কার্ড:
                </span>
                <div className="flex flex-wrap gap-2">
                  {tahqeeqWords.map((w, idx) => {
                    const arabicWord = w.word || w['শব্দ'] || '';
                    const meaningText = w.meaning_bn || w['কুরআনিক পরিভাষাগত অর্থ'] || w['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র'] || '';

                    return (
                      <div 
                        key={idx} 
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white dark:bg-gray-750 border border-emerald-200/80 dark:border-emerald-700/60 shadow-2xs text-xs"
                      >
                        <span className="font-arabic font-bold text-emerald-800 dark:text-emerald-300 text-sm sm:text-base" dir="rtl">
                          {arabicWord}
                        </span>
                        <span className="text-gray-400 text-xs">→</span>
                        <span className="font-medium text-gray-800 dark:text-gray-200">
                          {meaningText}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* 3. Detailed Academic Layer (Split View on Desktop or Stacked View) */}
      <div className={`grid gap-4 sm:gap-6 ${splitView ? 'lg:grid-cols-12' : 'grid-cols-1'}`}>
        {/* Left Column: Jalalayn Commentary & Matin */}
        <div className={`space-y-4 ${splitView ? 'lg:col-span-6' : ''}`}>
          {/* Jalalayn Card */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-5 sm:p-6 shadow-xs space-y-3">
            <div className="flex items-center justify-between pb-2.5 border-b border-gray-100 dark:border-gray-700">
              <div className="flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                <h3 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100 font-bengali">
                  তাফসীরুল জালালাইন (মতন ও ব্যাখ্যা)
                </h3>
              </div>
              <span className="text-[11px] font-semibold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 px-2 py-0.5 rounded-full font-bengali">
                ইমাম জালালুদ্দীন আল-মাহাল্লী ও আস-সুয়ূতী
              </span>
            </div>

            <div 
              className="prose font-bengali leading-relaxed text-gray-800 dark:text-gray-200"
              style={{ fontSize: `${bengaliFontSize}px` }}
            >
              <MarkdownContent content={ayah.jalalayn} />
            </div>
          </div>

          {/* Shan-e-Nuzul if exists */}
          {ayah.shane_nuzul && (
            <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5 shadow-xs space-y-2 font-bengali">
              <div className="flex items-center gap-2 pb-2 border-b border-gray-100 dark:border-gray-700 text-teal-800 dark:text-teal-300 font-bold text-sm">
                <Bookmark className="w-4 h-4 text-teal-600" />
                <span>শানে নুযূল ও সংশ্লিষ্ট হাদীসের তাখরীজ</span>
              </div>
              <div className="prose text-xs sm:text-sm leading-relaxed text-gray-700 dark:text-gray-300">
                <MarkdownContent content={ayah.shane_nuzul} />
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Comprehensive Tahqeeq Table & Qiraat */}
        <div className={`space-y-4 ${splitView ? 'lg:col-span-6' : ''}`}>
          {/* Tahqeeq Table Card */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5 shadow-xs">
            <TahqeeqTable 
              words={tahqeeqWords} 
              ayahNumber={ayah.ayah} 
            />
          </div>

          {/* Qiraat Table if exists */}
          {qiraatList.length > 0 && (
            <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5 shadow-xs">
              <QiraatTable 
                tableData={qiraatList} 
                title={`আয়াত ${toBn(ayah.ayah)}-এর ১০ কিরাআত পাঠভেদ`}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

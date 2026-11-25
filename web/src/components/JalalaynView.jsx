import React, { useState } from 'react';
import { BookOpen, Layers, Eye, BookMarked, Sparkles } from 'lucide-react';
import MarkdownContent, { normalizeQuranBrackets } from './MarkdownContent';
import { parseJalalayn } from '../utils/tafsirTakhrijAdapter';

export default function JalalaynView({ 
  ayah, 
  bengaliFontSize = 16, 
  arabicFontSize = 26 
}) {
  // View Modes: 'combined' (all layers), 'ayah_only' (Quran text), 'jalalayn_only' (sharh only)
  const [viewMode, setViewMode] = useState('combined');

  const parsed = parseJalalayn(ayah?.jalalayn, ayah?.text_uthmani);

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-6 shadow-xs space-y-4 font-bengali transition-colors">
      {/* 1. Header Bar with Scholar Badge & View Mode Switcher */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-700/80">
        <div className="flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
          <div>
            <h3 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100">
              তাফসীরুল জালালাইন (মতন ও ব্যাখ্যা)
            </h3>
            <span className="text-[11px] font-semibold text-emerald-700 dark:text-emerald-400">
              {parsed.scholar}
            </span>
          </div>
        </div>

        {/* View Mode Switcher */}
        <div className="flex items-center gap-1 bg-gray-100 dark:bg-gray-700/60 p-1 rounded-xl text-xs font-semibold self-start sm:self-center">
          <button
            onClick={() => setViewMode('combined')}
            className={`px-2.5 py-1 rounded-lg transition-all ${
              viewMode === 'combined'
                ? 'bg-white dark:bg-gray-800 text-emerald-800 dark:text-emerald-300 shadow-2xs font-bold'
                : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100'
            }`}
            title="মূল আয়াত, আরবি ইবারত ও বাংলা ব্যাখ্যা সমন্বিত"
          >
            সমন্বিত ভিউ
          </button>
          <button
            onClick={() => setViewMode('ayah_only')}
            className={`px-2.5 py-1 rounded-lg transition-all ${
              viewMode === 'ayah_only'
                ? 'bg-white dark:bg-gray-800 text-emerald-800 dark:text-emerald-300 shadow-2xs font-bold'
                : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100'
            }`}
            title="শুধু কুরআনের মূল আয়াত"
          >
            শুধু আয়াত
          </button>
          <button
            onClick={() => setViewMode('jalalayn_only')}
            className={`px-2.5 py-1 rounded-lg transition-all ${
              viewMode === 'jalalayn_only'
                ? 'bg-white dark:bg-gray-800 text-emerald-800 dark:text-emerald-300 shadow-2xs font-bold'
                : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100'
            }`}
            title="শুধু জালালাইন ইবারত ও ব্যাখ্যা"
          >
            শুধু জালালাইন
          </button>
        </div>
      </div>

      {/* 2. Layer 1: Quranic Verse Matn (when in 'combined' or 'ayah_only' mode) */}
      {(viewMode === 'combined' || viewMode === 'ayah_only') && (
        <div className="p-4 rounded-xl bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-100 dark:border-emerald-800/40 space-y-2">
          <div className="flex items-center justify-between text-xs text-emerald-800 dark:text-emerald-300 font-semibold">
            <span className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
              <span>কুরআনের মূল আয়াত (متن القرآن)</span>
            </span>
            <span className="font-mono text-emerald-700 dark:text-emerald-400">
              {ayah?.ayah ? `আয়াত নং ${ayah.ayah}` : ''}
            </span>
          </div>

          <div 
            className="font-quran text-right leading-[2.2] text-gray-900 dark:text-gray-100 select-text"
            dir="rtl"
            style={{ fontSize: `${arabicFontSize}px` }}
          >
            {normalizeQuranBrackets(ayah?.text_uthmani || ayah?.text_simple || '')}
          </div>

          {ayah?.translation && (
            <div className="pt-2 text-xs sm:text-sm text-gray-700 dark:text-gray-300 border-t border-emerald-100/60 dark:border-emerald-900/40 font-bengali leading-relaxed">
              <span className="font-semibold text-emerald-800 dark:text-emerald-400">অনুবাদ: </span>
              {ayah.translation}
            </div>
          )}
        </div>
      )}

      {/* 3. Layer 2: Jalalayn Arabic Keywords & Terminology Chips */}
      {(viewMode === 'combined' || viewMode === 'jalalayn_only') && parsed.arabicTerms.length > 0 && (
        <div className="flex flex-wrap items-center gap-2 p-2.5 rounded-xl bg-amber-50/50 dark:bg-amber-950/20 border border-amber-200/60 dark:border-amber-800/40">
          <span className="text-xs font-bold text-amber-900 dark:text-amber-300 flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
            <span>জালালাইনে আলোচিত মূল আরবি শব্দাবলি:</span>
          </span>
          <div className="flex flex-wrap gap-1.5" dir="rtl">
            {parsed.arabicTerms.map((term, tIdx) => (
              <span 
                key={tIdx}
                className="font-arabic font-bold text-sm px-2.5 py-0.5 rounded-lg bg-white dark:bg-gray-800 text-amber-900 dark:text-amber-200 border border-amber-200 dark:border-amber-700 shadow-2xs"
                dir="rtl"
              >
                «{term}»
              </span>
            ))}
          </div>
        </div>
      )}

      {/* 4. Layer 3: Jalalayn Bengali Explanation & Sharh */}
      {(viewMode === 'combined' || viewMode === 'jalalayn_only') && (
        <div>
          {parsed.hasContent ? (
            <div 
              className="prose font-bengali leading-relaxed text-gray-800 dark:text-gray-200 space-y-2"
              style={{ fontSize: `${bengaliFontSize}px` }}
            >
              <MarkdownContent content={parsed.cleanSharh} />
            </div>
          ) : (
            <div className="p-4 rounded-xl bg-gray-50 dark:bg-gray-700/30 border border-dashed border-gray-300 dark:border-gray-600 text-center text-xs sm:text-sm text-gray-500 dark:text-gray-400 italic">
              এই নির্দিষ্ট আয়াতের জন্য স্বতন্ত্র জালালাইন টীকা সংরক্ষিত নেই; রুকুর সামগ্রিক তাফসীর ও শাব্দিক তাহকীক দ্রষ্টব্য।
            </div>
          )}
        </div>
      )}
    </div>
  );
}

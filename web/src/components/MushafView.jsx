import React, { useState } from 'react';
import { toBn } from '../utils/helpers';
import { BookOpen, X, Bookmark, ArrowRight, Sparkles } from 'lucide-react';
import MarkdownContent from './MarkdownContent';

export default function MushafView({
  rukuData,
  surahInfo,
  onSelectAyah,
  arabicFontSize = 30,
  arabicLineHeight = 2.4
}) {
  const [activeSheetAyah, setActiveSheetAyah] = useState(null);

  if (!rukuData || !rukuData.ayahs) return null;

  const handleOpenStudy = (ayahNum) => {
    setActiveSheetAyah(null);
    if (onSelectAyah) {
      onSelectAyah(ayahNum);
    }
  };

  return (
    <div className="max-w-[820px] mx-auto px-3 sm:px-6 py-6 transition-colors">
      {/* 1. Traditional Mushaf Page Frame */}
      <div className="bg-[#FFFDF9] dark:bg-gray-800/90 rounded-3xl p-6 sm:p-11 shadow-sm border border-amber-200/70 dark:border-gray-700 transition-colors">
        {/* Decorative Mushaf Header Banner */}
        <div className="flex items-center justify-between border-b-2 border-emerald-800/20 dark:border-emerald-500/20 pb-3.5 mb-7">
          <div className="text-xs font-bold text-gray-500 dark:text-gray-400 font-bengali">
            রুকু {toBn(rukuData.ruku_id)} • আয়াত {rukuData.ayah_range_bn}
          </div>
          <div className="text-lg sm:text-2xl font-bold font-amiri text-emerald-900 dark:text-emerald-300 tracking-wide">
            سُورَةُ {surahInfo?.name_ar || ''}
          </div>
          <div className="text-xs font-bold text-gray-500 dark:text-gray-400 font-bengali">
            সূরা {surahInfo?.name_bn || ''} ({toBn(surahInfo?.id || '')})
          </div>
        </div>

        {/* 2. Continuous Justified Mushaf Text */}
        <div 
          className="uthmani-text leading-loose text-gray-950 dark:text-gray-100 text-justify cursor-pointer select-text"
          style={{ 
            fontSize: `${arabicFontSize}px`, 
            lineHeight: arabicLineHeight,
            textAlign: 'justify',
            textAlignLast: 'right'
          }}
          dir="rtl"
        >
          {rukuData.ayahs.map((a, idx) => {
            const isLastAyahOfRuku = idx === rukuData.ayahs.length - 1;
            return (
              <span
                key={a.ayah}
                onClick={() => setActiveSheetAyah(a)}
                className="hover:bg-amber-100/70 dark:hover:bg-emerald-950/50 rounded-lg px-1 transition duration-150 inline"
                title={`আয়াত ${toBn(a.ayah)} — ক্লিক করে কুইক-পিক তাফসীর দেখুন`}
              >
                {a.text_uthmani}
                {/* Traditional Ayah End Marker */}
                <span className="ayah-end-symbol text-emerald-800 dark:text-emerald-400 text-[0.82em] font-normal mx-1 select-none">
                  ۝{toBn(a.ayah)}
                </span>
                {/* Traditional Ruku End Margin Marker 'ع' */}
                {isLastAyahOfRuku && (
                  <span 
                    className="mushaf-ruku-marker" 
                    title={`রুকু ${toBn(rukuData.ruku_id)} সমাপ্ত`}
                  >
                    ع
                  </span>
                )}
              </span>
            );
          })}
        </div>

        {/* Page Footer decoration */}
        <div className="mt-8 pt-3 border-t border-amber-200/50 dark:border-gray-700/50 flex items-center justify-between text-[11px] text-gray-400 font-bengali">
          <span>পবিত্র কুরআনুল কারীম • উসমানী রসম</span>
          <span className="font-mono">রুকু {toBn(rukuData.ruku_id)} সমাপ্তি চিহ্নিত (ع)</span>
        </div>
      </div>

      {/* 3. Quick-Peek Drawer (স্লিম বটম শীট / সাইডনোট ড্রয়ার) */}
      {activeSheetAyah && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-end justify-center p-0 sm:p-4 animate-in fade-in duration-150">
          <div className="bg-white dark:bg-gray-800 rounded-t-3xl sm:rounded-2xl max-w-xl w-full max-h-[85vh] overflow-y-auto p-5 sm:p-6 shadow-2xl border border-gray-200 dark:border-gray-700 space-y-4">
            {/* Quick-Peek Header */}
            <div className="flex items-center justify-between pb-2.5 border-b border-gray-100 dark:border-gray-700">
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950/80 text-emerald-900 dark:text-emerald-300 text-xs font-bold">
                  কুইক-পিক • আয়াত {toBn(activeSheetAyah.ayah)}
                </span>
                <span className="text-xs text-gray-500 dark:text-gray-400 font-semibold font-bengali">
                  সূরা {surahInfo?.name_bn}
                </span>
              </div>
              <button
                onClick={() => setActiveSheetAyah(null)}
                className="p-1 rounded-full text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Arabic Uthmani Snippet */}
            <div className="uthmani-text text-xl sm:text-2xl text-emerald-950 dark:text-emerald-100 font-bold leading-relaxed" dir="rtl">
              {activeSheetAyah.text_uthmani}
              <span className="ayah-end-symbol text-emerald-700 dark:text-emerald-400 text-[0.8em] font-normal mr-1">
                ۝{toBn(activeSheetAyah.ayah)}
              </span>
            </div>

            {/* Translation */}
            <div className="text-gray-800 dark:text-gray-200 text-xs sm:text-sm leading-relaxed bg-gray-50 dark:bg-gray-700/40 p-3.5 rounded-xl border border-gray-100 dark:border-gray-700 font-bengali">
              <span className="font-bold text-emerald-700 dark:text-emerald-400 mr-1.5">অনুবাদ:</span>
              {activeSheetAyah.translation}
            </div>

            {/* Jalalayn Preview */}
            <div className="space-y-2">
              <span className="text-xs font-bold text-emerald-900 dark:text-emerald-300 flex items-center gap-1.5 font-bengali">
                <BookOpen className="w-4 h-4 text-emerald-600" />
                <span>তাফসীরুল জালালাইন (ইবারত ও ব্যাখ্যা):</span>
              </span>
              <div className="text-xs sm:text-sm text-gray-700 dark:text-gray-300 bg-emerald-50/50 dark:bg-emerald-950/20 p-3.5 rounded-xl border border-emerald-100 dark:border-emerald-900/30 font-bengali max-h-56 overflow-y-auto">
                {activeSheetAyah.jalalayn ? (
                  <MarkdownContent content={activeSheetAyah.jalalayn} />
                ) : (
                  "জালালাইন তাফসীর লোড হচ্ছে..."
                )}
              </div>
            </div>

            {/* Quick Action Button: Jump directly into Ayat Study */}
            <div className="pt-2">
              <button
                onClick={() => handleOpenStudy(activeSheetAyah.ayah)}
                className="w-full py-2.5 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs sm:text-sm flex items-center justify-center gap-2 transition shadow-sm"
              >
                <span>এই আয়াতের পূর্ণাঙ্গ স্টাডি ভিউতে যান</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

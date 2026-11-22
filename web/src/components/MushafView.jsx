import React, { useState } from 'react';
import { toBn } from '../utils/helpers';
import { BookOpen, X, Bookmark, FileText } from 'lucide-react';

export default function MushafView({
  rukuData,
  surahInfo,
  onSelectAyah,
  arabicFontSize = 30,
  arabicLineHeight = 2.4
}) {
  const [activeSheetAyah, setActiveSheetAyah] = useState(null);

  if (!rukuData || !rukuData.ayahs) return null;

  return (
    <div className="max-w-4xl mx-auto px-3 sm:px-6 py-6">
      {/* Mushaf Page Frame */}
      <div className="bg-[#fffef9] dark:bg-gray-800 rounded-3xl p-6 sm:p-10 shadow-md border-2 border-amber-200/60 dark:border-gray-700 transition-colors">
        {/* Decorative Mushaf Header */}
        <div className="flex items-center justify-between border-b-2 border-amber-300/40 dark:border-gray-700 pb-3 mb-6">
          <div className="text-xs font-bold text-amber-900/70 dark:text-gray-400">
            রুকু {toBn(rukuData.ruku_id)} • আয়াত {rukuData.ayah_range_bn}
          </div>
          <div className="text-base sm:text-lg font-bold font-amiri text-emerald-800 dark:text-emerald-400">
            سُورَةُ {surahInfo?.name_ar || ''}
          </div>
          <div className="text-xs font-bold text-amber-900/70 dark:text-gray-400">
            সূরা {surahInfo?.name_bn || ''}
          </div>
        </div>

        {/* Continuous Mushaf Text */}
        <div 
          className="uthmani-text leading-loose text-gray-900 dark:text-gray-100 text-justify selection:bg-amber-100 dark:selection:bg-emerald-900/60 cursor-pointer"
          style={{ fontSize: `${arabicFontSize}px`, lineHeight: arabicLineHeight }}
        >
          {rukuData.ayahs.map((a) => (
            <span
              key={a.ayah}
              onClick={() => setActiveSheetAyah(a)}
              className="hover:bg-amber-100/60 dark:hover:bg-gray-700/60 rounded px-1 transition duration-150 inline"
              title={`আয়াত ${toBn(a.ayah)} - ক্লিক করে তাফসীর দেখুন`}
            >
              {a.text_uthmani}
              <span className="ayah-end-symbol text-emerald-700 dark:text-emerald-400 text-[0.8em] font-normal mx-1 select-none">
                ۝{toBn(a.ayah)}
              </span>
            </span>
          ))}
        </div>
      </div>

      {/* Tap Bottom Sheet (Modal for Ayah Detail in Mushaf Mode) */}
      {activeSheetAyah && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-end sm:items-center justify-center p-0 sm:p-4 animate-in fade-in duration-200">
          <div className="bg-white dark:bg-gray-800 rounded-t-3xl sm:rounded-2xl max-w-2xl w-full max-h-[85vh] sm:max-h-[80vh] overflow-y-auto p-5 sm:p-6 shadow-2xl border border-gray-200 dark:border-gray-700 space-y-4">
            {/* Modal Header */}
            <div className="flex items-center justify-between pb-2 border-b border-gray-200 dark:border-gray-700">
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 text-xs font-bold">
                  আয়াত {toBn(activeSheetAyah.ayah)}
                </span>
                <span className="text-xs text-gray-500 dark:text-gray-400">
                  সূরা {surahInfo?.name_bn}
                </span>
              </div>
              <button
                onClick={() => setActiveSheetAyah(null)}
                className="p-1 rounded-full text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 transition"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Arabic & Translation */}
            <div className="uthmani-text text-xl sm:text-2xl text-emerald-950 dark:text-emerald-100 leading-relaxed">
              {activeSheetAyah.text_uthmani}
            </div>

            <div className="text-gray-800 dark:text-gray-200 text-sm sm:text-base leading-relaxed bg-gray-50 dark:bg-gray-700/40 p-3 rounded-xl border border-gray-100 dark:border-gray-700">
              <span className="font-bold text-emerald-700 dark:text-emerald-400 mr-1">অনুবাদ:</span>
              {activeSheetAyah.translation}
            </div>

            {/* Jalalayn Preview */}
            <div className="space-y-2">
              <span className="text-xs font-bold text-emerald-800 dark:text-emerald-300 flex items-center gap-1.5">
                <BookOpen className="w-4 h-4" />
                <span>তাফসীরুল জালালাইন (ইবারত ও ব্যাখ্যা):</span>
              </span>
              <div className="text-xs sm:text-sm text-gray-700 dark:text-gray-300 bg-emerald-50/40 dark:bg-emerald-950/20 p-3 rounded-xl leading-relaxed whitespace-pre-line border border-emerald-100 dark:border-emerald-900/40 font-bengali max-h-48 overflow-y-auto">
                {activeSheetAyah.jalalayn || "জালালাইন তাফসীর লোড হচ্ছে..."}
              </div>
            </div>

            {/* Jump to Full Study Button */}
            <div className="pt-2 flex gap-2">
              <button
                onClick={() => {
                  onSelectAyah(activeSheetAyah.ayah);
                  setActiveSheetAyah(null);
                }}
                className="flex-1 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs sm:text-sm transition flex items-center justify-center gap-1.5 shadow-sm"
              >
                <BookOpen className="w-4 h-4" />
                <span>আয়াত স্টাডি মোডে বিস্তারিত খুলুন</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

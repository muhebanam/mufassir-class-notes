import React from 'react';
import { X, Sliders, Sun, Moon, Sparkles } from 'lucide-react';
import { toBn } from '../utils/helpers';

export default function SettingsModal({
  isOpen,
  onClose,
  arabicFontSize,
  setArabicFontSize,
  bengaliFontSize,
  setBengaliFontSize,
  arabicLineHeight,
  setArabicLineHeight,
  theme,
  setTheme
}) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-150">
      <div className="bg-white dark:bg-gray-800 rounded-2xl max-w-md w-full shadow-2xl p-5 sm:p-6 border border-gray-200 dark:border-gray-700 space-y-5">
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-2">
            <Sliders className="w-5 h-5 text-emerald-600" />
            <h3 className="font-bold text-base text-gray-900 dark:text-gray-100">
              পাঠ ও টাইপোগ্রাফি সেটিংস
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-full text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Theme Selectors */}
        <div className="space-y-2">
          <label className="text-xs font-bold text-gray-700 dark:text-gray-300">
            কালার থিম নির্বাচন:
          </label>
          <div className="grid grid-cols-3 gap-2">
            <button
              onClick={() => setTheme('light')}
              className={`py-2 px-3 rounded-xl border text-xs font-semibold flex items-center justify-center gap-1.5 transition ${
                theme === 'light'
                  ? 'bg-emerald-50 border-emerald-600 text-emerald-800 font-bold ring-2 ring-emerald-400/30'
                  : 'bg-white border-gray-200 text-gray-700 hover:bg-gray-50'
              }`}
            >
              <Sun className="w-4 h-4 text-amber-500" />
              <span>ডে-লাইট</span>
            </button>

            <button
              onClick={() => setTheme('sepia')}
              className={`py-2 px-3 rounded-xl border text-xs font-semibold flex items-center justify-center gap-1.5 transition ${
                theme === 'sepia'
                  ? 'bg-[#f7f3e8] border-amber-700 text-amber-900 font-bold ring-2 ring-amber-500/30'
                  : 'bg-[#faf8f5] border-amber-200 text-amber-900 hover:bg-[#f3eedf]'
              }`}
            >
              <Sparkles className="w-4 h-4 text-amber-700" />
              <span>সেপিয়া পেপার</span>
            </button>

            <button
              onClick={() => setTheme('dark')}
              className={`py-2 px-3 rounded-xl border text-xs font-semibold flex items-center justify-center gap-1.5 transition ${
                theme === 'dark'
                  ? 'bg-gray-900 border-emerald-500 text-white font-bold ring-2 ring-emerald-500/30'
                  : 'bg-gray-800 border-gray-700 text-gray-300 hover:bg-gray-700'
              }`}
            >
              <Moon className="w-4 h-4 text-indigo-400" />
              <span>নাইট ডার্ক</span>
            </button>
          </div>
        </div>

        {/* Arabic Font Size Slider */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-xs font-bold text-gray-700 dark:text-gray-300">
            <span>আরবি ফন্ট সাইজ:</span>
            <span className="text-emerald-700 dark:text-emerald-400 font-mono">{toBn(arabicFontSize)} px</span>
          </div>
          <input
            type="range"
            min="20"
            max="42"
            value={arabicFontSize}
            onChange={(e) => setArabicFontSize(Number(e.target.value))}
            className="w-full accent-emerald-600 cursor-pointer"
          />
        </div>

        {/* Arabic Line Height Slider */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-xs font-bold text-gray-700 dark:text-gray-300">
            <span>আরবি লাইন হাইট (হরকত সুরক্ষায়):</span>
            <span className="text-emerald-700 dark:text-emerald-400 font-mono">{toBn(arabicLineHeight)}</span>
          </div>
          <input
            type="range"
            min="1.8"
            max="3.0"
            step="0.1"
            value={arabicLineHeight}
            onChange={(e) => setArabicLineHeight(Number(e.target.value))}
            className="w-full accent-emerald-600 cursor-pointer"
          />
        </div>

        {/* Bengali Font Size Slider */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-xs font-bold text-gray-700 dark:text-gray-300">
            <span>বাংলা অনুবাদ ও তাফসীর ফন্ট সাইজ:</span>
            <span className="text-emerald-700 dark:text-emerald-400 font-mono">{toBn(bengaliFontSize)} px</span>
          </div>
          <input
            type="range"
            min="14"
            max="22"
            value={bengaliFontSize}
            onChange={(e) => setBengaliFontSize(Number(e.target.value))}
            className="w-full accent-emerald-600 cursor-pointer"
          />
        </div>

        {/* Font Preview Card */}
        <div className="p-3 bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 space-y-2">
          <div 
            className="uthmani-text text-center text-emerald-900 dark:text-emerald-200"
            style={{ fontSize: `${arabicFontSize}px`, lineHeight: arabicLineHeight }}
          >
            بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ
          </div>
          <div 
            className="text-center text-gray-700 dark:text-gray-300"
            style={{ fontSize: `${bengaliFontSize}px` }}
          >
            পরম করুণাময় অতি দয়ালু আল্লাহর নামে
          </div>
        </div>

        {/* Done Button */}
        <button
          onClick={onClose}
          className="w-full py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm transition shadow-sm"
        >
          সম্পন্ন
        </button>
      </div>
    </div>
  );
}

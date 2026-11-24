import React from 'react';
import { X, Sliders, Sun, Moon, Sparkles, Columns, Rows } from 'lucide-react';
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
  setTheme,
  splitView,
  setSplitView
}) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-150">
      <div className="bg-white dark:bg-gray-800 rounded-2xl max-w-md w-full shadow-2xl p-5 sm:p-6 border border-gray-200 dark:border-gray-700 space-y-5">
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-2">
            <Sliders className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            <h3 className="font-bold text-base text-gray-900 dark:text-gray-100">
              পাঠ ও টাইপোগ্রাফি সেটিংস
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-full text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* 3 Academic Themes */}
        <div className="space-y-2">
          <label className="text-xs font-bold text-gray-700 dark:text-gray-300">
            কালার থিম ও চোখের আরাম:
          </label>
          <div className="grid grid-cols-3 gap-2">
            <button
              onClick={() => setTheme('light')}
              className={`py-2 px-2.5 rounded-xl border text-xs font-semibold flex flex-col items-center justify-center gap-1 transition ${
                theme === 'light'
                  ? 'bg-[#FAF9F6] border-[#0F5132] text-[#0F5132] font-bold ring-2 ring-emerald-500/30 shadow-xs'
                  : 'bg-white border-gray-200 text-gray-700 hover:bg-gray-50'
              }`}
            >
              <Sun className="w-4 h-4 text-amber-500" />
              <span>Paper Light</span>
              <span className="text-[10px] text-gray-400 font-normal">ডিফল্ট</span>
            </button>

            <button
              onClick={() => setTheme('sepia')}
              className={`py-2 px-2.5 rounded-xl border text-xs font-semibold flex flex-col items-center justify-center gap-1 transition ${
                theme === 'sepia'
                  ? 'bg-[#F4ECD8] border-[#8B5E34] text-[#8B5E34] font-bold ring-2 ring-amber-500/30 shadow-xs'
                  : 'bg-[#faf8f5] border-amber-200 text-amber-900 hover:bg-[#f3eedf]'
              }`}
            >
              <Sparkles className="w-4 h-4 text-amber-700" />
              <span>Warm Sepia</span>
              <span className="text-[10px] text-amber-700/70 font-normal">উষ্ণ সেপিয়া</span>
            </button>

            <button
              onClick={() => setTheme('dark')}
              className={`py-2 px-2.5 rounded-xl border text-xs font-semibold flex flex-col items-center justify-center gap-1 transition ${
                theme === 'dark'
                  ? 'bg-[#121518] border-[#34D3BE] text-[#34D3BE] font-bold ring-2 ring-emerald-400/30 shadow-xs'
                  : 'bg-gray-800 border-gray-700 text-gray-300 hover:bg-gray-700'
              }`}
            >
              <Moon className="w-4 h-4 text-indigo-400" />
              <span>Academic Dark</span>
              <span className="text-[10px] text-gray-400 font-normal">নাইট মোড</span>
            </button>
          </div>
        </div>

        {/* Layout View Mode (Split View vs Stacked View) */}
        {setSplitView && (
          <div className="space-y-2 pt-1 border-t border-gray-100 dark:border-gray-700/60">
            <label className="text-xs font-bold text-gray-700 dark:text-gray-300">
              আয়াত স্টাডি লেআউট (বড় স্ক্রিনে):
            </label>
            <div className="grid grid-cols-2 gap-2">
              <button
                onClick={() => setSplitView(true)}
                className={`py-2 px-3 rounded-xl border text-xs font-semibold flex items-center justify-center gap-1.5 transition ${
                  splitView
                    ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-600 text-emerald-800 dark:text-emerald-300 font-bold'
                    : 'bg-gray-50 dark:bg-gray-700/40 border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300'
                }`}
              >
                <Columns className="w-4 h-4 text-emerald-600" />
                <span>Split View (ডুয়াল)</span>
              </button>

              <button
                onClick={() => setSplitView(false)}
                className={`py-2 px-3 rounded-xl border text-xs font-semibold flex items-center justify-center gap-1.5 transition ${
                  !splitView
                    ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-600 text-emerald-800 dark:text-emerald-300 font-bold'
                    : 'bg-gray-50 dark:bg-gray-700/40 border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300'
                }`}
              >
                <Rows className="w-4 h-4 text-emerald-600" />
                <span>Stacked View (স্ট্যাকড)</span>
              </button>
            </div>
          </div>
        )}

        {/* Arabic Font Size Slider */}
        <div className="space-y-1.5 pt-1 border-t border-gray-100 dark:border-gray-700/60">
          <div className="flex items-center justify-between text-xs font-bold text-gray-700 dark:text-gray-300">
            <span>আরবি ফন্ট সাইজ (উসমানী রসম):</span>
            <span className="text-emerald-700 dark:text-emerald-400 font-mono font-bold">{toBn(arabicFontSize)} px</span>
          </div>
          <input
            type="range"
            min="22"
            max="40"
            value={arabicFontSize}
            onChange={(e) => setArabicFontSize(Number(e.target.value))}
            className="w-full accent-emerald-600 cursor-pointer"
          />
        </div>

        {/* Bengali Font Size Slider */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-xs font-bold text-gray-700 dark:text-gray-300">
            <span>বাংলা ফন্ট সাইজ (অনুবাদ ও তাফসীর):</span>
            <span className="text-emerald-700 dark:text-emerald-400 font-mono font-bold">{toBn(bengaliFontSize)} px</span>
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

        {/* Arabic Line Height Slider */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-xs font-bold text-gray-700 dark:text-gray-300">
            <span>আরবি লাইন হাইট (হরকত স্পষ্টতা):</span>
            <span className="text-emerald-700 dark:text-emerald-400 font-mono font-bold">{arabicLineHeight}</span>
          </div>
          <input
            type="range"
            min="1.8"
            max="2.8"
            step="0.1"
            value={arabicLineHeight}
            onChange={(e) => setArabicLineHeight(Number(e.target.value))}
            className="w-full accent-emerald-600 cursor-pointer"
          />
        </div>

        {/* Reset Button */}
        <div className="pt-2">
          <button
            onClick={() => {
              setArabicFontSize(28);
              setBengaliFontSize(16);
              setArabicLineHeight(2.2);
              setTheme('light');
              if (setSplitView) setSplitView(true);
            }}
            className="w-full py-2 rounded-xl text-xs font-semibold text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition"
          >
            ডিফল্ট সেটিংসে ফিরিয়ে নিন
          </button>
        </div>
      </div>
    </div>
  );
}

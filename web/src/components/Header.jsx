import React from 'react';
import { BookOpen, Search, FileText, UserCheck, Moon, Sun, Sparkles } from 'lucide-react';
import { toBn } from '../utils/helpers';

export default function Header({
  surahs,
  currentSurah,
  currentRuku,
  surahMeta,
  studyMode,
  setStudyMode,
  onSelectSurah,
  onSelectRuku,
  onOpenSearch,
  onOpenSettings,
  onOpenNotes,
  onOpenAuthor,
  theme,
  setTheme,
  isHidden = false
}) {
  return (
    <header 
      className={`sticky top-0 z-30 bg-white/95 dark:bg-gray-800/95 backdrop-blur-md border-b border-gray-200/90 dark:border-gray-700/80 shadow-xs transition-transform duration-300 ${
        isHidden ? '-translate-y-full shadow-none' : 'translate-y-0'
      }`}
    >
      <div className="max-w-7xl mx-auto px-3 sm:px-4 h-14 sm:h-16 flex items-center justify-between gap-2">
        {/* Left: Brand & Surah / Ruku Navigation */}
        <div className="flex items-center gap-1.5 min-w-0">
          <button
            onClick={() => onSelectSurah(null)}
            className="flex items-center gap-1.5 text-emerald-800 dark:text-emerald-400 font-bold hover:opacity-85 transition shrink-0"
            title="হোম / সূরা তালিকা"
          >
            <div className="w-8 h-8 rounded-xl bg-emerald-100 dark:bg-emerald-950/80 flex items-center justify-center text-emerald-700 dark:text-emerald-300 shadow-2xs">
              <BookOpen className="w-4 h-4" />
            </div>
            <span className="hidden xl:inline font-bold text-base tracking-tight font-bengali">তাফসীরুল জালালাইন</span>
          </button>

          {/* Surah Selector Dropdown */}
          {surahs && surahs.length > 0 && (
            <select
              value={currentSurah?.id || ""}
              onChange={(e) => onSelectSurah(Number(e.target.value))}
              aria-label="সূরা নির্বাচন করুন"
              className="bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-xs sm:text-sm font-semibold rounded-xl px-2 sm:px-3 py-1.5 border border-transparent hover:border-gray-300 dark:hover:border-gray-600 focus:outline-none focus:ring-2 focus:ring-emerald-500 max-w-[110px] sm:max-w-[170px] truncate shrink-0 transition"
            >
              {surahs.map((s) => (
                <option key={s.id} value={s.id}>
                  {toBn(s.id)}. {s.name_bn} ({s.name_ar})
                </option>
              ))}
            </select>
          )}

          {/* Ruku Selector Dropdown */}
          {surahMeta?.rukus && surahMeta.rukus.length > 0 && (
            <select
              value={currentRuku || 1}
              onChange={(e) => onSelectRuku(Number(e.target.value))}
              aria-label="রুকু নির্বাচন করুন"
              className="bg-emerald-50 dark:bg-emerald-950/50 text-emerald-900 dark:text-emerald-300 text-xs sm:text-sm font-bold rounded-xl px-2 sm:px-2.5 py-1.5 border border-emerald-200 dark:border-emerald-800 focus:outline-none focus:ring-2 focus:ring-emerald-500 max-w-[105px] sm:max-w-none truncate shrink-0 transition"
            >
              {surahMeta.rukus.map((r) => (
                <option key={r.ruku_id} value={r.ruku_id}>
                  রুকু {toBn(r.ruku_id)} ({r.ayah_range_bn})
                </option>
              ))}
            </select>
          )}
        </div>

        {/* Center: Top Segmented Control (3 Distinct Academic Modes) */}
        <div className="hidden md:flex items-center bg-gray-100/90 dark:bg-gray-700/70 p-1 rounded-2xl text-xs font-bold border border-gray-200/50 dark:border-gray-600/50 shadow-2xs">
          <button
            onClick={() => setStudyMode('mushaf')}
            className={`px-3 py-1.5 rounded-xl transition flex items-center gap-1.5 ${
              studyMode === 'mushaf'
                ? 'bg-white dark:bg-gray-800 text-emerald-800 dark:text-emerald-300 shadow-xs font-bold'
                : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
            }`}
          >
            <span>📖</span>
            <span>মুসহাফ রিডিং</span>
          </button>

          <button
            onClick={() => setStudyMode('ayah')}
            className={`px-3 py-1.5 rounded-xl transition flex items-center gap-1.5 ${
              studyMode === 'ayah'
                ? 'bg-white dark:bg-gray-800 text-emerald-800 dark:text-emerald-300 shadow-xs font-bold'
                : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
            }`}
          >
            <span>🔍</span>
            <span>আয়াত স্টাডি</span>
          </button>

          <button
            onClick={() => setStudyMode('thematic')}
            className={`px-3 py-1.5 rounded-xl transition flex items-center gap-1.5 ${
              studyMode === 'thematic'
                ? 'bg-white dark:bg-gray-800 text-emerald-800 dark:text-emerald-300 shadow-xs font-bold'
                : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
            }`}
          >
            <span>🏛️</span>
            <span>রুকু শাস্ত্র-আলোচনা</span>
          </button>
        </div>

        {/* Right: Actions, Command Palette Search & Typography Settings */}
        <div className="flex items-center gap-1 sm:gap-1.5 shrink-0">
          {/* Command Palette Search (Ctrl + K) */}
          <button
            onClick={onOpenSearch}
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 border border-gray-200/70 dark:border-gray-700 transition"
            title="কমান্ড প্যালেট সার্চ (Ctrl + K)"
          >
            <Search className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
            <span className="hidden lg:inline text-xs font-mono text-gray-400">Ctrl+K</span>
          </button>

          {/* Notes Drawer */}
          <button
            onClick={onOpenNotes}
            className="hidden sm:flex p-2 rounded-xl text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition relative"
            title="ব্যক্তিগত ক্লাস নোটসমূহ"
          >
            <FileText className="w-4 h-4 sm:w-5 sm:h-5" />
          </button>

          {/* Author Rights Modal */}
          <button
            onClick={onOpenAuthor}
            className="hidden sm:flex p-2 rounded-xl text-emerald-700 dark:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 transition"
            title="অনুবাদক ও গ্রন্থ পরিচিতি"
          >
            <UserCheck className="w-4 h-4 sm:w-5 sm:h-5" />
          </button>

          {/* Theme Switcher Button */}
          <button
            onClick={() => setTheme(theme === 'dark' ? 'light' : theme === 'light' ? 'sepia' : 'dark')}
            className="p-2 rounded-xl text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition border border-gray-200/70 dark:border-gray-700"
            title={`থিম পরিবর্তন (বর্তমান: ${
              theme === 'dark' ? 'Academic Dark' : theme === 'sepia' ? 'Warm Sepia' : 'Paper Light'
            })`}
          >
            {theme === 'dark' ? (
              <Moon className="w-4 h-4 text-indigo-400" />
            ) : theme === 'sepia' ? (
              <Sparkles className="w-4 h-4 text-amber-700" />
            ) : (
              <Sun className="w-4 h-4 text-amber-500" />
            )}
          </button>

          {/* Reading & Typography Settings Popover Trigger (Aa icon) */}
          <button
            onClick={onOpenSettings}
            className="px-2.5 py-1.5 rounded-xl font-serif font-bold text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 border border-gray-200/70 dark:border-gray-700 transition flex items-center justify-center gap-1 shadow-2xs"
            title="পাঠ ও টাইপোগ্রাফি সেটিংস (Aa)"
          >
            <span>Aa</span>
          </button>
        </div>
      </div>
    </header>
  );
}

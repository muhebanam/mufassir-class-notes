import React from 'react';
import { BookOpen, Search, Settings, FileText, UserCheck, Moon, Sun, Layers } from 'lucide-react';
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
  setTheme
}) {
  return (
    <header className="sticky top-0 z-30 bg-white/95 dark:bg-gray-800/95 backdrop-blur-md border-b border-gray-200 dark:border-gray-700 shadow-sm transition-colors">
      <div className="max-w-7xl mx-auto px-3 sm:px-4 h-14 sm:h-16 flex items-center justify-between gap-2">
        {/* Brand & Surah Selector */}
        <div className="flex items-center gap-2 min-w-0">
          <button
            onClick={() => onSelectSurah(null)}
            className="flex items-center gap-1.5 text-emerald-800 dark:text-emerald-400 font-bold hover:opacity-80 transition shrink-0"
            title="হোম / সূরা তালিকা"
          >
            <div className="w-8 h-8 rounded-lg bg-emerald-100 dark:bg-emerald-950/60 flex items-center justify-center text-emerald-700 dark:text-emerald-400">
              <BookOpen className="w-4 h-4" />
            </div>
            <span className="hidden sm:inline font-bold text-base sm:text-lg tracking-tight">মুফাস্সির নোট</span>
          </button>

          {/* Surah Selector Dropdown */}
          {surahs && surahs.length > 0 && (
            <select
              value={currentSurah?.id || ""}
              onChange={(e) => onSelectSurah(Number(e.target.value))}
              aria-label="সূরা নির্বাচন করুন"
              className="bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-xs sm:text-sm font-medium rounded-lg px-2 sm:px-3 py-1.5 border border-transparent hover:border-gray-300 dark:hover:border-gray-600 focus:outline-none focus:ring-2 focus:ring-emerald-500 max-w-[130px] sm:max-w-[180px] truncate"
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
              className="bg-emerald-50 dark:bg-emerald-950/40 text-emerald-900 dark:text-emerald-300 text-xs sm:text-sm font-semibold rounded-lg px-2 py-1.5 border border-emerald-200 dark:border-emerald-800 focus:outline-none focus:ring-2 focus:ring-emerald-500 shrink-0"
            >
              {surahMeta.rukus.map((r) => (
                <option key={r.ruku_id} value={r.ruku_id}>
                  রুকু {toBn(r.ruku_id)} ({r.ayah_range_bn})
                </option>
              ))}
            </select>
          )}
        </div>

        {/* Study Mode Tabs (Desktop / Tablet) */}
        <div className="hidden md:flex items-center bg-gray-100 dark:bg-gray-700/60 p-1 rounded-xl text-xs font-semibold">
          <button
            onClick={() => setStudyMode('ayah')}
            className={`px-3 py-1 rounded-lg transition ${
              studyMode === 'ayah'
                ? 'bg-white dark:bg-gray-800 text-emerald-800 dark:text-emerald-300 shadow-sm'
                : 'text-gray-600 dark:text-gray-300 hover:text-gray-900'
            }`}
          >
            আয়াত স্টাডি
          </button>
          <button
            onClick={() => setStudyMode('thematic')}
            className={`px-3 py-1 rounded-lg transition ${
              studyMode === 'thematic'
                ? 'bg-white dark:bg-gray-800 text-emerald-800 dark:text-emerald-300 shadow-sm'
                : 'text-gray-600 dark:text-gray-300 hover:text-gray-900'
            }`}
          >
            রুকু শাস্ত্র-আলোচনা
          </button>
          <button
            onClick={() => setStudyMode('mushaf')}
            className={`px-3 py-1 rounded-lg transition ${
              studyMode === 'mushaf'
                ? 'bg-white dark:bg-gray-800 text-emerald-800 dark:text-emerald-300 shadow-sm'
                : 'text-gray-600 dark:text-gray-300 hover:text-gray-900'
            }`}
          >
            মুসহাফ রিডিং
          </button>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-1 sm:gap-1.5">
          {/* Quick Search */}
          <button
            onClick={onOpenSearch}
            className="p-2 rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition"
            title="সার্চ করুন (Ctrl + K)"
          >
            <Search className="w-4 h-4 sm:w-5 sm:h-5" />
          </button>

          {/* Notes Drawer */}
          <button
            onClick={onOpenNotes}
            className="p-2 rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition relative"
            title="সংরক্ষিত ক্লাস নোটসমূহ"
          >
            <FileText className="w-4 h-4 sm:w-5 sm:h-5" />
          </button>

          {/* Author & Rights Info */}
          <button
            onClick={onOpenAuthor}
            className="p-2 rounded-lg text-emerald-700 dark:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 transition"
            title="অনুবাদক ও প্রকাশনা অধিকার"
          >
            <UserCheck className="w-4 h-4 sm:w-5 sm:h-5" />
          </button>

          {/* Theme Toggle */}
          <button
            onClick={() => setTheme(theme === 'dark' ? 'light' : theme === 'light' ? 'sepia' : 'dark')}
            className="p-2 rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition"
            title={`থিম পরিবর্তন (বর্তমান: ${theme === 'dark' ? 'ডার্ক' : theme === 'sepia' ? 'সেপিয়া' : 'লাইট'})`}
          >
            {theme === 'dark' ? <Moon className="w-4 h-4 text-indigo-400" /> : <Sun className="w-4 h-4 text-amber-500" />}
          </button>

          {/* Settings */}
          <button
            onClick={onOpenSettings}
            className="p-2 rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition"
            title="পাঠ ও ফন্ট সেটিংস"
          >
            <Settings className="w-4 h-4 sm:w-5 sm:h-5" />
          </button>
        </div>
      </div>
    </header>
  );
}

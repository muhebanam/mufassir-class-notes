import React, { useState, useMemo } from 'react';
import { Search, BookOpen, Layers, Sparkles, UserCheck, ShieldCheck } from 'lucide-react';
import { toBn } from '../utils/helpers';

export default function SurahDashboard({ surahs, siteMeta, onSelectSurah, onOpenAuthor }) {
  const [searchQuery, setSearchQuery] = useState("");
  const [filterType, setFilterType] = useState("all"); // 'all', 'makki', 'madani'

  const filteredSurahs = useMemo(() => {
    if (!surahs) return [];
    return surahs.filter((s) => {
      const matchSearch =
        s.name_bn.toLowerCase().includes(searchQuery.toLowerCase()) ||
        s.name_ar.includes(searchQuery) ||
        String(s.id).includes(searchQuery) ||
        toBn(s.id).includes(searchQuery);

      return matchSearch;
    });
  }, [surahs, searchQuery]);

  return (
    <div className="max-w-6xl mx-auto px-3 sm:px-6 py-6 space-y-6">
      {/* Hero Banner */}
      <div className="relative overflow-hidden bg-gradient-to-br from-emerald-800 via-teal-900 to-emerald-950 text-white rounded-3xl p-6 sm:p-10 shadow-xl">
        <div className="max-w-2xl space-y-3 relative z-10">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-700/60 text-emerald-200 text-xs font-semibold backdrop-blur-sm border border-emerald-500/30">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-300" />
            <span>ডিজিটাল অডিট ও ১০ কিরাআত সমন্বিত মাস্টার সংস্করণ</span>
          </div>

          <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight font-bengali">
            মুফাস্সির ক্লাস নোট
          </h1>
          <p className="text-sm sm:text-base text-emerald-100/90 leading-relaxed font-bengali">
            তাফসীরুল জালালাইনভিত্তিক প্রামাণ্য তাহকীক, শব্দার্থ, ই'রাব, ১০ মুতাওয়াতির কিরাআত, ৪ মাযহাবের ফিকহ ও দরসের পূর্ণাঙ্গ ডিজিটাল হ্যান্ডনোট।
          </p>

          {/* Author Badge */}
          <div className="pt-2 flex flex-wrap items-center gap-2">
            <button
              onClick={onOpenAuthor}
              className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/10 hover:bg-white/20 text-xs text-emerald-100 border border-white/20 transition"
            >
              <UserCheck className="w-4 h-4 text-emerald-300" />
              <span>অনুবাদ ও তাহকীক: <strong className="text-white">মুফতী মুহাম্মাদ মুহিব্বুল্লাহ</strong></span>
            </button>
            <span className="text-xs text-emerald-300/80">
              • প্রকাশনা: মাকতাবাতুল ইসহাক, ঢাকা
            </span>
          </div>
        </div>

        {/* Decorative Background Pattern */}
        <div className="absolute right-[-40px] bottom-[-40px] opacity-10 text-[200px] select-none font-amiri pointer-events-none">
          📖
        </div>
      </div>

      {/* Surah Search & Stats Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 bg-white dark:bg-gray-800 p-3 sm:p-4 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 transition-colors">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="সূরার নাম (বাংলা/আরবি) বা নম্বর লিখে খুঁজুন (উদা. ২৪, নূর, النور)..."
            className="w-full pl-10 pr-4 py-2 rounded-xl text-sm bg-gray-50 dark:bg-gray-700/60 text-gray-900 dark:text-gray-100 border border-gray-200 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
        </div>

        <div className="flex items-center justify-between sm:justify-end gap-3 text-xs text-gray-500 dark:text-gray-400 px-1 font-semibold">
          <span>মোট: {toBn(filteredSurahs.length)}টি সূরা</span>
          <span>•</span>
          <span>রুকু: ২৫৯টি</span>
          <span>•</span>
          <span>আয়াত: ৩,৪৪৫টি</span>
        </div>
      </div>

      {/* Surahs Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 sm:gap-4">
        {filteredSurahs.map((s) => (
          <button
            key={s.id}
            onClick={() => onSelectSurah(s.id)}
            className="group text-left bg-white dark:bg-gray-800 p-4 rounded-2xl border border-gray-200 dark:border-gray-700 hover:border-emerald-500 dark:hover:border-emerald-500 hover:shadow-md transition-all duration-200 flex items-center justify-between gap-3"
          >
            <div className="flex items-center gap-3 min-w-0">
              {/* Surah Number Badge */}
              <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 font-extrabold flex items-center justify-center text-sm shrink-0 group-hover:bg-emerald-600 group-hover:text-white transition">
                {toBn(s.id)}
              </div>

              <div className="min-w-0">
                <div className="font-bold text-gray-900 dark:text-gray-100 text-base truncate group-hover:text-emerald-700 dark:group-hover:text-emerald-400 transition">
                  {s.name_bn}
                </div>
                <div className="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-2 mt-0.5">
                  <span>{s.ayah_count_bn} আয়াত</span>
                  <span>•</span>
                  <span>{s.ruku_count_bn} রুকু</span>
                </div>
              </div>
            </div>

            {/* Arabic Name */}
            <div className="font-amiri text-xl text-emerald-800 dark:text-emerald-400 text-right shrink-0">
              {s.name_ar}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

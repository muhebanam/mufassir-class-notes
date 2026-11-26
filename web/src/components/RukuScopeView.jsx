import React, { useState, useEffect } from 'react';
import { 
  BookOpen, Layers, Sparkles, Scale, Volume2, Compass, ArrowRight, ChevronRight,
  FileText, BookMarked, GitCompare, Feather, HelpCircle, CheckCircle2, Info, List, ExternalLink
} from 'lucide-react';
import MarkdownContent from './MarkdownContent';
import QiraatTable from './QiraatTable';
import HadithTakhrijSection from './HadithTakhrijSection';
import MasalaCard from './MasalaCard';

export default function RukuScopeView({ 
  rukuData, 
  surahInfo, 
  onSelectAyah,
  onSwitchToAyahScope,
  initialTab
}) {
  // Reading Mode: 'tabbed' (single chapter) or 'continuous' (journal article with sticky TOC)
  const [readingLayout, setReadingLayout] = useState('tabbed');
  const [activeTab, setActiveTab] = useState(initialTab || 'makasid');

  useEffect(() => {
    if (initialTab) {
      setActiveTab(initialTab);
    }
  }, [initialTab]);

  const toBn = (num) => {
    const bn = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
    return String(num).replace(/[0-9]/g, d => bn[d]);
  };

  if (!rukuData) {
    return (
      <div className="max-w-4xl mx-auto py-16 text-center space-y-3 font-bengali">
        <div className="w-8 h-8 border-3 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
        <p className="text-gray-500 text-sm">রুকু বিশ্লেষণ ডাটা লোড হচ্ছে...</p>
      </div>
    );
  }

  const topics = rukuData.thematic_topics || {};
  const qiraatTableData = topics.qiraat_full?.table || [];

  // All 14 Academic Chapters
  const allSections = [
    { id: 'makasid', label: 'ভূমিকা ও মাকাসিদ', num: '০১', icon: Compass, sec: topics.makasid },
    { id: 'connections', label: 'আন্তঃআয়াত সংযোগ ও মুনাসাবাত', num: '০২', icon: CheckCircle2, sec: topics.connections || topics.munasabat },
    { id: 'irab', label: 'ই\'রাব ও নাহব', num: '০৩', icon: FileText, sec: topics.irab_full },
    { id: 'qiraat', label: '১০ কিরাআত সারণি', num: '০৪', icon: Volume2, sec: topics.qiraat_full, count: qiraatTableData.length },
    { id: 'tafsir', label: 'তুলনামূলক তাফসীর', num: '০৫', icon: BookMarked, sec: topics.tafsir_comparative },
    { id: 'hadith', label: 'শানে নুযূল ও হাদীস তাখরীজ', num: '০৬', icon: Sparkles, sec: topics.hadith },
    { id: 'ikhtilaf', label: 'ফিকহী মতভেদ ও তারজীহ', num: '০৭', icon: GitCompare, sec: topics.ikhtilaf },
    { id: 'ahkam', label: 'আহকাম ও ৪ মাযহাব', num: '০৮', icon: Scale, sec: topics.ahkam },
    { id: 'ulumul_quran', label: 'উলূমুল কুরআন', num: '০৯', icon: BookOpen, sec: topics.ulumul_quran },
    { id: 'balaghat', label: 'বালাগাত ও ই\'জায', num: '১০', icon: Feather, sec: topics.balaghat },
    { id: 'samakalin', label: 'সমকালীন প্রাসঙ্গিকতা', num: '১১', icon: HelpCircle, sec: topics.samakalin },
    { id: 'dars', label: 'দরসের উপকরণ', num: '১২', icon: BookOpen, sec: topics.dars },
    { id: 'bibliography', label: 'গ্রন্থপঞ্জি ও রেফারেন্স', num: '১৩', icon: Layers, sec: topics.bibliography },
    { id: 'limitations', label: 'গবেষণার সীমাবদ্ধতা', num: '১৪', icon: Info, sec: topics.limitations },
  ];

  // Filter sections that have meaningful content or tables/cards in this ruku
  const availableSections = allSections.filter(s => {
    if (!s.sec) return false;
    if (s.id === 'qiraat') return true;
    return Boolean(
      s.sec.content || 
      s.sec.summary || 
      (s.sec.cards && s.sec.cards.length > 0) || 
      (s.sec.table && s.sec.table.length > 0)
    );
  });

  // Ensure active tab is valid
  const currentActiveTab = availableSections.some(s => s.id === activeTab)
    ? activeTab
    : (availableSections[0]?.id || 'makasid');

  // Helper: Render individual chapter content
  const renderChapterContent = (item) => {
    if (item.id === 'qiraat') {
      return (
        <QiraatTable 
          tableData={qiraatTableData} 
          title={`রুকু ${toBn(rukuData.ruku_id)}-এর ১০ মুতাওয়াতির কিরাআত সারণি`}
        />
      );
    }

    if (item.id === 'hadith') {
      return (
        <HadithTakhrijSection 
          content={item.sec?.content || item.sec?.summary || ''}
          title={`রুকু ${toBn(rukuData.ruku_id)}-এর শানে নুযূল, সংশ্লিষ্ট ঘটনা ও হাদীসের তাখরীজ`}
        />
      );
    }

    if (item.id === 'ahkam' && item.sec?.cards && item.sec.cards.length > 0) {
      return (
        <div className="space-y-4">
          {item.sec?.intro && (
            <div className="mb-4 p-4 rounded-xl bg-gray-50 dark:bg-gray-750 border border-gray-200 dark:border-gray-700">
              <MarkdownContent content={item.sec.intro} />
            </div>
          )}
          <div className="space-y-4">
            {item.sec.cards.map((card, idx) => (
              <MasalaCard key={idx} card={card} index={idx} />
            ))}
          </div>
        </div>
      );
    }

    if (item.sec?.content || item.sec?.summary) {
      return (
        <div className="prose font-bengali text-sm sm:text-base leading-relaxed text-gray-800 dark:text-gray-200 space-y-3">
          <MarkdownContent content={item.sec.content || item.sec.summary} />
        </div>
      );
    }

    return (
      <div className="text-gray-500 italic py-6 text-center font-bengali text-sm">
        এই রুকুর জন্য এই শাস্ত্রীয় অধ্যায়ের তথ্য সাধারণ বিধানের অন্তর্ভুক্ত।
      </div>
    );
  };

  const scrollToSection = (id) => {
    setActiveTab(id);
    if (readingLayout !== 'continuous') return;
    const el = document.getElementById(`ruku-sec-${id}`);
    if (el) {
      const topOffset = el.getBoundingClientRect().top + window.pageYOffset - 90;
      window.scrollTo({ top: topOffset, behavior: 'smooth' });
    }
  };

  return (
    <div className="w-full max-w-6xl mx-auto px-3 sm:px-6 py-4 sm:py-8 space-y-6 sm:space-y-8 layout-safe">
      {/* 1. Ruku Scope Header Banner */}
      <div className="rounded-2xl sm:rounded-3xl bg-gradient-to-r from-emerald-800 to-teal-900 text-white p-5 sm:p-7 shadow-sm border border-emerald-700/40">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1.5">
            <div className="flex flex-wrap items-center gap-2 text-xs font-semibold">
              <span className="px-2.5 py-0.5 rounded-full bg-white/20 font-mono">
                রুকু {toBn(rukuData.ruku_id)} / {toBn(surahInfo?.ruku_count || 9)}
              </span>
              <span className="text-emerald-200 font-bengali">
                আয়াত {rukuData.ayah_range_bn || `${toBn(rukuData.ayah_start)}–${toBn(rukuData.ayah_end)}`}
              </span>
              <span>•</span>
              <span className="text-gray-200 font-bengali">
                মোট {toBn(rukuData.ayah_count || 10)}টি আয়াত
              </span>
              <span>•</span>
              <span className="text-teal-200 font-bengali font-bold">
                {toBn(availableSections.length)}টি প্রামাণ্য শাস্ত্রীয় অধ্যায়
              </span>
            </div>

            <h1 className="text-xl sm:text-2xl font-bold font-bengali leading-snug">
              রুকু {toBn(rukuData.ruku_id)}-এর বিষয়ভিত্তিক শাস্ত্রীয় আলোচনা ও পূর্ণাঙ্গ তাহকীক
            </h1>
            <p className="text-xs sm:text-sm text-emerald-100 font-bengali">
              মাকাসিদ, ই'রাব, তুলনামূলক তাফসীর, শানে নুযূল ও হাদিস তাখরীজ, ৪ মাযহাবের ফিকহ ও ১০ মুতাওয়াতির কিরাআত
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 self-start sm:self-center">
            {/* Reading Mode Switcher */}
            <div className="flex items-center gap-1 bg-white/15 p-1 rounded-xl text-xs font-semibold backdrop-blur-xs">
              <button
                onClick={() => setReadingLayout('tabbed')}
                className={`px-3 py-1.5 rounded-lg transition-all ${
                  readingLayout === 'tabbed'
                    ? 'bg-white text-emerald-900 font-bold shadow-2xs'
                    : 'text-emerald-100 hover:text-white'
                }`}
                title="অধ্যায়ভিত্তিক একক ট্যাব ভিউ"
              >
                ট্যাবড ভিউ
              </button>
              <button
                onClick={() => setReadingLayout('continuous')}
                className={`px-3 py-1.5 rounded-lg transition-all ${
                  readingLayout === 'continuous'
                    ? 'bg-white text-emerald-900 font-bold shadow-2xs'
                    : 'text-emerald-100 hover:text-white'
                }`}
                title="একটানা জার্নাল প্রবন্ধ ও সূচিপত্র"
              >
                প্রবন্ধ মোড (TOC)
              </button>
            </div>

            {/* External Tafsir.app Link */}
            <a
              href={`https://tafsir.app/${surahInfo?.id || 24}/${rukuData.ayah_start || 1}`}
              target="_blank"
              rel="noopener noreferrer"
              title="الباحث القرآني (tafsir.app)-এ এই রুকুর মূল তাফসীরসমূহ দেখুন"
              className="px-3 py-1.5 rounded-xl bg-white/15 hover:bg-white/25 text-white border border-white/20 text-xs font-semibold backdrop-blur-xs flex items-center justify-center gap-1.5 transition"
            >
              <ExternalLink className="w-3.5 h-3.5 text-emerald-300" />
              <span className="font-arabic text-sm leading-none" dir="rtl">الباحث القرآني</span>
            </a>

            {/* Jump to Ayah Study */}
            <button
              onClick={() => {
                if (onSelectAyah) onSelectAyah(rukuData.ayah_start || 1);
                if (onSwitchToAyahScope) onSwitchToAyahScope();
              }}
              className="px-3.5 py-1.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-white text-xs sm:text-sm font-bold font-bengali flex items-center justify-center gap-1.5 shadow-xs transition"
            >
              <span>আয়াত স্টাডি</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* 2. Reading Layout: Tabbed Mode vs Continuous Journal Mode */}
      {readingLayout === 'tabbed' ? (
        /* TABBED LAYOUT: Pill Navigation + Single Chapter Container */
        <div className="space-y-4">
          {/* Horizontal Scrollable Tabs */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-2 shadow-2xs">
            <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar p-1">
              {availableSections.map((tab) => {
                const Icon = tab.icon;
                const isActive = currentActiveTab === tab.id;

                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-bold font-bengali transition-all whitespace-nowrap shrink-0 ${
                      isActive
                        ? 'bg-emerald-600 text-white shadow-xs'
                        : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700/60'
                    }`}
                  >
                    <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-emerald-600 dark:text-emerald-400'}`} />
                    <span>{tab.label}</span>
                    {tab.count !== undefined && tab.count > 0 && (
                      <span className={`px-1.5 py-0.2 rounded-full text-[10px] font-mono ${
                        isActive ? 'bg-white/20 text-white' : 'bg-emerald-100 dark:bg-emerald-900/60 text-emerald-700 dark:text-emerald-300'
                      }`}>
                        {toBn(tab.count)}
                      </span>
                    )}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Active Chapter Display Container */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-5 sm:p-7 shadow-xs">
            {(() => {
              const activeItem = availableSections.find(s => s.id === currentActiveTab);
              if (!activeItem) return null;

              return (
                <div className="space-y-4">
                  {/* Chapter Header */}
                  <div className="flex items-center justify-between pb-3 border-b border-gray-100 dark:border-gray-700">
                    <div className="flex items-center gap-2">
                      <activeItem.icon className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
                      <h3 className="text-base sm:text-lg font-bold text-gray-900 dark:text-gray-100 font-bengali">
                        {activeItem.sec?.title || activeItem.label}
                      </h3>
                    </div>
                    <span className="text-xs font-mono font-bold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 px-2.5 py-0.5 rounded-full">
                      অধ্যায় {activeItem.num}
                    </span>
                  </div>

                  {/* Chapter Body */}
                  {renderChapterContent(activeItem)}
                </div>
              );
            })()}
          </div>
        </div>
      ) : (
        /* CONTINUOUS JOURNAL LAYOUT: Sticky TOC + Full Paper Stack */
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Sticky Table of Contents (TOC) */}
          <aside className="hidden lg:block lg:col-span-3 sticky top-20 max-h-[calc(100vh-6rem)] overflow-y-auto no-scrollbar space-y-1.5 bg-white dark:bg-gray-800 p-3 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-xs font-bengali">
            <div className="flex items-center gap-2 text-xs font-bold text-gray-600 dark:text-gray-300 pb-2 border-b border-gray-100 dark:border-gray-700">
              <List className="w-4 h-4 text-emerald-600" />
              <span>সূচিপত্র (Quick Index)</span>
            </div>
            {availableSections.map((sec) => (
              <button
                key={sec.id}
                onClick={() => scrollToSection(sec.id)}
                className={`w-full text-left px-2.5 py-1.5 rounded-lg text-xs font-semibold flex items-center justify-between transition ${
                  activeTab === sec.id
                    ? 'bg-emerald-50 dark:bg-emerald-950/50 text-emerald-800 dark:text-emerald-300 font-bold'
                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700/50'
                }`}
              >
                <span className="truncate">{sec.label}</span>
                <span className="font-mono text-[10px] text-gray-400">{sec.num}</span>
              </button>
            ))}
          </aside>

          {/* Full Content Stream */}
          <div className="lg:col-span-9 space-y-6">
            {availableSections.map((sec) => (
              <div 
                key={sec.id} 
                id={`ruku-sec-${sec.id}`}
                className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-5 sm:p-7 shadow-xs space-y-4 font-bengali scroll-mt-24"
              >
                <div className="flex items-center justify-between pb-3 border-b border-gray-100 dark:border-gray-700">
                  <div className="flex items-center gap-2">
                    <sec.icon className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
                    <h3 className="text-base sm:text-lg font-bold text-gray-900 dark:text-gray-100">
                      {sec.sec?.title || sec.label}
                    </h3>
                  </div>
                  <span className="text-xs font-mono font-bold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 px-2.5 py-0.5 rounded-full">
                    অধ্যায় {sec.num}
                  </span>
                </div>

                {renderChapterContent(sec)}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 3. Bottom Ayah Bridge Card */}
      <div className="bg-emerald-50/60 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-800/50 rounded-2xl p-4 sm:p-5 flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="text-center sm:text-left font-bengali">
          <h4 className="font-bold text-sm sm:text-base text-emerald-900 dark:text-emerald-200">
            রুকু {toBn(rukuData.ruku_id)}-এর শাব্দিক তাহকীক ও জালালাইন অধ্যয়নে যেতে চান?
          </h4>
          <p className="text-xs text-emerald-700 dark:text-emerald-400 mt-0.5">
            এই রুকুর আয়াত {rukuData.ayah_range_bn}-এর প্রতিটি শব্দের সরফ, নাহু, কিরাআত ও তাফসীর উন্মুক্ত করুন।
          </p>
        </div>
        <button
          onClick={() => {
            if (onSelectAyah) onSelectAyah(rukuData.ayah_start || 1);
            if (onSwitchToAyahScope) onSwitchToAyahScope();
          }}
          className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs sm:text-sm font-bold font-bengali flex items-center gap-1.5 shadow-xs transition"
        >
          <span>আয়াত স্টাডিতে যান</span>
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}

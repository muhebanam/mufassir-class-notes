import React, { useState, useEffect } from 'react';
import { 
  Scale, Feather, GitCompare, BookMarked, Sparkles, 
  HelpCircle, BookOpen, Layers, CheckCircle2,
  Compass, FileText, ArrowRight
} from 'lucide-react';
import { toBn } from '../utils/helpers';
import MarkdownContent from './MarkdownContent';
import MasalaCard from './MasalaCard';

export default function ThematicView({ rukuData, surahInfo, onSwitchToAyahStudy }) {
  const [activeTab, setActiveTab] = useState('makasid');
  const [viewAllChapters, setViewAllChapters] = useState(false);

  const tabDefs = [
    { id: 'makasid', label: 'ভূমিকা ও মাকাসিদ', icon: Compass, sec: rukuData?.thematic_topics?.makasid, num: 0 },
    { id: 'irab', label: 'ই\'রাব ও নাহব', icon: FileText, sec: rukuData?.thematic_topics?.irab_full, num: 3 },
    { id: 'qiraat', label: '১০ কিরাআত সারণি', icon: BookOpen, sec: rukuData?.thematic_topics?.qiraat_full, num: 4 },
    { id: 'jalalayn', label: 'তুলনামূলক তাফসীর', icon: BookMarked, sec: rukuData?.thematic_topics?.tafsir_comparative, num: 5 },
    { id: 'hadith', label: 'শানে নুযূল ও হাদীস', icon: Sparkles, sec: rukuData?.thematic_topics?.hadith, num: 6 },
    { id: 'ikhtilaf', label: 'মতভেদ ও তারজীহ', icon: GitCompare, sec: rukuData?.thematic_topics?.ikhtilaf, num: 7 },
    { id: 'ahkam', label: 'আহকাম ও ৪ মাযহাব', icon: Scale, sec: rukuData?.thematic_topics?.ahkam, num: 8 },
    { id: 'ulumul_quran', label: 'উলূমুল কুরআন', icon: BookMarked, sec: rukuData?.thematic_topics?.ulumul_quran, num: 9 },
    { id: 'balaghat', label: 'বালাগাত ও ই\'জায', icon: Feather, sec: rukuData?.thematic_topics?.balaghat, num: 10 },
    { id: 'samakalin', label: 'সমকালীন প্রাসঙ্গিকতা', icon: HelpCircle, sec: rukuData?.thematic_topics?.samakalin, num: 11 },
    { id: 'connections', label: 'আন্তঃআয়াত সংযোগ', icon: CheckCircle2, sec: rukuData?.thematic_topics?.connections, num: 12 },
    { id: 'dars', label: 'দরসের উপকরণ', icon: BookOpen, sec: rukuData?.thematic_topics?.dars, num: 13 },
    { id: 'bibliography', label: 'গ্রন্থপঞ্জি ও সূত্র', icon: Layers, sec: rukuData?.thematic_topics?.bibliography, num: 14 },
    { id: 'limitations', label: 'গবেষণার সীমাবদ্ধতা', icon: HelpCircle, sec: rukuData?.thematic_topics?.limitations, num: 15 },
  ];

  // Sync tab with URL query param on mount
  useEffect(() => {
    try {
      const params = new URLSearchParams(window.location.search);
      const tabParam = params.get('tab');
      if (tabParam && tabDefs.some(t => t.id === tabParam)) {
        setActiveTab(tabParam);
      }
    } catch {
      // Fallback if URL parsing fails
    }
  }, []);

  const handleTabChange = (tabId) => {
    setActiveTab(tabId);
    try {
      const url = new URL(window.location.href);
      url.searchParams.set('tab', tabId);
      window.history.replaceState(null, '', url.toString());
    } catch {
      // Ignore if URL update fails
    }
  };

  if (!rukuData || !rukuData.thematic_topics) {
    return (
      <div className="max-w-4xl mx-auto p-12 text-center text-gray-500 font-bengali">
        রুকুর বিষয়ভিত্তিক তথ্য লোড হচ্ছে...
      </div>
    );
  }

  const topics = rukuData.thematic_topics;
  const currentTab = tabDefs.find(t => t.id === activeTab) || tabDefs[0];
  const isNeedsWork = rukuData.status && rukuData.status !== 'gold';

  // Render Qiraat table helper
  const renderQiraatSection = (sec) => {
    if (sec?.table && sec.table.length > 0) {
      return (
        <div className="space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-2 text-xs text-gray-600 dark:text-gray-300 font-bengali">
            <span>মোট কিরাআত পাঠভেদ: <strong className="text-emerald-700 dark:text-emerald-400">{toBn(sec.table.length)}</strong>টি</span>
            <span className="font-semibold text-emerald-800 dark:text-emerald-300">সূত্র: মাদীনা মুনাওয়ারা প্রামাণ্য বাহাউথ ডেটাবেস</span>
          </div>
          <div className="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
            <table className="w-full text-left text-xs sm:text-sm border-collapse">
              <thead className="bg-gray-50 dark:bg-gray-800/80 text-gray-700 dark:text-gray-300 border-b border-gray-200 dark:border-gray-700 font-bengali">
                <tr>
                  <th className="px-3.5 py-2.5 text-center font-bold">আয়াত</th>
                  <th className="px-3.5 py-2.5 font-bold">শব্দ (ক্রম)</th>
                  <th className="px-3.5 py-2.5 font-bold">ক্বারী / রাবী</th>
                  <th className="px-3.5 py-2.5 font-bold">কিরাআতের পাঠভেদ ও নিয়ম (অবিকৃত মূল পাঠ)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 dark:divide-gray-700/60 bg-white dark:bg-gray-800">
                {sec.table.map((row, rIdx) => (
                  <tr key={rIdx} className="hover:bg-gray-50/70 dark:hover:bg-gray-700/40 transition-colors">
                    <td className="px-3.5 py-2.5 text-center font-mono font-semibold text-emerald-700 dark:text-emerald-400 whitespace-nowrap">
                      <MarkdownContent inline content={row['আয়াত'] || ''} />
                    </td>
                    <td className="px-3.5 py-2.5 whitespace-nowrap text-right font-arabic" dir="rtl">
                      <MarkdownContent inline content={row['শব্দ (ক্রম)'] || ''} />
                    </td>
                    <td className="px-3.5 py-2.5 font-medium whitespace-nowrap text-right font-arabic" dir="rtl">
                      <MarkdownContent inline content={row['ক্বারী / রাবী (বাহাউথ)'] || ''} />
                    </td>
                    <td className="px-3.5 py-2.5 leading-relaxed font-arabic text-right" dir="rtl">
                      <MarkdownContent inline content={row['কিরাআতের পাঠভেদ ও নিয়ম (অবিকৃত মূল পাঠ)'] || ''} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      );
    }
    if (sec?.content) {
      return <MarkdownContent content={sec.content} />;
    }
    return (
      <div className="text-gray-500 italic py-6 text-center font-bengali text-sm">
        এই রুকুর জন্য এই শাস্ত্রীয় অধ্যায়ের তথ্য সংকলনাধীন বা সাধারণ বিধানের অন্তর্ভুক্ত।
      </div>
    );
  };

  // Section content dispatcher
  const renderSectionBody = (tabItem) => {
    if (tabItem.id === 'ahkam' && tabItem.sec?.cards && tabItem.sec.cards.length > 0) {
      return (
        <div className="space-y-4">
          {tabItem.sec?.intro && (
            <div className="mb-6 p-4 rounded-xl bg-gray-50 dark:bg-gray-700/60 border border-gray-200 dark:border-gray-700">
              <MarkdownContent content={tabItem.sec.intro} />
            </div>
          )}
          <div className="space-y-4">
            {tabItem.sec.cards.map((card, idx) => (
              <MasalaCard key={idx} card={card} index={idx} />
            ))}
          </div>
        </div>
      );
    }

    if (tabItem.id === 'qiraat') {
      return renderQiraatSection(tabItem.sec);
    }

    if (tabItem.sec?.content) {
      return <MarkdownContent content={tabItem.sec.content} />;
    }

    return (
      <div className="text-gray-500 italic py-6 text-center font-bengali text-sm">
        এই রুকুর জন্য এই শাস্ত্রীয় অধ্যায়ের তথ্য সংকলনাধীন বা সাধারণ বিধানের অন্তর্ভুক্ত।
      </div>
    );
  };

  return (
    <div className="max-w-7xl mx-auto px-3 sm:px-4 py-4 space-y-5">
      {/* Ruku Header & Overview Card */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl p-4 sm:p-5 shadow-sm border border-gray-200 dark:border-gray-700 border-l-4 border-l-emerald-600 transition-colors">
        <div className="flex flex-wrap items-center justify-between gap-2 mb-1">
          <div className="flex items-center gap-2 text-emerald-700 dark:text-emerald-400 text-xs font-bold uppercase tracking-wider">
            <span>সূরা {surahInfo?.name_bn}</span>
            <span>•</span>
            <span>রুকু {toBn(rukuData.ruku_id)}</span>
            <span>•</span>
            <span>আয়াত {rukuData.ayah_range_bn}</span>
          </div>

          {isNeedsWork && (
            <span className="px-2.5 py-0.5 rounded-full bg-amber-100 dark:bg-amber-950/70 text-amber-800 dark:text-amber-300 text-xs font-semibold border border-amber-300 dark:border-amber-800 font-bengali">
              সম্পাদনা ও হালনাগাদ চলমান
            </span>
          )}
        </div>

        <h2 className="text-base sm:text-xl font-bold font-bengali tracking-tight text-gray-900 dark:text-gray-100">
          {topics.makasid?.title || `রুকু ${toBn(rukuData.ruku_id)}-এর সার্বিক শাস্ত্রীয় বিশ্লেষণ`}
        </h2>

        {topics.makasid?.summary && (
          <p className="mt-1.5 text-xs sm:text-sm text-gray-600 dark:text-gray-300 leading-relaxed font-bengali line-clamp-3">
            {topics.makasid.summary}
          </p>
        )}
      </div>

      {/* Main Layout: Fixed 280px Desktop Sidebar + Flexible Content Pane */}
      <div className="grid grid-cols-1 lg:grid-cols-[280px_minmax(0,1fr)] gap-6 items-start">
        {/* Mobile / Tablet Controls (< lg) */}
        <div className="lg:hidden space-y-2.5">
          {/* Quick Select & View Mode Toggle */}
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2 bg-gray-50 dark:bg-gray-800 p-2.5 rounded-xl border border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-2 flex-1 min-w-0">
              <span className="text-xs font-bold text-gray-700 dark:text-gray-300 shrink-0 font-bengali">অধ্যায়:</span>
              <select
                value={activeTab}
                onChange={(e) => {
                  handleTabChange(e.target.value);
                  if (viewAllChapters) {
                    const el = document.getElementById(`section-${e.target.value}`);
                    if (el) el.scrollIntoView({ behavior: 'smooth' });
                  }
                }}
                aria-label="অধ্যায় নির্বাচন"
                className="flex-1 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-xs font-semibold rounded-lg px-2 py-1.5 border border-gray-200 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-emerald-500 truncate"
              >
                {tabDefs.map((t) => (
                  <option key={t.id} value={t.id}>
                    {toBn(t.num)}. {t.label}
                  </option>
                ))}
              </select>
            </div>

            <button
              onClick={() => setViewAllChapters(!viewAllChapters)}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center justify-center gap-1.5 shrink-0 ${viewAllChapters
                ? 'bg-emerald-600 text-white shadow-sm'
                : 'bg-emerald-50 dark:bg-emerald-950/50 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800'
                }`}
            >
              <Layers className="w-3.5 h-3.5" />
              <span>{viewAllChapters ? "অধ্যায়ভিত্তিক দেখুন" : "সব অধ্যায় একসাথে প্রকাশ"}</span>
            </button>
          </div>

          {/* Horizontal scroll pills */}
          {!viewAllChapters && (
            <div role="tablist" aria-label="মোবাইল অধ্যায় তালিকা" className="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-1">
              {tabDefs.map((t) => {
                const Icon = t.icon;
                const isActive = activeTab === t.id;
                return (
                  <button
                    key={t.id}
                    role="tab"
                    id={`mobile-tab-${t.id}`}
                    aria-selected={isActive}
                    aria-controls={`panel-${t.id}`}
                    onClick={() => handleTabChange(t.id)}
                    className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-semibold transition shrink-0 ${isActive
                      ? 'bg-emerald-600 text-white shadow-sm ring-2 ring-emerald-400/30'
                      : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-emerald-50 dark:hover:bg-gray-700 border border-gray-200 dark:border-gray-700'
                      }`}
                  >
                    <Icon className="w-3.5 h-3.5" />
                    <span>{t.label}</span>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        {/* Desktop Table of Contents Sidebar (>= lg) */}
        {viewAllChapters ? (
          <nav
            aria-label="সূচিপত্র অধ্যায় তালিকা"
            className="hidden lg:block sticky top-20 bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-3 shadow-sm space-y-2 max-h-[calc(100vh-6rem)] overflow-y-auto"
          >
            <div className="flex items-center justify-between px-3 py-1 border-b border-gray-100 dark:border-gray-700/60 pb-2">
              <span className="text-xs font-bold uppercase tracking-wider text-gray-500 dark:text-gray-400">
                সূচিপত্র (অধ্যায় ০, ৩–১৫)
              </span>
              <button
                onClick={() => setViewAllChapters(false)}
                className="text-[11px] px-2 py-0.5 rounded font-bold transition bg-emerald-600 text-white"
              >
                একক ভিউ
              </button>
            </div>

            {/* Quick links to Chapter 1 & 2 */}
            {onSwitchToAyahStudy && (
              <div className="px-3 py-1.5 bg-gray-50 dark:bg-gray-700/40 rounded-xl border border-gray-200/60 dark:border-gray-700/60 text-xs text-gray-600 dark:text-gray-300 font-bengali space-y-1">
                <div className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">আয়াত ও শব্দার্থ:</div>
                <button
                  onClick={onSwitchToAyahStudy}
                  className="w-full flex items-center justify-between text-left hover:text-emerald-600 transition"
                >
                  <span>১. আয়াত ও ২. মুফরাদাত</span>
                  <ArrowRight className="w-3 h-3" />
                </button>
              </div>
            )}

            <div className="space-y-1">
              {tabDefs.map((t) => {
                const Icon = t.icon;
                return (
                  <button
                    key={t.id}
                    onClick={() => {
                      const el = document.getElementById(`section-${t.id}`);
                      if (el) el.scrollIntoView({ behavior: 'smooth' });
                    }}
                    className="w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs sm:text-sm font-semibold transition text-left text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50"
                  >
                    <div className="flex items-center gap-2.5 truncate">
                      <Icon className="w-4 h-4 shrink-0 text-gray-400" />
                      <span className="truncate">{t.label}</span>
                    </div>
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-gray-100 dark:bg-gray-700 text-gray-500">
                      {toBn(t.num)}
                    </span>
                  </button>
                );
              })}
            </div>
          </nav>
        ) : (
          <aside
            role="tablist"
            aria-label="সূচিপত্র অধ্যায় তালিকা"
            className="hidden lg:block sticky top-20 bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-3 shadow-sm space-y-2 max-h-[calc(100vh-6rem)] overflow-y-auto"
          >
            <div className="flex items-center justify-between px-3 py-1 border-b border-gray-100 dark:border-gray-700/60 pb-2">
              <span className="text-xs font-bold uppercase tracking-wider text-gray-500 dark:text-gray-400">
                সূচিপত্র (অধ্যায় ০, ৩–১৫)
              </span>
              <button
                onClick={() => setViewAllChapters(true)}
                className="text-[11px] px-2 py-0.5 rounded font-bold transition bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200"
              >
                সব অধ্যায় একসাথে
              </button>
            </div>

            {/* Quick links to Chapter 1 & 2 */}
            {onSwitchToAyahStudy && (
              <div className="px-3 py-1.5 bg-gray-50 dark:bg-gray-700/40 rounded-xl border border-gray-200/60 dark:border-gray-700/60 text-xs text-gray-600 dark:text-gray-300 font-bengali space-y-1">
                <div className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">আয়াত ও শব্দার্থ:</div>
                <button
                  onClick={onSwitchToAyahStudy}
                  className="w-full flex items-center justify-between text-left hover:text-emerald-600 transition"
                >
                  <span>১. আয়াত ও ২. মুফরাদাত</span>
                  <ArrowRight className="w-3 h-3" />
                </button>
              </div>
            )}

            <div className="space-y-1">
              {tabDefs.map((t) => {
                const Icon = t.icon;
                const isActive = activeTab === t.id;
                return (
                  <button
                    key={t.id}
                    role="tab"
                    id={`tab-${t.id}`}
                    aria-selected={isActive}
                    aria-controls={`panel-${t.id}`}
                    onClick={() => handleTabChange(t.id)}
                    className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition text-left ${isActive
                      ? 'bg-emerald-50 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300 border-l-4 border-emerald-600 font-bold'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50'
                      }`}
                  >
                    <div className="flex items-center gap-2.5 truncate">
                      <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-emerald-600 dark:text-emerald-400' : 'text-gray-400'}`} />
                      <span className="truncate">{t.label}</span>
                    </div>
                    <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${isActive ? 'bg-emerald-200 dark:bg-emerald-900 text-emerald-900 dark:text-emerald-200' : 'bg-gray-100 dark:bg-gray-700 text-gray-500'}`}>
                      {toBn(t.num)}
                    </span>
                  </button>
                );
              })}
            </div>
          </aside>
        )}

        {/* Content Reading Area */}
        <main className="w-full min-w-0 bg-white dark:bg-gray-800 rounded-2xl p-4 sm:p-7 shadow-sm border border-gray-200 dark:border-gray-700 transition-colors">
          {viewAllChapters ? (
            <div className="space-y-10">
              {tabDefs.map((t) => {
                const Icon = t.icon;
                return (
                  <section key={t.id} id={`section-${t.id}`} className="scroll-mt-24 pb-8 border-b border-gray-200 dark:border-gray-700 last:border-b-0 last:pb-0">
                    <div className="flex items-center justify-between pb-3 mb-5 border-b border-gray-100 dark:border-gray-700">
                      <h3 className="text-base sm:text-xl font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2.5 font-bengali">
                        <Icon className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0" />
                        <span>{t.sec?.title || t.label}</span>
                      </h3>
                      <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 font-semibold font-bengali shrink-0">
                        অধ্যায় {toBn(t.sec?.sec_id ?? t.num)}
                      </span>
                    </div>

                    <div className="w-full">
                      {renderSectionBody(t)}
                    </div>
                  </section>
                );
              })}
            </div>
          ) : (
            <div role="tabpanel" id={`panel-${currentTab.id}`} aria-labelledby={`tab-${currentTab.id}`} className="w-full">
              {/* Header of Active Section */}
              <div className="flex items-center justify-between pb-3.5 mb-5 border-b border-gray-100 dark:border-gray-700">
                <h3 className="text-base sm:text-xl font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2.5 font-bengali">
                  <currentTab.icon className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0" />
                  <span>{currentTab.sec?.title || currentTab.label}</span>
                </h3>
                <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 font-semibold font-bengali shrink-0">
                  অধ্যায় {toBn(currentTab.sec?.sec_id ?? currentTab.num)}
                </span>
              </div>

              {/* Section Body */}
              <div className="w-full">
                {renderSectionBody(currentTab)}
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

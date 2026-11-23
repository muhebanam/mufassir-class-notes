import React, { useState } from 'react';
import { 
  Scale, Feather, GitCompare, BookMarked, Sparkles, 
  HelpCircle, BookOpen, Layers, CheckCircle2, ChevronDown, 
  ChevronUp, Compass, FileText, Bookmark, Share2 
} from 'lucide-react';
import { toBn } from '../utils/helpers';
import MarkdownContent from './MarkdownContent';
import MasalaCard from './MasalaCard';

export default function ThematicView({ rukuData, surahInfo }) {
  const [activeTab, setActiveTab] = useState('ahkam');
  const [showFullMakasid, setShowFullMakasid] = useState(false);

  if (!rukuData || !rukuData.thematic_topics) {
    return (
      <div className="max-w-4xl mx-auto p-12 text-center text-gray-500 font-bengali">
        রুকুর বিষয়ভিত্তিক তথ্য লোড হচ্ছে...
      </div>
    );
  }

  const topics = rukuData.thematic_topics;

  const tabDefs = [
    { id: 'makasid', label: '০. ভূমিকা ও মাকাসিদ', icon: Compass, sec: topics.makasid, num: 0 },
    { id: 'irab', label: '৩. ই\'রাব ও নাহব', icon: FileText, sec: topics.irab_full, num: 3 },
    { id: 'qiraat', label: '৪. ১০ কিরাআত সারণি', icon: BookOpen, sec: topics.qiraat_full, num: 4 },
    { id: 'jalalayn', label: '৫. তুলনামূলক তাফসীর', icon: BookMarked, sec: topics.tafsir_comparative, num: 5 },
    { id: 'hadith', label: '৬. শানে নুযূল ও হাদীস', icon: Sparkles, sec: topics.hadith, num: 6 },
    { id: 'ikhtilaf', label: '৭. মতভেদ ও তারজীহ', icon: GitCompare, sec: topics.ikhtilaf, num: 7 },
    { id: 'ahkam', label: '৮. আহকাম ও ৪ মাযহাব', icon: Scale, sec: topics.ahkam, num: 8 },
    { id: 'ulumul_quran', label: '৯. উলূমুল কুরআন', icon: BookMarked, sec: topics.ulumul_quran, num: 9 },
    { id: 'balaghat', label: '১০. বালাগাত ও ই\'জায', icon: Feather, sec: topics.balaghat, num: 10 },
    { id: 'samakalin', label: '১১. সমকালীন প্রাসঙ্গিকতা', icon: HelpCircle, sec: topics.samakalin, num: 11 },
    { id: 'connections', label: '১২. আন্তঃআয়াত সংযোগ', icon: CheckCircle2, sec: topics.connections, num: 12 },
    { id: 'dars', label: '১৩. দরসের উপকরণ', icon: BookOpen, sec: topics.dars, num: 13 },
    { id: 'bibliography', label: '১৪. গ্রন্থপঞ্জি ও সূত্র', icon: Layers, sec: topics.bibliography, num: 14 },
    { id: 'limitations', label: '১৫. গবেষণার সীমাবদ্ধতা', icon: HelpCircle, sec: topics.limitations, num: 15 },
  ];

  const currentTab = tabDefs.find(t => t.id === activeTab) || tabDefs[6];

  return (
    <div className="max-w-7xl mx-auto px-3 sm:px-4 py-4 space-y-5">
      {/* Ruku Header & Summary Card */}
      <div className="bg-gradient-to-r from-emerald-800 via-teal-850 to-teal-900 text-white rounded-2xl p-5 sm:p-7 shadow-md">
        <div className="flex items-center gap-2 text-emerald-200 text-xs font-semibold uppercase tracking-wider mb-1.5">
          <span>সূরা {surahInfo?.name_bn}</span>
          <span>•</span>
          <span>রুকু {toBn(rukuData.ruku_id)}</span>
          <span>•</span>
          <span>আয়াত {rukuData.ayah_range_bn}</span>
        </div>
        <h2 className="text-xl sm:text-2xl font-bold font-bengali tracking-tight">
          {topics.makasid?.title || `রুকু ${toBn(rukuData.ruku_id)}-এর সার্বিক শাস্ত্রীয় বিশ্লেষণ`}
        </h2>

        {/* Clean First-Paragraph Summary */}
        {topics.makasid?.summary ? (
          <div className="mt-3.5 text-sm sm:text-base text-emerald-50/95 leading-relaxed font-bengali">
            <p>{topics.makasid.summary}</p>
          </div>
        ) : topics.makasid?.content ? (
          <div className="mt-3.5 text-sm text-emerald-100/90 leading-relaxed font-bengali">
            <p>{topics.makasid.content.split('\n\n')[0]}</p>
          </div>
        ) : null}

        {/* Expandable Full Makasid Section */}
        {topics.makasid?.content && (
          <div className="mt-4 pt-3 border-t border-emerald-700/60">
            <button
              onClick={() => setShowFullMakasid(!showFullMakasid)}
              className="inline-flex items-center gap-1.5 text-xs sm:text-sm font-semibold text-emerald-200 hover:text-white transition"
            >
              <span>{showFullMakasid ? "মাকাসিদ সংক্ষেপ করুন" : "সম্পূর্ণ ভূমিকা ও মাকাসিদ বিস্তারিত পড়ুন"}</span>
              {showFullMakasid ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>

            {showFullMakasid && (
              <div className="mt-4 p-4 rounded-xl bg-black/20 text-emerald-100 text-sm leading-relaxed max-h-96 overflow-y-auto">
                <MarkdownContent content={topics.makasid.content} className="text-emerald-100 dark:text-emerald-100" />
              </div>
            )}
          </div>
        )}
      </div>

      {/* Main Layout: Desktop Sidebar (Left) + Content (Center/Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
        {/* Mobile / Tablet Horizontal Navigation (< lg) */}
        <div className="lg:hidden col-span-1 flex items-center gap-1.5 overflow-x-auto no-scrollbar py-1">
          {tabDefs.map((t) => {
            const Icon = t.icon;
            const isActive = activeTab === t.id;
            return (
              <button
                key={t.id}
                onClick={() => setActiveTab(t.id)}
                className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-semibold transition shrink-0 ${
                  isActive
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

        {/* Desktop Sticky Table of Contents Sidebar (>= lg) */}
        <aside className="hidden lg:block lg:col-span-4 sticky top-20 bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-3 shadow-xs space-y-1 max-h-[calc(100vh-6rem)] overflow-y-auto">
          <div className="px-3 py-2 text-xs font-bold uppercase tracking-wider text-gray-500 dark:text-gray-400 border-b border-gray-100 dark:border-gray-700/60 mb-1">
            এই রুকুর সূচিপত্র (অধ্যায় ০–১৫)
          </div>
          {tabDefs.map((t) => {
            const Icon = t.icon;
            const isActive = activeTab === t.id;
            return (
              <button
                key={t.id}
                onClick={() => setActiveTab(t.id)}
                className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition text-left ${
                  isActive
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
        </aside>

        {/* Active Content Reading Area */}
        <main className="col-span-1 lg:col-span-8 bg-white dark:bg-gray-800 rounded-2xl p-5 sm:p-7 shadow-xs border border-gray-200 dark:border-gray-700 transition-colors">
          {/* Header of Active Section */}
          <div className="flex items-center justify-between pb-3.5 mb-5 border-b border-gray-100 dark:border-gray-700">
            <h3 className="text-lg sm:text-xl font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2.5 font-bengali">
              <currentTab.icon className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
              <span>{currentTab.sec?.title || currentTab.label}</span>
            </h3>
            <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 font-semibold font-bengali">
              অধ্যায় {toBn(currentTab.sec?.sec_id ?? currentTab.num)}
            </span>
          </div>

          {/* Section Body */}
          <div className="max-w-[72ch]">
            {/* If Section 8 Ahkam has Mas'ala Cards, render structured cards */}
            {activeTab === 'ahkam' && currentTab.sec?.cards && currentTab.sec.cards.length > 0 ? (
              <div className="space-y-4">
                {currentTab.sec?.intro && (
                  <div className="mb-6 p-4 rounded-xl bg-gray-50 dark:bg-gray-750 border border-gray-200 dark:border-gray-700">
                    <MarkdownContent content={currentTab.sec.intro} />
                  </div>
                )}

                <div className="space-y-4">
                  {currentTab.sec.cards.map((card, idx) => (
                    <MasalaCard key={idx} card={card} index={idx} />
                  ))}
                </div>
              </div>
            ) : currentTab.sec?.content ? (
              /* Standard Rich Markdown Rendering */
              <MarkdownContent content={currentTab.sec.content} />
            ) : (
              <div className="text-gray-500 italic py-12 text-center font-bengali">
                এই রুকুতে এই শাস্ত্রীয় বিষয়টি বিশেষ কোনো মতভেদ ব্যতীত সাধারণ বিধানের অন্তর্ভুক্ত।
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}

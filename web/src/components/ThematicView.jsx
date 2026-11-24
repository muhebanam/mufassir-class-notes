import React, { useState, useEffect, useRef } from 'react';
import { 
  Scale, Feather, GitCompare, BookMarked, Sparkles, 
  HelpCircle, BookOpen, Layers, CheckCircle2,
  Compass, FileText, ArrowRight, List, BookCheck, Bookmark
} from 'lucide-react';
import { toBn } from '../utils/helpers';
import MarkdownContent, { normalizeQuranBrackets } from './MarkdownContent';
import MasalaCard from './MasalaCard';

export default function ThematicView({ rukuData, surahInfo, onSwitchToAyahStudy }) {
  // Mode: 'continuous' (Journal Article with Sticky TOC) or 'tabbed' (Single chapter focus)
  const [readingLayout, setReadingLayout] = useState('continuous'); 
  const [activeSectionId, setActiveSectionId] = useState('makasid');
  const sectionRefs = useRef({});

  const sections = [
    { id: 'makasid', label: 'ভূমিকা ও মাকাসিদ', num: '০০', icon: Compass, sec: rukuData?.thematic_topics?.makasid },
    { id: 'irab', label: 'ই\'রাব ও নাহব', num: '০৩', icon: FileText, sec: rukuData?.thematic_topics?.irab_full },
    { id: 'qiraat', label: '১০ কিরাআত সারণি', num: '০৪', icon: BookOpen, sec: rukuData?.thematic_topics?.qiraat_full },
    { id: 'jalalayn', label: 'তুলনামূলক তাফসীর', num: '০৫', icon: BookMarked, sec: rukuData?.thematic_topics?.tafsir_comparative },
    { id: 'hadith', label: 'শানে নুযূল ও হাদীস', num: '০৬', icon: Sparkles, sec: rukuData?.thematic_topics?.hadith },
    { id: 'ikhtilaf', label: 'মতভেদ ও তারজীহ', num: '০৭', icon: GitCompare, sec: rukuData?.thematic_topics?.ikhtilaf },
    { id: 'ahkam', label: 'আহকাম ও ৪ মাযহাব', num: '০৮', icon: Scale, sec: rukuData?.thematic_topics?.ahkam },
    { id: 'ulumul_quran', label: 'উলূমুল কুরআন', num: '০৯', icon: BookMarked, sec: rukuData?.thematic_topics?.ulumul_quran },
    { id: 'balaghat', label: 'বালাগাত ও ই\'জায', num: '১০', icon: Feather, sec: rukuData?.thematic_topics?.balaghat },
    { id: 'samakalin', label: 'সমকালীন প্রাসঙ্গিকতা', num: '১১', icon: HelpCircle, sec: rukuData?.thematic_topics?.samakalin },
    { id: 'connections', label: 'আন্তঃআয়াত সংযোগ', num: '১২', icon: CheckCircle2, sec: rukuData?.thematic_topics?.connections },
    { id: 'dars', label: 'দরসের উপকরণ', num: '১৩', icon: BookOpen, sec: rukuData?.thematic_topics?.dars },
    { id: 'bibliography', label: 'গ্রন্থপঞ্জি ও সূত্র', num: '১৪', icon: Layers, sec: rukuData?.thematic_topics?.bibliography },
    { id: 'limitations', label: 'গবেষণার সীমাবদ্ধতা', num: '১৫', icon: HelpCircle, sec: rukuData?.thematic_topics?.limitations },
  ].filter(s => s.sec && (s.sec.content || (s.sec.cards && s.sec.cards.length > 0) || (s.sec.table && s.sec.table.length > 0)));

  // Scroll Spy for Sticky Table of Contents
  useEffect(() => {
    if (readingLayout !== 'continuous') return;

    const handleScroll = () => {
      const scrollPosition = window.scrollY + 200;
      for (let i = sections.length - 1; i >= 0; i--) {
        const item = sections[i];
        const el = document.getElementById(`sec-${item.id}`);
        if (el && el.offsetTop <= scrollPosition) {
          setActiveSectionId(item.id);
          break;
        }
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, [readingLayout, sections]);

  const scrollToSection = (id) => {
    setActiveSectionId(id);
    if (readingLayout !== 'continuous') {
      return;
    }
    const el = document.getElementById(`sec-${id}`);
    if (el) {
      const topOffset = el.getBoundingClientRect().top + window.pageYOffset - 90;
      window.scrollTo({ top: topOffset, behavior: 'smooth' });
    }
  };

  if (!rukuData || !rukuData.thematic_topics) {
    return (
      <div className="max-w-4xl mx-auto p-12 text-center text-gray-500 font-bengali">
        রুকুর শাস্ত্রীয় আলোচনা লোড হচ্ছে...
      </div>
    );
  }

  // Render Qiraat table helper
  const renderQiraatSection = (sec) => {
    if (sec?.table && sec.table.length > 0) {
      return (
        <div className="space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-2 text-xs text-gray-600 dark:text-gray-300 font-bengali">
            <span>মোট কিরাআত পাঠভেদ: <strong className="text-emerald-700 dark:text-emerald-400">{toBn(sec.table.length)}</strong>টি</span>
            <span className="font-semibold text-emerald-800 dark:text-emerald-300">সূত্র: মাদীনা মুনাওয়ারা প্রামাণ্য বাহাউথ ডেটাবেস</span>
          </div>
          <div className="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700 shadow-xs">
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
                      <span className="font-arabic text-sm sm:text-base leading-relaxed" dir="rtl">
                        {normalizeQuranBrackets(row['শব্দ (ক্রম)'] || '')}
                      </span>
                    </td>
                    <td className="px-3.5 py-2.5 font-medium whitespace-nowrap text-right font-arabic" dir="rtl">
                      <span className="font-arabic text-sm sm:text-base" dir="rtl">
                        {row['ক্বারী / রাবী (বাহাউথ)'] || ''}
                      </span>
                    </td>
                    <td className="px-3.5 py-2.5 leading-relaxed font-arabic text-right" dir="rtl">
                      <span className="font-arabic text-sm sm:text-base leading-loose" dir="rtl">
                        {row['কিরাআতের পাঠভেদ ও নিয়ম (অবিকৃত মূল পাঠ)'] || ''}
                      </span>
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
        এই রুকুর জন্য এই শাস্ত্রীয় অধ্যায়ের তথ্য সাধারণ বিধানের অন্তর্ভুক্ত।
      </div>
    );
  };

  // Section content dispatcher
  const renderSectionContent = (item) => {
    if (item.id === 'ahkam' && item.sec?.cards && item.sec.cards.length > 0) {
      return (
        <div className="space-y-4">
          {item.sec?.intro && (
            <div className="mb-4 p-4 rounded-xl bg-gray-50 dark:bg-gray-700/40 border border-gray-200 dark:border-gray-700">
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

    if (item.id === 'qiraat') {
      return renderQiraatSection(item.sec);
    }

    if (item.sec?.content) {
      return <MarkdownContent content={item.sec.content} />;
    }

    return (
      <div className="text-gray-500 italic py-4 text-center font-bengali text-sm">
        তথ্য সংকলনাধীন বা পরবর্তী অংশে অন্তর্ভুক্ত।
      </div>
    );
  };

  return (
    <div className="max-w-7xl mx-auto px-3 sm:px-6 py-6">
      {/* 1. Scholarly Paper Header & Layout Switcher */}
      <div className="max-w-[740px] mx-auto mb-8 space-y-4">
        {/* Ruku Banner */}
        <div className="bg-white dark:bg-gray-800 rounded-3xl p-5 sm:p-7 shadow-xs border border-gray-200/90 dark:border-gray-700 border-l-4 border-l-emerald-600 transition-colors">
          <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
            <span className="text-emerald-800 dark:text-emerald-400 font-bold text-xs uppercase tracking-wider">
              সূরা {surahInfo?.name_bn} ({toBn(surahInfo?.id || '')})
            </span>
            <div className="flex items-center gap-1.5">
              <span className="bg-emerald-100 dark:bg-emerald-950/80 text-emerald-900 dark:text-emerald-300 px-2.5 py-0.5 rounded-full text-xs font-bold">
                রুকু {toBn(rukuData.ruku_id)}
              </span>
              <span className="bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 px-2.5 py-0.5 rounded-full text-xs font-semibold">
                আয়াত {rukuData.ayah_range_bn}
              </span>
            </div>
          </div>

          <h1 className="text-xl sm:text-2xl font-bold text-gray-900 dark:text-gray-100 font-bengali leading-snug">
            রুকু ভিত্তিক সামগ্রিক শাস্ত্র-আলোচনা ও তাহকীক
          </h1>
          <p className="text-xs sm:text-sm text-gray-600 dark:text-gray-400 font-bengali mt-1">
            মাকাসিদ, নাহব, ১০ কিরাআত, চার মাযহাবের ফিকহ, উলূমুল কুরআন ও সমকালীন প্রাসঙ্গিকতার সমন্বিত পাঠ।
          </p>

          {/* Quick Action to jump to Ayah Study */}
          <div className="mt-4 pt-4 border-t border-gray-100 dark:border-gray-700/60 flex flex-wrap items-center justify-between gap-2">
            <button
              onClick={onSwitchToAyahStudy}
              className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-700 dark:text-emerald-400 hover:text-emerald-800 transition"
            >
              <span>আয়াতভিত্তিক বিশদ স্টাডি ভিউতে যান</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>

            {/* Layout Mode Toggler */}
            <div className="flex items-center gap-1 bg-gray-100 dark:bg-gray-700/60 p-1 rounded-xl text-xs font-semibold">
              <button
                onClick={() => setReadingLayout('continuous')}
                className={`px-3 py-1 rounded-lg transition ${
                  readingLayout === 'continuous'
                    ? 'bg-white dark:bg-gray-800 text-emerald-800 dark:text-emerald-300 shadow-2xs font-bold'
                    : 'text-gray-600 dark:text-gray-300'
                }`}
                title="একটানা জার্নাল প্রবন্ধ ও স্টিকি সূচিপত্র"
              >
                প্রবন্ধ মোড (TOC সহ)
              </button>
              <button
                onClick={() => setReadingLayout('tabbed')}
                className={`px-3 py-1 rounded-lg transition ${
                  readingLayout === 'tabbed'
                    ? 'bg-white dark:bg-gray-800 text-emerald-800 dark:text-emerald-300 shadow-2xs font-bold'
                    : 'text-gray-600 dark:text-gray-300'
                }`}
                title="অধ্যায়ভিত্তিক একক ট্যাব"
              >
                ট্যাবড ভিউ
              </button>
            </div>
          </div>
        </div>

        {/* 2. সারসংক্ষেপ বক্স (Abstract / Academic Callout Box) */}
        <div className="academic-callout shadow-xs space-y-2">
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-900 dark:text-emerald-300 font-bengali uppercase tracking-wide">
            <Bookmark className="w-4 h-4 text-emerald-700 dark:text-emerald-400" />
            <span>রুকুর কেন্দ্রীয় ভাব ও মূল সারসংক্ষেপ (Executive Abstract)</span>
          </div>
          <div className="text-xs sm:text-sm leading-relaxed text-gray-800 dark:text-gray-200 font-bengali">
            এই রুকুতে ওহীর প্রামাণিকতা, তাওহীদের গভীর তত্ত্ব, শরয়ী বিধানের হিকমত এবং আখেরাতের প্রতিদানের শাস্ত্রীয় রূপরেখা নিখুঁতভাবে উপস্থাপিত হয়েছে। নিম্নোক্ত অধ্যায়সমূহে প্রামাণ্য সনদের ভিত্তিতে প্রতিটি আয়াতের বিশদ ব্যাখ্যা বিশ্লেষিত হলো।
          </div>
        </div>
      </div>

      {/* 3. Main Reading Area with Sticky TOC */}
      {readingLayout === 'continuous' ? (
        /* Journal Article Layout with Sticky Sidebar TOC */
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-8 items-start">
          {/* Sticky Table of Contents (TOC) on Desktop (xl+) */}
          <aside className="hidden xl:block xl:col-span-3 sticky top-20 max-h-[calc(100vh-6rem)] overflow-y-auto no-scrollbar space-y-2 pr-2">
            <div className="flex items-center gap-2 text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider px-2 pb-1 border-b border-gray-200 dark:border-gray-700">
              <List className="w-4 h-4 text-emerald-600" />
              <span>সূচিপত্র (TOC)</span>
            </div>
            <nav className="space-y-1">
              {sections.map((item) => {
                const isActive = activeSectionId === item.id;
                const Icon = item.icon;
                return (
                  <button
                    key={item.id}
                    onClick={() => scrollToSection(item.id)}
                    className={`w-full text-left px-3 py-2 rounded-xl text-xs font-medium flex items-center justify-between transition ${
                      isActive
                        ? 'bg-emerald-600 text-white font-bold shadow-xs'
                        : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-gray-200'
                    }`}
                  >
                    <span className="flex items-center gap-2 truncate">
                      <Icon className="w-3.5 h-3.5 shrink-0" />
                      <span className="truncate">{item.label}</span>
                    </span>
                    <span className={`text-[10px] font-mono px-1 rounded ${
                      isActive ? 'bg-white/20 text-white' : 'text-gray-400'
                    }`}>
                      {item.num}
                    </span>
                  </button>
                );
              })}
            </nav>
          </aside>

          {/* Main Academic Reading Column (Constrained to 680px-740px) */}
          <main className="xl:col-span-9 max-w-[740px] mx-auto w-full space-y-10">
            {sections.map((item) => {
              const Icon = item.icon;
              return (
                <section
                  key={item.id}
                  id={`sec-${item.id}`}
                  className="bg-white dark:bg-gray-800 rounded-3xl p-6 sm:p-9 shadow-xs border border-gray-200/90 dark:border-gray-700 transition-colors scroll-mt-24"
                >
                  {/* Chapter Section Title */}
                  <div className="flex items-center justify-between pb-3 mb-5 border-b border-gray-100 dark:border-gray-700/60">
                    <div className="flex items-center gap-2.5 text-base sm:text-lg font-bold text-gray-900 dark:text-gray-100 font-bengali">
                      <div className="w-8 h-8 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 flex items-center justify-center text-emerald-700 dark:text-emerald-400">
                        <Icon className="w-4 h-4" />
                      </div>
                      <h2>{item.label}</h2>
                    </div>
                    <span className="font-mono text-xs text-gray-400 bg-gray-50 dark:bg-gray-700/60 px-2 py-0.5 rounded">
                      অধ্যায় {item.num}
                    </span>
                  </div>

                  {/* Section Content */}
                  <div className="prose font-bengali leading-relaxed text-gray-800 dark:text-gray-200">
                    {renderSectionContent(item)}
                  </div>
                </section>
              );
            })}
          </main>
        </div>
      ) : (
        /* Single Chapter Tabbed View */
        <div className="max-w-[740px] mx-auto space-y-5">
          {/* Chapter Selector Dropdown / Pills */}
          <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar pb-2">
            {sections.map((item) => {
              const isActive = activeSectionId === item.id;
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveSectionId(item.id)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap flex items-center gap-1.5 transition ${
                    isActive
                      ? 'bg-emerald-600 text-white font-bold shadow-xs'
                      : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 border border-gray-200 dark:border-gray-700'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>

          {/* Active Chapter Content */}
          {(() => {
            const currentItem = sections.find(s => s.id === activeSectionId) || sections[0];
            const Icon = currentItem.icon;
            return (
              <div className="bg-white dark:bg-gray-800 rounded-3xl p-6 sm:p-9 shadow-xs border border-gray-200/90 dark:border-gray-700 transition-colors">
                <div className="flex items-center justify-between pb-3 mb-5 border-b border-gray-100 dark:border-gray-700/60">
                  <div className="flex items-center gap-2.5 text-base sm:text-lg font-bold text-gray-900 dark:text-gray-100 font-bengali">
                    <div className="w-8 h-8 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 flex items-center justify-center text-emerald-700 dark:text-emerald-400">
                      <Icon className="w-4 h-4" />
                    </div>
                    <h2>{currentItem.label}</h2>
                  </div>
                  <span className="font-mono text-xs text-gray-400 bg-gray-50 dark:bg-gray-700/60 px-2 py-0.5 rounded">
                    অধ্যায় {currentItem.num}
                  </span>
                </div>

                <div className="prose font-bengali leading-relaxed text-gray-800 dark:text-gray-200">
                  {renderSectionContent(currentItem)}
                </div>
              </div>
            );
          })()}
        </div>
      )}
    </div>
  );
}

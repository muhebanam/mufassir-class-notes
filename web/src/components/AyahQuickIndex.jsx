import React, { useRef, useEffect } from 'react';
import { 
  Compass, BookOpen, Layers, Eye, BookMarked, 
  ChevronDown, ChevronUp, Sparkles, Scale, GraduationCap, 
  Library, AlertCircle, Bookmark, CheckCircle2, FileText
} from 'lucide-react';
import { toBn } from '../utils/helpers';

export const AYAH_SECTIONS = [
  { id: 'sec-tahqeeq', num: 'শাব্দিক', label: 'তাহকীক ও মুফরাদাত', icon: Bookmark, type: 'ayah' },
  { id: 'sec-02-munasabat', num: '০২', label: 'আন্তঃআয়াত মুনাসাবাত', icon: Compass, type: 'ayah' },
  { id: 'sec-03-irab', num: '০৩', label: "ই'রাব ও ব্যাকরণ", icon: FileText, type: 'ayah' },
  { id: 'sec-04-qiraat', num: '০৪', label: '১০ কিরাআত পাঠভেদ', icon: Sparkles, type: 'ayah' },
  { id: 'sec-05-tafsir', num: '০৫', label: 'জালালাইন ও তাফসীর', icon: BookOpen, type: 'ayah' },
  { id: 'sec-06-hadith', num: '০৬', label: 'শানে নুযূল ও তাখরীজ', icon: BookMarked, type: 'ayah' },
];

export const RUKU_CONTEXT_SECTIONS = [
  { id: 'sec-01-makasid', num: '০১', label: 'ভূমিকা ও মাকাসিদ', secKey: 'makasid', icon: Compass, type: 'ruku' },
  { id: 'sec-07-ikhtilaf', num: '০৭', label: 'ফিকহী মতভেদ ও তারজীহ', secKey: 'ikhtilaf', icon: Scale, type: 'ruku' },
  { id: 'sec-08-ahkam', num: '০৮', label: 'আহকাম ও ৪ মাযহাব', secKey: 'ahkam', icon: Scale, type: 'ruku' },
  { id: 'sec-09-ulum', num: '০৯', label: 'উলূমুল কুরআন', secKey: 'ulumul_quran', icon: GraduationCap, type: 'ruku' },
  { id: 'sec-10-balaghat', num: '১০', label: "বালাগাত ও ই'জায", secKey: 'balaghat', icon: Sparkles, type: 'ruku' },
  { id: 'sec-11-samakalin', num: '১১', label: 'সমকালীন প্রাসঙ্গিকতা', secKey: 'samakalin', icon: AlertCircle, type: 'ruku' },
  { id: 'sec-12-dars', num: '১২', label: 'দরসের উপকরণ', secKey: 'dars', icon: BookOpen, type: 'ruku' },
  { id: 'sec-13-bibliography', num: '১৩', label: 'গ্রন্থপঞ্জি ও রেফারেন্স', secKey: 'bibliography', icon: Library, type: 'ruku' },
  { id: 'sec-14-limitations', num: '১৪', label: 'গবেষণার সীমাবদ্ধতা', secKey: 'limitations', icon: AlertCircle, type: 'ruku' },
];

export default function AyahQuickIndex({
  activeSection,
  onSelectSection,
  viewMode = 'continuous', // 'continuous' | 'single'
  onToggleViewMode,
  rukuInfo,
  ayahNumber,
  isRukuGroupOpen = false,
  onToggleRukuGroup
}) {
  const scrollRef = useRef(null);

  // Auto scroll active pill into horizontal view
  useEffect(() => {
    if (scrollRef.current && activeSection) {
      const activeBtn = scrollRef.current.querySelector(`[data-section="${activeSection}"]`);
      if (activeBtn) {
        activeBtn.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
      }
    }
  }, [activeSection]);

  const ayahRange = rukuInfo ? `${toBn(rukuInfo.ayah_start || 1)}–${toBn(rukuInfo.ayah_end || 1)}` : '';

  return (
    <div className="sticky top-[92px] sm:top-[102px] z-10 bg-white/95 dark:bg-gray-900/95 backdrop-blur-md border-b border-gray-200 dark:border-gray-800 shadow-2xs font-bengali transition-all">
      <div className="max-w-7xl mx-auto px-2 sm:px-4 py-2 space-y-1.5">
        
        {/* Top Control Bar: Mode Toggle + Group Indicators */}
        <div className="flex items-center justify-between gap-2 text-xs">
          {/* Group 1 Indicator */}
          <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar">
            <span className="font-bold text-emerald-800 dark:text-emerald-400 flex items-center gap-1 shrink-0">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              সূচিপত্র:
            </span>
            <span className="text-[11px] text-gray-500 dark:text-gray-400 hidden sm:inline">
              (দল ১: এই আয়াতের স্বতন্ত্র অধ্যায় | দল ২: রুকুর সামগ্রিক প্রেক্ষাপট)
            </span>
          </div>

          {/* View Mode Switcher Button */}
          <div className="flex items-center gap-1.5 shrink-0">
            <button
              onClick={onToggleViewMode}
              className="flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-semibold bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 border border-gray-300 dark:border-gray-700 transition"
              title={viewMode === 'continuous' ? 'একক শাস্ত্র ফোকাস মোডে যান' : 'একটানা স্ক্রল ভিউতে যান'}
            >
              <Eye className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
              <span>{viewMode === 'continuous' ? 'একটানা ভিউ' : 'একক ফোকাস'}</span>
            </button>
          </div>
        </div>

        {/* Section Navigation Tabs (Horizontal Scrollable) */}
        <div 
          ref={scrollRef}
          role="tablist"
          aria-label="১৪টি অধ্যায়ের দ্রুত সূচিপত্র"
          className="flex items-center gap-1.5 overflow-x-auto no-scrollbar scroll-smooth py-1"
        >
          {/* GROUP 1: Ayah Specific Chapters */}
          <div className="flex items-center gap-1 bg-emerald-50/60 dark:bg-emerald-950/30 p-1 rounded-xl border border-emerald-200/60 dark:border-emerald-800/40 shrink-0">
            <span className="text-[10px] font-bold text-emerald-800 dark:text-emerald-300 px-1.5 shrink-0 hidden md:inline">
              আয়াত {toBn(ayahNumber)}:
            </span>
            {AYAH_SECTIONS.map((sec) => {
              const isActive = activeSection === sec.id;
              const Icon = sec.icon;
              return (
                <button
                  key={sec.id}
                  data-section={sec.id}
                  role="tab"
                  aria-selected={isActive}
                  onClick={() => onSelectSection(sec.id, 'ayah')}
                  className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold transition-all shrink-0 ${
                    isActive
                      ? 'bg-emerald-600 text-white shadow-xs scale-102 ring-1 ring-emerald-400'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-white dark:hover:bg-gray-800 hover:text-emerald-700 dark:hover:text-emerald-300'
                  }`}
                  title={sec.label}
                >
                  <span className="font-mono text-[10px] opacity-75">{sec.num}</span>
                  <span className="whitespace-nowrap">{sec.label}</span>
                </button>
              );
            })}
          </div>

          <div className="w-[1px] h-6 bg-gray-300 dark:bg-gray-700 shrink-0 mx-1"></div>

          {/* GROUP 2: Ruku Context Chapters Toggle & Quick Links */}
          <div className="flex items-center gap-1 bg-indigo-50/50 dark:bg-indigo-950/30 p-1 rounded-xl border border-indigo-200/60 dark:border-indigo-800/40 shrink-0">
            <button
              onClick={onToggleRukuGroup}
              className="flex items-center gap-1 px-2 py-1 rounded-lg text-[11px] font-bold text-indigo-900 dark:text-indigo-300 hover:bg-indigo-100/60 dark:hover:bg-indigo-900/40 transition shrink-0"
              title="রুকু-স্তরের সামগ্রিক অধ্যায়গুলো খুলুন/ভাঁজ করুন"
            >
              <Layers className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400" />
              <span>রুকুর প্রেক্ষাপট ({ayahRange})</span>
              {isRukuGroupOpen ? (
                <ChevronUp className="w-3 h-3 ml-0.5" />
              ) : (
                <ChevronDown className="w-3 h-3 ml-0.5" />
              )}
            </button>

            {/* Quick buttons for ruku sections */}
            {RUKU_CONTEXT_SECTIONS.map((sec) => {
              const isActive = activeSection === sec.id;
              return (
                <button
                  key={sec.id}
                  data-section={sec.id}
                  role="tab"
                  aria-selected={isActive}
                  onClick={() => onSelectSection(sec.id, 'ruku')}
                  className={`flex items-center gap-1 px-2 py-1 rounded-lg text-xs font-medium transition-all shrink-0 ${
                    isActive
                      ? 'bg-indigo-600 text-white shadow-xs ring-1 ring-indigo-400'
                      : 'text-gray-600 dark:text-gray-300 hover:bg-white dark:hover:bg-gray-800 hover:text-indigo-700 dark:hover:text-indigo-300'
                  }`}
                  title={`${sec.num} ${sec.label}`}
                >
                  <span className="font-mono text-[10px] text-indigo-500 dark:text-indigo-400 font-bold">{sec.num}</span>
                  <span className="whitespace-nowrap">{sec.label.split(' ')[0]}</span>
                </button>
              );
            })}
          </div>
        </div>

      </div>
    </div>
  );
}

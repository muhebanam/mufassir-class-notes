import React, { useState } from 'react';
import { 
  Scale, Feather, GitCompare, BookMarked, Sparkles, 
  HelpCircle, BookOpen, Layers, CheckCircle2 
} from 'lucide-react';
import { toBn } from '../utils/helpers';

export default function ThematicView({ rukuData, surahInfo }) {
  const [activeTab, setActiveTab] = useState('ahkam');

  if (!rukuData || !rukuData.thematic_topics) {
    return (
      <div className="max-w-4xl mx-auto p-6 text-center text-gray-500">
        রুকুর বিষয়ভিত্তিক তথ্য লোড হচ্ছে...
      </div>
    );
  }

  const topics = rukuData.thematic_topics;

  const tabDefs = [
    { id: 'ahkam', label: 'আহকাম ও ৪ মাযহাব', icon: Scale, sec: topics.ahkam },
    { id: 'balaghat', label: 'বালাগাত ও ই\'জায', icon: Feather, sec: topics.balaghat },
    { id: 'ikhtilaf', label: 'মতভেদ ও তারজীহ', icon: GitCompare, sec: topics.ikhtilaf },
    { id: 'hadith', label: 'শানে নুযূল ও হাদীস', icon: Sparkles, sec: topics.hadith },
    { id: 'ulumul_quran', label: 'উলূমুল কুরআন', icon: BookMarked, sec: topics.ulumul_quran },
    { id: 'dars', label: 'দরসের উপকরণ', icon: BookOpen, sec: topics.dars },
    { id: 'samakalin', label: 'সমকালীন প্রাসঙ্গিকতা', icon: HelpCircle, sec: topics.samakalin },
    { id: 'bibliography', label: 'গ্রন্থপঞ্জি ও সূত্র', icon: Layers, sec: topics.bibliography },
  ];

  const currentTab = tabDefs.find(t => t.id === activeTab) || tabDefs[0];

  return (
    <div className="max-w-4xl mx-auto px-3 sm:px-4 py-4 space-y-4">
      {/* Ruku Header Card */}
      <div className="bg-gradient-to-r from-emerald-800 to-teal-900 text-white rounded-2xl p-4 sm:p-6 shadow-md">
        <div className="flex items-center gap-2 text-emerald-200 text-xs font-semibold uppercase tracking-wider mb-1">
          <span>সূরা {surahInfo?.name_bn}</span>
          <span>•</span>
          <span>রুকু {toBn(rukuData.ruku_id)}</span>
          <span>•</span>
          <span>আয়াত {rukuData.ayah_range_bn}</span>
        </div>
        <h2 className="text-xl sm:text-2xl font-bold font-bengali">
          {topics.makasid?.title || `রুকু ${toBn(rukuData.ruku_id)}-এর সার্বিক শাস্ত্রীয় বিশ্লেষণ`}
        </h2>
        {topics.makasid?.content && (
          <div className="mt-3 text-xs sm:text-sm text-emerald-100/90 leading-relaxed font-bengali max-h-36 overflow-y-auto pr-2">
            {topics.makasid.content.slice(0, 350)}...
          </div>
        )}
      </div>

      {/* Thematic Tabs Navigation Bar */}
      <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-1">
        {tabDefs.map((t) => {
          const Icon = t.icon;
          const isActive = activeTab === t.id;
          return (
            <button
              key={t.id}
              onClick={() => setActiveTab(t.id)}
              className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs sm:text-sm font-semibold transition shrink-0 ${
                isActive
                  ? 'bg-emerald-600 text-white shadow-sm ring-2 ring-emerald-400/30'
                  : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-emerald-50 dark:hover:bg-gray-700 border border-gray-200 dark:border-gray-700'
              }`}
            >
              <Icon className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
              <span>{t.label}</span>
            </button>
          );
        })}
      </div>

      {/* Active Topic Content Card */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl p-4 sm:p-6 shadow-sm border border-gray-200 dark:border-gray-700 transition-colors">
        <div className="flex items-center justify-between pb-3 mb-4 border-b border-gray-100 dark:border-gray-700">
          <h3 className="text-base sm:text-lg font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2">
            <currentTab.icon className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            <span>{currentTab.sec?.title || currentTab.label}</span>
          </h3>
          <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 font-semibold">
            অধ্যায় {toBn(currentTab.sec?.sec_id || 0)}
          </span>
        </div>

        <div className="text-gray-800 dark:text-gray-200 text-sm sm:text-base leading-relaxed whitespace-pre-line font-bengali space-y-4">
          {currentTab.sec?.content ? (
            currentTab.sec.content
          ) : (
            <div className="text-gray-500 italic py-6 text-center">
              এই রুকুতে এই শাস্ত্রীয় বিষয়টি বিশেষ কোনো মতভেদ ব্যতীত সাধারণ বিধানের অন্তর্ভুক্ত।
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

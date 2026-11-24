import React, { useState } from 'react';
import { BookOpen, Layers, Sparkles, Scale, Volume2, Compass, ArrowRight, ChevronRight } from 'lucide-react';
import MarkdownContent from './MarkdownContent';
import QiraatTable from './QiraatTable';

export default function RukuScopeView({ 
  rukuData, 
  surahInfo, 
  onSelectAyah,
  onSwitchToAyahScope 
}) {
  const [activeTab, setActiveTab] = useState('makasid'); // 'makasid', 'munasabat', 'ahkam', 'balaghat', 'qiraat'

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

  const tabItems = [
    { id: 'makasid', label: 'ভূমিকা ও মাকাসিদ', num: '০১', icon: BookOpen, data: topics.makasid },
    { id: 'munasabat', label: 'রাবত ও মুনাসাবাত', num: '০২', icon: Layers, data: topics.munasabat },
    { id: 'ahkam', label: 'ফিকহী আহকাম ও বিধান', num: '০৩', icon: Scale, data: topics.ahkam },
    { id: 'balaghat', label: 'বালাগাত ও অলংকার', num: '০৪', icon: Sparkles, data: topics.balaghat },
    { id: 'qiraat', label: '১০ কিরাআত সারণি', num: '০৫', icon: Volume2, count: qiraatTableData.length },
  ];

  return (
    <div className="w-full max-w-5xl mx-auto px-3 sm:px-6 py-4 sm:py-8 space-y-6 sm:space-y-8 layout-safe">
      {/* 1. Ruku Scope Header Banner */}
      <div className="rounded-2xl sm:rounded-3xl bg-gradient-to-r from-emerald-800 to-teal-900 text-white p-5 sm:p-7 shadow-sm border border-emerald-700/40">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="space-y-1">
            <div className="flex items-center gap-2 text-xs font-semibold">
              <span className="px-2 py-0.5 rounded-full bg-white/20 font-mono">
                রুকু {toBn(rukuData.ruku_id)} / {toBn(surahInfo?.ruku_count || 9)}
              </span>
              <span className="text-emerald-200 font-bengali">
                আয়াত {rukuData.ayah_range_bn || `${toBn(rukuData.ayah_start)}–${toBn(rukuData.ayah_end)}`}
              </span>
              <span>•</span>
              <span className="text-gray-200 font-bengali">
                মোট {toBn(rukuData.ayah_count || 10)}টি আয়াত
              </span>
            </div>
            <h1 className="text-xl sm:text-2xl font-bold font-bengali">
              রুকু {toBn(rukuData.ruku_id)}-এর বিষয়ভিত্তিক শাস্ত্রীয় বিশ্লেষণ
            </h1>
            <p className="text-xs sm:text-sm text-emerald-100 font-bengali">
              মাকাসিদুশ শরীয়াহ, পূর্ববর্তী রুকুর রাবত, ফিকহী তুলনামূলক আলোচনা ও ১০ মুতাওয়াতির কিরাআত
            </p>
          </div>

          <button
            onClick={() => {
              if (onSelectAyah) onSelectAyah(rukuData.ayah_start || 1);
              if (onSwitchToAyahScope) onSwitchToAyahScope();
            }}
            className="self-start sm:self-center px-4 py-2.5 rounded-xl bg-white text-emerald-800 hover:bg-emerald-50 text-xs sm:text-sm font-bold font-bengali flex items-center gap-2 shadow-xs transition"
          >
            <span>এই রুকুর আয়াত স্টাডি খুলুন</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* 2. Horizontal Sticky Thematic Tab Switcher */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-2 shadow-2xs">
        <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar p-1">
          {tabItems.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;

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

      {/* 3. Thematic Tab Content Container */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-5 sm:p-7 shadow-xs">
        {activeTab === 'qiraat' ? (
          <QiraatTable 
            tableData={qiraatTableData} 
            title={`রুকু ${toBn(rukuData.ruku_id)}-এর ১০ মুতাওয়াতির কিরাআত সারণি`}
          />
        ) : (
          (() => {
            const currTopic = topics[activeTab];
            if (!currTopic || (!currTopic.content && !currTopic.summary)) {
              return (
                <div className="text-gray-500 italic py-8 text-center font-bengali text-sm">
                  এই রুকুর জন্য এই অধ্যায়ের তথ্য সাধারণ বিধানের অন্তর্ভুক্ত।
                </div>
              );
            }

            return (
              <div className="space-y-4">
                <div className="flex items-center gap-2 pb-3 border-b border-gray-100 dark:border-gray-700">
                  <h3 className="text-base sm:text-lg font-bold text-gray-900 dark:text-gray-100 font-bengali">
                    {currTopic.title || tabItems.find(t => t.id === activeTab)?.label}
                  </h3>
                </div>

                <div className="prose font-bengali text-sm sm:text-base leading-relaxed text-gray-800 dark:text-gray-200">
                  <MarkdownContent content={currTopic.content || currTopic.summary} />
                </div>
              </div>
            );
          })()
        )}
      </div>

      {/* 4. Bottom Ayah Bridge Card */}
      <div className="bg-emerald-50/60 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-800/50 rounded-2xl p-4 sm:p-5 flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="text-center sm:text-left">
          <h4 className="font-bold text-sm sm:text-base text-emerald-900 dark:text-emerald-200 font-bengali">
            রুকু {toBn(rukuData.ruku_id)}-এর শাব্দিক তাহকীক ও জালালাইন অধ্যয়নে যেতে চান?
          </h4>
          <p className="text-xs text-emerald-700 dark:text-emerald-400 font-bengali mt-0.5">
            এই রুকুর আয়াত {rukuData.ayah_range_bn}-এর প্রতিটি শব্দের সরফ, নাহু ও তাফসীর উন্মুক্ত করুন।
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

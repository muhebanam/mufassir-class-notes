import React from 'react';
import { BookOpen, Layers, Sparkles, Compass, ArrowRight, ShieldCheck } from 'lucide-react';
import MarkdownContent from './MarkdownContent';
import MindMap from './MindMap';

export default function SurahScopeView({ 
  surahMeta, 
  surahInfo, 
  onSelectRuku,
  onSwitchToRukuScope,
  onSwitchToAyahScope
}) {
  const toBn = (num) => {
    const bn = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
    return String(num).replace(/[0-9]/g, d => bn[d]);
  };

  if (!surahMeta) {
    return (
      <div className="max-w-4xl mx-auto py-16 text-center space-y-3 font-bengali">
        <div className="w-8 h-8 border-3 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
        <p className="text-gray-500 text-sm">সূরা পরিচিতি ডাটা লোড হচ্ছে...</p>
      </div>
    );
  }

  const rukusList = surahMeta.rukus || [];

  return (
    <div className="w-full max-w-5xl mx-auto px-3 sm:px-6 py-4 sm:py-8 space-y-6 sm:space-y-8 layout-safe">
      {/* 1. Surah Hero Banner */}
      <div className="relative overflow-hidden rounded-2xl sm:rounded-3xl bg-gradient-to-br from-emerald-800 via-teal-900 to-gray-900 text-white p-5 sm:p-8 shadow-md border border-emerald-700/40">
        <div className="relative z-10 space-y-3">
          <div className="flex flex-wrap items-center gap-2 text-xs font-semibold">
            <span className="px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-200 border border-emerald-400/30 font-mono">
              সূরা নং {toBn(surahMeta.id || surahInfo?.id || 24)}
            </span>
            <span className="px-2.5 py-1 rounded-full bg-teal-500/20 text-teal-200 border border-teal-400/30 font-bengali">
              মাদানী সূরা
            </span>
            <span className="px-2.5 py-1 rounded-full bg-white/10 text-gray-200 font-bengali">
              {toBn(surahMeta.ruku_count || 9)}টি রুকু • {toBn(surahMeta.ayah_count || 64)}টি আয়াত
            </span>
          </div>

          <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2">
            <div>
              <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight font-bengali">
                সূরা {surahMeta.name_bn || surahInfo?.name_bn || 'আন-নূর'}
              </h1>
              <p className="text-sm text-emerald-100 font-bengali mt-1">
                সামাজিক ও পারিবারিক পবিত্রতা, অপবাদ প্রতিরোধ ও আল্লাহর নূর সম্পর্কিত সুমহান ঐশী সংবিধান
              </p>
            </div>
            <div className="text-right sm:text-left">
              <span className="font-arabic text-3xl sm:text-5xl font-bold text-emerald-300 drop-shadow-xs" dir="rtl">
                سُورَةُ {surahMeta.name_ar || 'النُّورِ'}
              </span>
            </div>
          </div>
        </div>

        {/* Ambient Glow Decoration */}
        <div className="absolute -right-12 -bottom-12 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
      </div>

      {/* 2. Surah Level Overview & Shan-e-Nuzul (Strictly Surah Scope) */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-5 sm:p-7 shadow-xs space-y-4">
        <div className="flex items-center gap-2.5 pb-3 border-b border-gray-100 dark:border-gray-700">
          <Sparkles className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
          <h2 className="text-lg sm:text-xl font-bold text-gray-900 dark:text-gray-100 font-bengali">
            সূরার নামকরণ, শানে নুযূল ও সামগ্রিক প্রেক্ষাপট
          </h2>
        </div>

        <div className="prose font-bengali leading-relaxed text-gray-800 dark:text-gray-200 text-sm sm:text-base space-y-3">
          {surahMeta.intro ? (
            <MarkdownContent content={surahMeta.intro} />
          ) : (
            <p>
              সূরা আন-নূর পবিত্র কুরআনের ২৪তম সূরা। এটি মদীনা মুনাওয়ারায় নাযিলকৃত। সূরার ৩৫তম আয়াতে আল্লাহ তাআলার পরিচয় হিসেবে ‘আল্লাহ আসমান ও জমিনের জ্যোতি (নূর)’ উপমা বর্ণিত হওয়ায় এর নাম ‘সূরা আন-নূর’ রাখা হয়েছে। সূরার মূল আলোচ্য বিষয় হলো মুসলিম সমাজের পবিত্রতা রক্ষা, ব্যভিচারের মূলোৎপাটন, সতী নারীর ওপর মিথ্যা অপবাদ প্রতিরোধ (ইফক), পর্দা ও দৃষ্টি সংযমের বিধান এবং পারিবারিক ও সামাজিক শিষ্টাচার প্রতিষ্ঠা।
            </p>
          )}
        </div>
      </div>

      {/* 3. Interactive Full Surah Mind Map */}
      <div className="space-y-3">
        <MindMap 
          surahInfo={surahInfo} 
          currentRuku={1}
          onSelectRuku={onSelectRuku}
          mode="surah"
        />
      </div>

      {/* 4. Ruku Index & Mapping Grid */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-5 sm:p-7 shadow-xs space-y-4">
        <div className="flex items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-700">
          <div className="flex items-center gap-2.5">
            <Layers className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            <h2 className="text-lg sm:text-xl font-bold text-gray-900 dark:text-gray-100 font-bengali">
              সূরার রুকুভিত্তিক রূপরেখা ও সূচিপত্র
            </h2>
          </div>
          <span className="text-xs text-gray-500 font-bengali">
            মোট {toBn(rukusList.length)}টি রুকু
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
          {rukusList.map((r) => (
            <div
              key={r.ruku_id}
              onClick={() => onSelectRuku && onSelectRuku(r.ruku_id)}
              className="group p-4 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-emerald-500 dark:hover:border-emerald-500 bg-gray-50/50 dark:bg-gray-850 hover:bg-emerald-50/40 dark:hover:bg-emerald-950/20 transition-all cursor-pointer shadow-2xs"
            >
              <div className="flex items-center justify-between gap-2 mb-2">
                <span className="w-7 h-7 rounded-lg bg-emerald-600 text-white font-mono text-xs font-bold flex items-center justify-center">
                  {r.ruku_id}
                </span>
                <span className="text-xs font-semibold text-emerald-700 dark:text-emerald-400 bg-emerald-100/60 dark:bg-emerald-900/40 px-2 py-0.5 rounded-full font-bengali">
                  আয়াত {r.ayah_range_bn || `${toBn(r.ayah_start)}–${toBn(r.ayah_end)}`}
                </span>
              </div>
              <h4 className="font-bold text-sm text-gray-900 dark:text-gray-100 font-bengali group-hover:text-emerald-700 dark:group-hover:text-emerald-400 transition-colors">
                রুকু {toBn(r.ruku_id)}: {r.title || `রুকু ${toBn(r.ruku_id)}-এর বিধানাবলি`}
              </h4>
              <p className="text-xs text-gray-500 dark:text-gray-400 font-bengali mt-1 line-clamp-2">
                মোট {toBn(r.ayah_count)}টি আয়াতের তাফসীর, ফিকহী নীতিমালা ও শাব্দিক তাহকীক।
              </p>
              <div className="mt-3 flex items-center gap-1 text-xs font-semibold text-emerald-600 dark:text-emerald-400 font-bengali group-hover:translate-x-1 transition-transform">
                <span>রুকু আলোচনা খুলুন</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

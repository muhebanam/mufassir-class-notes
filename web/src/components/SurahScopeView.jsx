import React, { useMemo, useRef } from 'react';
import { BookOpen, Layers, Sparkles, Compass, ArrowRight, ShieldCheck, CheckCircle2, AlertCircle } from 'lucide-react';
import MarkdownContent from './MarkdownContent';
import MindMap from './MindMap';

export default function SurahScopeView({ 
  surahMeta, 
  surahInfo, 
  onSelectRuku,
  onSwitchToRukuScope,
  onSwitchToAyahScope
}) {
  const introContainerRef = useRef(null);

  const toBn = (num) => {
    const bn = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
    return String(num).replace(/[0-9]/g, d => bn[d]);
  };

  // Extract ## headings from intro markdown for Quick Index navigation
  const introChapters = useMemo(() => {
    const raw = surahMeta?.intro || '';
    const matches = [...raw.matchAll(/^##\s+(.+)$/gm)];
    return matches.map((m, idx) => ({
      idx,
      label: m[1].replace(/[*`]/g, '').trim()
    }));
  }, [surahMeta?.intro]);

  const scrollToIntroChapter = (idx) => {
    if (!introContainerRef.current) return;
    const h2s = introContainerRef.current.querySelectorAll('h2');
    if (h2s && h2s[idx]) {
      h2s[idx].scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
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
  const surahId = surahMeta.id || surahInfo?.id || 24;
  const surahNameBn = surahMeta.name_bn || surahInfo?.name_bn || 'আন-নূর';
  const revelationType = surahMeta.revelation_type || surahInfo?.revelation_type || (surahId === 24 ? 'মাদানী সূরা' : 'মাক্কী / মাদানী');
  const subtitleText = surahMeta.subtitle || (surahId === 24
    ? 'সামাজিক ও পারিবারিক পবিত্রতা, অপবাদ প্রতিরোধ ও আল্লাহর নূর সম্পর্কিত সুমহান ঐশী সংবিধান'
    : `কুরআনুল কারীমের ${toBn(surahId)}তম পবিত্র সূরা`);

  // Adaptive grid columns for Section 4 Ruku Cards
  const rukuGridClass = rukusList.length === 1
    ? 'grid-cols-1 max-w-2xl'
    : rukusList.length === 2
      ? 'grid-cols-1 md:grid-cols-2'
      : 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3';

  return (
    <div className="w-full max-w-5xl mx-auto px-3 sm:px-6 py-4 sm:py-8 space-y-6 sm:space-y-8 layout-safe">
      {/* 1. Surah Hero Banner */}
      <div className="relative overflow-hidden rounded-2xl sm:rounded-3xl bg-gradient-to-br from-emerald-800 via-teal-900 to-gray-900 text-white p-5 sm:p-8 shadow-md border border-emerald-700/40">
        <div className="relative z-10 space-y-3">
          <div className="flex flex-wrap items-center gap-2 text-xs font-semibold">
            <span className="px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-200 border border-emerald-400/30 font-mono">
              সূরা নং {toBn(surahId)}
            </span>
            <span className="px-2.5 py-1 rounded-full bg-teal-500/20 text-teal-200 border border-teal-400/30 font-bengali">
              {revelationType}
            </span>
            <span className="px-2.5 py-1 rounded-full bg-white/10 text-gray-200 font-bengali">
              {toBn(surahMeta.ruku_count || surahInfo?.ruku_count || 1)}টি রুকু • {toBn(surahMeta.ayah_count || surahInfo?.ayah_count || 1)}টি আয়াত
            </span>
          </div>

          <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2">
            <div className="flex-1">
              <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight font-bengali">
                সূরা {surahNameBn}
              </h1>
              <p className="text-sm text-emerald-100 font-bengali mt-1 leading-relaxed">
                {subtitleText}
              </p>
            </div>
            <div className="text-right sm:text-left shrink-0">
              <span className="font-arabic text-3xl sm:text-5xl font-bold text-emerald-300 drop-shadow-xs" dir="rtl">
                سُورَةُ {surahMeta.name_ar || surahInfo?.name_ar || ''}
              </span>
            </div>
          </div>
        </div>

        {/* Ambient Glow Decoration */}
        <div className="absolute -right-12 -bottom-12 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
      </div>

      {/* 2. Surah Level Overview & 8-Chapter Quick Index (Strictly Surah Scope) */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-5 sm:p-7 shadow-xs space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-2.5 pb-3 border-b border-gray-100 dark:border-gray-700">
          <div className="flex items-center gap-2.5">
            <Sparkles className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            <h2 className="text-lg sm:text-xl font-bold text-gray-900 dark:text-gray-100 font-bengali">
              সূরার নামকরণ, শানে নুযূল ও সামগ্রিক প্রেক্ষাপট
            </h2>
          </div>
          {introChapters.length > 1 && (
            <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-emerald-50 dark:bg-emerald-950/50 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 font-bengali">
              {toBn(introChapters.length)}টি অধ্যায়
            </span>
          )}
        </div>

        {/* Quick Jump Index for Surah Chapters */}
        {introChapters.length > 1 && (
          <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-1 pb-2 border-b border-gray-100 dark:border-gray-700/60 font-bengali">
            {introChapters.map((ch) => (
              <button
                key={ch.idx}
                onClick={() => scrollToIntroChapter(ch.idx)}
                className="px-2.5 py-1 rounded-lg text-xs font-medium bg-gray-100 dark:bg-gray-700/60 hover:bg-emerald-100 dark:hover:bg-emerald-900/40 text-gray-700 dark:text-gray-200 hover:text-emerald-800 dark:hover:text-emerald-300 transition shrink-0 whitespace-nowrap"
              >
                {ch.label}
              </button>
            ))}
          </div>
        )}

        <div 
          ref={introContainerRef}
          className="prose dark:prose-invert font-bengali leading-relaxed text-gray-800 dark:text-gray-200 text-sm sm:text-base space-y-3 [&_h2]:scroll-mt-28"
        >
          {surahMeta.intro ? (
            <MarkdownContent content={surahMeta.intro} />
          ) : (
            <p>
              সূরা {surahNameBn} পবিত্র কুরআনের {toBn(surahId)}তম সূরা। এতে মোট {toBn(surahMeta.ruku_count || surahInfo?.ruku_count || 1)}টি রুকু এবং {toBn(surahMeta.ayah_count || surahInfo?.ayah_count || 1)}টি আয়াত রয়েছে।
            </p>
          )}
        </div>
      </div>

      {/* 3. Interactive Full Surah Mind Map (Surah Structure) */}
      <div className="space-y-3">
        <MindMap 
          surahInfo={surahInfo} 
          surahMeta={surahMeta}
          currentRuku={1}
          onSelectRuku={onSelectRuku}
          mode="surah"
        />
      </div>

      {/* 4. Ruku Index & Mapping Grid (সূরার রুকুভিত্তিক রূপরেখা ও সূচিপত্র) */}
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

        <div className={`grid gap-3.5 ${rukuGridClass}`}>
          {rukusList.map((r) => (
            <div
              key={r.ruku_id}
              onClick={() => onSelectRuku && onSelectRuku(r.ruku_id)}
              className="group p-4 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-emerald-500 dark:hover:border-emerald-500 bg-gray-50/50 dark:bg-gray-850 hover:bg-emerald-50/40 dark:hover:bg-emerald-950/20 transition-all cursor-pointer shadow-2xs flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-2">
                  <div className="flex items-center gap-1.5">
                    <span className="w-7 h-7 rounded-lg bg-emerald-600 text-white font-mono text-xs font-bold flex items-center justify-center">
                      {r.ruku_id}
                    </span>
                    {r.status === 'gold' ? (
                      <span className="inline-flex items-center gap-0.5 text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 font-bengali">
                        <CheckCircle2 className="w-2.5 h-2.5" />
                        <span>গোল্ড</span>
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-0.5 text-[10px] font-medium px-1.5 py-0.5 rounded-full bg-amber-100 dark:bg-amber-950 text-amber-800 dark:text-amber-300 font-bengali">
                        <AlertCircle className="w-2.5 h-2.5" />
                        <span>খসড়া</span>
                      </span>
                    )}
                  </div>
                  <span className="text-xs font-semibold text-emerald-700 dark:text-emerald-400 bg-emerald-100/60 dark:bg-emerald-900/40 px-2 py-0.5 rounded-full font-bengali">
                    আয়াত {r.ayah_range_bn || `${toBn(r.ayah_start)}–${toBn(r.ayah_end)}`}
                  </span>
                </div>
                <h4 className="font-bold text-sm text-gray-900 dark:text-gray-100 font-bengali group-hover:text-emerald-700 dark:group-hover:text-emerald-400 transition-colors">
                  রুকু {toBn(r.ruku_id)}: {r.title || `রুকু ${toBn(r.ruku_id)}-এর বিধানাবলি`}
                </h4>
                <p className="text-xs text-gray-600 dark:text-gray-300 font-bengali mt-1.5 line-clamp-3 leading-relaxed">
                  {r.summary || `মোট ${toBn(r.ayah_count)}টি আয়াতের তাফসীর, ফিকহী নীতিমালা ও শাব্দিক তাহকীক।`}
                </p>

                {/* Subtopics Preview */}
                {Array.isArray(r.subtopics) && r.subtopics.length > 0 && (
                  <div className="mt-2.5 pt-2 border-t border-gray-200/70 dark:border-gray-700/60 space-y-1">
                    {r.subtopics.slice(0, 3).map((st, sIdx) => (
                      <div key={sIdx} className="flex items-start gap-1 text-[11px] text-gray-500 dark:text-gray-400 font-bengali leading-snug">
                        <span className="text-emerald-600 dark:text-emerald-400">•</span>
                        <span className="flex-1 line-clamp-1">{st.text}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="mt-3 pt-2 flex items-center gap-1 text-xs font-semibold text-emerald-600 dark:text-emerald-400 font-bengali group-hover:translate-x-1 transition-transform">
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

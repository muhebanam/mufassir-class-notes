import React, { useState } from 'react';
import { Bookmark, BookCheck, ShieldCheck, Sparkles, LayoutGrid, Table, Info, BookOpen, Layers } from 'lucide-react';
import MarkdownContent from './MarkdownContent';
import { parseHadithTakhrij } from '../utils/tafsirTakhrijAdapter';
import { toBn } from '../utils/helpers';

export default function HadithTakhrijSection({ 
  content, 
  title = null,
  ayahNumber = null,
  covers = null,
  defaultLayout = 'cards'
}) {
  const [layoutMode, setLayoutMode] = useState(defaultLayout); // 'cards' or 'table'

  const parsed = parseHadithTakhrij(content);

  if (parsed.isEmpty) {
    return null;
  }

  // Format covers range badge (e.g., [২, ৩] -> "আয়াত ২–৩-এর যৌথ আলোচনা")
  const isMultiAyahCover = Array.isArray(covers) && covers.length === 2 && covers[0] !== covers[1];
  const coversLabel = isMultiAyahCover ? `আয়াত ${toBn(covers[0])}–${toBn(covers[1])}-এর যৌথ আলোচনা` : null;

  const dynamicTitle = title || (
    parsed.hasHadith 
      ? (ayahNumber ? `০৬. আয়াত ${toBn(ayahNumber)}-এর শানে নুযূল ও হাদীস তাখরীজ` : '০৬. শানে নুযূল ও সংশ্লিষ্ট হাদীসের তাখরীজ')
      : (ayahNumber ? `০৬. আয়াত ${toBn(ayahNumber)}-এর শানে নুযূল (নাযিলের ঐতিহাসিক প্রেক্ষাপট)` : '০৬. শানে নুযূল (নাযিলের ঐতিহাসিক প্রেক্ষাপট)')
  );

  const getHukmBadge = (grade, rawHukm) => {
    if (grade === 'sahih') {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
          <span>সহীহ (প্রামাণিক)</span>
        </span>
      );
    }
    if (grade === 'hasan') {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-bold bg-blue-100 dark:bg-blue-950/60 text-blue-800 dark:text-blue-300 border border-blue-300 dark:border-blue-800">
          <ShieldCheck className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
          <span>হাসান</span>
        </span>
      );
    }
    if (grade === 'daif') {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 border border-amber-300 dark:border-amber-800">
          <Info className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
          <span>যঈফ / পর্যালোচিত</span>
        </span>
      );
    }
    if (rawHukm) {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600">
          <span>{rawHukm}</span>
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300">
        <span>উৎস গ্রন্থ দ্রষ্টব্য</span>
      </span>
    );
  };

  return (
    <div 
      id="sec-06-hadith"
      className="scroll-mt-36 sm:scroll-mt-44 bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-6 shadow-xs space-y-4 font-bengali transition-colors"
    >
      {/* Header bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-700">
        <div className="flex items-center gap-2">
          <Bookmark className="w-5 h-5 text-teal-600 dark:text-teal-400" />
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <h3 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100">
                {dynamicTitle}
              </h3>
              {coversLabel && (
                <span className="inline-flex items-center gap-1 text-[11px] font-semibold px-2 py-0.5 rounded-full bg-indigo-50 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800 shadow-2xs">
                  <Layers className="w-3 h-3 text-indigo-500" />
                  <span>{coversLabel}</span>
                </span>
              )}
            </div>
            {parsed.hasHadith && parsed.realHadiths?.length > 0 && (
              <span className="text-xs text-teal-700 dark:text-teal-400 font-semibold">
                {toBn(parsed.realHadiths.length)}টি প্রামাণ্য হাদীসের তাখরীজ ও সনদ বিশ্লেষণ
              </span>
            )}
            {!parsed.hasHadith && (
              <span className="text-xs text-teal-700 dark:text-teal-400 font-semibold">
                আসবাবুন নুযূল ও আয়াত নাযিলের ঐতিহাসিক পটভূমি
              </span>
            )}
          </div>
        </div>

        {/* Layout toggle (Cards vs Table) when structured hadiths exist */}
        {parsed.hadiths.length > 0 && (
          <div className="flex items-center gap-1 bg-gray-100 dark:bg-gray-700/60 p-1 rounded-xl text-xs font-semibold self-start sm:self-center">
            <button
              onClick={() => setLayoutMode('cards')}
              className={`flex items-center gap-1 px-2.5 py-1 rounded-lg transition-all ${
                layoutMode === 'cards'
                  ? 'bg-white dark:bg-gray-800 text-teal-800 dark:text-teal-300 shadow-2xs font-bold'
                  : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100'
              }`}
            >
              <LayoutGrid className="w-3.5 h-3.5" />
              <span>কার্ড ভিউ</span>
            </button>
            <button
              onClick={() => setLayoutMode('table')}
              className={`flex items-center gap-1 px-2.5 py-1 rounded-lg transition-all ${
                layoutMode === 'table'
                  ? 'bg-white dark:bg-gray-800 text-teal-800 dark:text-teal-300 shadow-2xs font-bold'
                  : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100'
              }`}
            >
              <Table className="w-3.5 h-3.5" />
              <span>তাখরীজ সারণি</span>
            </button>
          </div>
        )}
      </div>

      {/* Narrative Lead Text (আসবাবুন নুযূল / প্রেক্ষাপট বর্ণনা) */}
      {parsed.narrative && (
        <div className="prose dark:prose-invert text-xs sm:text-sm text-gray-800 dark:text-gray-200 leading-relaxed bg-teal-50/40 dark:bg-teal-950/20 p-4 rounded-xl border border-teal-100/70 dark:border-teal-900/40">
          <MarkdownContent content={parsed.narrative} />
        </div>
      )}

      {/* Main Hadith Section: Cards Mode or Table Mode */}
      {parsed.hadiths.length > 0 && (
        <>
          {layoutMode === 'cards' ? (
            <div className="space-y-4">
              {parsed.hadiths.map((h, i) => (
                <div 
                  key={i} 
                  className="rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-800/60 p-4 sm:p-5 space-y-3 transition hover:shadow-xs"
                >
                  {/* Hadith Top Info */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2.5 border-b border-gray-200/70 dark:border-gray-700/60">
                    <div className="flex items-center gap-2">
                      <span className="w-6 h-6 rounded-full bg-teal-600 text-white text-xs font-bold flex items-center justify-center font-mono">
                        {toBn(i + 1)}
                      </span>
                      <h4 className="font-bold text-sm text-gray-900 dark:text-gray-100">
                        {h.cleanTitle || `হাদীস ${toBn(i + 1)}`}
                      </h4>
                    </div>

                    <div className="flex items-center gap-2">
                      {h.hukm && getHukmBadge(h.grade, h.hukm)}
                    </div>
                  </div>

                  {/* Main text & takhrij notes */}
                  <div className="prose dark:prose-invert text-xs sm:text-sm text-gray-800 dark:text-gray-200 leading-relaxed">
                    <MarkdownContent content={h.body} />
                  </div>

                  {/* Hadith Metadata Grid */}
                  {(h.sourceBook || h.takhrijNote) && (
                    <div className="pt-2.5 border-t border-gray-200/60 dark:border-gray-700/50 grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                      {h.sourceBook && (
                        <div className="flex items-center gap-1.5 text-gray-600 dark:text-gray-400">
                          <BookOpen className="w-3.5 h-3.5 text-teal-600 dark:text-teal-400 shrink-0" />
                          <span><strong>উৎস:</strong> {h.sourceBook}</span>
                        </div>
                      )}
                      {h.takhrijNote && (
                        <div className="flex items-center gap-1.5 text-gray-600 dark:text-gray-400">
                          <BookCheck className="w-3.5 h-3.5 text-teal-600 dark:text-teal-400 shrink-0" />
                          <span><strong>তাখরীজ:</strong> {h.takhrijNote}</span>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            /* Table Mode */
            <div className="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700">
              <table className="w-full text-left text-xs sm:text-sm border-collapse">
                <thead>
                  <tr className="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 font-bold border-b border-gray-200 dark:border-gray-600">
                    <th className="py-2.5 px-3 w-12 text-center">নং</th>
                    <th className="py-2.5 px-3 w-40">উৎস গ্রন্থ</th>
                    <th className="py-2.5 px-3">হাদীস বিবরণ ও সারসংক্ষেপ</th>
                    <th className="py-2.5 px-3 w-32">হুকুম / মান</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                  {parsed.hadiths.map((h, idx) => (
                    <tr key={idx} className="hover:bg-gray-50/70 dark:hover:bg-gray-750/50 transition">
                      <td className="py-2.5 px-3 text-center font-mono font-bold text-gray-500">
                        {toBn(idx + 1)}
                      </td>
                      <td className="py-2.5 px-3 font-semibold text-gray-800 dark:text-gray-200">
                        {h.sourceBook || h.cleanTitle || '—'}
                      </td>
                      <td className="py-2.5 px-3 text-gray-700 dark:text-gray-300">
                        <div className="prose dark:prose-invert line-clamp-3 text-xs">
                          <MarkdownContent content={h.body} />
                        </div>
                      </td>
                      <td className="py-2.5 px-3">
                        {getHukmBadge(h.grade, h.hukm)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  );
}

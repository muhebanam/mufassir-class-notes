import React, { useState } from 'react';
import { Bookmark, BookCheck, ShieldCheck, Sparkles, LayoutGrid, Table, Info, BookOpen } from 'lucide-react';
import MarkdownContent from './MarkdownContent';
import { parseHadithTakhrij } from '../utils/tafsirTakhrijAdapter';

export default function HadithTakhrijSection({ 
  content, 
  title = "শানে নুযূল ও সংশ্লিষ্ট হাদীসের তাখরীজ",
  defaultLayout = 'cards'
}) {
  const [layoutMode, setLayoutMode] = useState(defaultLayout); // 'cards' or 'table'

  const parsed = parseHadithTakhrij(content);

  if (parsed.isEmpty) {
    return null;
  }

  const toBn = (num) => {
    const bn = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
    return String(num).replace(/[0-9]/g, d => bn[d]);
  };

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
    <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-6 shadow-xs space-y-4 font-bengali transition-colors">
      {/* Header bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-700">
        <div className="flex items-center gap-2">
          <Bookmark className="w-5 h-5 text-teal-600 dark:text-teal-400" />
          <div>
            <h3 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100">
              {title}
            </h3>
            {parsed.hadiths.length > 0 && (
              <span className="text-xs text-teal-700 dark:text-teal-400 font-semibold">
                {toBn(parsed.hadiths.length)}টি প্রামাণ্য হাদীস ও ঐতিহাসিক বিবরণ
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

      {/* Narrative Intro / Context (if present) */}
      {parsed.narrativeIntro && (
        <div className="p-3.5 sm:p-4 rounded-xl bg-teal-50/50 dark:bg-teal-950/20 border border-teal-100 dark:border-teal-900/40 text-xs sm:text-sm text-gray-800 dark:text-gray-200 leading-relaxed">
          <MarkdownContent content={parsed.narrativeIntro} />
        </div>
      )}

      {/* Main Content Area: Cards or Table */}
      {parsed.hadiths.length > 0 ? (
        layoutMode === 'cards' ? (
          /* Cards View */
          <div className="space-y-4">
            {parsed.hadiths.map((hItem, idx) => (
              <div 
                key={hItem.id || idx}
                className="rounded-xl border border-gray-200 dark:border-gray-700 p-4 bg-gray-50/40 dark:bg-gray-800/60 shadow-2xs space-y-3"
              >
                {/* Card Title & Hukm Badge */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-gray-100 dark:border-gray-700/60">
                  <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100 flex items-center gap-2">
                    <span className="w-5 h-5 rounded-full bg-teal-100 dark:bg-teal-900/60 text-teal-800 dark:text-teal-300 text-xs flex items-center justify-center font-mono font-bold">
                      {toBn(idx + 1)}
                    </span>
                    <span>{hItem.title}</span>
                  </h4>
                  {getHukmBadge(hItem.hukmGrade, hItem.hukm)}
                </div>

                {/* Arabic Matn Box */}
                {hItem.arabicMatn && (
                  <div 
                    className="p-3.5 rounded-xl bg-white dark:bg-gray-800 border border-teal-100 dark:border-teal-900/50 text-right leading-[2.2] font-arabic text-base sm:text-lg text-gray-900 dark:text-gray-100 select-text"
                    dir="rtl"
                  >
                    “{hItem.arabicMatn}”
                  </div>
                )}

                {/* Takhrij Sources & Book Badges */}
                <div className="flex flex-wrap items-center gap-1.5 pt-1">
                  <span className="text-xs font-semibold text-gray-500 dark:text-gray-400">উৎস গ্রন্থ:</span>
                  {hItem.sources.length > 0 ? (
                    hItem.sources.map((src, sIdx) => (
                      <span 
                        key={sIdx}
                        className="px-2 py-0.5 rounded-md bg-teal-50 dark:bg-teal-950/40 text-teal-800 dark:text-teal-300 border border-teal-200 dark:border-teal-800 text-xs font-medium"
                      >
                        {src}
                      </span>
                    ))
                  ) : (
                    <span className="text-xs text-gray-600 dark:text-gray-400 italic">
                      {hItem.rawTakhrij || 'প্রামাণ্য হাদিস গ্রন্থ'}
                    </span>
                  )}
                  {hItem.numbers && (
                    <span className="px-2 py-0.5 rounded-md bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 text-xs font-mono font-bold">
                      হাদীস নং {hItem.numbers}
                    </span>
                  )}
                </div>

                {/* Full Takhrij details line if distinct */}
                {hItem.rawTakhrij && (
                  <div className="text-xs text-gray-600 dark:text-gray-400 leading-relaxed pt-1 border-t border-gray-100 dark:border-gray-700/40">
                    <span className="font-semibold text-gray-700 dark:text-gray-300">তাখরীজ বিবরণ: </span>
                    <MarkdownContent inline content={hItem.rawTakhrij} />
                  </div>
                )}

                {/* Explanation / Context */}
                {hItem.explanation && (
                  <div className="text-xs sm:text-sm text-gray-800 dark:text-gray-200 leading-relaxed bg-white/70 dark:bg-gray-800/80 p-3 rounded-lg border border-gray-100 dark:border-gray-700">
                    <span className="font-semibold text-teal-800 dark:text-teal-300">তাৎপর্য ও ব্যাখ্যা: </span>
                    <MarkdownContent inline content={hItem.explanation} />
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          /* Structured Table View (Desktop/Tablet) */
          <div className="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700 shadow-2xs">
            <table className="w-full text-left text-xs sm:text-sm border-collapse">
              <thead className="bg-teal-50/70 dark:bg-gray-800/90 text-gray-700 dark:text-gray-300 border-b border-gray-200 dark:border-gray-700 font-bengali">
                <tr>
                  <th className="px-3 py-2.5 font-bold w-44">শিরোনাম / বর্ণনাকারী</th>
                  <th className="px-3 py-2.5 font-bold w-48">উৎস কিতাব ও হাদিস নং</th>
                  <th className="px-3 py-2.5 font-bold text-center w-28">সনদ / হুকুম</th>
                  <th className="px-3.5 py-2.5 font-bold text-right">হাদীসের মূল পাঠ ও ব্যাখ্যা</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 dark:divide-gray-700/60 bg-white dark:bg-gray-800">
                {parsed.hadiths.map((hItem, idx) => (
                  <tr key={idx} className="hover:bg-teal-50/30 dark:hover:bg-gray-700/30 transition-colors">
                    {/* Title */}
                    <td className="px-3 py-3 align-top font-bold text-gray-900 dark:text-gray-100 font-bengali">
                      <div className="flex items-center gap-1.5">
                        <span className="w-4 h-4 rounded-full bg-teal-100 dark:bg-teal-900 text-teal-800 dark:text-teal-300 text-[10px] flex items-center justify-center font-mono">
                          {toBn(idx + 1)}
                        </span>
                        <span>{hItem.title}</span>
                      </div>
                    </td>

                    {/* Sources & Numbers */}
                    <td className="px-3 py-3 align-top text-xs space-y-1 font-bengali">
                      <div className="flex flex-wrap gap-1">
                        {hItem.sources.map((s, si) => (
                          <span key={si} className="px-1.5 py-0.2 rounded bg-teal-50 dark:bg-teal-950/40 text-teal-800 dark:text-teal-300 text-[11px] font-semibold border border-teal-200 dark:border-teal-800">
                            {s}
                          </span>
                        ))}
                      </div>
                      {hItem.numbers && (
                        <div className="font-mono text-gray-600 dark:text-gray-400 text-[11px]">
                          নং: {hItem.numbers}
                        </div>
                      )}
                    </td>

                    {/* Hukm */}
                    <td className="px-3 py-3 align-top text-center whitespace-nowrap">
                      {getHukmBadge(hItem.hukmGrade, hItem.hukm)}
                    </td>

                    {/* Arabic Text & Explanation */}
                    <td className="px-3.5 py-3 align-top space-y-2">
                      {hItem.arabicMatn && (
                        <div className="font-arabic text-sm text-right leading-relaxed text-gray-900 dark:text-gray-100" dir="rtl">
                          “{hItem.arabicMatn}”
                        </div>
                      )}
                      {hItem.explanation && (
                        <div className="text-xs text-gray-700 dark:text-gray-300 leading-relaxed font-bengali border-t border-gray-100 dark:border-gray-700/40 pt-1.5">
                          {hItem.explanation}
                        </div>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )
      ) : null}

      {/* Turath Citation tags footer */}
      {parsed.citations.length > 0 && (
        <div className="pt-2 border-t border-gray-100 dark:border-gray-700/60 flex flex-wrap items-center gap-1.5 text-[11px] text-gray-500 dark:text-gray-400">
          <BookOpen className="w-3.5 h-3.5 text-gray-400" />
          <span>প্রামাণ্য রেফারেন্স কোড:</span>
          {parsed.citations.map((c, ci) => (
            <span key={ci} className="px-1.5 py-0.5 rounded bg-gray-100 dark:bg-gray-700 font-mono text-[10px]">
              turath:{c.id}{c.page ? ` (পৃ. ${c.page})` : ''}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

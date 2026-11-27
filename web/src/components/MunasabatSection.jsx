import React, { useState } from 'react';
import { GitCommit, ArrowUpRight, ArrowDownRight, Compass, BookMarked, ChevronDown, ChevronUp, Sparkles } from 'lucide-react';
import { toBn } from '../utils/helpers';

export default function MunasabatSection({ munasabat, ayahNumber = null, prevAyah = null, nextAyah = null }) {
  const [isExpanded, setIsExpanded] = useState(true);

  if (!munasabat || (!munasabat.prev_ayah_link && !munasabat.current_ayah_focus && !munasabat.next_ayah_link)) {
    return null;
  }

  // Check if source explicitly mentions Imam Razi alone vs multi-scholar attribution
  const sourceText = munasabat.source || '';
  const hasRaziOnly = /রাযী|رازي|كبير|মাফাতীহ|مفاتيح/i.test(sourceText) && !/বিক্বাঈ|বিকায়ী|আশূর|সুয়ূতী|তানাসুক|নযমুদ/i.test(sourceText);
  const nazmScholars = Array.isArray(munasabat.nazm_scholars) ? munasabat.nazm_scholars : [];
  const [showNazmPanel, setShowNazmPanel] = useState(false);

  return (
    <div id="sec-02-munasabat" className="scroll-mt-36 sm:scroll-mt-44 bg-white dark:bg-gray-800 rounded-2xl border border-indigo-100 dark:border-indigo-900/50 p-4 sm:p-5 shadow-xs space-y-3 font-bengali transition-colors">
      {/* Header bar */}
      <div className="flex items-center justify-between pb-2.5 border-b border-indigo-50 dark:border-indigo-950">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-indigo-50 dark:bg-indigo-950/60 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
            <GitCommit className="w-4 h-4" />
          </div>
          <div>
            <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100 flex flex-wrap items-center gap-1.5">
              <span>০২. আন্তঃআয়াত সংযোগ ও মুনাসাবাত</span>
              {hasRaziOnly ? (
                <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-indigo-50 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 border border-indigo-200/50 dark:border-indigo-800/40">
                  তাফসীরে কাবীর (ইমাম রাযী)
                </span>
              ) : sourceText ? (
                <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-indigo-50 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 border border-indigo-200/50 dark:border-indigo-800/40">
                  {sourceText}
                </span>
              ) : null}
            </h4>
            <p className="text-[11px] text-gray-500 dark:text-gray-400">
              কুরআনিক নাযম (نظم القرآن) অনুসারে পূর্বাপর আয়াতের কার্যকারণ ও বিষয়গত সম্পর্ক
            </p>
          </div>
        </div>

        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="p-1.5 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-500 transition-colors"
          title={isExpanded ? 'সংক্ষেপ করুন' : 'বিস্তারিত দেখুন'}
        >
          {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>
      </div>

      {isExpanded && (
        <div className="space-y-2.5 text-xs sm:text-sm pt-1">
          {/* 1. Connection with Previous Ayah */}
          {munasabat.prev_ayah_link && (
            <div className="p-3 rounded-xl bg-slate-50/80 dark:bg-gray-900/40 border border-slate-200/70 dark:border-gray-700/60 space-y-1">
              <div className="flex items-center gap-1.5 font-bold text-slate-800 dark:text-slate-200 text-xs">
                <ArrowUpRight className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400" />
                <span>
                  {prevAyah ? `পূর্ববর্তী আয়াত (${toBn(prevAyah)})-এর সাথে সংযোগ:` : 'পূর্ববর্তী প্রসঙ্গের সাথে যোগসূত্র (ربط الآية بما قبلها):'}
                </span>
              </div>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed pl-5 bn-justify">
                {munasabat.prev_ayah_link}
              </p>
            </div>
          )}

          {/* 2. Core Focal Point of Current Ayah */}
          {munasabat.current_ayah_focus && (
            <div className="p-3 rounded-xl bg-indigo-50/60 dark:bg-indigo-950/20 border border-indigo-200/70 dark:border-indigo-800/50 space-y-1">
              <div className="flex items-center gap-1.5 font-bold text-indigo-900 dark:text-indigo-200 text-xs">
                <Compass className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400" />
                <span>
                  {ayahNumber ? `আয়াত ${toBn(ayahNumber)}-এর কেন্দ্রীয় বক্তব্য ও মূল হিকমত (محور الآية):` : 'আলোচ্য আয়াতের কেন্দ্রীয় তাৎপর্য:'}
                </span>
              </div>
              <p className="text-gray-800 dark:text-gray-200 leading-relaxed pl-5 font-medium bn-justify">
                {munasabat.current_ayah_focus}
              </p>
            </div>
          )}

          {/* 3. Transition to Next Ayah */}
          {munasabat.next_ayah_link && (
            <div className="p-3 rounded-xl bg-slate-50/80 dark:bg-gray-900/40 border border-slate-200/70 dark:border-gray-700/60 space-y-1">
              <div className="flex items-center gap-1.5 font-bold text-slate-800 dark:text-slate-200 text-xs">
                <ArrowDownRight className="w-3.5 h-3.5 text-teal-600 dark:text-teal-400" />
                <span>
                  {nextAyah ? `পরবর্তী আয়াত (${toBn(nextAyah)})-এর সাথে উত্তরণ ও সংযোগ:` : 'পরবর্তী প্রসঙ্গের সাথে সংযোগ (ربط الآية بما بعدها):'}
                </span>
              </div>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed pl-5 bn-justify">
                {munasabat.next_ayah_link}
              </p>
            </div>
          )}

          {/* Classical Nazm al-Quran Scholars Panel */}
          {nazmScholars.length > 0 && (
            <div className="pt-1">
              <button
                type="button"
                onClick={() => setShowNazmPanel((prev) => !prev)}
                className="w-full flex items-center justify-between px-3 py-2 rounded-lg text-xs font-semibold bg-amber-50/70 dark:bg-amber-950/30 hover:bg-amber-100/70 dark:hover:bg-amber-950/50 text-amber-900 dark:text-amber-200 border border-amber-200/70 dark:border-amber-800/40 transition-colors"
                aria-expanded={showNazmPanel}
              >
                <span>শাস্ত্রীয় নাযমুল কুরআন আকরগ্রন্থ ({nazmScholars.length}টি আকর উৎস: বিক্বাঈ / রাযী / ইবনে আশূর)</span>
                <span className="text-[11px] font-mono">{showNazmPanel ? '▲' : '▼'}</span>
              </button>

              {showNazmPanel && (
                <div className="mt-2.5 space-y-2.5">
                  {nazmScholars.map((item, idx) => (
                    <div
                      key={`${item.scholar || 'scholar'}-${idx}`}
                      className="rounded-lg border border-amber-200/60 dark:border-amber-800/40 bg-amber-50/30 dark:bg-gray-900/50 p-3 space-y-2"
                    >
                      <div className="flex flex-wrap items-center justify-between gap-1.5">
                        <span className="text-xs font-bold text-amber-900 dark:text-amber-200">
                          {item.scholar} — <span className="font-semibold text-gray-700 dark:text-gray-300">{item.book}</span>
                        </span>
                        {item.citation && (
                          <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-white dark:bg-gray-800 text-amber-800 dark:text-amber-300 border border-amber-200 dark:border-amber-800/60">
                            {item.citation}
                          </span>
                        )}
                      </div>

                      {item.arabic_excerpt && (
                        <blockquote
                          dir="rtl"
                          lang="ar"
                          className="font-arabic text-base sm:text-lg leading-loose text-right text-gray-900 dark:text-gray-100 bg-white/80 dark:bg-gray-800/70 border-r-4 border-amber-500 pr-3 pl-2.5 py-2 rounded"
                        >
                          {item.arabic_excerpt}
                        </blockquote>
                      )}

                      {item.analysis_bn && (
                        <p className="text-xs sm:text-sm text-gray-800 dark:text-gray-200 leading-relaxed">
                          {item.analysis_bn}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Source Citation Footer */}
          <div className="text-[10px] text-gray-400 dark:text-gray-500 flex items-center justify-between pt-1">
            <span>
              {hasRaziOnly
                ? 'উৎস: তাফসীরে কাবীর (মাফাতীহুল গায়েব) — ইমাম ফখরুদ্দীন আর-রাযী (র.)'
                : sourceText
                  ? `উৎস: ${sourceText}`
                  : 'ইলমুল মুনাসাবাত ও নাযমুত তানযীল'}
            </span>
            <span className="italic">ইলমুল মুনাসাবাত</span>
          </div>
        </div>
      )}
    </div>
  );
}

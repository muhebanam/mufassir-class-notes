import React, { useState } from 'react';
import { ChevronDown, ChevronUp, BookOpen, Scale, Sparkles } from 'lucide-react';
import MarkdownContent from './MarkdownContent';
import { toBn } from '../utils/helpers';

export default function MasalaCard({ card, index }) {
  // Default to true so research daleel is immediately visible on mobile
  const [showDaleel, setShowDaleel] = useState(true);

  if (!card) return null;

  // Determine agreement badge from explicit card data or defaults
  let badgeText = null;
  let badgeColor = "";

  if (card.consensus) {
    badgeText = "চার মাযহাবে একমত (ইজমা/সর্বসম্মত)";
    badgeColor = "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800";
  } else if (card.badge) {
    badgeText = card.badge;
    badgeColor = "bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border-amber-200 dark:border-amber-800";
  } else {
    badgeText = "৪ মাযহাবের তুলনামূলক ফতোয়া";
    badgeColor = "bg-teal-100 text-teal-800 dark:bg-teal-950 dark:text-teal-300 border-teal-200 dark:border-teal-800";
  }

  // Clean title
  const cleanTitle = (card.title || "").replace(/^\*+|\*+$/g, "");

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm overflow-hidden transition-all hover:shadow-md mb-5">
      {/* Card Header */}
      <div className="p-4 sm:p-5 bg-gradient-to-r from-gray-50 to-emerald-50/40 dark:from-gray-800 dark:to-emerald-950/20 border-b border-gray-200 dark:border-gray-700 flex flex-col sm:flex-row sm:items-center justify-between gap-2.5">
        <div className="flex items-start gap-2.5">
          <div className="p-1.5 rounded-lg bg-emerald-600 text-white shrink-0 mt-0.5">
            <Scale className="w-4 h-4" />
          </div>
          <h4 className="text-base sm:text-lg font-bold text-gray-900 dark:text-gray-100 font-bengali leading-snug">
            <MarkdownContent inline content={cleanTitle} />
          </h4>
        </div>
        {badgeText && (
          <span className={`text-xs px-2.5 py-1 rounded-full border font-semibold shrink-0 self-start sm:self-auto ${badgeColor}`}>
            {badgeText}
          </span>
        )}
      </div>

      {/* 2x2 Madhhab Grid */}
      <div className="p-4 sm:p-5 grid grid-cols-1 md:grid-cols-2 gap-3.5">
        {/* Hanafi */}
        <div className="p-3.5 rounded-xl bg-amber-50/50 dark:bg-amber-950/20 border-l-4 border-amber-500 border-t border-r border-b border-gray-200/60 dark:border-gray-700/60 space-y-1.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-amber-800 dark:text-amber-300 font-bengali">
              হানাফী মাযহাব (الحنفية)
            </span>
          </div>
          <div className="text-sm text-gray-800 dark:text-gray-200 font-bengali leading-relaxed bn-justify">
            <MarkdownContent inline content={card.hanafi || "—"} />
          </div>
        </div>

        {/* Maliki */}
        <div className="p-3.5 rounded-xl bg-teal-50/50 dark:bg-teal-950/20 border-l-4 border-teal-500 border-t border-r border-b border-gray-200/60 dark:border-gray-700/60 space-y-1.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-teal-800 dark:text-teal-300 font-bengali">
              মালিকী মাযহাব (المالكية)
            </span>
          </div>
          <div className="text-sm text-gray-800 dark:text-gray-200 font-bengali leading-relaxed bn-justify">
            <MarkdownContent inline content={card.maliki || "—"} />
          </div>
        </div>

        {/* Shafi'i */}
        <div className="p-3.5 rounded-xl bg-indigo-50/50 dark:bg-indigo-950/20 border-l-4 border-indigo-500 border-t border-r border-b border-gray-200/60 dark:border-gray-700/60 space-y-1.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-800 dark:text-indigo-300 font-bengali">
              শাফিঈ মাযহাব (الشافعية)
            </span>
          </div>
          <div className="text-sm text-gray-800 dark:text-gray-200 font-bengali leading-relaxed bn-justify">
            <MarkdownContent inline content={card.shafii || "—"} />
          </div>
        </div>

        {/* Hanbali */}
        <div className="p-3.5 rounded-xl bg-emerald-50/50 dark:bg-emerald-950/20 border-l-4 border-emerald-500 border-t border-r border-b border-gray-200/60 dark:border-gray-700/60 space-y-1.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-800 dark:text-emerald-300 font-bengali">
              হাম্বলী মাযহাব (الحنابلة)
            </span>
          </div>
          <div className="text-sm text-gray-800 dark:text-gray-200 font-bengali leading-relaxed bn-justify">
            <MarkdownContent inline content={card.hanbali || "—"} />
          </div>
        </div>
      </div>

      {/* Collapsible Daleel & Argument Section */}
      {card.daleel && card.daleel.length > 0 && (
        <div className="border-t border-gray-200 dark:border-gray-700">
          <button
            onClick={() => setShowDaleel(!showDaleel)}
            aria-expanded={showDaleel}
            className="w-full px-4 sm:px-5 py-2.5 bg-gray-50/70 dark:bg-gray-800/80 hover:bg-gray-100 dark:hover:bg-gray-700/60 flex items-center justify-between text-left text-xs sm:text-sm font-semibold text-gray-700 dark:text-gray-300 transition"
          >
            <div className="flex items-center gap-2">
              <Sparkles className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
              <span>প্রধান দলীল ও শাস্ত্রীয় পর্যালোচনা ({toBn(card.daleel.length)}টি দলীল)</span>
            </div>
            {showDaleel ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>

          {showDaleel && (
            <div className="p-4 sm:p-5 bg-white dark:bg-gray-800 space-y-2.5 border-t border-gray-100 dark:border-gray-700 text-sm">
              {card.daleel.map((d, dIdx) => (
                <div key={dIdx} className="leading-relaxed">
                  <MarkdownContent content={d} />
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Sources Tags / Chips */}
      {card.sources && card.sources.length > 0 && (
        <div className="px-4 sm:px-5 py-3 bg-gray-50/50 dark:bg-gray-800/50 border-t border-gray-100 dark:border-gray-700/60 flex flex-wrap items-center gap-1.5 text-xs">
          <span className="flex items-center gap-1 text-gray-500 dark:text-gray-400 font-semibold mr-1 font-bengali">
            <BookOpen className="w-3.5 h-3.5 text-gray-400" />
            <span>প্রামাণ্য উৎস:</span>
          </span>
          {card.sources.map((src, sIdx) => {
            const cleanSrc = src.replace(/।$/, "").trim();
            if (!cleanSrc) return null;
            return (
              <span
                key={sIdx}
                className="px-2 py-0.5 rounded-md bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-300 font-medium font-bengali shadow-sm"
              >
                <MarkdownContent inline content={cleanSrc} />
              </span>
            );
          })}
        </div>
      )}
    </div>
  );
}

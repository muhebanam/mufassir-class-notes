import React, { useState } from 'react';
import { BookMarked, ChevronDown, ChevronUp, Layers } from 'lucide-react';
import MarkdownContent from './MarkdownContent';
import TafsirAppMenu from './TafsirAppMenu';
import { toBn } from '../utils/helpers';

export default function ComparativeTafsirSection({ 
  content, 
  surah = 24, 
  ayahNumber = 1, 
  covers = null,
  bengaliFontSize = 16 
}) {
  const [isExpanded, setIsExpanded] = useState(true);

  if (!content || !content.trim()) {
    return null;
  }

  // Format covers range badge (e.g., [২, ৩] -> "আয়াত ২–৩-এর যৌথ আলোচনা")
  const isMultiAyahCover = Array.isArray(covers) && covers.length === 2 && covers[0] !== covers[1];
  const coversLabel = isMultiAyahCover ? `আয়াত ${toBn(covers[0])}–${toBn(covers[1])}-এর যৌথ আলোচনা` : null;

  return (
    <div 
      id="sec-05-tafsir"
      className="scroll-mt-36 sm:scroll-mt-44 bg-white dark:bg-gray-800 rounded-2xl border border-amber-200/80 dark:border-amber-800/60 p-4 sm:p-5 shadow-xs space-y-3 font-bengali transition-colors"
    >
      {/* Header bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 pb-3 border-b border-amber-100 dark:border-amber-900/40">
        <div className="flex items-start sm:items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl bg-amber-50 dark:bg-amber-950/70 flex items-center justify-center text-amber-600 dark:text-amber-400 shrink-0 border border-amber-200/60 dark:border-amber-800/40 shadow-2xs">
            <BookMarked className="w-4 h-4" />
          </div>
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100 flex items-center gap-1.5">
                <span>০৫. তুলনামূলক তাফসীর ও বিশ্লেষণ</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-amber-100/70 dark:bg-amber-950 text-amber-800 dark:text-amber-300 font-bold border border-amber-300/40 dark:border-amber-800/50">
                  আয়াত {toBn(ayahNumber)}
                </span>
              </h4>

              {/* Multi-Ayah Joint Coverage Badge */}
              {coversLabel && (
                <span className="inline-flex items-center gap-1 text-[11px] font-semibold px-2 py-0.5 rounded-full bg-indigo-50 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800 shadow-2xs animate-fadeIn">
                  <Layers className="w-3 h-3 text-indigo-500" />
                  <span>{coversLabel}</span>
                </span>
              )}
            </div>
            <p className="text-[11px] text-gray-500 dark:text-gray-400">
              তাফসীরে কবীর (ইমাম রাযী), জামিউল বায়ান (তাবারী), তাফসীর ইবনে কাসীর ও কুরতুবী
            </p>
          </div>
        </div>

        {/* Right Action: Enhanced Tafsir.app Dropdown Menu & Expand Toggle */}
        <div className="flex items-center gap-2 self-end sm:self-center">
          <TafsirAppMenu surah={surah} ayahNumber={ayahNumber} />

          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-1.5 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-500 transition-colors"
            title={isExpanded ? 'সংক্ষেপ করুন' : 'বিস্তারিত দেখুন'}
          >
            {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      {isExpanded && (
        <div 
          className="prose dark:prose-invert font-bengali leading-relaxed text-gray-800 dark:text-gray-200 text-xs sm:text-sm space-y-3 pt-1"
          style={{ fontSize: `${bengaliFontSize}px` }}
        >
          <MarkdownContent content={content} />
        </div>
      )}
    </div>
  );
}

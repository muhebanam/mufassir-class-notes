import React, { useState } from 'react';
import { BookMarked, ExternalLink, ChevronDown, ChevronUp, Sparkles, BookOpen } from 'lucide-react';
import MarkdownContent from './MarkdownContent';

export default function ComparativeTafsirSection({ 
  content, 
  surah = 24, 
  ayahNumber = 1, 
  bengaliFontSize = 16 
}) {
  const [isExpanded, setIsExpanded] = useState(true);

  if (!content || !content.trim()) {
    return null;
  }

  const toBn = (num) => {
    const bn = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
    return String(num).replace(/[0-9]/g, d => bn[d]);
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl border border-amber-200/80 dark:border-amber-800/60 p-4 sm:p-5 shadow-xs space-y-3 font-bengali transition-colors">
      {/* Header bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 pb-3 border-b border-amber-100 dark:border-amber-900/40">
        <div className="flex items-start sm:items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl bg-amber-50 dark:bg-amber-950/70 flex items-center justify-center text-amber-600 dark:text-amber-400 shrink-0 border border-amber-200/60 dark:border-amber-800/40 shadow-2xs">
            <BookMarked className="w-4 h-4" />
          </div>
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100 flex items-center gap-1.5">
                <span>তুলনামূলক তাফসীর ও বিশ্লেষণ</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-amber-100/70 dark:bg-amber-950 text-amber-800 dark:text-amber-300 font-bold border border-amber-300/40 dark:border-amber-800/50">
                  আয়াত {toBn(ayahNumber)}
                </span>
              </h4>
            </div>
            <p className="text-[11px] text-gray-500 dark:text-gray-400">
              তাফসীরে কবীর (ইমাম রাযী), জামিউল বায়ান (তাবারী), তাফসীর ইবনে কাসীর ও কুরতুবী
            </p>
          </div>
        </div>

        {/* Right Action: External Tafsir.app Link & Expand Toggle */}
        <div className="flex items-center gap-2 self-end sm:self-center">
          <a
            href={`https://tafsir.app/${surah}/${ayahNumber}`}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-semibold bg-emerald-50 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 hover:bg-emerald-100 transition shadow-2xs"
            title="الباحث القرآني (tafsir.app)-এ এই আয়াতের ২৫+ আরবি তাফসীর দেখুন"
          >
            <ExternalLink className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            <span>الباحث القرآني</span>
            <span className="text-[10px] font-mono text-emerald-600 dark:text-emerald-400 hidden sm:inline">(tafsir.app)</span>
          </a>

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

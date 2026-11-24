import React from 'react';
import { Volume2, BookOpen, ShieldCheck } from 'lucide-react';
import MarkdownContent, { normalizeQuranBrackets } from './MarkdownContent';

export default function QiraatTable({ tableData = [], title = "১০ মুতাওয়াতির কিরাআত পাঠভেদ সারণি" }) {
  const toBn = (num) => {
    const bn = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
    return String(num).replace(/[0-9]/g, d => bn[d]);
  };

  const toAr = (str) => {
    if (str === null || str === undefined) return '';
    const arDigits = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
    return String(str)
      .replace(/\s*-\s*(?:Dammah|Kasrah)\b/gi, '')
      .replace(/[0-9]/g, d => arDigits[Number(d)]);
  };

  if (!tableData || tableData.length === 0) {
    return (
      <div className="text-gray-500 italic py-6 text-center font-bengali text-sm">
        এই অংশের জন্য দশ কিরাআতের কোনো স্বতন্ত্র পাঠভেদ নেই; সকল ক্বারী বিশুদ্ধ মুতাওয়াতির ঐকমত্যে পাঠ করেছেন।
      </div>
    );
  }

  return (
    <div className="space-y-3 layout-safe">
      {/* Header bar */}
      <div className="flex flex-wrap items-center justify-between gap-2 text-xs font-bengali pb-2 border-b border-gray-100 dark:border-gray-700">
        <div className="flex items-center gap-2">
          <Volume2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
          <h4 className="font-bold text-sm text-gray-900 dark:text-gray-100">
            {title} ({toBn(tableData.length)}টি প্রামাণ্য বর্ণনা)
          </h4>
        </div>
        <span className="text-xs text-emerald-800 dark:text-emerald-300 font-semibold bg-emerald-50 dark:bg-emerald-950/40 px-2.5 py-0.5 rounded-full border border-emerald-200 dark:border-emerald-800">
          মাদীনা মুনাওয়ারা বাহাউথ ডেটাবেস
        </span>
      </div>

      {/* DESKTOP / TABLET: Structured Responsive Table */}
      <div className="hidden sm:block overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700 shadow-2xs">
        <table className="w-full text-left text-xs sm:text-sm border-collapse">
          <thead className="bg-emerald-50/70 dark:bg-gray-800/90 text-gray-700 dark:text-gray-300 border-b border-gray-200 dark:border-gray-700 font-bengali">
            <tr>
              <th className="px-3.5 py-2.5 text-center font-bold w-16">আয়াত</th>
              <th className="px-3.5 py-2.5 font-bold w-36 sm:w-44 text-right">শব্দ (ক্রম)</th>
              <th className="px-3.5 py-2.5 font-bold w-40 sm:w-48 text-right">ক্বারী / রাবী</th>
              <th className="px-4 py-2.5 font-bold text-right">কিরাআতের বিশুদ্ধ মূল পাঠ ও নিয়ম</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 dark:divide-gray-700/60 bg-white dark:bg-gray-800">
            {tableData.map((row, rIdx) => {
              const ayahNum = toAr(row['আয়াত'] || '');
              const wordStr = toAr(row['শব্দ (ক্রম)'] || row['শব্দ'] || '');
              const qariStr = toAr(row['ক্বারী / রাবী (বাহাউথ)'] || row['ক্বারী / রাবী'] || row['ক্বারী'] || '');
              const ruleStr = toAr(
                row['কিরাআতের পাঠভেদ ও নিয়ম (অবিকৃত মূল পাঠ)'] ||
                row['কিরাআতের বিশুদ্ধ মূল পাঠ ও নিয়ম'] ||
                row['কিরাআত রূপ'] ||
                row['নিয়ম'] ||
                row['পাঠভেদ'] || ''
              );

              return (
                <tr key={rIdx} className="hover:bg-emerald-50/30 dark:hover:bg-gray-700/30 transition-colors">
                  {/* Ayah number */}
                  <td className="px-3.5 py-3 text-center font-arabic font-bold text-emerald-700 dark:text-emerald-400 whitespace-nowrap text-base" dir="rtl">
                    <MarkdownContent inline content={ayahNum} />
                  </td>

                  {/* Word */}
                  <td className="px-3.5 py-3 text-right whitespace-nowrap table-cell-arabic" dir="rtl">
                    <span className="font-arabic text-sm sm:text-base text-emerald-900 dark:text-emerald-200" dir="rtl">
                      {normalizeQuranBrackets(wordStr)}
                    </span>
                  </td>

                  {/* Qari / Rawi */}
                  <td className="px-3.5 py-3 text-right font-medium whitespace-nowrap table-cell-arabic" dir="rtl">
                    <span className="font-arabic text-sm sm:text-base text-gray-800 dark:text-gray-200" dir="rtl">
                      {qariStr}
                    </span>
                  </td>

                  {/* Text & Rules */}
                  <td className="px-4 py-3 text-right table-cell-arabic" dir="rtl">
                    <span className="font-arabic text-sm sm:text-base text-gray-900 dark:text-gray-100 leading-loose" dir="rtl">
                      {ruleStr}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* MOBILE VIEW: Mobile Card Stack (<640px) */}
      <div className="sm:hidden space-y-2.5">
        {tableData.map((row, rIdx) => {
          const ayahNum = toAr(row['আয়াত'] || '');
          const wordStr = toAr(row['শব্দ (ক্রম)'] || row['শব্দ'] || '');
          const qariStr = toAr(row['ক্বারী / রাবী (বাহাউথ)'] || row['ক্বারী / রাবী'] || row['ক্বারী'] || '');
          const ruleStr = toAr(
            row['কিরাআতের পাঠভেদ ও নিয়ম (অবিকৃত মূল পাঠ)'] ||
            row['কিরাআতের বিশুদ্ধ মূল পাঠ ও নিয়ম'] ||
            row['কিরাআত রূপ'] ||
            row['নিয়ম'] ||
            row['পাঠভেদ'] || ''
          );

          return (
            <div
              key={rIdx}
              className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-3 shadow-2xs space-y-2 font-bengali"
            >
              <div className="flex items-center justify-between gap-2 border-b border-gray-100 dark:border-gray-700/60 pb-1.5">
                <span className="px-2 py-0.5 rounded bg-emerald-100 dark:bg-emerald-900/40 text-emerald-800 dark:text-emerald-300 font-arabic text-xs font-bold" dir="rtl">
                  آية {toAr(ayahNum.replace(/\*/g, ''))}
                </span>
                <span className="font-arabic font-bold text-sm text-emerald-800 dark:text-emerald-300 table-cell-arabic" dir="rtl">
                  {normalizeQuranBrackets(wordStr)}
                </span>
              </div>

              <div className="flex items-center justify-between gap-2 text-xs">
                <span className="text-gray-500 dark:text-gray-400">ক্বারী / রাবী:</span>
                <span className="font-arabic font-semibold text-gray-900 dark:text-gray-100 table-cell-arabic" dir="rtl">
                  {qariStr}
                </span>
              </div>

              <div className="bg-emerald-50/50 dark:bg-emerald-950/20 p-2.5 rounded-lg text-right table-cell-arabic" dir="rtl">
                <span className="font-arabic text-sm text-gray-900 dark:text-gray-100 leading-relaxed" dir="rtl">
                  {ruleStr}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

import React, { useEffect } from 'react';
import { X, Sparkles, BookOpen, Layers, ExternalLink, Bookmark } from 'lucide-react';

export default function WordInspectorModal({ word, ayahNumber, onClose }) {
  // Listen for Escape key to dismiss
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!word) return null;

  const toBn = (num) => {
    const bn = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
    return String(num).replace(/[0-9]/g, d => bn[d]);
  };

  const t = word.tahqeeqRef;
  const m = word.mufradatRef;
  const morph = t?.morphology || {};
  const isVerb = t?.word_type === 'فعل';
  const hasClassicalNotes = t?.classical_notes && t.classical_notes.length > 0;

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4 bg-black/50 backdrop-blur-xs transition-opacity duration-200">
      {/* Backdrop click dismiss */}
      <div className="absolute inset-0" onClick={onClose} />

      {/* Modal / Bottom Sheet Card */}
      <div 
        className="relative z-10 w-full sm:max-w-lg bg-white dark:bg-gray-850 rounded-t-3xl sm:rounded-3xl border border-gray-200 dark:border-gray-700 shadow-2xl overflow-hidden max-h-[85vh] sm:max-h-[90vh] flex flex-col transition-all duration-200 animate-in fade-in slide-in-from-bottom-4"
        dir="ltr"
      >
        {/* Header Bar */}
        <div className="flex items-center justify-between p-4 sm:p-5 border-b border-gray-100 dark:border-gray-700/80 bg-emerald-50/50 dark:bg-emerald-950/20">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-emerald-100 dark:bg-emerald-900/60 flex items-center justify-center text-emerald-700 dark:text-emerald-300">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100 font-bengali">
                শাব্দিক তাহকীক ও রূপতত্ত্ব
              </h3>
              <p className="text-xs text-gray-500 dark:text-gray-400 font-bengali">
                {ayahNumber ? `আয়াত ${toBn(ayahNumber)}-এর শব্দ ক্রম ${toBn(word.id)}` : 'শব্দ রূপতাত্ত্বিক বিশ্লেষণ'}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-xl text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition"
            title="বন্ধ করুন (Esc)"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Scrollable Content */}
        <div className="p-4 sm:p-6 overflow-y-auto space-y-4 font-bengali text-gray-800 dark:text-gray-200">
          {/* Main Word Hero Banner */}
          <div className="text-center p-4 rounded-2xl bg-gradient-to-b from-emerald-50/70 to-teal-50/40 dark:from-emerald-950/30 dark:to-teal-950/10 border border-emerald-200/60 dark:border-emerald-800/40 space-y-1">
            <div className="font-quran text-3xl sm:text-4xl font-bold text-emerald-800 dark:text-emerald-300 leading-loose" dir="rtl">
              {word.arabic}
            </div>
            <div className="text-base sm:text-lg font-bold text-gray-900 dark:text-gray-100">
              {word.meaning_bn}
            </div>
            {word.pos && (
              <span className="inline-block mt-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 dark:bg-emerald-900/50 text-emerald-800 dark:text-emerald-200 font-arabic" dir="rtl">
                {word.pos === 'فعل' ? 'فعل (ক্রিয়া)' : word.pos === 'اسم' ? 'اسم (বিশেষ্য)' : 'حرف (অব্যয়)'}
              </span>
            )}
          </div>

          {/* Deep Tahqeeq Section if available */}
          {t ? (
            <div className="space-y-3.5">
              {/* Badges Grid: Root, Bab, Jins */}
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs">
                {morph.root && (
                  <div className="p-2.5 rounded-xl bg-gray-50 dark:bg-gray-800 border border-gray-200/70 dark:border-gray-700">
                    <span className="text-gray-500 dark:text-gray-400 block text-[11px]">মূলবর্ণ (মাদ্দাহ)</span>
                    <strong className="font-arabic text-sm text-emerald-700 dark:text-emerald-300 block mt-0.5" dir="rtl">
                      {morph.root}
                    </strong>
                  </div>
                )}
                {morph.bab && (
                  <div className="p-2.5 rounded-xl bg-gray-50 dark:bg-gray-800 border border-gray-200/70 dark:border-gray-700">
                    <span className="text-gray-500 dark:text-gray-400 block text-[11px]">বাব (باب)</span>
                    <strong className="font-arabic text-sm text-gray-800 dark:text-gray-200 block mt-0.5" dir="rtl">
                      {morph.bab}
                    </strong>
                  </div>
                )}
                {morph.jins && (
                  <div className="p-2.5 rounded-xl bg-gray-50 dark:bg-gray-800 border border-gray-200/70 dark:border-gray-700">
                    <span className="text-gray-500 dark:text-gray-400 block text-[11px]">জিনস (جنس)</span>
                    <strong className="font-arabic text-sm text-gray-800 dark:text-gray-200 block mt-0.5" dir="rtl">
                      {morph.jins}
                    </strong>
                  </div>
                )}
              </div>

              {/* Verb Details: Sighah, Bahas, Masdar */}
              {isVerb && (
                <div className="p-3.5 rounded-xl bg-emerald-50/40 dark:bg-emerald-950/20 border border-emerald-100 dark:border-emerald-900/30 space-y-2 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-emerald-900 dark:text-emerald-300">সীগাহ ও বহছ:</span>
                    <span className="font-arabic font-bold text-emerald-800 dark:text-emerald-200" dir="rtl">
                      {morph.sighah} • {morph.bahas}
                    </span>
                  </div>
                  {morph.masdar && (
                    <div className="pt-2 border-t border-emerald-100 dark:border-emerald-900/40 text-gray-700 dark:text-gray-300">
                      <span className="text-gray-500 dark:text-gray-400">মাসদার:</span>{' '}
                      <strong className="font-arabic text-sm">{morph.masdar}</strong>{' '}
                      <span className="italic text-gray-500">({morph.masdar_meaning})</span>
                    </div>
                  )}
                </div>
              )}

              {/* Noun Details: Singular/Plural */}
              {!isVerb && morph.singular_plural && (
                <div className="p-3 rounded-xl bg-gray-50 dark:bg-gray-800 border border-gray-200/60 dark:border-gray-700 text-xs">
                  <span className="text-gray-500 dark:text-gray-400 block mb-1">বচন বিন্যাস:</span>
                  <span className="font-arabic font-semibold text-sm" dir="rtl">
                    {morph.singular_plural}
                  </span>
                </div>
              )}

              {/* Taleel / Irab */}
              {t.taleel_or_irab && (
                <div className="p-3.5 rounded-xl bg-gray-50 dark:bg-gray-800 border border-gray-200/60 dark:border-gray-700 text-xs leading-relaxed space-y-1">
                  <span className="font-bold text-gray-900 dark:text-gray-100 block">তালীল ও ইরাব:</span>
                  <p className="text-gray-700 dark:text-gray-300">{t.taleel_or_irab}</p>
                </div>
              )}

              {/* Classical Citations */}
              {hasClassicalNotes && (
                <div className="space-y-2 pt-1">
                  <span className="font-bold text-xs text-amber-900 dark:text-amber-300 block">
                    শাস্ত্রীয় প্রামাণ্য উদ্ধৃতি:
                  </span>
                  {t.classical_notes.map((cn, cIdx) => (
                    <div key={cIdx} className="p-3 rounded-xl bg-amber-50/70 dark:bg-amber-950/20 border border-amber-200/60 dark:border-amber-800/40 text-xs leading-relaxed">
                      <strong className="text-amber-900 dark:text-amber-300 block mb-0.5">
                        {cn.scholar_or_book}:
                      </strong>
                      <span className="text-gray-700 dark:text-gray-300">{cn.note}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : m ? (
            /* Legacy Mufradat View */
            <div className="space-y-3 text-xs">
              {m['মূলধাতু'] && (
                <div className="p-2.5 rounded-xl bg-gray-50 dark:bg-gray-800 border border-gray-200/70 dark:border-gray-700">
                  <span className="text-gray-500 dark:text-gray-400 block text-[11px]">মূলধাতু</span>
                  <strong className="font-arabic text-sm text-emerald-700 dark:text-emerald-300 block mt-0.5" dir="rtl">
                    {m['মূলধাতু']}
                  </strong>
                </div>
              )}
              {m['সীগা / ওযন'] && (
                <div className="p-2.5 rounded-xl bg-gray-50 dark:bg-gray-800 border border-gray-200/70 dark:border-gray-700">
                  <span className="text-gray-500 dark:text-gray-400 block text-[11px]">সীগা / ওযন</span>
                  <strong className="font-arabic text-sm block mt-0.5" dir="rtl">
                    {m['সীগা / ওযন']}
                  </strong>
                </div>
              )}
              {m['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র'] && (
                <div className="p-3 rounded-xl bg-gray-50 dark:bg-gray-800 border border-gray-200/70 dark:border-gray-700">
                  <span className="text-gray-500 dark:text-gray-400 block text-[11px] mb-1">ভাষাতাত্ত্বিক ব্যাখ্যা:</span>
                  <p className="leading-relaxed text-gray-700 dark:text-gray-300">
                    {m['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র']}
                  </p>
                </div>
              )}
            </div>
          ) : (
            /* Simple Word Fallback */
            <div className="p-4 rounded-xl bg-gray-50 dark:bg-gray-800 text-center text-xs text-gray-500 dark:text-gray-400 space-y-1">
              <p>এই শব্দের প্রাথমিক শব্দানুগ অর্থ ও প্রয়োগ উপরে উল্লেখ করা হয়েছে।</p>
              <p className="text-[11px] italic text-gray-400">
                কুরআনিক সরফ ও নাহু অনুসারে এটি সাধারণ শব্দ হিসেবে ব্যবহৃত হয়েছে।
              </p>
            </div>
          )}
        </div>

        {/* Footer Dismiss Button */}
        <div className="p-3.5 border-t border-gray-100 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-850 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bengali text-xs font-bold transition shadow-xs"
          >
            বন্ধ করুন
          </button>
        </div>
      </div>
    </div>
  );
}

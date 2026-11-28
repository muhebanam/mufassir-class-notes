import React, { useState, useEffect } from 'react';
import { X, ChevronDown, ChevronUp, ExternalLink, BookOpen } from 'lucide-react';

export default function RootConcordanceModal({ rootData, onClose }) {
  const [expanded, setExpanded] = useState(new Set());
  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState('surah'); // 'surah' | 'page'

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!rootData) return null;

  const { root_ar, count, verses } = rootData;
  const toBn = (num) => String(num).replace(/[0-9]/g, d => '০১২৩৪৫৬৭৮৯'[d]);

  // Filter & sort
  const filtered = verses
    .filter(v => 
      v.verse_key?.includes(search) ||
      v.text_raw?.includes(search) ||
      String(v.surah).includes(search) ||
      String(v.ayah).includes(search)
    )
    .sort((a, b) => {
      if (sortBy === 'surah') {
        if (a.surah !== b.surah) return a.surah - b.surah;
        return a.ayah - b.ayah;
      }
      return (a.page_number || 0) - (b.page_number || 0);
    });

  // Pagination
  const [page, setPage] = useState(0);
  const PAGE_SIZE = 20;
  const totalPages = Math.ceil(filtered.length / PAGE_SIZE);
  const paginated = filtered.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);

  const toggleExpand = (verseKey) => {
    setExpanded(prev => {
      const next = new Set(prev);
      if (next.has(verseKey)) next.delete(verseKey);
      else next.add(verseKey);
      return next;
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4 bg-black/50 backdrop-blur-xs">
      <div className="absolute inset-0" onClick={onClose} />
      <div 
        className="relative z-10 w-full sm:max-w-3xl bg-white dark:bg-gray-850 rounded-t-3xl sm:rounded-3xl border border-gray-200 dark:border-gray-700 shadow-2xl overflow-hidden max-h-[90vh] flex flex-col"
        dir="ltr"
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 sm:p-5 border-b border-gray-100 dark:border-gray-700 bg-emerald-50/50 dark:bg-emerald-950/20">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-100 dark:bg-emerald-900/60 flex items-center justify-center text-emerald-700 dark:text-emerald-300">
              <BookOpen className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-base sm:text-lg text-gray-900 dark:text-gray-100 font-bengali">
                মূলদান সমানুপাতিক (Root Concordance)
              </h3>
              <p className="text-xs text-gray-500 dark:text-gray-400 font-bengali">
                মূলবর্ণ <span className="font-arabic font-bold text-emerald-700 dark:text-emerald-300 ml-1" dir="rtl">{root_ar}</span> — মোট <span className="font-mono">{toBn(count)}</span> আয়াত
              </p>
            </div>
          </div>
          <button onClick={onClose} className="p-1.5 rounded-xl text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition" title="বন্ধ করুন (Esc)">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Toolbar: Search + Sort */}
        <div className="p-4 border-b border-gray-100 dark:border-gray-700 bg-gray-50/30 dark:bg-gray-900/30 space-y-2">
          <div className="relative">
            <input
              type="text"
              placeholder="খুঁজুন: সূরা:আয়াত, শব্দ, পৃষ্ঠা..."
              value={search}
              onChange={e => { setSearch(e.target.value); setPage(0); }}
              className="w-full px-3.5 py-2 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-sm font-bengali placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            />
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs text-gray-500 dark:text-gray-400 font-bengali">সাজান:</span>
            <select
              value={sortBy}
              onChange={e => { setSortBy(e.target.value); setPage(0); }}
              className="px-2.5 py-1.5 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-xs font-bengali text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="surah">সূরা-আয়াত ক্রমে</option>
              <option value="page">মুষাফ পৃষ্ঠা অনুযায়ী</option>
            </select>
          </div>
        </div>

        {/* Results List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-2">
          {filtered.length === 0 ? (
            <div className="text-center text-gray-500 dark:text-gray-400 py-8 font-bengali">
              কোনো ফলাফল পাওয়া যায়নি।
            </div>
          ) : (
            <>
              <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 font-bengali pb-2 border-b border-gray-100 dark:border-gray-700">
                <span>প্রদর্শিত: {paginated.length} / {toBn(filtered.length)} আয়াত</span>
                <span>পৃষ্ঠা {toBn(page + 1)} / {toBn(totalPages)}</span>
              </div>
              {paginated.map((v, idx) => {
                const verseKey = v.verse_key || `${v.surah}-${v.ayah}`;
                const isExpanded = expanded.has(verseKey);
                return (
                  <div
                    key={verseKey}
                    className="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 overflow-hidden transition-all"
                  >
                    <button
                      onClick={() => toggleExpand(verseKey)}
                      className="w-full p-3.5 flex items-center justify-between text-left hover:bg-gray-50 dark:hover:bg-gray-800/50"
                    >
                      <div className="flex items-center gap-3 min-w-0">
                        <span className="w-8 text-center font-mono text-gray-400 text-xs">{toBn(idx + 1 + page * PAGE_SIZE)}</span>
                        <div className="flex items-center gap-2">
                          <span className="px-2 py-0.5 rounded text-xs font-bold bg-emerald-100 dark:bg-emerald-900/40 text-emerald-800 dark:text-emerald-200 font-bengali">
                            {toBn(v.surah)}:{toBn(v.ayah)}
                          </span>
                          <span className="px-2 py-0.5 rounded text-xs font-mono text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-800">
                            পৃষ্ঠা {toBn(v.page_number)}
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <ChevronDown className={`w-4 h-4 text-gray-400 transition-transform ${isExpanded ? 'rotate-180' : ''}`} />
                      </div>
                    </button>
                    {isExpanded && (
                      <div className="p-3.5 border-t border-gray-100 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-900/30 space-y-2">
                        <div className="font-quran text-lg text-emerald-800 dark:text-emerald-300 leading-relaxed" dir="rtl">
                          {v.text_raw}
                        </div>
                        <div className="flex flex-wrap gap-2 text-xs text-gray-600 dark:text-gray-400 font-bengali">
                          <span>শব্দ: {toBn(v.word_count)}</span>
                          <span>অক্ষর: {toBn(v.letter_count)}</span>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
              {totalPages > 1 && (
                <div className="flex items-center justify-center gap-2 pt-4 border-t border-gray-100 dark:border-gray-700">
                  <button
                    onClick={() => setPage(p => Math.max(0, p - 1))}
                    disabled={page === 0}
                    className="px-3 py-1.5 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-xs font-bengali text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                  >
                    আগের পৃষ্ঠা
                  </button>
                  <span className="text-xs text-gray-500 dark:text-gray-400 font-bengali">
                    {toBn(page + 1)} / {toBn(totalPages)}
                  </span>
                  <button
                    onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))}
                    disabled={page >= totalPages - 1}
                    className="px-3 py-1.5 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-xs font-bengali text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                  >
                    পরের পৃষ্ঠা
                  </button>
                </div>
              )}
            </>
          )}
        </div>

        {/* Footer */}
        <div className="p-3.5 border-t border-gray-100 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-850 flex justify-between items-center">
          <span className="text-xs text-gray-500 dark:text-gray-400 font-bengali">
            উৎস: মাদীনা মুনাওয়ারা বাহাউথ ডেটাবেস
          </span>
          <button onClick={onClose} className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bengali text-xs font-bold transition">
            বন্ধ করুন
          </button>
        </div>
      </div>
    </div>
  );
}
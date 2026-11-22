import React, { useState, useEffect, useMemo } from 'react';
import { Search, X, BookOpen, ExternalLink } from 'lucide-react';
import { toBn, normalizeArabic, normalizeBengali } from '../utils/helpers';

export default function SearchModal({ isOpen, onClose, onSelectAyah }) {
  const [indexData, setIndexData] = useState([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen && indexData.length === 0) {
      setLoading(true);
      fetch('/data/search_index.json')
        .then(res => res.json())
        .then(data => {
          setIndexData(data);
          setLoading(false);
        })
        .catch(err => {
          console.error("Failed to load search index", err);
          setLoading(false);
        });
    }
  }, [isOpen, indexData.length]);

  const searchResults = useMemo(() => {
    if (!query.trim() || indexData.length === 0) return [];
    const qClean = query.trim();
    const qNormAr = normalizeArabic(qClean);
    const qNormBn = normalizeBengali(qClean);

    // If query matches "24:35" or "২৪:৩৫"
    const ayahMatch = qClean.match(/(\d+|[০-৯]+)[:\.\s]+(\d+|[০-৯]+)/);
    if (ayahMatch) {
      const sNum = parseInt(ayahMatch[1].replace(/[০-৯]/g, d => "০১২৩৪৫৬৭৮৯".indexOf(d)));
      const aNum = parseInt(ayahMatch[2].replace(/[০-৯]/g, d => "০১২৩৪৫৬৭৮৯".indexOf(d)));
      return indexData.filter(item => item.surah === sNum && item.ayah === aNum);
    }

    const results = [];
    for (const item of indexData) {
      const arNorm = normalizeArabic(item.text_uthmani);
      const bnNorm = normalizeBengali(item.translation + " " + (item.surah_name || ""));

      if (
        (qNormAr && arNorm.includes(qNormAr)) ||
        (qNormBn && bnNorm.includes(qNormBn))
      ) {
        results.push(item);
        if (results.length >= 50) break; // limit to 50 results
      }
    }
    return results;
  }, [query, indexData]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-start justify-center p-3 sm:p-6 animate-in fade-in duration-150">
      <div className="bg-white dark:bg-gray-800 rounded-2xl max-w-2xl w-full max-h-[85vh] shadow-2xl flex flex-col border border-gray-200 dark:border-gray-700 overflow-hidden mt-6 sm:mt-12">
        {/* Search Header Input */}
        <div className="p-3 sm:p-4 border-b border-gray-200 dark:border-gray-700 flex items-center gap-3">
          <Search className="w-5 h-5 text-emerald-600 shrink-0" />
          <input
            type="text"
            autoFocus
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="আয়াত নং (যেমন ২৪:৩৫), আরবি শব্দ (যেমন نور) বা বাংলা অনুবাদ লিখুন..."
            className="w-full bg-transparent text-gray-900 dark:text-gray-100 text-sm sm:text-base focus:outline-none placeholder-gray-400"
          />
          {query && (
            <button
              onClick={() => setQuery("")}
              className="p-1 rounded-full text-gray-400 hover:text-gray-600 transition"
            >
              <X className="w-4 h-4" />
            </button>
          )}
          <button
            onClick={onClose}
            className="text-xs px-2.5 py-1 rounded bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 font-semibold hover:bg-gray-200 transition"
          >
            ESC
          </button>
        </div>

        {/* Results Body */}
        <div className="flex-1 overflow-y-auto p-3 sm:p-4 space-y-2.5">
          {loading ? (
            <div className="text-center py-12 text-gray-400 text-sm">
              সার্চ ডাটাবেজ প্রস্তুত হচ্ছে...
            </div>
          ) : query.trim() === "" ? (
            <div className="text-center py-10 text-gray-400 text-xs sm:text-sm space-y-2">
              <BookOpen className="w-8 h-8 mx-auto opacity-30 text-emerald-600" />
              <p>কুরআনের যেকোনো আয়াত বা তাফসীর মুহূর্তের মধ্যে খুঁজে পেতে টাইপ করুন।</p>
              <div className="flex flex-wrap justify-center gap-1.5 pt-2">
                {["২৪:৩৫", "আল্লাহ নূর", "ব্যভিচার", "হিজাব", "লিআন", "তাকওয়া"].map(term => (
                  <button
                    key={term}
                    onClick={() => setQuery(term)}
                    className="px-2 py-1 rounded-lg bg-gray-100 dark:bg-gray-700 text-xs text-gray-600 dark:text-gray-300 hover:bg-emerald-50 dark:hover:bg-emerald-950 transition"
                  >
                    #{term}
                  </button>
                ))}
              </div>
            </div>
          ) : searchResults.length === 0 ? (
            <div className="text-center py-12 text-gray-400 text-sm">
              "{query}"-এর কোনো ফলাফল পাওয়া যায়নি।
            </div>
          ) : (
            searchResults.map((item, idx) => (
              <div
                key={idx}
                onClick={() => {
                  onSelectAyah(item.surah, item.ruku, item.ayah);
                  onClose();
                }}
                className="bg-gray-50 dark:bg-gray-700/50 p-3 rounded-xl border border-gray-200 dark:border-gray-600 hover:border-emerald-500 cursor-pointer transition space-y-1.5"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-xs text-emerald-800 dark:text-emerald-300">
                    সূরা {item.surah_name || item.surah} • আয়াত {toBn(item.ayah)}
                  </span>
                  <ExternalLink className="w-3.5 h-3.5 text-gray-400" />
                </div>
                <div className="uthmani-text text-base sm:text-lg text-gray-900 dark:text-gray-100 line-clamp-1">
                  {item.text_uthmani}
                </div>
                <div className="text-xs text-gray-600 dark:text-gray-300 line-clamp-2 leading-relaxed">
                  {item.translation}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

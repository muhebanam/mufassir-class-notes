import React, { useState, useMemo } from 'react';
import { X, Search, BookOpen, Compass, Check } from 'lucide-react';
import { toBn } from '../utils/helpers';
import { SURAH_CATALOG } from '../utils/surahCatalogData';

export default function SurahSidebar({
  isOpen,
  onClose,
  surahs = [],
  currentSurahId,
  onSelectSurah
}) {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState('all'); // 'all', 'মাক্কী', 'মাদানী'

  // Merge full catalog metadata (type, meaning) with runtime surahs list
  const catalogMap = useMemo(() => {
    const map = new Map();
    SURAH_CATALOG.forEach(s => map.set(s.id, s));
    return map;
  }, []);

  const mergedSurahs = useMemo(() => {
    return surahs.map(s => {
      const extra = catalogMap.get(s.id) || {};
      return {
        ...s,
        meaning: extra.meaning || '',
        type: extra.type || 'মাক্কী',
        featured: extra.featured || false
      };
    });
  }, [surahs, catalogMap]);

  const filteredSurahs = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();
    return mergedSurahs.filter(s => {
      // Type filter
      if (filterType !== 'all' && s.type !== filterType) {
        return false;
      }
      if (!q) return true;
      const idMatch = String(s.id).includes(q) || (s.id_bn && s.id_bn.includes(q));
      const bnMatch = s.name_bn && s.name_bn.toLowerCase().includes(q);
      const arMatch = s.name_ar && s.name_ar.includes(q);
      const meaningMatch = s.meaning && s.meaning.toLowerCase().includes(q);
      return idMatch || bnMatch || arMatch || meaningMatch;
    });
  }, [mergedSurahs, searchQuery, filterType]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex animate-in fade-in duration-200">
      {/* Sidebar Panel */}
      <div className="bg-white dark:bg-gray-800 w-full max-w-sm sm:max-w-md h-full shadow-2xl flex flex-col border-r border-gray-200 dark:border-gray-700 animate-in slide-in-from-left duration-200">
        {/* Header */}
        <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            <div>
              <h2 className="font-bold text-base text-gray-900 dark:text-gray-100">
                সূচিপত্র • সূরা ক্যাটালগ
              </h2>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                সূরা ২৪ থেকে ১১৪ (মোট {toBn(surahs.length)}টি সূরা)
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-full text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 transition"
            aria-label="Close catalog"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Search & Filter Bar */}
        <div className="p-3 bg-gray-50 dark:bg-gray-900/60 border-b border-gray-200 dark:border-gray-700 space-y-2.5">
          <div className="relative">
            <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="সূরার নাম, নম্বর বা অর্থ দিয়ে খুঁজুন..."
              className="w-full pl-9 pr-3 py-1.5 text-xs sm:text-sm bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl focus:outline-hidden focus:ring-2 focus:ring-emerald-500/40 text-gray-800 dark:text-gray-200 placeholder-gray-400"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-2.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xs font-bold"
              >
                ✕
              </button>
            )}
          </div>

          {/* Filter Pills */}
          <div className="flex items-center gap-1.5 text-xs font-medium">
            <button
              onClick={() => setFilterType('all')}
              className={`px-3 py-1 rounded-lg transition ${
                filterType === 'all'
                  ? 'bg-emerald-700 text-white font-bold shadow-xs'
                  : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              সকল ({toBn(mergedSurahs.length)})
            </button>
            <button
              onClick={() => setFilterType('মাক্কী')}
              className={`px-3 py-1 rounded-lg transition ${
                filterType === 'মাক্কী'
                  ? 'bg-amber-700 text-white font-bold shadow-xs'
                  : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              মাক্কী ({toBn(mergedSurahs.filter(s => s.type === 'মাক্কী').length)})
            </button>
            <button
              onClick={() => setFilterType('মাদানী')}
              className={`px-3 py-1 rounded-lg transition ${
                filterType === 'মাদানী'
                  ? 'bg-teal-700 text-white font-bold shadow-xs'
                  : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              মাদানী ({toBn(mergedSurahs.filter(s => s.type === 'মাদানী').length)})
            </button>
          </div>
        </div>

        {/* Surahs List */}
        <div className="flex-1 overflow-y-auto p-2.5 space-y-1.5 divide-y divide-gray-100 dark:divide-gray-800">
          {filteredSurahs.length === 0 ? (
            <div className="text-center py-12 text-gray-400 text-xs">
              "{searchQuery}" দিয়ে কোনো সূরা পাওয়া যায়নি।
            </div>
          ) : (
            filteredSurahs.map((s) => {
              const isSelected = s.id === currentSurahId;
              return (
                <div
                  key={s.id}
                  onClick={() => {
                    onSelectSurah(s.id);
                    onClose();
                  }}
                  className={`p-2.5 rounded-xl cursor-pointer transition flex items-center justify-between gap-3 ${
                    isSelected
                      ? 'bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-500 shadow-xs'
                      : 'hover:bg-gray-50 dark:hover:bg-gray-700/40 border border-transparent'
                  }`}
                >
                  <div className="flex items-center gap-3 min-w-0">
                    {/* Number Badge */}
                    <div
                      className={`w-9 h-9 rounded-xl flex items-center justify-center font-bold text-xs shrink-0 ${
                        isSelected
                          ? 'bg-emerald-700 text-white shadow-xs'
                          : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                      }`}
                    >
                      {toBn(s.id)}
                    </div>

                    {/* Name & Meaning */}
                    <div className="min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-sm text-gray-900 dark:text-gray-100 truncate">
                          {s.name_bn}
                        </span>
                        <span
                          className={`text-[10px] px-1.5 py-0.5 rounded font-semibold shrink-0 ${
                            s.type === 'মাদানী'
                              ? 'bg-teal-100 dark:bg-teal-950 text-teal-800 dark:text-teal-300'
                              : 'bg-amber-100 dark:bg-amber-950 text-amber-800 dark:text-amber-300'
                          }`}
                        >
                          {s.type}
                        </span>
                      </div>
                      <p className="text-[11px] text-gray-500 dark:text-gray-400 truncate">
                        {s.meaning ? `${s.meaning} • ` : ''}
                        {toBn(s.ayah_count)} আয়াত • {toBn(s.ruku_count)} রুকু
                      </p>
                    </div>
                  </div>

                  {/* Arabic Name */}
                  <div className="text-right shrink-0">
                    <span className="font-amiri text-lg text-emerald-900 dark:text-emerald-300 font-bold block" dir="rtl">
                      {s.name_ar}
                    </span>
                    {isSelected && (
                      <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 flex items-center justify-end gap-0.5">
                        <Check className="w-3 h-3" /> বর্তমান
                      </span>
                    )}
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Backdrop click to close */}
      <div className="flex-1" onClick={onClose} />
    </div>
  );
}

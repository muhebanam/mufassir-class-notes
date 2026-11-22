import React, { useRef, useEffect } from 'react';
import { toBn } from '../utils/helpers';

export default function AyahJumper({ ayahs, selectedAyah, onSelectAyah }) {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current && selectedAyah) {
      const activeEl = scrollRef.current.querySelector(`[data-ayah="${selectedAyah}"]`);
      if (activeEl) {
        activeEl.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
      }
    }
  }, [selectedAyah]);

  if (!ayahs || ayahs.length === 0) return null;

  return (
    <div className="sticky top-14 sm:top-16 z-20 bg-gray-100/95 dark:bg-gray-800/90 backdrop-blur-sm border-b border-gray-200 dark:border-gray-700 py-1.5 px-3 transition-colors">
      <div className="max-w-7xl mx-auto flex items-center gap-2">
        <span className="text-xs font-bold text-gray-500 dark:text-gray-400 shrink-0">আয়াত:</span>
        <div
          ref={scrollRef}
          className="flex items-center gap-1.5 overflow-x-auto no-scrollbar scroll-smooth py-0.5"
        >
          {ayahs.map((a) => {
            const isSelected = selectedAyah === a.ayah;
            return (
              <button
                key={a.ayah}
                data-ayah={a.ayah}
                onClick={() => onSelectAyah(a.ayah)}
                className={`min-w-[34px] h-[30px] px-2 rounded-lg text-xs font-semibold flex items-center justify-center transition-all shrink-0 ${
                  isSelected
                    ? 'bg-emerald-600 text-white shadow-sm ring-2 ring-emerald-400/40 scale-105'
                    : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-emerald-50 dark:hover:bg-gray-600 border border-gray-200 dark:border-gray-600'
                }`}
              >
                {toBn(a.ayah)}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}

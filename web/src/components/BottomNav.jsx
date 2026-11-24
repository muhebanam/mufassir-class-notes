import React from 'react';
import { Home, BookOpen, Layers, FileText, Sparkles } from 'lucide-react';

export default function BottomNav({
  activeView,
  setActiveView,
  studyMode,
  setStudyMode,
  onOpenNotes,
  onGoHome
}) {
  return (
    <nav className="md:hidden fixed bottom-0 left-0 right-0 z-30 bg-white/95 dark:bg-gray-800/95 backdrop-blur-md border-t border-gray-200 dark:border-gray-700 px-1 py-1 shadow-lg transition-colors">
      <div className="grid grid-cols-5 items-center justify-around text-center">
        {/* 1. Surah Dashboard */}
        <button
          onClick={onGoHome}
          className={`flex flex-col items-center justify-center py-1 transition ${
            activeView === 'dashboard'
              ? 'text-emerald-700 dark:text-emerald-400 font-bold'
              : 'text-gray-500 dark:text-gray-400 hover:text-gray-900'
          }`}
        >
          <Home className="w-4 h-4 mb-0.5" />
          <span className="text-[10px] truncate max-w-full font-bengali">সূরা সূচি</span>
        </button>

        {/* 2. Mushaf Reading */}
        <button
          onClick={() => {
            setActiveView('study');
            setStudyMode('mushaf');
          }}
          className={`flex flex-col items-center justify-center py-1 transition ${
            activeView === 'study' && studyMode === 'mushaf'
              ? 'text-emerald-700 dark:text-emerald-400 font-bold'
              : 'text-gray-500 dark:text-gray-400 hover:text-gray-900'
          }`}
        >
          <Sparkles className="w-4 h-4 mb-0.5" />
          <span className="text-[10px] truncate max-w-full font-bengali">মুসহাফ</span>
        </button>

        {/* 3. Ayah Study */}
        <button
          onClick={() => {
            setActiveView('study');
            setStudyMode('ayah');
          }}
          className={`flex flex-col items-center justify-center py-1 transition ${
            activeView === 'study' && studyMode === 'ayah'
              ? 'text-emerald-700 dark:text-emerald-400 font-bold'
              : 'text-gray-500 dark:text-gray-400 hover:text-gray-900'
          }`}
        >
          <BookOpen className="w-4 h-4 mb-0.5" />
          <span className="text-[10px] truncate max-w-full font-bengali">আয়াত স্টাডি</span>
        </button>

        {/* 4. Thematic / Ruku Scholarly Discussion */}
        <button
          onClick={() => {
            setActiveView('study');
            setStudyMode('thematic');
          }}
          className={`flex flex-col items-center justify-center py-1 transition ${
            activeView === 'study' && studyMode === 'thematic'
              ? 'text-emerald-700 dark:text-emerald-400 font-bold'
              : 'text-gray-500 dark:text-gray-400 hover:text-gray-900'
          }`}
        >
          <Layers className="w-4 h-4 mb-0.5" />
          <span className="text-[10px] truncate max-w-full font-bengali">রুকু আলোচনা</span>
        </button>

        {/* 5. Notes */}
        <button
          onClick={onOpenNotes}
          className="flex flex-col items-center justify-center py-1 text-gray-500 dark:text-gray-400 hover:text-gray-900 transition"
        >
          <FileText className="w-4 h-4 mb-0.5" />
          <span className="text-[10px] truncate max-w-full font-bengali">নোটস</span>
        </button>
      </div>
    </nav>
  );
}

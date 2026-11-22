import React from 'react';
import { Home, BookOpen, Layers, FileText, Settings } from 'lucide-react';

export default function BottomNav({
  activeView,
  setActiveView,
  onOpenNotes,
  onOpenSettings,
  onGoHome
}) {
  return (
    <nav className="md:hidden fixed bottom-0 left-0 right-0 z-30 bg-white/95 dark:bg-gray-800/95 backdrop-blur-md border-t border-gray-200 dark:border-gray-700 px-2 py-1 shadow-lg transition-colors">
      <div className="grid grid-cols-4 items-center justify-around text-center">
        <button
          onClick={onGoHome}
          className={`flex flex-col items-center justify-center py-1.5 transition ${
            activeView === 'dashboard'
              ? 'text-emerald-700 dark:text-emerald-400 font-bold'
              : 'text-gray-500 dark:text-gray-400 hover:text-gray-900'
          }`}
        >
          <Home className="w-5 h-5 mb-0.5" />
          <span className="text-[10px]">সূরা সূচি</span>
        </button>

        <button
          onClick={() => setActiveView('study')}
          className={`flex flex-col items-center justify-center py-1.5 transition ${
            activeView === 'study'
              ? 'text-emerald-700 dark:text-emerald-400 font-bold'
              : 'text-gray-500 dark:text-gray-400 hover:text-gray-900'
          }`}
        >
          <BookOpen className="w-5 h-5 mb-0.5" />
          <span className="text-[10px]">তাফসীর দরস</span>
        </button>

        <button
          onClick={onOpenNotes}
          className="flex flex-col items-center justify-center py-1.5 text-gray-500 dark:text-gray-400 hover:text-gray-900 transition"
        >
          <FileText className="w-5 h-5 mb-0.5" />
          <span className="text-[10px]">ক্লাস নোটস</span>
        </button>

        <button
          onClick={onOpenSettings}
          className="flex flex-col items-center justify-center py-1.5 text-gray-500 dark:text-gray-400 hover:text-gray-900 transition"
        >
          <Settings className="w-5 h-5 mb-0.5" />
          <span className="text-[10px]">সেটিংস</span>
        </button>
      </div>
    </nav>
  );
}

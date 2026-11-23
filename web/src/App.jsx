import React, { useState, useEffect, useCallback } from 'react';
import Header from './components/Header';
import BottomNav from './components/BottomNav';
import AyahJumper from './components/AyahJumper';
import AyahStudyView from './components/AyahStudyView';
import ThematicView from './components/ThematicView';
import MushafView from './components/MushafView';
import SurahDashboard from './components/SurahDashboard';
import SearchModal from './components/SearchModal';
import SettingsModal from './components/SettingsModal';
import NotesDrawer from './components/NotesDrawer';
import AuthorModal from './components/AuthorModal';

export default function App() {
  // Global Data
  const [surahs, setSurahs] = useState([]);
  const [siteMeta, setSiteMeta] = useState(null);

  // Navigation State
  const [currentSurahId, setCurrentSurahId] = useState(24);
  const [currentRukuId, setCurrentRukuId] = useState(1);
  const [selectedAyahNum, setSelectedAyahNum] = useState(1);

  // Loaded Surah & Ruku Data
  const [surahMeta, setSurahMeta] = useState(null);
  const [rukuData, setRukuData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Views & Modes
  const [activeView, setActiveView] = useState('study'); // 'dashboard' or 'study'
  const [studyMode, setStudyMode] = useState('ayah'); // 'ayah', 'thematic', 'mushaf'

  // Modals
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isNotesOpen, setIsNotesOpen] = useState(false);
  const [isAuthorOpen, setIsAuthorOpen] = useState(false);

  // Typography & Theme Settings (persisted in localStorage)
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'light');
  const [arabicFontSize, setArabicFontSize] = useState(() => Number(localStorage.getItem('arFontSize')) || 28);
  const [bengaliFontSize, setBengaliFontSize] = useState(() => Number(localStorage.getItem('bnFontSize')) || 16);
  const [arabicLineHeight, setArabicLineHeight] = useState(() => Number(localStorage.getItem('arLineHeight')) || 2.2);

  // Apply Theme to <body>
  useEffect(() => {
    localStorage.setItem('theme', theme);
    document.documentElement.classList.remove('dark');
    document.body.classList.remove('sepia-theme');

    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else if (theme === 'sepia') {
      document.body.classList.add('sepia-theme');
    }
  }, [theme]);

  // Persist font settings
  useEffect(() => {
    localStorage.setItem('arFontSize', arabicFontSize);
    localStorage.setItem('bnFontSize', bengaliFontSize);
    localStorage.setItem('arLineHeight', arabicLineHeight);
  }, [arabicFontSize, bengaliFontSize, arabicLineHeight]);

  // 1. Initial Load: Surahs & Site Meta
  useEffect(() => {
    Promise.all([
      fetch('/data/surahs.json').then((r) => r.json()),
      fetch('/data/site_meta.json').then((r) => r.json()).catch(() => null),
    ])
      .then(([surahsList, meta]) => {
        setSurahs(surahsList);
        setSiteMeta(meta);

        // Parse initial hash (e.g. #/24/35 or #/24/ruku-5)
        const hash = window.location.hash.replace('#/', '').replace('#', '');
        if (hash) {
          const parts = hash.split('/');
          const sId = parseInt(parts[0]);
          if (!isNaN(sId) && sId >= 24 && sId <= 114) {
            setCurrentSurahId(sId);
            setActiveView('study');
            if (parts[1]) {
              if (parts[1].startsWith('ruku-')) {
                const rId = parseInt(parts[1].replace('ruku-', ''));
                if (!isNaN(rId)) setCurrentRukuId(rId);
              } else {
                const aId = parseInt(parts[1]);
                if (!isNaN(aId)) setSelectedAyahNum(aId);
              }
            }
          }
        }
      })
      .catch((err) => console.error('Failed to load initial data', err));
  }, []);

  // 2. Load Surah Meta when currentSurahId changes
  useEffect(() => {
    if (!currentSurahId) return;
    setLoading(true);
    fetch(`/data/${currentSurahId}/meta.json`)
      .then((r) => r.json())
      .then((meta) => {
        setSurahMeta(meta);
        // Find which ruku contains selectedAyahNum or default to ruku 1
        let targetRuku = 1;
        if (meta.rukus && meta.rukus.length > 0) {
          const matchedR = meta.rukus.find(
            (r) => selectedAyahNum >= r.ayah_start && selectedAyahNum <= r.ayah_end
          );
          if (matchedR) {
            targetRuku = matchedR.ruku_id;
          } else {
            targetRuku = meta.rukus[0].ruku_id;
            setSelectedAyahNum(meta.rukus[0].ayah_start);
          }
        }
        setCurrentRukuId(targetRuku);
      })
      .catch((err) => console.error('Failed to load surah meta', err));
  }, [currentSurahId]);

  // 3. Load Ruku Data when currentSurahId or currentRukuId changes
  useEffect(() => {
    if (!currentSurahId || !currentRukuId) return;
    setLoading(true);
    fetch(`/data/${currentSurahId}/ruku-${currentRukuId}.json`)
      .then((r) => r.json())
      .then((data) => {
        setRukuData(data);
        setLoading(false);
        // Ensure selected ayah is within this ruku's range
        if (data.ayahs && data.ayahs.length > 0) {
          const exists = data.ayahs.some((a) => a.ayah === selectedAyahNum);
          if (!exists) {
            setSelectedAyahNum(data.ayahs[0].ayah);
          }
        }
      })
      .catch((err) => {
        console.error('Failed to load ruku data', err);
        setLoading(false);
      });
  }, [currentSurahId, currentRukuId]);

  // 4. Update URL Hash for Permanent Deep Linking
  useEffect(() => {
    if (activeView === 'dashboard') {
      window.location.hash = '#/';
    } else if (currentSurahId && selectedAyahNum) {
      window.location.hash = `#/${currentSurahId}/${selectedAyahNum}`;
    }
  }, [activeView, currentSurahId, selectedAyahNum]);

  // 5. Navigation Handlers
  const handleSelectSurah = (sId) => {
    if (sId === null) {
      setActiveView('dashboard');
    } else {
      setCurrentSurahId(sId);
      setCurrentRukuId(1);
      setSelectedAyahNum(1);
      setActiveView('study');
    }
  };

  const handleSelectRuku = (rId) => {
    setCurrentRukuId(rId);
    if (surahMeta?.rukus) {
      const rEntry = surahMeta.rukus.find((r) => r.ruku_id === rId);
      if (rEntry) {
        setSelectedAyahNum(rEntry.ayah_start);
      }
    }
  };

  const handleSelectAyah = (aNum) => {
    setSelectedAyahNum(aNum);
    // Switch to ayah study view if in another view
    if (studyMode === 'thematic') {
      setStudyMode('ayah');
    }
  };

  const handlePrevAyah = () => {
    if (selectedAyahNum > (rukuData?.ayah_start || 1)) {
      setSelectedAyahNum((prev) => prev - 1);
    }
  };

  const handleNextAyah = () => {
    if (selectedAyahNum < (rukuData?.ayah_end || 64)) {
      setSelectedAyahNum((prev) => prev + 1);
    }
  };

  const handleJumpFromNote = (sId, rId, aId) => {
    setCurrentSurahId(sId);
    setCurrentRukuId(rId);
    setSelectedAyahNum(aId);
    setActiveView('study');
    setStudyMode('ayah');
  };

  // Keyboard Navigation: Ctrl+K, Left/Right Arrows
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        setIsSearchOpen((prev) => !prev);
      } else if (e.key === 'Escape') {
        setIsSearchOpen(false);
        setIsSettingsOpen(false);
        setIsNotesOpen(false);
        setIsAuthorOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const currentSurah = surahs.find((s) => s.id === currentSurahId);
  const currentAyah = rukuData?.ayahs?.find((a) => a.ayah === selectedAyahNum);

  return (
    <div className="min-h-screen flex flex-col pb-16 md:pb-6">
      {/* Top Header */}
      <Header
        surahs={surahs}
        currentSurah={currentSurah}
        currentRuku={currentRukuId}
        surahMeta={surahMeta}
        studyMode={studyMode}
        setStudyMode={setStudyMode}
        onSelectSurah={handleSelectSurah}
        onSelectRuku={handleSelectRuku}
        onOpenSearch={() => setIsSearchOpen(true)}
        onOpenSettings={() => setIsSettingsOpen(true)}
        onOpenNotes={() => setIsNotesOpen(true)}
        onOpenAuthor={() => setIsAuthorOpen(true)}
        theme={theme}
        setTheme={setTheme}
      />

      {/* Mobile Study Mode Tabs (front and center on phone screens) */}
      {activeView === 'study' && (
        <div className="md:hidden bg-white/95 dark:bg-gray-800/95 backdrop-blur-md border-b border-gray-200 dark:border-gray-700 px-3 py-1.5 flex items-center justify-between gap-1.5 shadow-2xs">
          <button
            onClick={() => setStudyMode('ayah')}
            className={`flex-1 py-1.5 px-2 rounded-lg text-xs font-bold text-center transition flex items-center justify-center gap-1 ${
              studyMode === 'ayah'
                ? 'bg-emerald-600 text-white shadow-2xs'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            <span>আয়াত দরস</span>
          </button>
          <button
            onClick={() => setStudyMode('thematic')}
            className={`flex-1 py-1.5 px-2 rounded-lg text-xs font-bold text-center transition flex items-center justify-center gap-1 ${
              studyMode === 'thematic'
                ? 'bg-emerald-600 text-white shadow-2xs'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            <span>রুকু শাস্ত্র-আলোচনা</span>
          </button>
          <button
            onClick={() => setStudyMode('mushaf')}
            className={`flex-1 py-1.5 px-2 rounded-lg text-xs font-bold text-center transition flex items-center justify-center gap-1 ${
              studyMode === 'mushaf'
                ? 'bg-emerald-600 text-white shadow-2xs'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            <span>মুসহাফ</span>
          </button>
        </div>
      )}

      {/* Horizontal Ayah Jumper Bar (When in Study View and Ayah/Mushaf mode) */}
      {activeView === 'study' && rukuData && (
        <AyahJumper
          ayahs={rukuData.ayahs}
          selectedAyah={selectedAyahNum}
          onSelectAyah={handleSelectAyah}
        />
      )}

      {/* Main Content Area */}
      <main className="flex-1">
        {activeView === 'dashboard' ? (
          <SurahDashboard
            surahs={surahs}
            siteMeta={siteMeta}
            onSelectSurah={handleSelectSurah}
            onOpenAuthor={() => setIsAuthorOpen(true)}
          />
        ) : loading ? (
          <div className="max-w-4xl mx-auto py-24 text-center space-y-3">
            <div className="w-10 h-10 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
            <p className="text-gray-500 text-sm font-semibold">সূরা ও রুকুর ডাটা লোড হচ্ছে...</p>
          </div>
        ) : studyMode === 'thematic' ? (
          <ThematicView rukuData={rukuData} surahInfo={currentSurah} />
        ) : studyMode === 'mushaf' ? (
          <MushafView
            rukuData={rukuData}
            surahInfo={currentSurah}
            onSelectAyah={handleSelectAyah}
            arabicFontSize={arabicFontSize + 2}
            arabicLineHeight={arabicLineHeight}
          />
        ) : (
          <AyahStudyView
            ayah={currentAyah}
            surahInfo={currentSurah}
            rukuInfo={rukuData}
            onPrevAyah={handlePrevAyah}
            onNextAyah={handleNextAyah}
            arabicFontSize={arabicFontSize}
            bengaliFontSize={bengaliFontSize}
            arabicLineHeight={arabicLineHeight}
          />
        )}
      </main>

      {/* Bottom Sticky Navigation for Mobile (360px optimized) */}
      <BottomNav
        activeView={activeView}
        setActiveView={setActiveView}
        studyMode={studyMode}
        setStudyMode={setStudyMode}
        onOpenNotes={() => setIsNotesOpen(true)}
        onOpenSettings={() => setIsSettingsOpen(true)}
        onGoHome={() => setActiveView('dashboard')}
      />

      {/* Modals & Drawers */}
      <SearchModal
        isOpen={isSearchOpen}
        onClose={() => setIsSearchOpen(false)}
        onSelectAyah={handleJumpFromNote}
      />

      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        arabicFontSize={arabicFontSize}
        setArabicFontSize={setArabicFontSize}
        bengaliFontSize={bengaliFontSize}
        setBengaliFontSize={setBengaliFontSize}
        arabicLineHeight={arabicLineHeight}
        setArabicLineHeight={setArabicLineHeight}
        theme={theme}
        setTheme={setTheme}
      />

      <NotesDrawer
        isOpen={isNotesOpen}
        onClose={() => setIsNotesOpen(false)}
        onSelectAyahFromNote={handleJumpFromNote}
      />

      <AuthorModal
        isOpen={isAuthorOpen}
        onClose={() => setIsAuthorOpen(false)}
      />
    </div>
  );
}

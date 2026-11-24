import React, { useState, useEffect, useCallback, useRef } from 'react';
import Header from './components/Header';
import BottomNav from './components/BottomNav';
import AyahJumper from './components/AyahJumper';
import AyahStudyView from './components/AyahStudyView';
import ThematicView from './components/ThematicView';
import MushafView from './components/MushafView';
import SurahScopeView from './components/SurahScopeView';
import RukuScopeView from './components/RukuScopeView';
import AyahScopeView from './components/AyahScopeView';
import SurahDashboard from './components/SurahDashboard';
import SearchModal from './components/SearchModal';
import SettingsModal, { QURAN_COLOR_OPTIONS } from './components/SettingsModal';
import NotesDrawer from './components/NotesDrawer';
import AuthorModal from './components/AuthorModal';
import SurahSidebar from './components/SurahSidebar';

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

  // Views & Modes: 'dashboard' or 'study'
  const [activeView, setActiveView] = useState('study'); 
  // 3 Distinct Academic Modes: 'mushaf', 'ayah', 'thematic'
  const [studyMode, setStudyMode] = useState('ayah'); 

  // Modals & Sidebar
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isNotesOpen, setIsNotesOpen] = useState(false);
  const [isAuthorOpen, setIsAuthorOpen] = useState(false);

  // Typography & Theme Settings (Paper Light, Warm Sepia, Academic Dark)
  const [theme, setTheme] = useState(() => {
    const saved = localStorage.getItem('theme');
    if (saved) return saved;
    if (typeof window !== 'undefined' && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    return 'light'; // Paper Light default
  });

  const [quranColor, setQuranColor] = useState(() => localStorage.getItem('quranColor') || 'emerald');

  const [arabicFontSize, setArabicFontSize] = useState(() => Number(localStorage.getItem('arFontSize')) || 28);
  const [bengaliFontSize, setBengaliFontSize] = useState(() => Number(localStorage.getItem('bnFontSize')) || 16);
  const [arabicLineHeight, setArabicLineHeight] = useState(() => Number(localStorage.getItem('arLineHeight')) || 2.2);

  // Split View state for Ayah Study (defaults to true on wide screens)
  const [splitView, setSplitView] = useState(() => {
    const saved = localStorage.getItem('splitView');
    return saved !== null ? saved === 'true' : true;
  });

  // Auto-hide Header state (smooth fade/hide on scroll down, reappear on scroll up)
  const [isHeaderHidden, setIsHeaderHidden] = useState(false);
  const lastScrollY = useRef(0);

  useEffect(() => {
    const handleScroll = () => {
      const currentScrollY = window.scrollY;
      if (currentScrollY > 70 && currentScrollY > lastScrollY.current + 8) {
        setIsHeaderHidden(true);
      } else if (currentScrollY < lastScrollY.current - 8 || currentScrollY <= 70) {
        setIsHeaderHidden(false);
      }
      lastScrollY.current = currentScrollY;
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Apply Theme to <body> and <html>
  useEffect(() => {
    localStorage.setItem('theme', theme);
    document.documentElement.classList.remove('dark');
    document.body.classList.remove('sepia-theme', 'light-theme', 'dark');

    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
      document.body.classList.add('dark');
    } else if (theme === 'sepia') {
      document.body.classList.add('sepia-theme');
    } else {
      document.body.classList.add('light-theme');
    }
  }, [theme]);

  // Apply Quran text color dynamically to CSS variable --quran-color
  useEffect(() => {
    localStorage.setItem('quranColor', quranColor);
    const colObj = QURAN_COLOR_OPTIONS.find(c => c.id === quranColor) || QURAN_COLOR_OPTIONS[0];
    const val = theme === 'dark' ? colObj.dark : colObj.swatch;
    document.documentElement.style.setProperty('--quran-color', val);
  }, [quranColor, theme]);

  // Persist settings
  useEffect(() => {
    localStorage.setItem('arFontSize', arabicFontSize);
    localStorage.setItem('bnFontSize', bengaliFontSize);
    localStorage.setItem('arLineHeight', arabicLineHeight);
    localStorage.setItem('splitView', splitView);
  }, [arabicFontSize, bengaliFontSize, arabicLineHeight, splitView]);

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

  // 2. Load Surah Meta when currentSurahId changes (With AbortController)
  useEffect(() => {
    if (!currentSurahId) return;
    const controller = new AbortController();
    setLoading(true);
    fetch(`/data/${currentSurahId}/meta.json`, { signal: controller.signal })
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
      .catch((err) => {
        if (err.name !== 'AbortError') {
          console.error('Failed to load surah meta', err);
        }
      });

    return () => controller.abort();
  }, [currentSurahId]);

  // 3. Load Ruku Data when currentSurahId or currentRukuId changes (With AbortController & Zero Leakage)
  useEffect(() => {
    if (!currentSurahId || !currentRukuId) return;
    const controller = new AbortController();
    setLoading(true);
    setRukuData(null); // Clear previous ruku data immediately to prevent leakage

    fetch(`/data/${currentSurahId}/ruku-${currentRukuId}.json`, { signal: controller.signal })
      .then((r) => r.json())
      .then((data) => {
        setRukuData(data);
        setLoading(false);
        // Reset scroll position to top
        window.scrollTo({ top: 0, behavior: 'instant' });
        // Ensure selected ayah is within this ruku's range
        if (data.ayahs && data.ayahs.length > 0) {
          const exists = data.ayahs.some((a) => a.ayah === selectedAyahNum);
          if (!exists) {
            setSelectedAyahNum(data.ayahs[0].ayah);
          }
        }
      })
      .catch((err) => {
        if (err.name !== 'AbortError') {
          console.error('Failed to load ruku data', err);
          setLoading(false);
        }
      });

    return () => controller.abort();
  }, [currentSurahId, currentRukuId]);

  // 4. Update URL Hash for Permanent Deep Linking
  useEffect(() => {
    if (activeView === 'dashboard') {
      window.location.hash = '#/';
    } else if (currentSurahId && selectedAyahNum) {
      window.location.hash = `#/${currentSurahId}/${selectedAyahNum}`;
    }
  }, [activeView, currentSurahId, selectedAyahNum]);

  // Listen for hashchange events dynamically
  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash.replace('#/', '').replace('#', '');
      if (!hash) return;
      const parts = hash.split('/');
      const sId = parseInt(parts[0]);
      if (!isNaN(sId) && sId >= 24 && sId <= 114) {
        if (sId !== currentSurahId) setCurrentSurahId(sId);
        setActiveView('study');
        if (parts[1]) {
          if (parts[1].startsWith('ruku-')) {
            const rId = parseInt(parts[1].replace('ruku-', ''));
            if (!isNaN(rId)) handleSelectRuku(rId);
          } else {
            const aId = parseInt(parts[1]);
            if (!isNaN(aId)) {
              setSelectedAyahNum(aId);
              if (surahMeta?.rukus) {
                const match = surahMeta.rukus.find(r => aId >= r.ayah_start && aId <= r.ayah_end);
                if (match && match.ruku_id !== currentRukuId) {
                  setCurrentRukuId(match.ruku_id);
                }
              }
            }
          }
        }
      }
    };
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, [currentSurahId, currentRukuId, surahMeta]);

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
    if (studyMode !== 'ayah') {
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

  // Keyboard Navigation: Ctrl+K, Left/Right Arrows, Escape
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
    <div className="min-h-screen flex flex-col pb-16 md:pb-6 transition-colors">
      {/* Top Header with Auto-Hide on Scroll */}
      <Header
        surahs={surahs}
        currentSurah={currentSurah}
        currentRuku={currentRukuId}
        surahMeta={surahMeta}
        studyMode={studyMode}
        setStudyMode={setStudyMode}
        onSelectSurah={handleSelectSurah}
        onSelectRuku={handleSelectRuku}
        onOpenSidebar={() => setIsSidebarOpen(true)}
        onOpenSearch={() => setIsSearchOpen(true)}
        onOpenSettings={() => setIsSettingsOpen(true)}
        onOpenNotes={() => setIsNotesOpen(true)}
        onOpenAuthor={() => setIsAuthorOpen(true)}
        theme={theme}
        setTheme={setTheme}
        isHidden={isHeaderHidden}
      />

      {/* Mobile 3-Tier Switcher Tabs (Front and center on phone screens) */}
      {activeView === 'study' && (
        <div className="md:hidden bg-white/95 dark:bg-gray-800/95 backdrop-blur-md border-b border-gray-200 dark:border-gray-700 px-3 py-1.5 flex items-center justify-between gap-1.5 shadow-2xs font-bengali">
          <button
            onClick={() => setStudyMode('surah')}
            className={`flex-1 py-1.5 px-1.5 rounded-xl text-xs font-bold text-center transition flex items-center justify-center gap-1 ${
              studyMode === 'surah'
                ? 'bg-emerald-600 text-white shadow-xs'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            <span>🏛️ সূরা</span>
          </button>
          <button
            onClick={() => setStudyMode('ruku')}
            className={`flex-1 py-1.5 px-1.5 rounded-xl text-xs font-bold text-center transition flex items-center justify-center gap-1 ${
              studyMode === 'ruku' || studyMode === 'thematic'
                ? 'bg-emerald-600 text-white shadow-xs'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            <span>📑 রুকু</span>
          </button>
          <button
            onClick={() => setStudyMode('ayah')}
            className={`flex-1 py-1.5 px-1.5 rounded-xl text-xs font-bold text-center transition flex items-center justify-center gap-1 ${
              studyMode === 'ayah' || studyMode === 'mushaf'
                ? 'bg-emerald-600 text-white shadow-xs'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            <span>📖 আয়াত</span>
          </button>
        </div>
      )}

      {/* Horizontal Ayah Jumper Bar (When in Ayah Study or Mushaf mode) */}
      {activeView === 'study' && (studyMode === 'ayah' || studyMode === 'mushaf') && rukuData && (
        <AyahJumper
          ayahs={rukuData.ayahs}
          selectedAyah={selectedAyahNum}
          onSelectAyah={handleSelectAyah}
        />
      )}

      {/* Main Content Area: Strict 3-Tier Isolation */}
      <main className="flex-1">
        {activeView === 'dashboard' ? (
          <SurahDashboard
            surahs={surahs}
            siteMeta={siteMeta}
            onSelectSurah={handleSelectSurah}
            onOpenAuthor={() => setIsAuthorOpen(true)}
          />
        ) : loading ? (
          <div className="max-w-4xl mx-auto py-24 text-center space-y-3 font-bengali">
            <div className="w-10 h-10 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
            <p className="text-gray-500 text-sm font-semibold">সূরা ও রুকুর প্রামাণ্য তাহকীক ডাটা লোড হচ্ছে...</p>
          </div>
        ) : studyMode === 'surah' ? (
          <SurahScopeView
            key={`surah-scope-${currentSurahId}`}
            surahMeta={surahMeta}
            surahInfo={currentSurah}
            onSelectRuku={(rId) => {
              handleSelectRuku(rId);
              setStudyMode('ruku');
            }}
            onSwitchToRukuScope={() => setStudyMode('ruku')}
            onSwitchToAyahScope={() => setStudyMode('ayah')}
          />
        ) : (studyMode === 'ruku' || studyMode === 'thematic') ? (
          <RukuScopeView
            key={`ruku-scope-${currentSurahId}-${currentRukuId}`}
            rukuData={rukuData}
            surahInfo={currentSurah}
            onSelectAyah={(aNum) => {
              setSelectedAyahNum(aNum);
              setStudyMode('ayah');
            }}
            onSwitchToAyahScope={() => setStudyMode('ayah')}
          />
        ) : studyMode === 'mushaf' ? (
          <MushafView
            key={`mushaf-scope-${currentSurahId}-${currentRukuId}`}
            rukuData={rukuData}
            surahInfo={currentSurah}
            onSelectAyah={(aNum) => {
              setSelectedAyahNum(aNum);
              setStudyMode('ayah');
            }}
            arabicFontSize={arabicFontSize + 2}
            arabicLineHeight={arabicLineHeight}
          />
        ) : (
          <AyahScopeView
            key={`ayah-scope-${currentSurahId}-${currentRukuId}-${selectedAyahNum}`}
            ayah={currentAyah}
            surahInfo={currentSurah}
            rukuInfo={rukuData}
            onPrevAyah={handlePrevAyah}
            onNextAyah={handleNextAyah}
            onSelectAyah={(aNum) => setSelectedAyahNum(aNum)}
            arabicFontSize={arabicFontSize}
            bengaliFontSize={bengaliFontSize}
            arabicLineHeight={arabicLineHeight}
            splitView={splitView}
            onToggleSplitView={() => setSplitView(!splitView)}
          />
        )}
      </main>

      {/* Bottom Sticky Navigation for Mobile */}
      <BottomNav
        activeView={activeView}
        setActiveView={setActiveView}
        studyMode={studyMode}
        setStudyMode={setStudyMode}
        onOpenNotes={() => setIsNotesOpen(true)}
        onGoHome={() => setActiveView('dashboard')}
      />

      {/* Modals & Drawers */}
      <SurahSidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        surahs={surahs}
        currentSurahId={currentSurahId}
        onSelectSurah={handleSelectSurah}
      />

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
        splitView={splitView}
        setSplitView={setSplitView}
        quranColor={quranColor}
        setQuranColor={setQuranColor}
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

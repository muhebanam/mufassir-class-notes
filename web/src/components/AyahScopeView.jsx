import React, { useState, useEffect, useRef } from 'react';
import { 
  BookOpen, ChevronLeft, ChevronRight, Copy, Check, 
  Columns, AlignLeft, Volume2, Sparkles, Scale, Maximize2, Minimize2,
  Bookmark, Share2, Languages, ExternalLink, Compass, GraduationCap,
  AlertCircle, Library, FileText, Layers, CheckCircle2, ChevronDown, ChevronUp
} from 'lucide-react';
import MarkdownContent, { normalizeQuranBrackets } from './MarkdownContent';
import TahqeeqTable from './TahqeeqTable';
import QiraatTable from './QiraatTable';
import WordByWordSection from './WordByWordSection';
import JalalaynView from './JalalaynView';
import ComparativeTafsirSection from './ComparativeTafsirSection';
import HadithTakhrijSection from './HadithTakhrijSection';
import MunasabatSection from './MunasabatSection';
import MasalaCard from './MasalaCard';
import TafsirAppMenu from './TafsirAppMenu';
import AyahQuickIndex, { AYAH_SECTIONS, RUKU_CONTEXT_SECTIONS } from './AyahQuickIndex';
import { toBn } from '../utils/helpers';

export default function AyahScopeView({
  ayah,
  surahInfo,
  rukuInfo,
  onPrevAyah,
  onNextAyah,
  onSelectAyah,
  arabicFontSize = 28,
  bengaliFontSize = 16,
  arabicLineHeight = 2.2,
  splitView = true,
  onToggleSplitView
}) {
  const [copied, setCopied] = useState(false);
  const [activeSection, setActiveSection] = useState('sec-tahqeeq');
  const [viewMode, setViewMode] = useState('continuous'); // 'continuous' | 'single'
  const [isRukuGroupOpen, setIsRukuGroupOpen] = useState(false);

  // Reset local state whenever ayah changes
  useEffect(() => {
    setCopied(false);
  }, [ayah?.surah, ayah?.ruku, ayah?.ayah]);

  // Scroll spy via IntersectionObserver in continuous mode
  useEffect(() => {
    if (viewMode !== 'continuous') return;

    const allSectionIds = [
      ...AYAH_SECTIONS.map(s => s.id),
      ...RUKU_CONTEXT_SECTIONS.map(s => s.id)
    ];

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries.find(e => e.isIntersecting);
        if (visible) {
          setActiveSection(visible.target.id);
        }
      },
      {
        rootMargin: '-120px 0px -60% 0px',
        threshold: 0.1
      }
    );

    allSectionIds.forEach(id => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, [viewMode, isRukuGroupOpen, ayah?.ayah]);

  // Handle click on QuickIndex tab
  const handleSelectSection = (sectionId, groupType) => {
    setActiveSection(sectionId);

    if (groupType === 'ruku' && !isRukuGroupOpen) {
      setIsRukuGroupOpen(true);
    }

    if (viewMode === 'continuous') {
      setTimeout(() => {
        const el = document.getElementById(sectionId);
        if (el) {
          const offset = window.innerWidth >= 640 ? 195 : 185;
          const top = el.getBoundingClientRect().top + window.scrollY - offset;
          window.scrollTo({ top: Math.max(0, top), behavior: 'smooth' });
        }
      }, 60);
    }
  };

  // Zero Data Leakage Validation Guard
  if (!ayah || !rukuInfo) {
    return (
      <div className="max-w-4xl mx-auto py-16 text-center space-y-3 font-bengali">
        <div className="w-8 h-8 border-3 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
        <p className="text-gray-500 text-sm">আয়াত ডাটা লোড হচ্ছে...</p>
      </div>
    );
  }

  // Guard: Confirm ayah belongs to current ruku
  if (ayah.ayah < rukuInfo.ayah_start || ayah.ayah > rukuInfo.ayah_end) {
    return (
      <div className="max-w-2xl mx-auto my-12 p-6 rounded-2xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800 text-center font-bengali">
        <p className="text-amber-800 dark:text-amber-300 font-semibold text-sm">
          আয়াত {toBn(ayah.ayah)} বর্তমান রুকু {toBn(rukuInfo.ruku_id)}-এর সীমার ({toBn(rukuInfo.ayah_start)}–{toBn(rukuInfo.ayah_end)}) অন্তর্ভুক্ত নয়।
        </p>
        <button
          onClick={() => onSelectAyah && onSelectAyah(rukuInfo.ayah_start)}
          className="mt-3 px-4 py-2 rounded-xl bg-emerald-600 text-white text-xs font-bold"
        >
          রুকুর প্রথম আয়াতে ফিরে যান
        </button>
      </div>
    );
  }

  const handleCopyAyah = () => {
    const copyText = `${ayah.text_uthmani}\n\nঅনুবাদ: ${ayah.translation}\n(সূরা ${surahInfo?.name_bn || toBn(ayah.surah)}, আয়াত ${ayah.ayah})`;
    navigator.clipboard.writeText(copyText).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  const tahqeeqWords = (Array.isArray(ayah.tahqeeq) && ayah.tahqeeq.length > 0)
    ? ayah.tahqeeq
    : (ayah.mufradat || []);
  const qiraatList = ayah.qiraat || [];
  const thematic = rukuInfo.thematic_topics || {};

  const hasPrev = ayah.ayah > (rukuInfo.ayah_start || 1);
  const hasNext = ayah.ayah < (rukuInfo.ayah_end || 64);

  const isGoldStatus = rukuInfo.status === 'gold';
  const statusBadge = isGoldStatus ? (
    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800 text-[11px] font-bold">
      <CheckCircle2 className="w-3 h-3 text-emerald-600 dark:text-emerald-400" />
      <span>গোল্ড স্ট্যান্ডার্ড</span>
    </span>
  ) : (
    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 border border-amber-300 dark:border-amber-800 text-[11px] font-medium">
      <AlertCircle className="w-3 h-3 text-amber-600 dark:text-amber-400" />
      <span>কাজ চলমান (খসড়া)</span>
    </span>
  );

  // Helper for multi-ayah covers badge
  const renderCoversBadge = (covers) => {
    if (Array.isArray(covers) && covers.length === 2 && covers[0] !== covers[1]) {
      return (
        <span className="inline-flex items-center gap-1 text-[11px] font-semibold px-2 py-0.5 rounded-full bg-indigo-50 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800 shadow-2xs">
          <Layers className="w-3 h-3 text-indigo-500" />
          <span>আয়াত {toBn(covers[0])}–{toBn(covers[1])}-এর যৌথ আলোচনা</span>
        </span>
      );
    }
    return null;
  };

  return (
    <div 
      key={`${ayah.surah}-${ayah.ruku}-${ayah.ayah}`} 
      className="w-full max-w-6xl mx-auto px-3 sm:px-6 py-3 sm:py-5 space-y-4 sm:space-y-5 layout-safe"
    >
      {/* 1. Ayah Action & Navigation Top Bar */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-3 sm:p-4 shadow-2xs flex flex-wrap items-center justify-between gap-3">
        {/* Breadcrumb info + Status Badge */}
        <div className="flex flex-wrap items-center gap-2 text-xs sm:text-sm font-bengali">
          <span className="font-bold text-gray-900 dark:text-gray-100">
            সূরা {surahInfo?.name_bn || toBn(ayah.surah)}
          </span>
          <span className="text-gray-400">•</span>
          <span className="text-gray-600 dark:text-gray-300">
            রুকু {toBn(rukuInfo.ruku_id)}
          </span>
          <span className="text-gray-400">•</span>
          <span className="px-2.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-900/40 text-emerald-800 dark:text-emerald-300 font-bold font-mono">
            আয়াত {toBn(ayah.ayah)}
          </span>
          <div className="ml-1">
            {statusBadge}
          </div>
        </div>

        {/* Action Controls & Prev/Next */}
        <div className="flex items-center gap-2">
          {/* Split view toggle (desktop only) */}
          <button
            onClick={onToggleSplitView}
            title={splitView ? "স্ট্যাকড ভিউতে পরিবর্তন করুন" : "স্প্লিট ভিউতে পরিবর্তন করুন"}
            className="hidden lg:flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700 text-xs font-bengali text-gray-700 dark:text-gray-300 transition"
          >
            <Columns className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            <span>{splitView ? 'ডুয়াল স্প্লিট' : 'একক কলাম'}</span>
          </button>

          {/* Copy Ayah */}
          <button
            onClick={handleCopyAyah}
            title="আয়াত ও অনুবাদ কপি করুন"
            className="p-2 rounded-xl border border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-300 transition"
          >
            {copied ? <Check className="w-4 h-4 text-emerald-600" /> : <Copy className="w-4 h-4" />}
          </button>

          {/* External Tafsir.app Enhanced Dropdown */}
          <TafsirAppMenu surah={ayah.surah} ayahNumber={ayah.ayah} />

          {/* Prev Ayah */}
          <button
            onClick={onPrevAyah}
            disabled={!hasPrev}
            className={`p-2 rounded-xl border flex items-center justify-center transition ${
              hasPrev 
                ? 'border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700' 
                : 'border-gray-100 dark:border-gray-800 text-gray-300 dark:text-gray-600 cursor-not-allowed'
            }`}
            title="পূর্ববর্তী আয়াত"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>

          {/* Next Ayah */}
          <button
            onClick={onNextAyah}
            disabled={!hasNext}
            className={`p-2 rounded-xl border flex items-center justify-center transition ${
              hasNext 
                ? 'border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700' 
                : 'border-gray-100 dark:border-gray-800 text-gray-300 dark:text-gray-600 cursor-not-allowed'
            }`}
            title="পরবর্তী আয়াত"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* 2. Main Ayah Display Block (Uthmani Text + বঙ্গানুবাদ + শব্দানুগ অনুবাদ সেকশন) */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl sm:rounded-3xl border border-gray-200 dark:border-gray-700 p-5 sm:p-7 shadow-xs space-y-5">
        {/* Arabic Ayah with End Symbol */}
        <div 
          className="uthmani-text leading-loose text-right font-quran select-text" 
          dir="rtl"
          style={{ 
            fontSize: `${arabicFontSize}px`,
            lineHeight: `${arabicLineHeight}`
          }}
        >
          <span>{ayah.text_uthmani}</span>
          <span className="ayah-end-symbol text-emerald-700 dark:text-emerald-400 font-mono text-2xl mx-1.5" dir="rtl">
            ۝{toBn(ayah.ayah)}
          </span>
        </div>

        {/* Simple Ayah Text if available */}
        {ayah.text_simple && (
          <div className="text-right font-arabic text-sm text-gray-500 dark:text-gray-400 pt-2 border-t border-gray-100 dark:border-gray-700/60" dir="rtl">
            {ayah.text_simple}
          </div>
        )}

        {/* সহজি ও প্রামাণিক বঙ্গানুবাদ (Fluent Bengali Translation) */}
        <div className="bg-emerald-50/50 dark:bg-emerald-950/20 p-4 rounded-xl border border-emerald-100 dark:border-emerald-900/40 text-gray-900 dark:text-gray-100 font-bengali leading-relaxed">
          <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-800 dark:text-emerald-400 mb-1">
            <AlignLeft className="w-3.5 h-3.5" />
            <span>সহজ ও প্রামাণিক বঙ্গানুবাদ:</span>
          </div>
          <div className="text-sm sm:text-base font-medium">
            <span className="text-emerald-700 dark:text-emerald-400 font-bold mr-1.5">({toBn(ayah.ayah)})</span>
            {ayah.translation || "অনুবাদ প্রস্তুত করা হচ্ছে..."}
          </div>
        </div>

        {/* শব্দানুগ ইন্টারলিনিয়ার অনুবাদ সেকশন (Word-by-Word Interlinear Section) */}
        <WordByWordSection
          ayah={ayah}
          arabicFontSize={arabicFontSize}
          bengaliFontSize={bengaliFontSize}
          arabicLineHeight={arabicLineHeight}
        />
      </div>

      {/* 3. Quick Index Bar (Two Groups: Ayah Specific vs Ruku Context + Dual Reading Mode) */}
      <AyahQuickIndex
        activeSection={activeSection}
        onSelectSection={handleSelectSection}
        viewMode={viewMode}
        onToggleViewMode={() => setViewMode(viewMode === 'continuous' ? 'single' : 'continuous')}
        rukuInfo={rukuInfo}
        ayahNumber={ayah.ayah}
        isRukuGroupOpen={isRukuGroupOpen}
        onToggleRukuGroup={() => setIsRukuGroupOpen(!isRukuGroupOpen)}
      />

      {/* 4. CHAPTER DISPLAY: CONTINUOUS JOURNAL MODE vs SINGLE FOCUS MODE */}
      {viewMode === 'single' ? (
        /* SINGLE FOCUS VIEW: Renders only the selected chapter with navigation */
        <div className="space-y-4">
          <div className="flex items-center justify-between p-3 rounded-xl bg-gray-100 dark:bg-gray-800 text-xs font-bengali">
            <span className="font-semibold text-gray-600 dark:text-gray-300">
              একক শাস্ত্র ফোকাস মোড: <strong className="text-emerald-700 dark:text-emerald-400">{activeSection}</strong>
            </span>
            <button
              onClick={() => setViewMode('continuous')}
              className="text-emerald-600 hover:underline font-bold"
            >
              একটানা ভিউতে ফিরুন
            </button>
          </div>

          {/* Render target single card */}
          {activeSection === 'sec-tahqeeq' && (
            <div id="sec-tahqeeq" className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5 shadow-xs">
              <TahqeeqTable words={tahqeeqWords} ayahNumber={ayah.ayah} />
            </div>
          )}

          {activeSection === 'sec-02-munasabat' && (
            <div id="sec-02-munasabat">
              {ayah.munasabat ? (
                <MunasabatSection 
                  munasabat={ayah.munasabat}
                  ayahNumber={ayah.ayah}
                  prevAyah={ayah.ayah > (rukuInfo.ayah_start || 1) ? ayah.ayah - 1 : (ayah.ayah > 1 ? ayah.ayah - 1 : null)}
                  nextAyah={ayah.ayah < (rukuInfo.ayah_end || 64) ? ayah.ayah + 1 : null}
                />
              ) : (
                <div className="p-6 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-center text-gray-500 font-bengali text-sm italic">
                  এই আয়াতের জন্য স্বতন্ত্র আন্তঃআয়াত মুনাসাবাত সংকলিত হয়নি।
                </div>
              )}
            </div>
          )}

          {activeSection === 'sec-03-irab' && (
            <div id="sec-03-irab" className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-6 shadow-xs space-y-3 font-bengali">
              <div className="flex items-center justify-between pb-2 border-b border-gray-100 dark:border-gray-700">
                <div className="flex items-center gap-2">
                  <FileText className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                  <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100">
                    ০৩. ই'রাব ও ব্যাকরণগত বিশ্লেষণ (আয়াত {toBn(ayah.ayah)})
                  </h4>
                  {renderCoversBadge(ayah.irab_covers)}
                </div>
              </div>
              {ayah.irab ? (
                <div className="prose dark:prose-invert text-xs sm:text-sm text-gray-800 dark:text-gray-200 leading-relaxed pt-1">
                  <MarkdownContent content={ayah.irab} />
                </div>
              ) : (
                <p className="text-gray-500 text-sm italic text-center py-4">
                  এই আয়াতের জন্য স্বতন্ত্র ই'রাব সংকলিত হয়নি / প্রযোজ্য নয়।
                </p>
              )}
            </div>
          )}

          {activeSection === 'sec-04-qiraat' && (
            <div id="sec-04-qiraat" className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5 shadow-xs">
              <QiraatTable 
                tableData={qiraatList} 
                title={`আয়াত ${toBn(ayah.ayah)}-এর ১০ কিরাআত পাঠভেদ`}
              />
            </div>
          )}

          {activeSection === 'sec-05-tafsir' && (
            <div id="sec-05-tafsir" className="space-y-4">
              <JalalaynView 
                ayah={ayah} 
                bengaliFontSize={bengaliFontSize} 
                arabicFontSize={arabicFontSize - 2}
              />
              {ayah.comparative_tafsir && (
                <ComparativeTafsirSection 
                  content={ayah.comparative_tafsir}
                  surah={ayah.surah}
                  ayahNumber={ayah.ayah}
                  covers={ayah.comparative_tafsir_covers}
                  bengaliFontSize={bengaliFontSize}
                />
              )}
            </div>
          )}

          {activeSection === 'sec-06-hadith' && (
            <div id="sec-06-hadith">
              {ayah.shane_nuzul ? (
                <HadithTakhrijSection 
                  content={ayah.shane_nuzul} 
                  ayahNumber={ayah.ayah} 
                  covers={ayah.shane_nuzul_covers}
                />
              ) : (
                <div className="p-6 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-center text-gray-500 font-bengali text-sm italic">
                  এই আয়াতের জন্য স্বতন্ত্র শানে নুযূল বা হাদীস তাখরীজ সংকলিত হয়নি / প্রযোজ্য নয়।
                </div>
              )}
            </div>
          )}

          {/* Group 2 Ruku Sections when selected in single mode */}
          {RUKU_CONTEXT_SECTIONS.some(s => s.id === activeSection) && (
            <div className="bg-white dark:bg-gray-800 rounded-2xl border border-indigo-200 dark:border-indigo-800 p-4 sm:p-6 shadow-xs space-y-3 font-bengali">
              {(() => {
                const secDef = RUKU_CONTEXT_SECTIONS.find(s => s.id === activeSection);
                const topic = thematic[secDef?.secKey] || {};
                const Icon = secDef?.icon || BookOpen;
                return (
                  <>
                    <div className="flex items-center justify-between pb-3 border-b border-indigo-100 dark:border-indigo-900">
                      <div className="flex items-center gap-2">
                        <Icon className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                        <div>
                          <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100">
                            {secDef?.num}. {topic.title || secDef?.label}
                          </h4>
                          <span className="text-[11px] text-indigo-700 dark:text-indigo-400">
                            রুকুর সামগ্রিক প্রেক্ষাপট (আয়াত {toBn(rukuInfo.ayah_start)}–{toBn(rukuInfo.ayah_end)})
                          </span>
                        </div>
                      </div>
                    </div>
                    {topic.cards && Array.isArray(topic.cards) && topic.cards.length > 0 ? (
                      <div className="space-y-4 pt-2">
                        {topic.cards.map((card, idx) => (
                          <MasalaCard key={idx} card={card} index={idx} />
                        ))}
                      </div>
                    ) : topic.content ? (
                      <div className="prose dark:prose-invert text-xs sm:text-sm text-gray-800 dark:text-gray-200 leading-relaxed pt-2">
                        <MarkdownContent content={topic.content} />
                      </div>
                    ) : (
                      <p className="text-gray-500 text-sm italic text-center py-4">
                        এই অধ্যায়ের তথ্য এখনো প্রস্তুত করা হচ্ছে।
                      </p>
                    )}
                  </>
                );
              })()}
            </div>
          )}
        </div>
      ) : (
        /* CONTINUOUS JOURNAL MODE: Dual Split on Desktop or Stacked View */
        <div className="space-y-6">
          <div className={`grid gap-4 sm:gap-6 ${splitView ? 'lg:grid-cols-12' : 'grid-cols-1'}`}>
            
            {/* Left Column: Tafsir, Hadith, Irab, Munasabat */}
            <div className={`space-y-4 sm:space-y-5 ${splitView ? 'lg:col-span-6' : ''}`}>
              
              {/* 1. Jalalayn 3-Tier Layered View with View Toggles (sec-05-tafsir) */}
              <div id="sec-05-tafsir" className="scroll-mt-36 sm:scroll-mt-44 space-y-4">
                <JalalaynView 
                  ayah={ayah} 
                  bengaliFontSize={bengaliFontSize} 
                  arabicFontSize={arabicFontSize - 2}
                />

                {/* 2. Comparative Tafsir (Tafsir al-Kabir, Tabari, Ibn Kathir, Qurtubi) */}
                {ayah.comparative_tafsir && (
                  <ComparativeTafsirSection 
                    content={ayah.comparative_tafsir}
                    surah={ayah.surah}
                    ayahNumber={ayah.ayah}
                    covers={ayah.comparative_tafsir_covers}
                    bengaliFontSize={bengaliFontSize}
                  />
                )}
              </div>

              {/* 3. Shan-e-Nuzul & Hadith Takhrij (Cards / Table) */}
              {ayah.shane_nuzul ? (
                <HadithTakhrijSection 
                  content={ayah.shane_nuzul} 
                  ayahNumber={ayah.ayah} 
                  covers={ayah.shane_nuzul_covers}
                />
              ) : (
                <div id="sec-06-hadith" className="scroll-mt-36 sm:scroll-mt-44 p-4 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-center text-xs text-gray-500 font-bengali">
                  <span>০৬. শানে নুযূল ও হাদীস তাখরীজ: এই আয়াতের জন্য স্বতন্ত্র ঘটনা বর্ণিত হয়নি।</span>
                </div>
              )}

              {/* 4. Irab & Grammar Section (sec-03-irab) */}
              <div 
                id="sec-03-irab" 
                className="scroll-mt-36 sm:scroll-mt-44 bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5 shadow-xs space-y-3 font-bengali transition-colors"
              >
                <div className="flex items-center justify-between pb-2.5 border-b border-gray-100 dark:border-gray-700">
                  <div className="flex items-center gap-2">
                    <div className="w-7 h-7 rounded-lg bg-indigo-50 dark:bg-indigo-950/60 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
                      <FileText className="w-4 h-4" />
                    </div>
                    <div>
                      <div className="flex flex-wrap items-center gap-2">
                        <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100">
                          ০৩. ই'রাব ও ব্যাকরণগত বিশ্লেষণ
                        </h4>
                        {renderCoversBadge(ayah.irab_covers)}
                      </div>
                      <p className="text-[11px] text-gray-500 dark:text-gray-400">
                        তারকীব, বাক্যরীতি ও পদমর্যাদা বিশ্লেষণ
                      </p>
                    </div>
                  </div>
                </div>
                {ayah.irab ? (
                  <div className="prose dark:prose-invert text-xs sm:text-sm text-gray-800 dark:text-gray-200 leading-relaxed pt-1">
                    <MarkdownContent content={ayah.irab} />
                  </div>
                ) : (
                  <p className="text-gray-500 text-xs italic text-center py-3">
                    এই আয়াতের জন্য স্বতন্ত্র ই'রাব সংকলিত হয়নি / প্রযোজ্য নয়।
                  </p>
                )}
              </div>

              {/* 5. Tafsir al-Kabir: Munasabat between Ayahs */}
              {ayah.munasabat ? (
                <MunasabatSection 
                  munasabat={ayah.munasabat}
                  ayahNumber={ayah.ayah}
                  prevAyah={ayah.ayah > (rukuInfo.ayah_start || 1) ? ayah.ayah - 1 : (ayah.ayah > 1 ? ayah.ayah - 1 : null)}
                  nextAyah={ayah.ayah < (rukuInfo.ayah_end || 64) ? ayah.ayah + 1 : null}
                />
              ) : (
                <div id="sec-02-munasabat" className="scroll-mt-36 sm:scroll-mt-44 p-4 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-center text-xs text-gray-500 font-bengali">
                  <span>০২. আন্তঃআয়াত মুনাসাবাত: এই আয়াতের জন্য স্বতন্ত্র যোগসূত্র সংকলিত হয়নি।</span>
                </div>
              )}
            </div>

            {/* Right Column: Comprehensive Tahqeeq Table & Qiraat */}
            <div className={`space-y-4 sm:space-y-5 ${splitView ? 'lg:col-span-6' : ''}`}>
              {/* Tahqeeq Table Card */}
              <div id="sec-tahqeeq" className="scroll-mt-36 sm:scroll-mt-44 bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5 shadow-xs">
                <TahqeeqTable 
                  words={tahqeeqWords} 
                  ayahNumber={ayah.ayah} 
                />
              </div>

              {/* Qiraat Table */}
              <div id="sec-04-qiraat" className="scroll-mt-36 sm:scroll-mt-44 bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5 shadow-xs">
                <QiraatTable 
                  tableData={qiraatList} 
                  title={`আয়াত ${toBn(ayah.ayah)}-এর ১০ কিরাআত পাঠভেদ`}
                />
              </div>
            </div>

          </div>

          {/* GROUP 2: RUKU-LEVEL CONTEXT SECTIONS (COLLAPSIBLE TO PREVENT BLOAT) */}
          <div className="pt-4 border-t-2 border-dashed border-gray-200 dark:border-gray-700 font-bengali">
            <div className="rounded-2xl border border-indigo-200 dark:border-indigo-800 bg-gradient-to-br from-indigo-50/40 via-white to-teal-50/30 dark:from-gray-900 dark:via-gray-850 dark:to-gray-900 shadow-xs overflow-hidden transition-all">
              {/* Collapsible Header */}
              <button
                onClick={() => setIsRukuGroupOpen(!isRukuGroupOpen)}
                className="w-full p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-left hover:bg-indigo-50/50 dark:hover:bg-gray-800/80 transition"
              >
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-xl bg-indigo-600 text-white flex items-center justify-center shrink-0 shadow-xs">
                    <Layers className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <h3 className="font-bold text-base sm:text-lg text-gray-900 dark:text-gray-100">
                        রুকুর সামগ্রিক প্রেক্ষাপট ও গবেষণা অধ্যায়সমূহ
                      </h3>
                      <span className="text-xs px-2.5 py-0.5 rounded-full bg-indigo-100 dark:bg-indigo-950 text-indigo-800 dark:text-indigo-300 font-semibold border border-indigo-200 dark:border-indigo-800">
                        আয়াত {toBn(rukuInfo.ayah_start)}–{toBn(rukuInfo.ayah_end)}
                      </span>
                    </div>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                      ভূমিকা ও মাকাসিদ, ফিকহী মতভেদ, আহকাম ও ৪ মাযহাব, উলূমুল কুরআন, বালাগাত, সমকালীন প্রাসঙ্গিকতা ও দরস
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2 self-end sm:self-auto shrink-0">
                  <span className="text-xs font-semibold text-indigo-700 dark:text-indigo-400">
                    {isRukuGroupOpen ? 'ভাঁজ করুন' : 'বিস্তারিত উন্মুক্ত করুন'}
                  </span>
                  <div className="p-1 rounded-lg bg-indigo-100 dark:bg-indigo-900/60 text-indigo-700 dark:text-indigo-300">
                    {isRukuGroupOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                  </div>
                </div>
              </button>

              {/* Collapsible Content */}
              {isRukuGroupOpen && (
                <div className="p-4 sm:p-6 border-t border-indigo-100 dark:border-indigo-900/60 space-y-6">
                  
                  {/* 1. ভূমিকা ও মাকাসিদ (sec-01-makasid) */}
                  <div id="sec-01-makasid" className="scroll-mt-36 sm:scroll-mt-44 p-4 sm:p-5 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 space-y-3">
                    <div className="flex items-center gap-2 pb-2 border-b border-gray-100 dark:border-gray-700">
                      <Compass className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                      <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100">
                        ০১. ভূমিকা ও মাকাসিদ (সূরা {surahInfo?.name_bn || toBn(ayah.surah)}, রুকু {toBn(rukuInfo.ruku_id)})
                      </h4>
                    </div>
                    {thematic.makasid?.summary && (
                      <div className="p-3 rounded-xl bg-indigo-50/60 dark:bg-indigo-950/30 text-indigo-950 dark:text-indigo-200 text-xs sm:text-sm font-medium">
                        {thematic.makasid.summary}
                      </div>
                    )}
                    <div className="prose dark:prose-invert text-xs sm:text-sm text-gray-800 dark:text-gray-200 leading-relaxed">
                      <MarkdownContent content={thematic.makasid?.content || 'তথ্য সংকলিত হচ্ছে...'} />
                    </div>
                  </div>

                  {/* 7. ফিকহী মতভেদ ও তারজীহ (sec-07-ikhtilaf) */}
                  <div id="sec-07-ikhtilaf" className="scroll-mt-36 sm:scroll-mt-44 p-4 sm:p-5 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 space-y-3">
                    <div className="flex items-center gap-2 pb-2 border-b border-gray-100 dark:border-gray-700">
                      <Scale className="w-5 h-5 text-amber-600 dark:text-amber-400" />
                      <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100">
                        ০৭. ফিকহী মতভেদ ও তারজীহ (দলীলভিত্তিক পর্যালোচনা)
                      </h4>
                    </div>
                    <div className="prose dark:prose-invert text-xs sm:text-sm text-gray-800 dark:text-gray-200 leading-relaxed">
                      <MarkdownContent content={thematic.ikhtilaf?.content || 'এই রুকুর জন্য স্বতন্ত্র মতভেদ সংকলিত হয়নি।'} />
                    </div>
                  </div>

                  {/* 8. আহকাম ও ৪ মাযহাব (sec-08-ahkam) */}
                  <div id="sec-08-ahkam" className="scroll-mt-36 sm:scroll-mt-44 p-4 sm:p-5 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 space-y-3">
                    <div className="flex items-center justify-between pb-2 border-b border-gray-100 dark:border-gray-700">
                      <div className="flex items-center gap-2">
                        <Scale className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
                        <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100">
                          ০৮. আহকাম ও ৪ মাযহাবের তুলনামূলক ফতোয়া
                        </h4>
                      </div>
                    </div>
                    {thematic.ahkam?.intro && (
                      <p className="text-xs sm:text-sm text-gray-700 dark:text-gray-300 leading-relaxed italic bn-justify">
                        {thematic.ahkam.intro}
                      </p>
                    )}
                    {thematic.ahkam?.cards && Array.isArray(thematic.ahkam.cards) && thematic.ahkam.cards.length > 0 ? (
                      <div className="space-y-3 pt-2">
                        {thematic.ahkam.cards.map((card, idx) => (
                          <MasalaCard key={idx} card={card} index={idx} />
                        ))}
                      </div>
                    ) : thematic.ahkam?.content ? (
                      <div className="prose dark:prose-invert text-xs sm:text-sm text-gray-800 dark:text-gray-200 leading-relaxed">
                        <MarkdownContent content={thematic.ahkam.content} />
                      </div>
                    ) : (
                      <p className="text-gray-500 text-xs italic">কোনো মাযহাবী বিরোধ বা পৃথক মাসআলা প্রযোজ্য নয়।</p>
                    )}
                  </div>

                  {/* 9. উলূমুল কুরআন (sec-09-ulum) */}
                  <div id="sec-09-ulum" className="scroll-mt-36 sm:scroll-mt-44 p-4 sm:p-5 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 space-y-3">
                    <div className="flex items-center gap-2 pb-2 border-b border-gray-100 dark:border-gray-700">
                      <GraduationCap className="w-5 h-5 text-teal-600 dark:text-teal-400" />
                      <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100">
                        ০৯. উলূমুল কুরআন (নাসিখ-মানসূখ ও উসূল)
                      </h4>
                    </div>
                    <div className="prose dark:prose-invert text-xs sm:text-sm text-gray-800 dark:text-gray-200 leading-relaxed">
                      <MarkdownContent content={thematic.ulumul_quran?.content || 'তথ্য সংকলিত হচ্ছে...'} />
                    </div>
                  </div>

                  {/* 10. বালাগাত ও ই'জায (sec-10-balaghat) */}
                  <div id="sec-10-balaghat" className="scroll-mt-36 sm:scroll-mt-44 p-4 sm:p-5 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 space-y-3">
                    <div className="flex items-center gap-2 pb-2 border-b border-gray-100 dark:border-gray-700">
                      <Sparkles className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                      <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100">
                        ১০. বালাগাত ও অলঙ্কারশাস্ত্র (إعجاز وبلاغة)
                      </h4>
                    </div>
                    <div className="prose dark:prose-invert text-xs sm:text-sm text-gray-800 dark:text-gray-200 leading-relaxed">
                      <MarkdownContent content={thematic.balaghat?.content || 'তথ্য সংকলিত হচ্ছে...'} />
                    </div>
                  </div>

                  {/* 11. সমকালীন প্রাসঙ্গিকতা (sec-11-samakalin) */}
                  <div id="sec-11-samakalin" className="scroll-mt-36 sm:scroll-mt-44 p-4 sm:p-5 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 space-y-3">
                    <div className="flex items-center gap-2 pb-2 border-b border-gray-100 dark:border-gray-700">
                      <AlertCircle className="w-5 h-5 text-rose-600 dark:text-rose-400" />
                      <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100">
                        ১১. সমকালীন প্রাসঙ্গিকতা ও সংশয় নিরসন
                      </h4>
                    </div>
                    <div className="prose dark:prose-invert text-xs sm:text-sm text-gray-800 dark:text-gray-200 leading-relaxed">
                      <MarkdownContent content={thematic.samakalin?.content || 'তথ্য সংকলিত হচ্ছে...'} />
                    </div>
                  </div>

                  {/* 12. দরসের উপকরণ (sec-12-dars) */}
                  <div id="sec-12-dars" className="scroll-mt-36 sm:scroll-mt-44 p-4 sm:p-5 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 space-y-3">
                    <div className="flex items-center gap-2 pb-2 border-b border-gray-100 dark:border-gray-700">
                      <BookOpen className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
                      <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100">
                        ১২. দরসের উপকরণ (দারসে নেযামী পাঠদান গাইড)
                      </h4>
                    </div>
                    <div className="prose dark:prose-invert text-xs sm:text-sm text-gray-800 dark:text-gray-200 leading-relaxed">
                      <MarkdownContent content={thematic.dars?.content || 'তথ্য সংকলিত হচ্ছে...'} />
                    </div>
                  </div>

                  {/* 13. গ্রন্থপঞ্জি ও রেফারেন্স (sec-13-bibliography) */}
                  <div id="sec-13-bibliography" className="scroll-mt-36 sm:scroll-mt-44 p-4 sm:p-5 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 space-y-3">
                    <div className="flex items-center gap-2 pb-2 border-b border-gray-100 dark:border-gray-700">
                      <Library className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                      <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100">
                        ১৩. গ্রন্থপঞ্জি ও রেফারেন্স (প্রামাণ্য মূলগ্রন্থের তালিকা)
                      </h4>
                    </div>
                    <div className="prose dark:prose-invert text-xs sm:text-sm text-gray-800 dark:text-gray-200 leading-relaxed">
                      <MarkdownContent content={thematic.bibliography?.content || 'তথ্য সংকলিত হচ্ছে...'} />
                    </div>
                  </div>

                  {/* 14. গবেষণার সীমাবদ্ধতা (sec-14-limitations) */}
                  <div id="sec-14-limitations" className="scroll-mt-36 sm:scroll-mt-44 p-4 sm:p-5 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 space-y-3">
                    <div className="flex items-center gap-2 pb-2 border-b border-gray-100 dark:border-gray-700">
                      <AlertCircle className="w-5 h-5 text-gray-600 dark:text-gray-400" />
                      <h4 className="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100">
                        ১৪. গবেষণার সীমাবদ্ধতা ও ভবিষ্যৎ কর্মপন্থা
                      </h4>
                    </div>
                    <div className="prose dark:prose-invert text-xs sm:text-sm text-gray-800 dark:text-gray-200 leading-relaxed">
                      <MarkdownContent content={thematic.limitations?.content || 'তথ্য সংকলিত হচ্ছে...'} />
                    </div>
                  </div>

                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

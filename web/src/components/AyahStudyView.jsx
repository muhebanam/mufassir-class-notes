import React, { useState, useEffect } from 'react';
import { 
  BookOpen, ChevronDown, ChevronUp, Copy, Check, Bookmark, 
  BookmarkCheck, Languages, Compass, Volume2, 
  FileText, ArrowLeft, ArrowRight, Share2, Columns, Rows,
  Sparkles, Layers
} from 'lucide-react';
import { toBn, copyToClipboard } from '../utils/helpers';
import MarkdownContent from './MarkdownContent';
import CornerOrnament from './CornerOrnament';
import { saveAyahNote, getAyahNote, toggleBookmark, isBookmarked } from '../utils/db';

export default function AyahStudyView({
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
  const [bookmarked, setBookmarked] = useState(false);
  const [activeTab, setActiveTab] = useState('jalalayn'); // 'jalalayn', 'mufradat', 'irab', 'qiraat', 'nuzul', 'notes'
  const [expandAll, setExpandAll] = useState(false);
  const [viewMode, setViewMode] = useState('card'); // 'card' or 'kitab'

  // Note state
  const [noteText, setNoteText] = useState("");
  const [noteTags, setNoteTags] = useState([]);
  const [newTag, setNewTag] = useState("");
  const [noteSavedMsg, setNoteSavedMsg] = useState(false);

  useEffect(() => {
    if (ayah) {
      isBookmarked(ayah.surah, ayah.ayah).then(setBookmarked);
      getAyahNote(ayah.surah, ayah.ayah).then((n) => {
        if (n) {
          setNoteText(n.text || "");
          setNoteTags(n.tags || []);
        } else {
          setNoteText("");
          setNoteTags([]);
        }
      });
    }
  }, [ayah]);

  const handleCopyAyahWithRef = async () => {
    const sName = surahInfo?.name_bn || ayah.surah;
    const textToCopy = `সূরা ${sName} (${toBn(ayah.surah)}:${toBn(ayah.ayah)}) — তাফসীরে জালালাইন\n\n${ayah.text_uthmani} ۝${toBn(ayah.ayah)}\n\nঅনুবাদ: ${ayah.translation || ''}\n\nতাফসীর সারাংশ:\n${ayah.jalalayn || ''}`;
    const success = await copyToClipboard(textToCopy);
    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleShareLink = async () => {
    const url = `${window.location.origin}${window.location.pathname}#/${ayah.surah}/${ayah.ayah}`;
    await copyToClipboard(url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleToggleBookmark = async () => {
    const res = await toggleBookmark(ayah.surah, ayah.ayah, ayah.ruku, surahInfo?.name_bn || "");
    setBookmarked(res);
  };

  const handleSaveNote = async () => {
    await saveAyahNote(ayah.surah, ayah.ayah, ayah.ruku, noteText, noteTags);
    setNoteSavedMsg(true);
    setTimeout(() => setNoteSavedMsg(false), 2000);
  };

  const handleAddTag = (e) => {
    if (e.key === 'Enter' && newTag.trim()) {
      e.preventDefault();
      if (!noteTags.includes(newTag.trim())) {
        const updated = [...noteTags, newTag.trim()];
        setNoteTags(updated);
        saveAyahNote(ayah.surah, ayah.ayah, ayah.ruku, noteText, updated);
      }
      setNewTag("");
    }
  };

  const handleRemoveTag = (tagToRemove) => {
    const updated = noteTags.filter(t => t !== tagToRemove);
    setNoteTags(updated);
    saveAyahNote(ayah.surah, ayah.ayah, ayah.ruku, noteText, updated);
  };

  if (!ayah) return null;

  const tabs = [
    { id: 'jalalayn', label: 'জালালাইন তাফসীর', icon: BookOpen, count: null, available: !!ayah.jalalayn },
    { id: 'mufradat', label: 'মুফরাদাত ও সরফ', icon: Languages, count: (ayah.tahqeeq?.length || ayah.mufradat?.length), available: !!((ayah.tahqeeq && ayah.tahqeeq.length > 0) || (ayah.mufradat && ayah.mufradat.length > 0)) },
    { id: 'irab', label: 'ই\'রাব ও তারকীব', icon: Compass, count: null, available: !!ayah.irab },
    { id: 'qiraat', label: '১০ কিরাআত পাঠভেদ', icon: Volume2, count: ayah.qiraat?.length, available: !!(ayah.qiraat && ayah.qiraat.length > 0) },
    { id: 'nuzul', label: 'শানে নুযূল ও তাখরীজ', icon: Sparkles, count: null, available: !!ayah.nuzul },
    { id: 'notes', label: 'ক্লাস নোট', icon: FileText, count: noteText ? '১' : null, available: true },
  ];

  return (
    <div className="max-w-[1080px] mx-auto px-3 sm:px-5 py-4 space-y-5">
      {/* 1. Ayat Header & Academic Breadcrumb */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl px-4 py-3 shadow-xs border border-gray-200 dark:border-gray-700/80 flex flex-wrap items-center justify-between gap-2 transition-colors">
        <div className="flex items-center gap-1.5 text-xs sm:text-sm font-semibold text-gray-600 dark:text-gray-300">
          <span className="text-emerald-800 dark:text-emerald-400 font-bold">
            সূরা {surahInfo?.name_bn} ({toBn(ayah.surah)})
          </span>
          <span className="text-gray-300 dark:text-gray-600">•</span>
          <span>রুকু {toBn(ayah.ruku)}</span>
          <span className="text-gray-300 dark:text-gray-600">•</span>
          <span className="bg-emerald-100 dark:bg-emerald-950/80 text-emerald-900 dark:text-emerald-300 px-2 py-0.5 rounded-full font-bold">
            আয়াত {toBn(ayah.ayah)}
          </span>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-1 sm:gap-1.5">
          {/* Split / Stacked View Toggle (Visible on lg+) */}
          {onToggleSplitView && viewMode === 'card' && (
            <button
              onClick={onToggleSplitView}
              className="hidden lg:flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 transition"
              title="স্প্লিট ভিউ ও স্ট্যাকড ভিউ টগল করুন"
            >
              {splitView ? <Columns className="w-3.5 h-3.5 text-emerald-600" /> : <Rows className="w-3.5 h-3.5 text-emerald-600" />}
              <span>{splitView ? "ডুয়াল স্প্লিট" : "স্ট্যাকড ভিউ"}</span>
            </button>
          )}

          {/* Kitab Mode / Card Mode Toggle */}
          <button
            onClick={() => setViewMode(viewMode === 'card' ? 'kitab' : 'card')}
            className={`flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold transition ${
              viewMode === 'kitab'
                ? 'bg-amber-100 dark:bg-amber-950/70 text-amber-900 dark:text-amber-300 font-bold border border-amber-300 dark:border-amber-700 shadow-2xs'
                : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200'
            }`}
            title="ধারাবাহিক কিতাব মোড ও কার্ড ভিউ টগল করুন"
          >
            <BookOpen className="w-3.5 h-3.5 text-amber-600" />
            <span className="hidden sm:inline">{viewMode === 'kitab' ? "কিতাব পাঠ" : "কার্ড ভিউ"}</span>
          </button>

          {/* Copy with Reference */}
          <button
            onClick={handleCopyAyahWithRef}
            className="flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold bg-gray-100 dark:bg-gray-700 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 text-gray-700 dark:text-gray-200 transition"
            title="রেফারেন্সসহ আয়াত ও তাফসীর কপি করুন"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
            <span className="hidden sm:inline">{copied ? "কপি হয়েছে" : "কপি"}</span>
          </button>

          {/* Bookmark Button */}
          <button
            onClick={handleToggleBookmark}
            className={`flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold transition ${
              bookmarked 
                ? 'bg-amber-100 dark:bg-amber-950/60 text-amber-900 dark:text-amber-300 font-bold border border-amber-300 dark:border-amber-700' 
                : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200'
            }`}
            title="বুকমার্ক সংরক্ষণ"
          >
            {bookmarked ? <BookmarkCheck className="w-3.5 h-3.5 text-amber-600" /> : <Bookmark className="w-3.5 h-3.5" />}
            <span className="hidden sm:inline">{bookmarked ? "সংরক্ষিত" : "বুকমার্ক"}</span>
          </button>

          {/* Share Link */}
          <button
            onClick={handleShareLink}
            className="p-1.5 rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition"
            title="আয়াতের লিংক কপি করুন"
          >
            <Share2 className="w-3.5 h-3.5" />
          </button>

          {/* Prev / Next Ayah Arrows */}
          <div className="flex items-center border-l border-gray-200 dark:border-gray-700 pl-1.5 ml-1 gap-1">
            <button
              onClick={onPrevAyah}
              disabled={ayah.ayah <= (rukuInfo?.ayah_start || 1)}
              className="p-1.5 rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-30 disabled:cursor-not-allowed transition"
              title="পূর্ববর্তী আয়াত"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={onNextAyah}
              disabled={ayah.ayah >= (rukuInfo?.ayah_end || 64)}
              className="p-1.5 rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-30 disabled:cursor-not-allowed transition"
              title="পরবর্তী আয়াত"
            >
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* 2. Primary Verse Card or Continuous Kitab Mode */}
      {viewMode === 'kitab' && rukuInfo?.ayahs && rukuInfo.ayahs.length > 0 ? (
        <div className="relative bg-white dark:bg-gray-800 rounded-3xl p-6 sm:p-8 shadow-xs border border-gray-200/90 dark:border-gray-700/80 transition-colors space-y-6 overflow-hidden">
          <CornerOrnament className="absolute top-2 left-2 text-emerald-600/30 dark:text-emerald-400/20" />
          <CornerOrnament className="absolute bottom-2 right-2 rotate-180 text-emerald-600/30 dark:text-emerald-400/20" />

          <div className="flex items-center justify-between pb-2 border-b border-gray-100 dark:border-gray-700/60">
            <span className="text-xs font-bold text-amber-800 dark:text-amber-400 flex items-center gap-1.5 font-bengali">
              <BookOpen className="w-4 h-4 text-amber-600" />
              <span>ধারাবাহিক কিতাব মোড • রুকু {toBn(rukuInfo.ruku_id || ayah.ruku)} ({toBn(rukuInfo.ayahs.length)}টি আয়াত)</span>
            </span>
            <span className="text-[11px] text-gray-500 dark:text-gray-400 hidden sm:inline">
              যেকোনো আয়াতে ক্লিক করে নির্বাচিত করুন
            </span>
          </div>

          {/* Continuous Flowing Manuscript Text */}
          <div
            className="uthmani-text text-gray-950 dark:text-gray-50 text-justify leading-loose selection:bg-amber-100 dark:selection:bg-amber-900/60"
            style={{ fontSize: `${arabicFontSize + 2}px`, lineHeight: arabicLineHeight + 0.3 }}
            dir="rtl"
          >
            {rukuInfo.ayahs.map((a) => {
              const isActive = a.ayah === ayah.ayah;
              return (
                <span
                  key={a.ayah}
                  onClick={() => onSelectAyah && onSelectAyah(a.ayah)}
                  className={`cursor-pointer rounded-xl px-1.5 py-0.5 transition inline-block m-0.5 ${
                    isActive
                      ? 'bg-amber-100/90 dark:bg-amber-950/70 ring-2 ring-amber-500/70 text-amber-950 dark:text-amber-100 font-bold shadow-2xs'
                      : 'hover:bg-emerald-50 dark:hover:bg-emerald-950/40'
                  }`}
                  title={`আয়াত ${toBn(a.ayah)} নির্বাচন করুন`}
                >
                  {a.text_uthmani}
                  <span className="ayah-end-symbol text-emerald-700 dark:text-emerald-400 font-normal mx-1 select-none">
                    ۝{toBn(a.ayah)}
                  </span>
                </span>
              );
            })}
          </div>

          {/* Active Ayah Quick Summary Drawer */}
          <div className="bg-emerald-50/50 dark:bg-emerald-950/30 rounded-2xl p-4 border border-emerald-100 dark:border-emerald-800/40 space-y-2">
            <div className="flex items-center justify-between text-xs font-bold text-emerald-900 dark:text-emerald-300">
              <span>নির্বাচিত আয়াত {toBn(ayah.ayah)}-এর বঙ্গানুবাদ:</span>
              <span className="text-[10px] text-gray-500 dark:text-gray-400">নিচে শাস্ত্রীয় গবেষণা ট্যাবসমূহ দেখুন</span>
            </div>
            <p className="text-xs sm:text-sm text-gray-800 dark:text-gray-200 font-bengali leading-relaxed">
              {ayah.translation}
            </p>
          </div>
        </div>
      ) : (
        <div className="relative bg-white dark:bg-gray-800 rounded-3xl p-5 sm:p-7 shadow-xs border border-gray-200/90 dark:border-gray-700/80 transition-colors overflow-hidden">
          <CornerOrnament className="absolute top-2 left-2 text-emerald-600/30 dark:text-emerald-400/20" />
          <CornerOrnament className="absolute bottom-2 right-2 rotate-180 text-emerald-600/30 dark:text-emerald-400/20" />
          {splitView ? (
            /* Dual-Column Split View on large screens */
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
              {/* Right Column (RTL): Uthmani Arabic Text & Jalalayn Matan */}
              <div className="lg:col-span-7 space-y-4 lg:border-l lg:border-gray-100 dark:lg:border-gray-700/60 lg:pl-6 order-1 lg:order-2">
                <div className="flex items-center justify-between text-xs font-bold text-gray-500 dark:text-gray-400 pb-1 border-b border-gray-100 dark:border-gray-700/50">
                  <span className="font-arabic font-bold text-emerald-800 dark:text-emerald-400">النَّصُّ الْقُرْآنِيُّ الْمُبَارَكُ</span>
                  <span className="font-mono text-[11px] bg-emerald-50 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 px-2 py-0.5 rounded">
                    আয়াত {toBn(ayah.ayah)}
                  </span>
                </div>

                {/* Quranic Arabic Verse */}
                <div 
                  className="uthmani-text text-gray-950 dark:text-gray-50 font-bold selection:bg-emerald-100 dark:selection:bg-emerald-900/60"
                  style={{ fontSize: `${arabicFontSize}px`, lineHeight: arabicLineHeight }}
                >
                  {ayah.text_uthmani}
                  <span className="ayah-end-symbol text-emerald-700 dark:text-emerald-400 font-normal mr-1.5 select-none">
                    ۝{toBn(ayah.ayah)}
                  </span>
                </div>

                {/* Jalalayn Classical Matan Accent Box */}
                {ayah.jalalayn && (
                  <div className="bg-emerald-50/50 dark:bg-emerald-950/20 rounded-2xl p-4 border border-emerald-100 dark:border-emerald-900/30 text-xs sm:text-sm space-y-2">
                    <div className="flex items-center justify-between font-bold text-emerald-900 dark:text-emerald-300 text-xs font-bengali">
                      <span className="flex items-center gap-1.5">
                        <BookOpen className="w-3.5 h-3.5 text-emerald-600" />
                        <span>জালালাইনের মূল পাঠ ও ব্যাখ্যা সংক্ষেপ</span>
                      </span>
                      <span className="text-[10px] text-emerald-700/80 dark:text-emerald-400">ইমাম মাহাল্লী / সুয়ূতী</span>
                    </div>
                    <div className="prose text-gray-800 dark:text-gray-200 font-bengali text-xs sm:text-sm leading-relaxed max-h-48 overflow-y-auto">
                      <MarkdownContent content={ayah.jalalayn} />
                    </div>
                  </div>
                )}
              </div>

              {/* Left Column (LTR): Fluent Bengali Translation & Word Breakdown */}
              <div className="lg:col-span-5 space-y-4 order-2 lg:order-1">
                <div className="flex items-center justify-between text-xs font-bold text-gray-500 dark:text-gray-400 pb-1 border-b border-gray-100 dark:border-gray-700/50">
                  <span className="font-bengali text-emerald-800 dark:text-emerald-400 font-bold">সহজ ও প্রামাণিক বঙ্গানুবাদ</span>
                  <span className="text-[11px] font-mono text-gray-400">বাংলা</span>
                </div>

                {/* Fluent Bengali Translation */}
                <div 
                  className="text-gray-800 dark:text-gray-100 font-medium leading-relaxed font-bengali"
                  style={{ fontSize: `${bengaliFontSize}px` }}
                >
                  <span className="text-emerald-700 dark:text-emerald-400 font-bold mr-1.5">
                    ({toBn(ayah.ayah)})
                  </span>
                  {ayah.translation || "অনুবাদ প্রস্তুত করা হচ্ছে..."}
                </div>

                {/* Word-by-word Mufradat preview */}
                {ayah.word_translation && (
                  <div className="text-xs sm:text-sm text-gray-600 dark:text-gray-300 bg-gray-50 dark:bg-gray-700/40 p-3 rounded-xl border border-gray-100 dark:border-gray-700 space-y-1">
                    <span className="font-bold text-gray-800 dark:text-gray-200 block text-xs font-bengali">
                      শব্দানুগ অনুবাদ:
                    </span>
                    <div className="leading-relaxed font-bengali text-xs">
                      {ayah.word_translation}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ) : (
            /* Stacked View: Traditional vertical layering */
            <div className="space-y-4">
              {/* Arabic Uthmani Text */}
              <div 
                className="uthmani-text leading-loose text-gray-950 dark:text-gray-50 font-bold mb-3 selection:bg-emerald-100 dark:selection:bg-emerald-900/60"
                style={{ fontSize: `${arabicFontSize}px`, lineHeight: arabicLineHeight }}
              >
                {ayah.text_uthmani}
                <span className="ayah-end-symbol text-emerald-700 dark:text-emerald-400 text-[0.85em] font-normal mr-1.5 select-none">
                  ۝{toBn(ayah.ayah)}
                </span>
              </div>

              {/* Fluent Translation */}
              <div 
                className="text-gray-800 dark:text-gray-100 font-medium leading-relaxed pt-3 border-t border-gray-100 dark:border-gray-700/60 font-bengali"
                style={{ fontSize: `${bengaliFontSize}px` }}
              >
                <span className="text-emerald-700 dark:text-emerald-400 font-bold mr-1.5">({toBn(ayah.ayah)})</span>
                {ayah.translation || "অনুবাদ প্রস্তুত করা হচ্ছে..."}
              </div>

              {/* Word-by-word translation */}
              {ayah.word_translation && (
                <div className="mt-3 text-xs sm:text-sm text-gray-600 dark:text-gray-300 bg-gray-50 dark:bg-gray-700/40 p-3 rounded-xl border border-gray-100 dark:border-gray-700">
                  <span className="font-bold text-gray-800 dark:text-gray-200 block mb-1 text-xs">শব্দানুগ অর্থ:</span>
                  {ayah.word_translation}
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* 3. Layered Scholarly Analysis Tabs (শানে নুযূল, ব্যাকরণ, কিরাআত, জালালাইন) */}
      <div className="space-y-3">
        {/* Tab Selection Header */}
        <div className="flex items-center justify-between gap-2 overflow-x-auto no-scrollbar pb-1 border-b border-gray-200 dark:border-gray-700/60">
          <div className="flex items-center gap-1.5">
            {tabs.filter(t => t.available).map((t) => {
              const Icon = t.icon;
              const isActive = activeTab === t.id && !expandAll;
              return (
                <button
                  key={t.id}
                  onClick={() => {
                    setActiveTab(t.id);
                    setExpandAll(false);
                  }}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold whitespace-nowrap flex items-center gap-1.5 transition ${
                    isActive
                      ? 'bg-emerald-600 text-white shadow-xs'
                      : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 border border-gray-200 dark:border-gray-700'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{t.label}</span>
                  {t.count !== null && (
                    <span className={`text-[10px] px-1.5 py-0.2 rounded-full font-mono ${
                      isActive ? 'bg-white/20 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
                    }`}>
                      {toBn(t.count)}
                    </span>
                  )}
                </button>
              );
            })}
          </div>

          {/* Toggle All Chapters Expand/Collapse */}
          <button
            onClick={() => setExpandAll(!expandAll)}
            className="text-xs px-2.5 py-1.5 rounded-xl bg-gray-100 dark:bg-gray-700 hover:bg-emerald-50 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 font-semibold transition border border-gray-200 dark:border-gray-600 shrink-0"
          >
            {expandAll ? "ট্যাব ভিউতে ফিরুন" : "সব অধ্যায় একসাথে"}
          </button>
        </div>

        {/* Tab Content Display */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-4 sm:p-6 shadow-xs border border-gray-200 dark:border-gray-700 transition-colors">
          {/* TAB 1: Jalalayn */}
          {(expandAll || activeTab === 'jalalayn') && (
            <div className="space-y-3 mb-6 last:mb-0">
              <div className="flex items-center gap-2 pb-2 border-b border-gray-100 dark:border-gray-700 font-bold text-emerald-900 dark:text-emerald-300 text-sm sm:text-base">
                <BookOpen className="w-4 h-4 text-emerald-600" />
                <span>তাফসীরুল জালালাইন (ইবারত ও পূর্ণাঙ্গ ব্যাখ্যা)</span>
              </div>
              {ayah.jalalayn ? (
                <div className="prose font-bengali leading-relaxed text-gray-800 dark:text-gray-200">
                  <MarkdownContent content={ayah.jalalayn} />
                </div>
              ) : (
                <div className="text-gray-500 italic py-3 text-sm font-bengali">
                  এই আয়াতের জালালাইন তাফসীর সংকলনাধীন...
                </div>
              )}
            </div>
          )}

          {/* TAB 2: Mufradat & Tahqeeq */}
          {(expandAll || activeTab === 'mufradat') && ((ayah.tahqeeq && ayah.tahqeeq.length > 0) || (ayah.mufradat && ayah.mufradat.length > 0)) && (
            <div className="space-y-4 mb-6 last:mb-0">
              <div className="flex flex-wrap items-center justify-between gap-2 pb-2 border-b border-gray-100 dark:border-gray-700 font-bold text-blue-900 dark:text-blue-300 text-sm sm:text-base">
                <div className="flex items-center gap-2">
                  <Languages className="w-4 h-4 text-blue-600" />
                  <span>শব্দার্থ, সরফ ও শাব্দিক তাহকীক ({toBn(ayah.tahqeeq?.length || ayah.mufradat?.length)}টি শব্দ)</span>
                </div>
                {ayah.tahqeeq && ayah.tahqeeq.length > 0 && (
                  <span className="text-[10px] sm:text-xs font-semibold bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300 px-2.5 py-0.5 rounded-full border border-emerald-200 dark:border-emerald-800">
                    মুকাম্মাল লুগাতুল কুরআন মানদণ্ড
                  </span>
                )}
              </div>

              {ayah.tahqeeq && ayah.tahqeeq.length > 0 ? (
                /* Advanced Academic Tahqeeq Cards */
                <div className="space-y-3.5">
                  {ayah.tahqeeq.map((t, idx) => (
                    <div
                      key={idx}
                      className="bg-gray-50/80 dark:bg-gray-700/40 p-4 rounded-2xl border border-gray-200/90 dark:border-gray-600/80 text-xs sm:text-sm space-y-3"
                    >
                      {/* Top Bar: Word, Word Type Badge, Meaning */}
                      <div className="flex flex-wrap items-center justify-between gap-2 pb-2.5 border-b border-gray-200/80 dark:border-gray-600">
                        <div className="flex items-center gap-2.5">
                          <span className="font-amiri text-2xl font-bold text-emerald-900 dark:text-emerald-300" dir="rtl">
                            {t.word}
                          </span>
                          <span className="px-2 py-0.5 rounded-md text-[11px] font-bold bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 font-arabic">
                            {t.word_type}
                          </span>
                          {t.prefix_suffix_note && (
                            <span className="text-[11px] text-gray-500 dark:text-gray-400 font-bengali">
                              ({t.prefix_suffix_note})
                            </span>
                          )}
                        </div>
                        <div className="font-bold text-gray-800 dark:text-gray-100 font-bengali text-sm sm:text-base">
                          {t.meaning_bn}
                        </div>
                      </div>

                      {/* Middle Grid: Dars-e-Nizami Morphology Attributes */}
                      {t.morphology && (
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
                          {t.morphology.root && (
                            <div className="bg-white dark:bg-gray-800 p-2.5 rounded-xl border border-gray-100 dark:border-gray-700">
                              <span className="text-[10px] text-gray-400 block font-bengali">মূলবর্ণ (মাদ্দাহ):</span>
                              <span className="font-bold text-emerald-800 dark:text-emerald-300 font-mono text-sm">
                                {t.morphology.root}
                              </span>
                            </div>
                          )}
                          {t.morphology.jins && (
                            <div className="bg-white dark:bg-gray-800 p-2.5 rounded-xl border border-gray-100 dark:border-gray-700">
                              <span className="text-[10px] text-gray-400 block font-bengali">জিনস (সাত প্রকার):</span>
                              <span className="font-semibold text-gray-800 dark:text-gray-200 font-arabic text-xs">
                                {t.morphology.jins}
                              </span>
                            </div>
                          )}
                          {t.morphology.bab && (
                            <div className="bg-white dark:bg-gray-800 p-2.5 rounded-xl border border-gray-100 dark:border-gray-700">
                              <span className="text-[10px] text-gray-400 block font-bengali">বাব:</span>
                              <span className="font-semibold text-gray-800 dark:text-gray-200 font-arabic text-xs">
                                {t.morphology.bab}
                              </span>
                            </div>
                          )}
                          {t.morphology.sighah && (
                            <div className="bg-white dark:bg-gray-800 p-2.5 rounded-xl border border-gray-100 dark:border-gray-700">
                              <span className="text-[10px] text-gray-400 block font-bengali">সীগাহ ও বহছ:</span>
                              <span className="font-semibold text-gray-800 dark:text-gray-200 font-arabic text-xs">
                                {t.morphology.sighah} • {t.morphology.bahas}
                              </span>
                            </div>
                          )}
                          {t.morphology.masdar && (
                            <div className="bg-white dark:bg-gray-800 p-2.5 rounded-xl border border-gray-100 dark:border-gray-700 col-span-2">
                              <span className="text-[10px] text-gray-400 block font-bengali">মাসদার ও মৌলিক অর্থ:</span>
                              <span className="font-semibold text-gray-800 dark:text-gray-200 font-arabic">
                                {t.morphology.masdar}
                              </span>
                              <span className="text-gray-500 dark:text-gray-400 text-[11px] ml-1.5 font-bengali">
                                ({t.morphology.masdar_meaning})
                              </span>
                            </div>
                          )}
                          {t.morphology.singular_plural && (
                            <div className="bg-white dark:bg-gray-800 p-2.5 rounded-xl border border-gray-100 dark:border-gray-700 col-span-2">
                              <span className="text-[10px] text-gray-400 block font-bengali">বচন রূপ (মুফরাদ ও জমা):</span>
                              <span className="font-semibold text-gray-800 dark:text-gray-200 font-arabic">
                                {t.morphology.singular_plural}
                              </span>
                            </div>
                          )}
                        </div>
                      )}

                      {/* Taleel or Irab */}
                      {t.taleel_or_irab && (
                        <div className="bg-amber-50/70 dark:bg-amber-950/30 p-2.5 rounded-xl border border-amber-200/70 dark:border-amber-800/40 text-xs space-y-1">
                          <span className="font-bold text-amber-900 dark:text-amber-300 block font-bengali">
                            তালীল ও তারকীব / ই'রাব:
                          </span>
                          <p className="text-gray-800 dark:text-gray-200 leading-relaxed font-bengali">
                            {t.taleel_or_irab}
                          </p>
                        </div>
                      )}

                      {/* Lexical Depth */}
                      {t.lexical_depth_bn && (
                        <div className="bg-white dark:bg-gray-800 p-2.5 rounded-xl border border-gray-100 dark:border-gray-700 text-xs space-y-1">
                          <span className="font-bold text-emerald-800 dark:text-emerald-400 block font-bengali">
                            লুগাত ও ব্যুৎপত্তিগত তাৎপর্য:
                          </span>
                          <p className="text-gray-700 dark:text-gray-300 leading-relaxed font-bengali">
                            {t.lexical_depth_bn}
                          </p>
                        </div>
                      )}

                      {/* Classical Notes Accordion */}
                      {t.classical_notes && t.classical_notes.length > 0 && (
                        <div className="space-y-1.5 pt-1">
                          <span className="text-[11px] font-bold text-gray-500 dark:text-gray-400 block uppercase tracking-wide font-bengali">
                            ক্লাসিক্যাল ভাষাতাত্ত্বিক উদ্ধৃতি:
                          </span>
                          <div className="space-y-1.5">
                            {t.classical_notes.map((cn, cIdx) => (
                              <div
                                key={cIdx}
                                className="bg-blue-50/70 dark:bg-blue-950/30 p-3 rounded-xl border border-blue-100 dark:border-blue-900/40 text-xs"
                              >
                                <span className="font-bold text-blue-900 dark:text-blue-300 block font-bengali">
                                  📖 {cn.scholar_or_book}
                                </span>
                                <p className="text-gray-800 dark:text-gray-200 mt-1 leading-relaxed italic font-bengali">
                                  "{cn.note}"
                                </p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : ayah.mufradat && ayah.mufradat.length > 0 ? (
                /* Traditional Mufradat fallback */
                <div className="grid gap-3 sm:grid-cols-2">
                  {ayah.mufradat.map((m, idx) => (
                    <div key={idx} className="bg-gray-50 dark:bg-gray-700/40 p-3.5 rounded-xl border border-gray-200/80 dark:border-gray-600 text-xs sm:text-sm space-y-1.5">
                      <div className="flex items-center justify-between font-bold text-emerald-800 dark:text-emerald-300">
                        <span className="text-base font-amiri font-bold">{m['শব্দ'] || m['শব্দ (মূল)'] || 'শব্দ'}</span>
                        <span className="text-xs font-mono bg-emerald-100 dark:bg-emerald-900/60 px-2 py-0.5 rounded text-emerald-900 dark:text-emerald-200">
                          ধাতু: {m['মূলধাতু'] || '—'}
                        </span>
                      </div>
                      <div className="text-gray-600 dark:text-gray-300">
                        <span className="font-semibold text-gray-700 dark:text-gray-200">সীগা / ওযন:</span> {m['সীগা / ওযন'] || m['সীগা'] || '—'}
                      </div>
                      <div className="text-gray-700 dark:text-gray-300">
                        <span className="font-semibold text-gray-800 dark:text-gray-200">আভিধানিক অর্থ:</span> {m['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র'] || m['অর্থ'] || '—'}
                      </div>
                      {m['কুরআনিক পরিভাষাগত অর্থ'] && (
                        <div className="text-gray-700 dark:text-gray-300 text-xs bg-white dark:bg-gray-800 p-2 rounded-lg border border-gray-100 dark:border-gray-600">
                          <span className="font-bold text-emerald-700 dark:text-emerald-400">কুরআনিক তাৎপর্য:</span> {m['কুরআনিক পরিভাষাগত অর্থ']}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : null}
            </div>
          )}

          {/* TAB 3: Irab */}
          {(expandAll || activeTab === 'irab') && ayah.irab && (
            <div className="space-y-3 mb-6 last:mb-0">
              <div className="flex items-center gap-2 pb-2 border-b border-gray-100 dark:border-gray-700 font-bold text-purple-900 dark:text-purple-300 text-sm sm:text-base">
                <Compass className="w-4 h-4 text-purple-600" />
                <span>ই'রাব ও নাহবী তারকীব</span>
              </div>
              <div className="prose font-bengali leading-relaxed text-gray-800 dark:text-gray-200">
                <MarkdownContent content={ayah.irab} />
              </div>
            </div>
          )}

          {/* TAB 4: Qiraat */}
          {(expandAll || activeTab === 'qiraat') && ayah.qiraat && ayah.qiraat.length > 0 && (
            <div className="space-y-3 mb-6 last:mb-0">
              <div className="flex items-center gap-2 pb-2 border-b border-gray-100 dark:border-gray-700 font-bold text-amber-900 dark:text-amber-300 text-sm sm:text-base">
                <Volume2 className="w-4 h-4 text-amber-600" />
                <span>১০ মুতাওয়াতির কিরাআত পাঠভেদ ({toBn(ayah.qiraat.length)}টি বর্ণনা — বাহাউথ প্রামাণ্য সারণি)</span>
              </div>
              <div className="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700">
                <table className="w-full text-xs sm:text-sm border-collapse">
                  <thead className="bg-amber-50/70 dark:bg-gray-700/80 text-gray-700 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600">
                    <tr>
                      <th className="px-3 py-2 text-left font-bold">শব্দ (ক্রম)</th>
                      <th className="px-3 py-2 text-left font-bold">ক্বারী / রাবী</th>
                      <th className="px-3 py-2 text-left font-bold">নিয়ম ও বিশুদ্ধ পাঠ</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100 dark:divide-gray-700 bg-white dark:bg-gray-800">
                    {ayah.qiraat.map((q, qIdx) => (
                      <tr key={qIdx} className="hover:bg-amber-50/40 dark:hover:bg-gray-700/30">
                        <td className="px-3 py-2 font-arabic text-right whitespace-nowrap" dir="rtl">
                          <MarkdownContent inline content={q['শব্দ (ক্রম)'] || q['শব্দ'] || ''} />
                        </td>
                        <td className="px-3 py-2 font-medium font-arabic text-right whitespace-nowrap" dir="rtl">
                          <MarkdownContent inline content={q['ক্বারী / রাবী (বাহাউথ)'] || q['ক্বারী'] || ''} />
                        </td>
                        <td className="px-3 py-2 font-arabic text-right leading-relaxed" dir="rtl">
                          <MarkdownContent inline content={q['কিরাআতের পাঠভেদ ও নিয়ম (অবিকৃত মূল পাঠ)'] || q['নিয়ম'] || ''} />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* TAB 5: Shan-e-Nuzul */}
          {(expandAll || activeTab === 'nuzul') && ayah.nuzul && (
            <div className="space-y-3 mb-6 last:mb-0">
              <div className="flex items-center gap-2 pb-2 border-b border-gray-100 dark:border-gray-700 font-bold text-teal-900 dark:text-teal-300 text-sm sm:text-base">
                <Sparkles className="w-4 h-4 text-teal-600" />
                <span>শানে নুযূল ও সংশ্লিষ্ট হাদীসের তাখরীজ</span>
              </div>
              <div className="prose font-bengali leading-relaxed text-gray-800 dark:text-gray-200">
                <MarkdownContent content={ayah.nuzul} />
              </div>
            </div>
          )}

          {/* TAB 6: Notes */}
          {(expandAll || activeTab === 'notes') && (
            <div className="space-y-3 mb-6 last:mb-0">
              <div className="flex items-center justify-between pb-2 border-b border-gray-100 dark:border-gray-700">
                <span className="flex items-center gap-2 font-bold text-gray-900 dark:text-gray-100 text-sm sm:text-base">
                  <FileText className="w-4 h-4 text-emerald-600" />
                  <span>ব্যক্তিগত ক্লাস নোট ও তাহকীকী মন্তব্য</span>
                </span>
                {noteSavedMsg && (
                  <span className="text-xs text-emerald-600 font-bold animate-in fade-in">
                    ✓ নোট সংরক্ষিত হয়েছে
                  </span>
                )}
              </div>

              <textarea
                value={noteText}
                onChange={(e) => setNoteText(e.target.value)}
                placeholder="এই আয়াত সম্পর্কিত আপনার ব্যক্তিগত নোট, ক্লাসের সারসংক্ষেপ বা প্রশ্ন এখানে লিখুন..."
                rows={4}
                className="w-full p-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-gray-100 text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 font-bengali"
              />

              <div className="flex flex-wrap items-center justify-between gap-2">
                {/* Tags */}
                <div className="flex flex-wrap items-center gap-1.5">
                  {noteTags.map((t, idx) => (
                    <span 
                      key={idx} 
                      className="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full bg-emerald-50 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800"
                    >
                      #{t}
                      <button onClick={() => handleRemoveTag(t)} className="hover:text-red-500">×</button>
                    </span>
                  ))}
                  <input
                    type="text"
                    value={newTag}
                    onChange={(e) => setNewTag(e.target.value)}
                    onKeyDown={handleAddTag}
                    placeholder="+ ট্যাগ দিন (Enter)"
                    className="text-xs px-2 py-0.5 rounded-lg border border-dashed border-gray-300 dark:border-gray-600 bg-transparent text-gray-600 dark:text-gray-300 w-28"
                  />
                </div>

                <button
                  onClick={handleSaveNote}
                  className="px-4 py-1.5 rounded-xl bg-emerald-600 text-white font-bold text-xs hover:bg-emerald-700 transition shadow-xs"
                >
                  নোট সেভ করুন
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

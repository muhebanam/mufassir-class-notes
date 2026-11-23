import React, { useState, useEffect } from 'react';
import { 
  BookOpen, ChevronDown, ChevronUp, Copy, Check, Bookmark, 
  BookmarkCheck, Sparkles, Languages, Compass, Volume2, 
  FileText, Tag, ArrowLeft, ArrowRight, Share2 
} from 'lucide-react';
import { toBn, copyToClipboard } from '../utils/helpers';
import MarkdownContent from './MarkdownContent';
import { saveAyahNote, getAyahNote, toggleBookmark, isBookmarked } from '../utils/db';

export default function AyahStudyView({
  ayah,
  surahInfo,
  rukuInfo,
  onPrevAyah,
  onNextAyah,
  arabicFontSize = 28,
  bengaliFontSize = 16,
  arabicLineHeight = 2.2
}) {
  const [copied, setCopied] = useState(false);
  const [bookmarked, setBookmarked] = useState(false);
  
  // Accordion drawer states - all open by default so no research text is hidden on mobile
  const [openDrawers, setOpenDrawers] = useState({
    jalalayn: true,
    mufradat: true,
    irab: true,
    qiraat: true,
    nuzul: true,
    notes: true
  });

  const areAllDrawersOpen = Object.values(openDrawers).every(Boolean);

  const toggleAllDrawers = () => {
    const nextState = !areAllDrawersOpen;
    setOpenDrawers({
      jalalayn: nextState,
      mufradat: nextState,
      irab: nextState,
      qiraat: nextState,
      nuzul: nextState,
      notes: nextState
    });
  };

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

  const toggleDrawer = (key) => {
    setOpenDrawers(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const handleCopyAyah = async () => {
    const textToCopy = `${ayah.text_uthmani} [সূরা ${surahInfo?.name_bn || ayah.surah}:${toBn(ayah.ayah)}]\n${ayah.translation}`;
    const success = await copyToClipboard(textToCopy);
    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
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

  return (
    <div className="max-w-4xl mx-auto px-3 sm:px-4 py-4 space-y-4">
      {/* Top Breadcrumb & Quick Actions */}
      <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 pb-2 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-1 font-semibold">
          <span>সূরা {surahInfo?.name_bn} ({toBn(ayah.surah)})</span>
          <span>•</span>
          <span>রুকু {toBn(ayah.ruku)}</span>
          <span>•</span>
          <span className="text-emerald-700 dark:text-emerald-400 font-bold">আয়াত {toBn(ayah.ayah)}</span>
        </div>

        <div className="flex items-center gap-1.5">
          <button
            onClick={handleCopyAyah}
            className="flex items-center gap-1 px-2 py-1 rounded bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition"
            title="আয়াত ও অনুবাদ কপি করুন"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? "কপি হয়েছে" : "কপি"}</span>
          </button>

          <button
            onClick={handleToggleBookmark}
            className={`flex items-center gap-1 px-2 py-1 rounded transition ${
              bookmarked 
                ? 'bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 font-bold' 
                : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'
            }`}
            title="বুকমার্ক সংরক্ষণ"
          >
            {bookmarked ? <BookmarkCheck className="w-3.5 h-3.5 text-amber-600" /> : <Bookmark className="w-3.5 h-3.5" />}
            <span>{bookmarked ? "চিহ্নিত" : "বুকমার্ক"}</span>
          </button>
        </div>
      </div>

      {/* Main Quran Verse Card */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl p-4 sm:p-6 shadow-sm border border-gray-200 dark:border-gray-700 transition-colors">
        {/* Arabic Uthmani Text */}
        <div 
          className="uthmani-text leading-loose text-gray-900 dark:text-gray-50 mb-4 selection:bg-emerald-200 dark:selection:bg-emerald-900"
          style={{ fontSize: `${arabicFontSize}px`, lineHeight: arabicLineHeight }}
        >
          {ayah.text_uthmani}
          <span className="ayah-end-symbol text-emerald-600 dark:text-emerald-400 text-[0.85em] font-normal mr-1">
            ۝{toBn(ayah.ayah)}
          </span>
        </div>

        {/* Fluent Translation */}
        <div 
          className="text-gray-800 dark:text-gray-200 font-medium leading-relaxed pt-3 border-t border-gray-100 dark:border-gray-700/60"
          style={{ fontSize: `${bengaliFontSize}px` }}
        >
          <span className="text-emerald-700 dark:text-emerald-400 font-bold mr-1">({toBn(ayah.ayah)})</span>
          {ayah.translation || "অনুবাদ প্রস্তুত করা হচ্ছে..."}
        </div>

        {/* Word-by-word translation if available */}
        {ayah.word_translation && (
          <div className="mt-3 text-xs sm:text-sm text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-700/40 p-3 rounded-xl border border-gray-100 dark:border-gray-700">
            <span className="font-bold text-gray-700 dark:text-gray-300 block mb-1">শব্দানুগ অর্থ:</span>
            {ayah.word_translation}
          </div>
        )}
      </div>

      {/* Section Drawers (Accordions) */}
      <div className="flex items-center justify-between px-1 pt-1 pb-0.5">
        <span className="text-xs sm:text-sm font-bold text-gray-700 dark:text-gray-300 font-bengali">
          তাহকীক ও শাস্ত্রীয় বিশ্লেষণ (সব শাখা দৃশ্যমান):
        </span>
        <button
          onClick={toggleAllDrawers}
          className="text-xs px-2.5 py-1 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-emerald-50 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 font-semibold transition border border-gray-200 dark:border-gray-600 shadow-2xs"
        >
          {areAllDrawersOpen ? "সবগুলো সংক্ষেপ করুন" : "সবগুলো উন্মুক্ত করুন"}
        </button>
      </div>

      <div className="space-y-3">
        {/* 1. Tafsir al-Jalalayn Drawer */}
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden shadow-sm transition">
          <button
            onClick={() => toggleDrawer('jalalayn')}
            className="w-full px-4 py-3 bg-emerald-50/60 dark:bg-emerald-950/30 flex items-center justify-between text-left hover:bg-emerald-100/50 dark:hover:bg-emerald-900/40 transition"
          >
            <div className="flex items-center gap-2 text-emerald-900 dark:text-emerald-300 font-bold text-sm sm:text-base">
              <BookOpen className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              <span>তাফসীরুল জালালাইন (মূল ইবারত ও বঙ্গানুবাদ)</span>
            </div>
            {openDrawers.jalalayn ? <ChevronUp className="w-4 h-4 text-emerald-700" /> : <ChevronDown className="w-4 h-4 text-emerald-700" />}
          </button>

          {openDrawers.jalalayn && (
            <div className="p-4 sm:p-5 border-t border-gray-100 dark:border-gray-700">
              {ayah.jalalayn ? (
                <MarkdownContent content={ayah.jalalayn} />
              ) : (
                <div className="text-gray-500 italic py-2 font-bengali">
                  এই আয়াতের জালালাইন তাফসীর অন্তর্ভুক্ত করা হচ্ছে...
                </div>
              )}
            </div>
          )}
        </div>

        {/* 2. Mufradat (Word Analysis) Drawer */}
        {ayah.mufradat && ayah.mufradat.length > 0 && (
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden shadow-sm transition">
            <button
              onClick={() => toggleDrawer('mufradat')}
              className="w-full px-4 py-3 bg-blue-50/60 dark:bg-blue-950/30 flex items-center justify-between text-left hover:bg-blue-100/50 dark:hover:bg-blue-900/40 transition"
            >
              <div className="flex items-center gap-2 text-blue-900 dark:text-blue-300 font-bold text-sm sm:text-base">
                <Languages className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                <span>শব্দার্থ, সরফ ও মুফরাদাত ({toBn(ayah.mufradat.length)}টি শব্দ)</span>
              </div>
              {openDrawers.mufradat ? <ChevronUp className="w-4 h-4 text-blue-700" /> : <ChevronDown className="w-4 h-4 text-blue-700" />}
            </button>

            {openDrawers.mufradat && (
              <div className="p-3 sm:p-4 border-t border-gray-100 dark:border-gray-700 overflow-x-auto">
                <div className="grid gap-3 sm:grid-cols-2">
                  {ayah.mufradat.map((m, idx) => (
                    <div key={idx} className="bg-gray-50 dark:bg-gray-700/40 p-3 rounded-lg border border-gray-200 dark:border-gray-600 text-xs sm:text-sm space-y-1">
                      <div className="flex items-center justify-between font-bold text-emerald-800 dark:text-emerald-300">
                        <span className="text-base font-amiri">{m['শব্দ'] || m['শব্দ (মূল)'] || 'শব্দ'}</span>
                        <span className="text-xs font-mono bg-emerald-100 dark:bg-emerald-900 px-1.5 py-0.5 rounded text-emerald-900 dark:text-emerald-200">
                          {m['মূলধাতু'] || ''}
                        </span>
                      </div>
                      <div className="text-gray-600 dark:text-gray-300">
                        <span className="font-semibold text-gray-700 dark:text-gray-200">সীগা/ওযন:</span> {m['সীগা / ওযন'] || m['সীগা'] || '—'}
                      </div>
                      <div className="text-gray-700 dark:text-gray-300">
                        <span className="font-semibold text-gray-800 dark:text-gray-200">অর্থ ও ব্যুৎপত্তি:</span> {m['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র'] || m['অর্থ'] || '—'}
                      </div>
                      {m['কুরআনিক পরিভাষাগত অর্থ'] && (
                        <div className="text-gray-700 dark:text-gray-300 text-[11px] sm:text-xs bg-white dark:bg-gray-800 p-2 rounded border border-gray-100 dark:border-gray-600">
                          <span className="font-bold text-emerald-700 dark:text-emerald-400">কুরআনিক পরিভাষা:</span> {m['কুরআনিক পরিভাষাগত অর্থ']}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* 3. Irab Drawer */}
        {ayah.irab && (
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden shadow-sm transition">
            <button
              onClick={() => toggleDrawer('irab')}
              className="w-full px-4 py-3 bg-purple-50/60 dark:bg-purple-950/30 flex items-center justify-between text-left hover:bg-purple-100/50 dark:hover:bg-purple-900/40 transition"
            >
              <div className="flex items-center gap-2 text-purple-900 dark:text-purple-300 font-bold text-sm sm:text-base">
                <Compass className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                <span>ই'রাব ও নাহবী তারকীব</span>
              </div>
              {openDrawers.irab ? <ChevronUp className="w-4 h-4 text-purple-700" /> : <ChevronDown className="w-4 h-4 text-purple-700" />}
            </button>

            {openDrawers.irab && (
              <div className="p-4 sm:p-5 border-t border-gray-100 dark:border-gray-700">
                <MarkdownContent content={ayah.irab} />
              </div>
            )}
          </div>
        )}

        {/* 4. Qiraat Drawer */}
        {ayah.qiraat && ayah.qiraat.length > 0 && (
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden shadow-sm transition">
            <button
              onClick={() => toggleDrawer('qiraat')}
              className="w-full px-4 py-3 bg-amber-50/60 dark:bg-amber-950/30 flex items-center justify-between text-left hover:bg-amber-100/50 dark:hover:bg-amber-900/40 transition"
            >
              <div className="flex items-center gap-2 text-amber-900 dark:text-amber-300 font-bold text-sm sm:text-base">
                <Volume2 className="w-4 h-4 text-amber-600 dark:text-amber-400" />
                <span>১০ মুতাওয়াতির কিরাআত পাঠভেদ ({toBn(ayah.qiraat.length)}টি বর্ণনা)</span>
              </div>
              {openDrawers.qiraat ? <ChevronUp className="w-4 h-4 text-amber-700" /> : <ChevronDown className="w-4 h-4 text-amber-700" />}
            </button>

            {openDrawers.qiraat && (
              <div className="p-3 sm:p-4 border-t border-gray-100 dark:border-gray-700 overflow-x-auto">
                <div className="space-y-2">
                  {ayah.qiraat.map((q, idx) => (
                    <div key={idx} className="bg-gray-50 dark:bg-gray-700/50 p-2.5 rounded-lg border border-gray-200 dark:border-gray-600 text-xs sm:text-sm">
                      <div className="flex items-center justify-between font-bold text-amber-800 dark:text-amber-300 mb-1">
                        <span>{q['ক্বারী / রাবী'] || q['ক্বারী'] || 'ক্বারী'}</span>
                        <span className="font-amiri text-sm">{q['শব্দ (ক্রম)'] || q['শব্দ'] || ''}</span>
                      </div>
                      <div className="text-gray-700 dark:text-gray-300 text-xs">
                        {q['কিরাআতের পাঠভেদ ও নিয়ম (অবিকৃত মূল পাঠ)'] || q['পাঠভেদ'] || '—'}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* 5. Shan-e-Nuzul & Hadith Drawer */}
        {ayah.shane_nuzul && (
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden shadow-sm transition">
            <button
              onClick={() => toggleDrawer('nuzul')}
              className="w-full px-4 py-3 bg-teal-50/60 dark:bg-teal-950/30 flex items-center justify-between text-left hover:bg-teal-100/50 dark:hover:bg-teal-900/40 transition"
            >
              <div className="flex items-center gap-2 text-teal-900 dark:text-teal-300 font-bold text-sm sm:text-base">
                <Sparkles className="w-4 h-4 text-teal-600 dark:text-teal-400" />
                <span>শানে নুযূল ও সংশ্লিষ্ট হাদীস</span>
              </div>
              {openDrawers.nuzul ? <ChevronUp className="w-4 h-4 text-teal-700" /> : <ChevronDown className="w-4 h-4 text-teal-700" />}
            </button>

            {openDrawers.nuzul && (
              <div className="p-4 sm:p-5 border-t border-gray-100 dark:border-gray-700">
                <MarkdownContent content={ayah.shane_nuzul} />
              </div>
            )}
          </div>
        )}

        {/* 6. Teacher's Lecture Notes Box */}
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden shadow-sm transition">
          <button
            onClick={() => toggleDrawer('notes')}
            className="w-full px-4 py-3 bg-amber-50/40 dark:bg-amber-950/20 flex items-center justify-between text-left hover:bg-amber-100/40 dark:hover:bg-amber-900/30 transition"
          >
            <div className="flex items-center gap-2 text-amber-950 dark:text-amber-200 font-bold text-sm sm:text-base">
              <FileText className="w-4 h-4 text-amber-600 dark:text-amber-400" />
              <span>আমার ক্লাস নোট (অফলাইন সংরক্ষিত)</span>
            </div>
            {openDrawers.notes ? <ChevronUp className="w-4 h-4 text-amber-700" /> : <ChevronDown className="w-4 h-4 text-amber-700" />}
          </button>

          {openDrawers.notes && (
            <div className="p-4 border-t border-gray-100 dark:border-gray-700 space-y-3">
              <textarea
                value={noteText}
                onChange={(e) => setNoteText(e.target.value)}
                onBlur={handleSaveNote}
                placeholder="ক্লাসে দরস দেওয়ার সময় গুরুত্বপূর্ণ পয়েন্ট, প্রশ্ন বা ব্যাখ্যা এখানে লিখে রাখুন (স্বয়ংক্রিয়ভাবে সংরক্ষিত হবে)..."
                rows={3}
                className="w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />

              {/* Tag Chips */}
              <div className="flex flex-wrap items-center gap-1.5">
                {noteTags.map((tag, i) => (
                  <span
                    key={i}
                    className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-200"
                  >
                    <span>#{tag}</span>
                    <button
                      onClick={() => handleRemoveTag(tag)}
                      className="hover:text-red-600 transition"
                    >
                      &times;
                    </button>
                  </span>
                ))}
                
                <input
                  type="text"
                  value={newTag}
                  onChange={(e) => setNewTag(e.target.value)}
                  onKeyDown={handleAddTag}
                  placeholder="+ ট্যাগ যোগ করুন (Enter)"
                  className="text-xs px-2 py-1 rounded border border-gray-200 dark:border-gray-600 bg-transparent focus:outline-none focus:ring-1 focus:ring-emerald-500"
                />
              </div>

              <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 pt-1">
                <span>নোট আপনার ফোনের মেমোরিতে (IndexedDB) সংরক্ষিত থাকে।</span>
                {noteSavedMsg && (
                  <span className="text-emerald-600 dark:text-emerald-400 font-bold flex items-center gap-1">
                    <Check className="w-3.5 h-3.5" /> সংরক্ষিত হয়েছে!
                  </span>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Navigation Buttons */}
      <div className="flex items-center justify-between pt-4 pb-8">
        <button
          onClick={onPrevAyah}
          disabled={ayah.ayah <= (rukuInfo?.ayah_start || 1)}
          className={`flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition ${
            ayah.ayah <= (rukuInfo?.ayah_start || 1)
              ? 'opacity-40 cursor-not-allowed bg-gray-100 dark:bg-gray-800 text-gray-400'
              : 'bg-white dark:bg-gray-800 hover:bg-emerald-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 border border-gray-200 dark:border-gray-700 shadow-sm'
          }`}
        >
          <ArrowLeft className="w-4 h-4" />
          <span>পূর্ববর্তী আয়াত</span>
        </button>

        <span className="text-xs font-bold text-gray-500 dark:text-gray-400">
          আয়াত {toBn(ayah.ayah)} / {toBn(rukuInfo?.ayah_end || ayah.ayah)}
        </span>

        <button
          onClick={onNextAyah}
          disabled={ayah.ayah >= (rukuInfo?.ayah_end || 64)}
          className={`flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition ${
            ayah.ayah >= (rukuInfo?.ayah_end || 64)
              ? 'opacity-40 cursor-not-allowed bg-gray-100 dark:bg-gray-800 text-gray-400'
              : 'bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm'
          }`}
        >
          <span>পরবর্তী আয়াত</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}

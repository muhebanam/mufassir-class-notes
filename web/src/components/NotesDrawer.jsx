import React, { useState, useEffect } from 'react';
import { 
  X, FileText, Download, Upload, Trash2, Tag, 
  ExternalLink, Bookmark, Check, AlertCircle, Edit3, Save
} from 'lucide-react';
import { 
  getAllNotes, getAllBookmarks, deleteNote, saveAyahNote,
  exportBackupJson, exportNotesMarkdown, importBackupJson 
} from '../utils/db';
import { toBn } from '../utils/helpers';

export default function NotesDrawer({ isOpen, onClose, onSelectAyahFromNote }) {
  const [activeTab, setActiveTab] = useState('notes'); // 'notes' or 'bookmarks'
  const [notes, setNotes] = useState([]);
  const [bookmarks, setBookmarks] = useState([]);
  const [statusMsg, setStatusMsg] = useState("");

  // Inline editing state
  const [editingNoteId, setEditingNoteId] = useState(null);
  const [editDraftText, setEditDraftText] = useState("");

  const refreshData = async () => {
    const allN = await getAllNotes();
    const allB = await getAllBookmarks();
    setNotes(allN);
    setBookmarks(allB);
  };

  useEffect(() => {
    if (isOpen) {
      refreshData();
      setEditingNoteId(null);
    }
  }, [isOpen]);

  const handleDeleteNote = async (id) => {
    if (window.confirm("আপনি কি নিশ্চিতভাবে এই ক্লাস নোটটি মুছে ফেলতে চান?")) {
      await deleteNote(id);
      refreshData();
    }
  };

  const handleStartEdit = (note) => {
    setEditingNoteId(note.id);
    setEditDraftText(note.text || "");
  };

  const handleSaveEdit = async (note) => {
    if (!editDraftText.trim()) return;
    await saveAyahNote(note.surah, note.ayah, editDraftText.trim(), note.tags || []);
    setEditingNoteId(null);
    setStatusMsg("নোট সফলভাবে সংরক্ষণ করা হয়েছে!");
    refreshData();
    setTimeout(() => setStatusMsg(""), 3000);
  };

  const handleImport = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try {
      await importBackupJson(file);
      setStatusMsg("ব্যাকআপ সফলভাবে পুনরুদ্ধার করা হয়েছে!");
      refreshData();
      setTimeout(() => setStatusMsg(""), 3000);
    } catch (err) {
      alert("ব্যাকআপ ফাইল পড়তে ত্রুটি হয়েছে। সঠিক JSON ফাইল নির্বাচন করুন।");
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex justify-end animate-in fade-in duration-200">
      <div className="bg-white dark:bg-gray-800 w-full max-w-md h-full shadow-2xl flex flex-col border-l border-gray-200 dark:border-gray-700">
        {/* Drawer Header */}
        <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            <h2 className="font-bold text-base sm:text-lg text-gray-900 dark:text-gray-100">
              ব্যক্তিগত ক্লাস নোট ও বুকমার্ক
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-full text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Buttons */}
        <div className="grid grid-cols-2 p-2 bg-gray-50 dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 text-xs font-semibold">
          <button
            onClick={() => { setActiveTab('notes'); setEditingNoteId(null); }}
            className={`py-2 rounded-lg transition ${
              activeTab === 'notes'
                ? 'bg-white dark:bg-gray-800 text-emerald-700 dark:text-emerald-400 shadow-xs'
                : 'text-gray-600 dark:text-gray-400'
            }`}
          >
            নোটসমূহ ({toBn(notes.length)})
          </button>
          <button
            onClick={() => { setActiveTab('bookmarks'); setEditingNoteId(null); }}
            className={`py-2 rounded-lg transition ${
              activeTab === 'bookmarks'
                ? 'bg-white dark:bg-gray-800 text-emerald-700 dark:text-emerald-400 shadow-xs'
                : 'text-gray-600 dark:text-gray-400'
            }`}
          >
            বুকমার্ক ({toBn(bookmarks.length)})
          </button>
        </div>

        {statusMsg && (
          <div className="p-2.5 mx-3 mt-2 bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-200 text-xs rounded-lg flex items-center gap-1.5 font-bold">
            <Check className="w-4 h-4 text-emerald-600" />
            <span>{statusMsg}</span>
          </div>
        )}

        {/* Content List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {activeTab === 'notes' ? (
            notes.length === 0 ? (
              <div className="text-center py-12 text-gray-400 text-xs space-y-2">
                <FileText className="w-8 h-8 mx-auto opacity-40" />
                <p>এখনো কোনো ক্লাস নোট লেখা হয়নি।</p>
                <p className="text-[11px]">যেকোনো আয়াত খুলে "আমার ক্লাস নোট" বক্সে লিখলেই তা এখানে জমা হবে।</p>
              </div>
            ) : (
              notes.map((n) => (
                <div
                  key={n.id}
                  className="bg-gray-50 dark:bg-gray-700/50 p-3 rounded-xl border border-gray-200 dark:border-gray-600 text-xs space-y-2"
                >
                  <div className="flex items-center justify-between font-bold text-emerald-800 dark:text-emerald-300">
                    <span>সূরা {toBn(n.surah)}, আয়াত {toBn(n.ayah)}</span>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleStartEdit(n)}
                        className="text-gray-500 hover:text-emerald-600 transition"
                        title="নোট সম্পাদনা করুন"
                      >
                        <Edit3 className="w-3.5 h-3.5" />
                      </button>
                      <button
                        onClick={() => {
                          onSelectAyahFromNote(n.surah, n.ruku, n.ayah);
                          onClose();
                        }}
                        className="text-gray-500 hover:text-emerald-600 transition"
                        title="এই আয়াতে যান"
                      >
                        <ExternalLink className="w-3.5 h-3.5" />
                      </button>
                      <button
                        onClick={() => handleDeleteNote(n.id)}
                        className="text-gray-400 hover:text-red-600 transition"
                        title="নোট মুছুন"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>

                  {editingNoteId === n.id ? (
                    <div className="space-y-2 pt-1">
                      <textarea
                        rows={3}
                        value={editDraftText}
                        onChange={(e) => setEditDraftText(e.target.value)}
                        className="w-full p-2 text-xs bg-white dark:bg-gray-800 border border-emerald-500 rounded-lg focus:outline-hidden text-gray-800 dark:text-gray-200"
                        placeholder="নোট লিখুন..."
                      />
                      <div className="flex justify-end gap-1.5">
                        <button
                          onClick={() => setEditingNoteId(null)}
                          className="px-2.5 py-1 text-[11px] rounded bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300"
                        >
                          বাতিল
                        </button>
                        <button
                          onClick={() => handleSaveEdit(n)}
                          className="px-2.5 py-1 text-[11px] rounded bg-emerald-600 text-white font-semibold flex items-center gap-1"
                        >
                          <Save className="w-3 h-3" /> সংরক্ষণ
                        </button>
                      </div>
                    </div>
                  ) : (
                    <p className="text-gray-800 dark:text-gray-200 whitespace-pre-wrap leading-relaxed">
                      {n.text}
                    </p>
                  )}

                  {n.tags && n.tags.length > 0 && (
                    <div className="flex flex-wrap gap-1 pt-1">
                      {n.tags.map((t, i) => (
                        <span key={i} className="px-1.5 py-0.5 rounded bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 text-[10px]">
                          #{t}
                        </span>
                      ))}
                    </div>
                  )}

                  <div className="text-[10px] text-gray-400 pt-1">
                    হালনাগাদ: {new Date(n.updatedAt).toLocaleDateString('bn-BD')}
                  </div>
                </div>
              ))
            )
          ) : bookmarks.length === 0 ? (
            <div className="text-center py-12 text-gray-400 text-xs space-y-2">
              <Bookmark className="w-8 h-8 mx-auto opacity-40" />
              <p>কোনো আয়াত বুকমার্ক করা হয়নি।</p>
            </div>
          ) : (
            bookmarks.map((b) => (
              <div
                key={b.id}
                onClick={() => {
                  onSelectAyahFromNote(b.surah, b.ruku, b.ayah);
                  onClose();
                }}
                className="bg-gray-50 dark:bg-gray-700/50 p-3 rounded-xl border border-gray-200 dark:border-gray-600 text-xs flex items-center justify-between cursor-pointer hover:border-emerald-500 transition"
              >
                <div>
                  <div className="font-bold text-gray-900 dark:text-gray-100">
                    সূরা {toBn(b.surah)}: আয়াত {toBn(b.ayah)}
                  </div>
                  <div className="text-[10px] text-gray-400 mt-0.5">
                    রুকু {toBn(b.ruku)}
                  </div>
                </div>
                <ExternalLink className="w-4 h-4 text-emerald-600" />
              </div>
            ))
          )}
        </div>

        {/* 1-Click Backup Export / Import Footer */}
        <div className="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 space-y-2">
          <div className="text-xs font-bold text-gray-700 dark:text-gray-300">
            ক্লাস নোট ব্যাকআপ ও রিস্টোর
          </div>
          <div className="grid grid-cols-2 gap-2">
            <button
              onClick={exportBackupJson}
              className="py-2 px-3 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-xs font-semibold text-gray-700 dark:text-gray-200 hover:bg-gray-100 transition flex items-center justify-center gap-1.5"
            >
              <Download className="w-3.5 h-3.5 text-emerald-600" />
              <span>JSON ব্যাকআপ</span>
            </button>

            <button
              onClick={exportNotesMarkdown}
              className="py-2 px-3 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-xs font-semibold text-gray-700 dark:text-gray-200 hover:bg-gray-100 transition flex items-center justify-center gap-1.5"
            >
              <FileText className="w-3.5 h-3.5 text-amber-600" />
              <span>Markdown এক্সপোর্ট</span>
            </button>
          </div>

          <label className="w-full py-2 px-3 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 text-xs font-semibold text-emerald-800 dark:text-emerald-300 hover:bg-emerald-100 transition flex items-center justify-center gap-1.5 cursor-pointer">
            <Upload className="w-3.5 h-3.5" />
            <span>JSON ব্যাকআপ ফাইল থেকে রিস্টোর</span>
            <input type="file" accept=".json" onChange={handleImport} className="hidden" />
          </label>
        </div>
      </div>
    </div>
  );
}

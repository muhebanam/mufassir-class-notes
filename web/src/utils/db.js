import Dexie from 'dexie';

export const db = new Dexie('MufassirClassNotesDB');

db.version(1).stores({
  notes: '++id, surah, ayah, ruku, updatedAt',
  bookmarks: '++id, surah, ayah, ruku, createdAt'
});

// Save or update an ayah note
export async function saveAyahNote(surah, ayah, ruku, text, tags = []) {
  const existing = await db.notes.where({ surah, ayah }).first();
  const now = new Date().toISOString();
  if (existing) {
    if (!text.trim()) {
      await db.notes.delete(existing.id);
      return null;
    }
    await db.notes.update(existing.id, { text, tags, updatedAt: now });
    return { ...existing, text, tags, updatedAt: now };
  } else if (text.trim()) {
    const id = await db.notes.add({ surah, ayah, ruku, text, tags, updatedAt: now });
    return { id, surah, ayah, ruku, text, tags, updatedAt: now };
  }
  return null;
}

// Get note for a specific ayah
export async function getAyahNote(surah, ayah) {
  return await db.notes.where({ surah, ayah }).first();
}

// Get all notes
export async function getAllNotes() {
  return await db.notes.orderBy('updatedAt').reverse().toArray();
}

// Delete a note
export async function deleteNote(id) {
  await db.notes.delete(id);
}

// Toggle bookmark
export async function toggleBookmark(surah, ayah, ruku, label = '') {
  const existing = await db.bookmarks.where({ surah, ayah }).first();
  if (existing) {
    await db.bookmarks.delete(existing.id);
    return false;
  } else {
    await db.bookmarks.add({ surah, ayah, ruku, label, createdAt: new Date().toISOString() });
    return true;
  }
}

// Check bookmark
export async function isBookmarked(surah, ayah) {
  const count = await db.bookmarks.where({ surah, ayah }).count();
  return count > 0;
}

// Get all bookmarks
export async function getAllBookmarks() {
  return await db.bookmarks.orderBy('createdAt').reverse().toArray();
}

// 1-Click JSON Export
export async function exportBackupJson() {
  const notes = await db.notes.toArray();
  const bookmarks = await db.bookmarks.toArray();
  const data = {
    app: "Mufassir Class Notes",
    version: "1.0",
    exportDate: new Date().toISOString(),
    notes,
    bookmarks
  };
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `mufassir_class_notes_backup_${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

// 1-Click Markdown Export for class notes
export async function exportNotesMarkdown() {
  const notes = await db.notes.toArray();
  let md = `# মুফাস্সির ক্লাস নোট — সংগৃহীত ব্যক্তিগত নোটসমূহ\n\n`;
  md += `> ব্যাকআপ তারিখ: ${new Date().toLocaleDateString('bn-BD')}\n\n---\n\n`;
  for (const n of notes) {
    md += `### সূরা ${n.surah}, রুকু ${n.ruku}, আয়াত ${n.ayah}\n\n`;
    md += `${n.text}\n\n`;
    if (n.tags && n.tags.length > 0) {
      md += `*ট্যাগসমূহ:* ${n.tags.join(', ')}\n\n`;
    }
    md += `---\n\n`;
  }
  const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `mufassir_class_notes_${new Date().toISOString().slice(0, 10)}.md`;
  a.click();
  URL.revokeObjectURL(url);
}

// Import JSON Backup
export async function importBackupJson(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const data = JSON.parse(e.target.result);
        if (data.notes && Array.isArray(data.notes)) {
          for (const note of data.notes) {
            delete note.id; // allow auto-increment
            await db.notes.put(note);
          }
        }
        if (data.bookmarks && Array.isArray(data.bookmarks)) {
          for (const b of data.bookmarks) {
            delete b.id;
            await db.bookmarks.put(b);
          }
        }
        resolve(true);
      } catch (err) {
        reject(err);
      }
    };
    reader.onerror = reject;
    reader.readAsText(file);
  });
}

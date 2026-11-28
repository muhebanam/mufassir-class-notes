/**
 * Central Word-by-Word Parser and Adapter Utility
 * Normalizes word-by-word data from markdown strings, tahqeeq arrays, and legacy mufradat
 * into a unified internal model:
 * [
 *   {
 *     id: number,
 *     arabic: string,
 *     meaning_bn: string,
 *     pos?: 'فعل' | 'اسم' | 'حرف' | null,
 *     root?: string | null,
 *     hasDeepTahqeeq: boolean,
 *     tahqeeqRef?: object | null
 *   }
 * ]
 */

// Helper to strip Arabic diacritics / tashkeel for fuzzy matching
export function normalizeArabicForMatching(text) {
  if (!text || typeof text !== 'string') return '';
  return text
    .replace(/[\u064B-\u065F\u0670\u0640]/g, '') // remove fathatan, dammatan, kasratan, fatha, damma, kasra, shadda, sukun, dagger alif, tatweel
    .replace(/[إأآٱ]/g, 'ا')
    .replace(/ة/g, 'ه')
    .replace(/ى/g, 'ي')
    .replace(/[^\u0600-\u06FF]/g, '')
    .trim();
}

/**
 * Main Universal Parser
 * @param {object} ayah - The full ayah object from ruku json
 * @returns {object} { isAvailable: boolean, words: Array, rawText: string }
 */
export function parseWordByWord(ayah) {
  if (!ayah) {
    return { isAvailable: false, words: [], rawText: '' };
  }

  const tahqeeqList = Array.isArray(ayah.tahqeeq) ? ayah.tahqeeq : [];
  const mufradatList = Array.isArray(ayah.mufradat) ? ayah.mufradat : [];

  // Helper map for fast lookup of deep tahqeeq by normalized Arabic text
  const tahqeeqMap = new Map();
  tahqeeqList.forEach(t => {
    const rawWord = t.word || t['শব্দ'] || '';
    const norm = normalizeArabicForMatching(rawWord);
    if (norm) {
      tahqeeqMap.set(norm, t);
    }
  });

  // Helper map for legacy mufradat lookup
  const mufradatMap = new Map();
  mufradatList.forEach(m => {
    const rawWord = m['শব্দ'] || m.word || '';
    const norm = normalizeArabicForMatching(rawWord);
    if (norm) {
      mufradatMap.set(norm, m);
    }
  });

  const rawWordTranslation = typeof ayah.word_translation === 'string' ? ayah.word_translation.trim() : '';

  // 1. If explicit formatted word_translation markdown string exists
  if (rawWordTranslation) {
    // Regex matches **Arabic** followed by Bengali meaning up to the next **Arabic** or end of string
    const regex = /\*\*([^*]+)\*\*\s*([^*]+?)(?=(?:\s*\*\*[^*]+\*\*|$))/g;
    const words = [];
    let m;
    let idx = 1;

    while ((m = regex.exec(rawWordTranslation)) !== null) {
      const ar = m[1].trim();
      let bn = m[2].trim()
        .replace(/^[-–—:;،,\s\u061B]+/, '')
        .replace(/[-–—:;،,\s\u061B]+$/, '')
        .trim();

      if (ar) {
        const normAr = normalizeArabicForMatching(ar);
        const matchedTahqeeq = tahqeeqMap.get(normAr) || null;
        const matchedMufradat = mufradatMap.get(normAr) || null;

        const pos = matchedTahqeeq?.word_type || null;
        const root = matchedTahqeeq?.morphology?.root || matchedMufradat?.['মূলধাতু'] || null;
        const hasDeepTahqeeq = !!(matchedTahqeeq || (matchedMufradat && Object.keys(matchedMufradat).length > 2));

        words.push({
          id: idx++,
          arabic: ar,
          meaning_bn: bn || matchedTahqeeq?.meaning_bn || '',
          pos,
          root,
          hasDeepTahqeeq,
          tahqeeqRef: matchedTahqeeq,
          mufradatRef: matchedMufradat
        });
      }
    }

    if (words.length > 0) {
      return {
        isAvailable: true,
        words,
        rawText: rawWordTranslation
      };
    }
  }

  // 2. Fallback: If word_translation was empty, but tahqeeq array exists (e.g. Surah 24 ayahs)
  if (tahqeeqList.length > 0) {
    const words = tahqeeqList.map((t, i) => ({
      id: i + 1,
      arabic: (t.word || t['শব্দ'] || t['আরবি শব্দ'] || '').replace(/\*/g, '').trim(),
      meaning_bn: t.meaning_bn || t['কুরআনিক পরিভাষাগত অর্থ'] || t['মূল অর্থ'] || t['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র'] || '',
      pos: t.word_type || null,
      root: t.morphology?.root || null,
      hasDeepTahqeeq: true,
      tahqeeqRef: t,
      mufradatRef: null
    }));

    return {
      isAvailable: true,
      words,
      rawText: words.map(w => `**${w.arabic}** ${w.meaning_bn}`).join(' ')
    };
  }

  // 3. Fallback: If mufradat list exists
  if (mufradatList.length > 0) {
    const words = mufradatList.map((m, i) => {
      const arClean = (m['শব্দ'] || '').replace(/\*\*/g, '').trim();
      return {
        id: i + 1,
        arabic: arClean,
        meaning_bn: m['আভিধানিক অর্থ'] || m['আভিধানিক অর্থ ও ভাষাতাত্ত্বিক সূত্র'] || m['কুরআনিক প্রয়োগ ও তাৎপর্য'] || '',
        pos: null,
        root: m['মূলধাতু'] || null,
        hasDeepTahqeeq: true,
        tahqeeqRef: null,
        mufradatRef: m
      };
    });

    return {
      isAvailable: true,
      words,
      rawText: words.map(w => `**${w.arabic}** ${w.meaning_bn}`).join(' ')
    };
  }

  // 4. Fallback: Bahouth words (build-time mapped) - NEW
  if (ayah.bahouth_words_mapped && Array.isArray(ayah.bahouth_words_mapped) && ayah.bahouth_words_mapped.length > 0) {
    const words = ayah.bahouth_words_mapped.map((bw, i) => {
      // Extract root from slash-wrapped token
      const rootRaw = bw.root_token_raw || '';
      const root = rootRaw.startsWith('/') && rootRaw.endsWith('/') && rootRaw.length > 2
        ? rootRaw.slice(1, -1)
        : rootRaw;
      return {
        id: i + 1,
        arabic: bw.word_raw || bw.plain_text_raw || '',
        meaning_bn: bw.site_meaning_bn || '',
        pos: null,
        root: root || null,
        hasDeepTahqeeq: false,
        tahqeeqRef: null,
        mufradatRef: null,
        bahouthMatch: bw.match || 'none',
        bahouthRoot: root || null,
        bahouthWordId: bw.word_id,
        bahouthOrder: bw.word_order_in_verse,
      };
    });
    return {
      isAvailable: true,
      words,
      rawText: words.map(w => `**${w.arabic}** ${w.meaning_bn}`).join(' ')
    };
  }

  // 5. Clean fallback when no word-level data is currently present
  return {
    isAvailable: false,
    words: [],
    rawText: ''
  };
}

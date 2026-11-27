// -*- coding: utf-8 -*-
/**
 * Tafsir al-Jalalayn & Hadith Takhrij Central Normalizer & Adapter
 * Provides deterministic parsing, typography layering, and zero-fabrication safety
 * across Surah 24 to 114 without breaking or altering any underlying data.
 */

const KNOWN_HADITH_BOOKS = [
  { key: 'bukhari', name_bn: 'সহীহ বুখারী', regex: /সহীহ\s+বুখারী|বুখারী/i, badgeColor: 'emerald' },
  { key: 'muslim', name_bn: 'সহীহ মুসলিম', regex: /সহীহ\s+মুসলিম|মুসলিমে/i, badgeColor: 'teal' },
  { key: 'tirmidhi', name_bn: 'সুনান আত-তিরমিযী', regex: /তিরমিযী/i, badgeColor: 'blue' },
  { key: 'abu_dawood', name_bn: 'সুনানে আবী দাউদ', regex: /আব[ূী]\s+দাউদ/i, badgeColor: 'indigo' },
  { key: 'nasai', name_bn: 'সুনানে নাসাঈ', regex: /নাসাঈ/i, badgeColor: 'sky' },
  { key: 'ibn_majah', name_bn: 'সুনানে ইবনে মাজাহ', regex: /ইবনে\s+মাজাহ/i, badgeColor: 'cyan' },
  { key: 'ahmad', name_bn: 'মুসনাদে আহমাদ', regex: /মুসনাদ[েএ]?\s+আহমাদ|আহমাদ/i, badgeColor: 'amber' },
  { key: 'malik', name_bn: 'মুয়াত্তা ইমাম মালিক', regex: /মুয়াত্তা\s+মালিক|মুয়াত্তা/i, badgeColor: 'purple' },
  { key: 'hakim', name_bn: 'মুস্তাদরাক হাকিম', regex: /মুস্তাদরাক[েএ]?\s+হাকিম|হাকিম/i, badgeColor: 'rose' },
  { key: 'bayhaqi', name_bn: 'সুনানে কুবরা লিল-বাইহাকী', regex: /বায়হাকী|বাইহাকী/i, badgeColor: 'slate' },
  { key: 'shafii', name_bn: 'কিতাবুল উম্ম (ইমাম শাফিঈ)', regex: /আল-উম্ম|ইমাম\s+শাফিঈ/i, badgeColor: 'emerald' },
  { key: 'ibn_abi_shaybah', name_bn: 'মুসান্নাফে ইবনে আবি শাইবাহ', regex: /ইবনে\s+আব[ূী]\s+শাইবাহ|আবী\s+শায়বাহ/i, badgeColor: 'slate' },
  { key: 'tabarani', name_bn: 'আল-মু‘জাম (তাবারানী)', regex: /তাবারানী/i, badgeColor: 'indigo' },
  { key: 'bazzar', name_bn: 'মুসনাদে বাযযার', regex: /বাযযার/i, badgeColor: 'amber' },
  { key: 'darimi', name_bn: 'সুনানে দারিমী', regex: /দারিমী/i, badgeColor: 'cyan' },
  { key: 'abdur_razzaq', name_bn: 'মুসান্নাফে আব্দুর রাযযাক', regex: /আব্দুর\s+রাযযাক/i, badgeColor: 'slate' },
  { key: 'tabari', name_bn: 'তাফসীরে তাবারী (ইবনে জারীর)', regex: /তাবারী|ইবনে\s+জারীর/i, badgeColor: 'blue' },
  { key: 'wahidi', name_bn: 'আসবাবুন নুযূল (আল-ওয়াহিদী)', regex: /ওয়াহিদী|ওয়াহিদী|আসবাবুন\s+নুযূল/i, badgeColor: 'rose' },
  { key: 'lubab', name_bn: 'লুবাবুন নুকূল (সুয়ূতী)', regex: /লুবাবুন\s+নুকূল|লুবাব/i, badgeColor: 'teal' },
  { key: 'wadiei', name_bn: 'আস-সহীহুল মুসনাদ (আল-ওয়াদিঈ)', regex: /ওয়াদিঈ|ওয়াদিঈ|আস-সহীহুল\s+মুসনাদ/i, badgeColor: 'emerald' },
  { key: 'adab_mufrad', name_bn: 'আল-আদাবুল মুফরাদ (বুখারী)', regex: /আদাবুল\s+মুফরাদ/i, badgeColor: 'emerald' },
];

/**
 * Extracts and cleans Tafsir al-Jalalayn text for layered visual presentation.
 */
export function parseJalalayn(rawText, ayahText = '') {
  if (!rawText || !rawText.trim()) {
    return {
      hasContent: false,
      scholar: 'ইমাম জালালুদ্দীন আল-মাহাল্লী ও আস-সুয়ূতী',
      arabicMatn: '',
      bengaliSharh: '',
      arabicTerms: [],
      cleanSharh: '',
      rawContent: ''
    };
  }

  const str = rawText.trim();

  // 1. Detect Scholar Attribution
  let scholar = 'ইমাম জালালুদ্দীন আল-মাহাল্লী ও আস-সুয়ূতী';
  if (/আল-মাহাল্লী|মাহাল্লী/i.test(str)) {
    scholar = 'ইমাম জালালুদ্দীন আল-মাহাল্লী (র.)';
  } else if (/আস-সুয়ূতী|সুয়ূতী/i.test(str)) {
    scholar = 'ইমাম জালালুদ্দীন আস-সুয়ূতী (র.)';
  }

  // 2. Extract Authentic Arabic Matn of Tafsir al-Jalalayn
  let arabicMatn = '';
  const matnMatch = str.match(/«([\s\S]*?)»/);
  if (matnMatch) {
    arabicMatn = matnMatch[1].replace(/\[src:[^\]]+\]/g, '').trim();
  }

  // 3. Extract Bengali Translation & Commentary (Sharh)
  let bengaliSharh = '';
  const bnMatch = str.match(/(?:-\s+\*\*(?:(?:পূর্ণাঙ্গ|সহজ|সার্বিক)\s+)?(?:বঙ্গানুবাদ|টীকা|ব্যাখ্যা|অনুবাদ)[^*]*\*\*[:\s]*)([\s\S]+)/);
  if (bnMatch) {
    bengaliSharh = bnMatch[1].replace(/\[src:[^\]]+\]/g, '').trim();
  } else {
    bengaliSharh = str.replace(/>\s*«[\s\S]*?»(?:\s*\[src:[^\]]+\])?/, '').trim();
  }

  // 4. Extract individual terms if any
  const arabicTerms = [];
  if (arabicMatn) {
    const terms = arabicMatn.match(/﴿([^﴾]+)﴾/g);
    if (terms) {
      terms.forEach(t => {
        const cleanT = t.replace(/[﴿﴾]/g, '').trim();
        if (cleanT && !arabicTerms.includes(cleanT)) {
          arabicTerms.push(cleanT);
        }
      });
    }
  }

  return {
    hasContent: true,
    scholar,
    arabicMatn,
    bengaliSharh,
    arabicTerms,
    cleanSharh: bengaliSharh || str,
    rawContent: str
  };
}

/**
 * Parses Hadith Takhrij and Shan-e-Nuzul markdown into structured cards and table rows.
 */
export function parseHadithTakhrij(rawText) {
  if (!rawText || !rawText.trim()) {
    return {
      isEmpty: true,
      narrativeIntro: '',
      hadiths: [],
      citations: []
    };
  }

  const fullText = rawText.trim();

  // Extract Turath tags e.g. `turath:8473`, page: 69
  const citations = [];
  const turathMatches = fullText.matchAll(/`turath:(\d+)`(?:\s*,\s*page:\s*(\d+))?/gi);
  for (const tm of turathMatches) {
    citations.push({
      id: tm[1],
      page: tm[2] || null
    });
  }

  // Check if content has structured bullet blocks: `- **Title**`, numbered `১. **Title**`, or `### (n) Title`
  const hasBullets = /(?:^|\n)-\s+\*\*([^*]+)\*\*/.test(fullText);
  const hasNumbered = /(?:^|\n)[০-৯0-9]+\.\s+\*\*([^*]+)\*\*/.test(fullText);
  const hasSections = /(?:^|\n)###\s+([^\n]+)/.test(fullText);

  if (!hasBullets && !hasNumbered && !hasSections) {
    // Return as single narrative block
    return {
      isEmpty: false,
      narrativeIntro: fullText,
      hadiths: [],
      citations
    };
  }

  const hadiths = [];
  let narrativeIntro = '';

  // Smart splitting:
  // Split on section headers `### ` OR top-level item bullets `- **` that are NOT metadata tags
  const itemSplitRegex = /\n(?=###\s+|-\s+\*\*(?!(?:তাখরীজ|মুহাদ্দিস|হুকুম|মান|উৎস|গ্রন্থসূত্র|অনুবাদ|তাৎপর্য|ব্যাখ্যা|সনদ|গ্রন্থ|নোট)))/i;

  let rawChunks = fullText.split(itemSplitRegex);
  let chunks = [];

  for (const rc of rawChunks) {
    const t = rc.trim();
    if (!t) continue;
    // If it is just a section heading or source tag with no items or quotes
    if (!t.includes('- **') && !t.includes('>') && (/^###\s+/.test(t) || /^[*_]+\s*\[উৎস:/.test(t))) {
      if (!narrativeIntro) {
        narrativeIntro = t.replace(/^[*_]+\s*\[উৎস:[^\]]+\]\s*[*_]*/, '').replace(/^###\s+/, '').trim();
      }
      continue;
    }
    chunks.push(t);
  }

  // If no chunks were extracted, fallback to full text
  if (chunks.length === 0 && fullText) {
    chunks = [fullText];
  }

  chunks.forEach((chunk, idx) => {
    const cleanChunk = chunk.trim();
    if (!cleanChunk) return;

    // 1. Title / Narrator
    let title = `হাদীস ও শানে নুযূল #${idx + 1}`;
    let inlineContent = '';
    const titleMatch = cleanChunk.match(/^(?:-\s+\*\*|[০-৯0-9]+\.\s+\*\*|###\s+)([^*#\n]+)(?:\*\*|:)\s*(.*)/);
    if (titleMatch && titleMatch[1]) {
      title = titleMatch[1].replace(/^[:\s]+|[:\s]+$/g, '').trim();
      inlineContent = (titleMatch[2] || '').trim();
    }

    // 2. Arabic Matn & Narrative Matn
    let arabicMatn = '';
    let narrativeMatn = '';
    const bqMatch = cleanChunk.match(/(?:^|\n)\s*>\s*([^\n]+(?:\n\s*>\s*[^\n]+)*)/);
    if (bqMatch && bqMatch[1]) {
      const bqText = bqMatch[1].replace(/\n\s*>\s*/g, ' ').trim();
      const bnChars = (bqText.match(/[\u0980-\u09FF]/g) || []).length;
      const arChars = (bqText.match(/[\u0621-\u064A]/g) || []).length;

      // Only treat as Arabic Matn when there is no substantial Bengali prose and Bengali doesn't outweigh Arabic
      if (arChars >= 6 && bnChars < 3 && arChars > bnChars) {
        arabicMatn = bqText;
      } else {
        narrativeMatn = bqText;
      }
    } else {
      // Check inline Arabic quote
      const inlineArabic = cleanChunk.match(/[“"']([\u0600-\u06FF\s،؛ـ؟().0-9٠-٩«»ﷺ:﴿﴾\-]{12,})[”"']/);
      if (inlineArabic && inlineArabic[1]) {
        arabicMatn = inlineArabic[1].trim();
      }
    }

    // 3. Takhrij Sources & Raw string
    let rawTakhrij = '';
    const takhrijMatch = cleanChunk.match(/-\s+\*\*(?:তাখরীজ|উৎস ও প্রামাণ্য গ্রন্থসূত্র|উৎস):\*\*\s*([^\n]+)/);
    if (takhrijMatch && takhrijMatch[1]) {
      rawTakhrij = takhrijMatch[1].trim();
    }

    // Detect individual known books strictly from the takhrij/source metadata line (never from narrative story text)
    const detectedSources = [];
    if (rawTakhrij) {
      KNOWN_HADITH_BOOKS.forEach(b => {
        if (b.regex.test(rawTakhrij)) {
          detectedSources.push(b.name_bn);
        }
      });
    }

    // Extract Hadith Numbers or Vol/Page
    let numbers = '';
    const numMatch = rawTakhrij.match(/(?:হাদীস\s*(?:নং)?\s*[:\s]*|নং\s*)(\*{0,2}[0-9٠-٩০-৯/–-]+\*{0,2})/i);
    if (numMatch && numMatch[1]) {
      numbers = numMatch[1].replace(/\*/g, '').trim();
    }

    // 4. Muhaddith Ruling / Hukm
    let hukm = null;
    let hukmGrade = 'unknown';
    const hukmMatch = cleanChunk.match(/-\s+\*\*(?:মুহাদ্দিসদের হুকুম|মান):\*\*\s*([^\n]+)/);
    if (hukmMatch && hukmMatch[1]) {
      hukm = hukmMatch[1].trim();
      if (/সহীহ|মুত্তাফাকুন|صحيح|متفق عليه/i.test(hukm)) {
        hukmGrade = 'sahih';
      } else if (/হাসান|حسن/i.test(hukm)) {
        hukmGrade = 'hasan';
      } else if (/যঈফ|দুর্বল|ضعيف/i.test(hukm)) {
        hukmGrade = 'daif';
      }
    }

    // 5. Explanation / Context
    let explanation = '';
    const expMatch = cleanChunk.match(/-\s+\*\*(?:অনুবাদ ও শানে নুযূল|অনুবাদ ও তাৎপর্য|অনুবাদ ও ঐতিহাসিক প্রেক্ষাপট|অনুবাদ ও লি‘আনের পদ্ধতি|অনুবাদ ও বিশ্লেষণ|অনুবাদ ও পটভূমি|অনুবাদ|ব্যাখ্যা|প্রেক্ষাপট|ঐতিহাসিক প্রেক্ষাপট):\*\*\s*([^\n]+(?:\n(?!\s*-\s*\*\*)[^\n]+)*)/);
    if (expMatch && expMatch[1]) {
      explanation = expMatch[1].trim();
    } else if (inlineContent && !inlineContent.startsWith('- **') && !inlineContent.startsWith('>')) {
      explanation = inlineContent;
    } else {
      // If no explicit translation/context heading, use the remaining body lines as explanation
      const bodyLines = cleanChunk
        .replace(/^(?:-\s+\*\*|[০-৯0-9]+\.\s+\*\*|###\s+)[^\n]+/, '')
        .split('\n')
        .map(l => l.replace(/^\s*[-*]+\s*/, '').trim())
        .filter(l => l && !l.startsWith('>') && !l.startsWith('---') && !l.startsWith('**তাখরীজ') && !l.startsWith('**মুহাদ্দিস') && !l.startsWith('**উৎস'));
      if (bodyLines.length > 0) {
        explanation = bodyLines.join('\n\n');
      }
    }

    // If inlineContent exists and wasn't captured, prepend it
    if (inlineContent && !inlineContent.startsWith('- **') && !inlineContent.startsWith('>') && !explanation.includes(inlineContent)) {
      explanation = inlineContent + (explanation ? '\n\n' + explanation : '');
    }

    const isRealHadith = !!(arabicMatn || rawTakhrij || detectedSources.length > 0 || numbers || hukm);
    const isNuzul = cleanChunk.includes('শানে নুযূল') || cleanChunk.includes('নাযিল') || cleanChunk.includes('প্রেক্ষাপট') || cleanChunk.includes('আসবাব');

    // Filter out empty ghost items with no substance
    if (!arabicMatn && !explanation && !rawTakhrij && !hukm && cleanChunk.length < 30) {
      return;
    }

    const cleanTitle = title.replace(/^[\s\-–—:]+|[\s\-–—:]+$/g, '').trim();
    const grade = hukmGrade;
    const takhrijNote = rawTakhrij;
    const sourceBook = detectedSources.length > 0 
      ? detectedSources.join(', ') 
      : (rawTakhrij ? rawTakhrij.split(/[,;(]/)[0].trim() : '');
    const body = explanation || cleanChunk.replace(/^(?:-\s+\*\*|[০-৯0-9]+\.\s+\*\*|###\s+)[^\n]+/, '').trim();

    hadiths.push({
      id: `hadith-${idx}`,
      title,
      cleanTitle,
      arabicMatn,
      narrativeMatn,
      rawTakhrij,
      takhrijNote,
      sources: detectedSources,
      sourceBook,
      numbers,
      hukm,
      grade,
      hukmGrade,
      explanation,
      body,
      isRealHadith,
      isNuzul,
      rawItem: cleanChunk
    });
  });

  const realHadiths = hadiths.filter(h => h.isRealHadith);
  const nuzulItems = hadiths.filter(h => h.isNuzul || !h.isRealHadith);

  return {
    isEmpty: false,
    narrativeIntro,
    hadiths,
    realHadiths,
    nuzulItems,
    hasHadith: realHadiths.length > 0,
    hasNuzul: nuzulItems.length > 0 || !!narrativeIntro,
    citations
  };
}

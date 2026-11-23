const A = '\\u0600-\\u06FF\\u0750-\\u077F\\uFB50-\\uFDFF\\uFE70-\\uFEFF';
const MARK = '\\u064B-\\u065F\\u0670';
const DIGITS = '0-9\\u0660-\\u0669\\u06F0-\\u06F9';
const AR_CHAR = `[${A}${MARK}]`;
// Content inside Arabic delimiter: strictly Arabic letters, diacritics, numbers, spaces, and Arabic punctuation
const AR_INNER = `[${A}${MARK}${DIGITS}\\s،؟:؛\\-–—«»“”﴿﴾]*`;

const PAIRS = [
  `«${AR_INNER}${AR_CHAR}${AR_INNER}»`,
  `“${AR_INNER}${AR_CHAR}${AR_INNER}”`,
  `﴿${AR_INNER}${AR_CHAR}${AR_INNER}﴾`,
  `\\(${AR_INNER}${AR_CHAR}${AR_INNER}\\)`,
  `\\[${AR_INNER}${AR_CHAR}${AR_INNER}\\]`
].join('|');

const BARE = `${AR_CHAR}[${A}${MARK}${DIGITS}\\s،؟:؛\\-–—]*${AR_CHAR}|${AR_CHAR}`;

const REGEX = new RegExp(`(?:${PAIRS})|(?:${BARE})`, 'g');

const samples = [
  'আসার: “لَيْسَ فِي دِينِنَا تَجْرِيدٌ” (আমাদের দ্বীনে)',
  'নিদর্শন (التَّغْرِيبِ) বলা হয়',
  'কুরআনের বাণী ﴿الم﴾ পরম সত্য',
  'হাদীসের পাঠ «مَتْنُ الْحَدِيثِ» প্রামাণিক',
  'রেফারেন্স (যেমন: [سورة البقرة: ٨٣]) দ্রষ্টব্য',
  '“الله” (حق الله) মহিমান্বিত',
  'আল্লাহ বলেন: ﴿وَقَالَ إِنَّمَا اتَّخَذْتُم مِّن دُونِ اللَّهِ أَوْثَانًا﴾ [سورة العنكبوت: ٢٥] যা স্পষ্ট।',
  'বাংলা টেক্সট (কোনো আরবি নেই)'
];

for (const s of samples) {
  console.log('INPUT :', s);
  console.log('MATCH :', s.match(REGEX) || []);
  console.log('---');
}

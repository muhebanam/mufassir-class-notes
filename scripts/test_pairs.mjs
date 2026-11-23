import assert from 'node:assert/strict';
import { getArabicRegex } from '../web/src/utils/arabicRegex.js';

const tests = [
  {
    input: 'আসার: “لَيْسَ فِي دِينِنَا تَجْرِيدٌ” (আমাদের দ্বীনে)',
    expected: ['“لَيْسَ فِي دِينِنَا تَجْرِيدٌ”']
  },
  {
    input: 'নিদর্শন (التَّغْرِيبِ) বলা হয়',
    expected: ['(التَّغْرِيبِ)']
  },
  {
    input: 'কুরআনের বাণী ﴿الم﴾ পরম সত্য',
    expected: ['﴿الم﴾']
  },
  {
    input: 'হাদীসের পাঠ «مَتْنُ الْحَدِيثِ» প্রামাণিক',
    expected: ['«مَتْنُ الْحَدِيثِ»']
  },
  {
    input: 'রেফারেন্স (যেমন: [سورة البقرة: ٨٣]) দ্রষ্টব্য',
    expected: ['[سورة البقرة: ٨٣]']
  },
  {
    input: '“الله” (حق الله) মহিমান্বিত',
    expected: ['“الله”', '(حق الله)']
  },
  {
    input: 'আল্লাহ বলেন: ﴿وَقَالَ إِنَّمَا اتَّخَذْتُم مِّن دُونِ اللَّهِ أَوْثَانًا﴾ [سورة العنكبوت: ٢٥] যা স্পষ্ট।',
    expected: [
      '﴿وَقَالَ إِنَّمَا اتَّخَذْتُم مِّن دُونِ اللَّهِ أَوْثَانًا﴾',
      '[سورة العنكبوت: ٢٥]'
    ]
  },
  {
    input: 'বাংলা টেক্সট (কোনো আরবি নেই)',
    expected: []
  },
  {
    input: '﴿سُورَةٌ﴾ ﴿أَنزَلْنَاهَا﴾',
    expected: ['﴿سُورَةٌ﴾', '﴿أَنزَلْنَاهَا﴾']
  },
  {
    input: '«قرأ بإمالة هاء التأنيث.»',
    expected: ['«قرأ بإمالة هاء التأنيث.»']
  },
  {
    input: '«كلمة أولى» ও «كلمة ثانية» পাশাপাশি',
    expected: ['«كلمة أولى»', '«كلمة ثانية»']
  }
];

let failed = 0;
for (const t of tests) {
  const reg = getArabicRegex();
  const matches = t.input.match(reg) || [];
  try {
    assert.deepEqual(matches, t.expected);
    console.log('INPUT :', t.input);
    console.log('MATCH :', matches);
    console.log('STATUS: ✓ PASSED');
    console.log('---');
  } catch (err) {
    console.error(`✗ FAIL: ${t.input}`);
    console.error(`  Expected: ${JSON.stringify(t.expected)}`);
    console.error(`  Actual:   ${JSON.stringify(matches)}`);
    failed++;
  }
}

if (failed === 0) {
  console.log(`\nAll ${tests.length} test cases passed strict assertions with 100% accuracy.`);
} else {
  process.exit(1);
}

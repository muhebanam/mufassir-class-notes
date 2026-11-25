import { parseJalalayn, parseHadithTakhrij } from '../web/src/utils/tafsirTakhrijAdapter.js';
import fs from 'fs';

const r1 = JSON.parse(fs.readFileSync('web/public/data/24/ruku-1.json', 'utf8'));

console.log('--- Testing Jalalayn Parsing (24:1) ---');
const j1 = parseJalalayn(r1.ayahs[0].jalalayn);
console.log('Scholar:', j1.scholar);
console.log('Arabic terms:', j1.arabicTerms);
console.log('Clean sharh:', j1.cleanSharh.substring(0, 100) + '...');

console.log('\n--- Testing Ayah Hadith Takhrij (24:2) ---');
const h2 = parseHadithTakhrij(r1.ayahs[1].shane_nuzul);
console.log('Hadiths count:', h2.hadiths.length);
if (h2.hadiths.length > 0) {
  console.log('Hadith 1 title:', h2.hadiths[0].title);
  console.log('Hadith 1 sources:', h2.hadiths[0].sources);
  console.log('Hadith 1 grade:', h2.hadiths[0].hukmGrade);
  console.log('Hadith 1 matn preview:', h2.hadiths[0].arabicMatn.substring(0, 50));
}

console.log('\n--- Testing Ruku Thematic Hadith (24:1) ---');
const rukuHadith = parseHadithTakhrij(r1.thematic_topics.hadith.content);
console.log('Ruku Hadiths count:', rukuHadith.hadiths.length);
for (const h of rukuHadith.hadiths.slice(0, 3)) {
  console.log(' *', h.title, '| Sources:', h.sources.join(', '), '| Grade:', h.hukmGrade);
}

console.log('\n✓ Adapter test completed successfully!');

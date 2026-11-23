import fs from 'fs';
import path from 'path';
import { marked } from '../web/node_modules/marked/lib/marked.esm.js';

marked.setOptions({ gfm: true, breaks: true });

const DATA_DIR = path.resolve('d:/আমার গবেষণা/জালালাইন/web/public/data');
const surahsFile = path.join(DATA_DIR, 'surahs.json');

if (!fs.existsSync(surahsFile)) {
  console.error('surahs.json not found in', DATA_DIR);
  process.exit(1);
}

const surahs = JSON.parse(fs.readFileSync(surahsFile, 'utf-8'));
console.log(`Starting Markdown Rendering Regression Test for ${surahs.length} surahs...`);

let totalRukusTested = 0;
let totalFailures = 0;
const failureDetails = [];

// Regression forbidden patterns in compiled HTML
const FORBIDDEN_PATTERNS = [
  { name: 'Unparsed Table Separator (|---|)', regex: /\|[\s\-:]*--[\s\-:]*\|/ },
  { name: 'Escaped HTML <br> (&lt;br&gt;)', regex: /&lt;br\s*\/?&gt;/i },
  { name: 'Unparsed Heading Symbol (###)', regex: /(?:^|\n)\s*#{1,6}\s+[^\n]+/ },
  { name: 'Unparsed Blockquote Symbol (>)', regex: /(?:^|\n)\s*&gt;\s+[^\n]+/ },
];

for (const s of surahs) {
  const surahId = s.id;
  const sDir = path.join(DATA_DIR, String(surahId));
  if (!fs.existsSync(sDir)) continue;

  const rukuFiles = fs.readdirSync(sDir).filter(f => f.startsWith('ruku-') && f.endsWith('.json'));

  for (const rf of rukuFiles) {
    totalRukusTested++;
    const rukuData = JSON.parse(fs.readFileSync(path.join(sDir, rf), 'utf-8'));
    const topics = rukuData.thematic_topics || {};

    // Test each thematic topic's content
    for (const [key, topic] of Object.entries(topics)) {
      if (!topic || typeof topic !== 'object') continue;
      const content = topic.content || '';
      if (!content || typeof content !== 'string') continue;

      const html = marked.parse(content);

      for (const rule of FORBIDDEN_PATTERNS) {
        if (rule.regex.test(html)) {
          totalFailures++;
          failureDetails.push({
            surah: surahId,
            ruku: rf,
            topic: key,
            rule: rule.name,
            snippet: html.match(rule.regex)[0]
          });
        }
      }
    }

    // Also test Ayah jalalayn, irab, and shane_nuzul
    for (const a of rukuData.ayahs || []) {
      const texts = [a.jalalayn, a.irab, a.shane_nuzul].filter(Boolean);
      for (const txt of texts) {
        const html = marked.parse(txt);
        for (const rule of FORBIDDEN_PATTERNS) {
          if (rule.regex.test(html)) {
            totalFailures++;
            failureDetails.push({
              surah: surahId,
              ruku: rf,
              ayah: a.ayah,
              rule: rule.name,
              snippet: html.match(rule.regex)[0]
            });
          }
        }
      }
    }
  }
}

console.log('--------------------------------------------------');
console.log(`Total Rukus Audited: ${totalRukusTested}`);
console.log(`Total Rendering Failures: ${totalFailures}`);

const countsByRule = {};
for (const f of failureDetails) {
  countsByRule[f.rule] = (countsByRule[f.rule] || 0) + 1;
}
console.log('Counts by rule:', countsByRule);

if (totalFailures === 0) {
  console.log('✓ 100% PASSED: Zero unparsed Markdown artifacts found in any ruku!');
  process.exit(0);
} else {
  console.error(`✗ FAILED: Found ${totalFailures} unparsed Markdown leaks:`);
  for (const f of failureDetails.slice(0, 10)) {
    console.error(`  - Surah ${f.surah} / ${f.ruku} [${f.topic || f.ayah}]: ${f.rule} -> "${f.snippet}"`);
  }
  process.exit(1);
}

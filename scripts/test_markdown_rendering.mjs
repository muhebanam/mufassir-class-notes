// -*- coding: utf-8 -*-
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import assert from 'node:assert/strict';
import { marked } from '../web/node_modules/marked/lib/marked.esm.js';

marked.setOptions({ gfm: true, breaks: true });

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');
const DATA_DIR = path.join(ROOT_DIR, 'web', 'public', 'data');
const surahsFile = path.join(DATA_DIR, 'surahs.json');

if (!fs.existsSync(surahsFile)) {
  console.error('surahs.json not found in', DATA_DIR);
  process.exit(1);
}

const surahs = JSON.parse(fs.readFileSync(surahsFile, 'utf-8'));
console.log(`Starting Comprehensive Markdown & Data Quality Regression Test for ${surahs.length} surahs...`);

let totalRukusTested = 0;
let totalSurahsTested = 0;
let totalFailures = 0;
const failureDetails = [];

// Regression forbidden patterns in compiled HTML or raw content
const FORBIDDEN_HTML_PATTERNS = [
  { name: 'Unparsed Table Separator (|---|)', regex: /\|[\s\-:]*--[\s\-:]*\|/ },
  { name: 'Escaped HTML <br> (&lt;br&gt;)', regex: /&lt;br\s*\/?&gt;/i },
  { name: 'Unparsed Heading Symbol (###)', regex: /(?:^|\n)\s*#{1,6}\s+[^\n]+/ },
  { name: 'Unparsed Blockquote Symbol (>)', regex: /(?:^|\n)\s*&gt;\s+[^\n]+/ },
  { name: 'Broken Markdown Link (.md)', regex: /href="[^"]*\.md(?:#[^"]*)?"/i },
];

const FORBIDDEN_RAW_PATTERNS = [
  { name: 'Broken Local Markdown Link', regex: /\[[^\]]+\]\(\s*\.[^)]+\.md\s*\)/ },
  { name: 'Arabic Trapped in Backticks', regex: /`[\u0600-\u06FF]{2,}[^`]*`/ },
];

function checkText(txt, contextInfo, isRaw = false) {
  if (!txt || typeof txt !== 'string') return;

  // Check raw patterns
  for (const rule of FORBIDDEN_RAW_PATTERNS) {
    if (rule.regex.test(txt)) {
      totalFailures++;
      failureDetails.push({
        ...contextInfo,
        rule: rule.name,
        snippet: txt.match(rule.regex)[0]
      });
    }
  }

  // Compile and check HTML patterns
  try {
    const rawHtml = isRaw ? marked.parse(txt) : marked.parseInline(txt);
    // Strip fenced code blocks from compiled HTML so mermaid/code snippets don't false-positive on escaped tags
    const html = isRaw ? rawHtml.replace(/<pre><code[\s\S]*?<\/code><\/pre>/gi, '') : rawHtml;
    for (const rule of FORBIDDEN_HTML_PATTERNS) {
      if (rule.regex.test(html)) {
        totalFailures++;
        failureDetails.push({
          ...contextInfo,
          rule: rule.name,
          snippet: html.match(rule.regex)[0]
        });
      }
    }
  } catch (err) {
    totalFailures++;
    failureDetails.push({
      ...contextInfo,
      rule: 'Marked Parse Error',
      snippet: String(err)
    });
  }
}

for (const s of surahs) {
  const surahId = s.id;
  const sDir = path.join(DATA_DIR, String(surahId));
  if (!fs.existsSync(sDir)) continue;

  totalSurahsTested++;

  // 1. Audit Surah meta.json (intro, summary, title)
  const metaFile = path.join(sDir, 'meta.json');
  if (fs.existsSync(metaFile)) {
    const metaData = JSON.parse(fs.readFileSync(metaFile, 'utf-8'));
    if (metaData.intro) {
      checkText(metaData.intro, { surah: surahId, file: 'meta.json', section: 'intro' }, true);
    }
    if (metaData.summary) {
      checkText(metaData.summary, { surah: surahId, file: 'meta.json', section: 'summary' }, false);
    }
  }

  const rukuFiles = fs.readdirSync(sDir).filter(f => f.startsWith('ruku-') && f.endsWith('.json'));

  for (const rf of rukuFiles) {
    totalRukusTested++;
    const rukuData = JSON.parse(fs.readFileSync(path.join(sDir, rf), 'utf-8'));
    const topics = rukuData.thematic_topics || {};

    // 2. Test each thematic topic's content
    for (const [key, topic] of Object.entries(topics)) {
      if (!topic || typeof topic !== 'object') continue;
      const content = topic.content || '';
      if (content) {
        checkText(content, { surah: surahId, ruku: rf, topic: key }, true);
      }

      // 3. Audit Ahkam intro, cards, daleel, sources
      if (key === 'ahkam') {
        if (topic.intro) {
          checkText(topic.intro, { surah: surahId, ruku: rf, topic: 'ahkam.intro' }, true);
        }
        if (Array.isArray(topic.cards)) {
          for (const card of topic.cards) {
            const cardTexts = [card.title, card.hanafi, card.shafii, card.maliki, card.hanbali].filter(Boolean);
            for (const cText of cardTexts) {
              checkText(cText, { surah: surahId, ruku: rf, topic: `ahkam.card.${card.title?.slice(0, 15)}` }, false);
            }
            if (Array.isArray(card.daleel)) {
              for (const d of card.daleel) {
                checkText(d, { surah: surahId, ruku: rf, topic: `ahkam.daleel` }, true);
              }
            }
            if (Array.isArray(card.sources)) {
              for (const src of card.sources) {
                checkText(src, { surah: surahId, ruku: rf, topic: `ahkam.source` }, false);
              }
            }
          }
        }
      }

      // 4. Audit Qiraat table cells
      if (key === 'qiraat_full' && Array.isArray(topic.table)) {
        for (const row of topic.table) {
          for (const [cellK, cellV] of Object.entries(row)) {
            checkText(String(cellV), { surah: surahId, ruku: rf, topic: `qiraat.table.${cellK}` }, false);
          }
        }
      }
    }

    // 5. Audit Mufradat table cells
    if (Array.isArray(rukuData.mufradat)) {
      for (const mRow of rukuData.mufradat) {
        for (const [mK, mV] of Object.entries(mRow)) {
          checkText(String(mV), { surah: surahId, ruku: rf, topic: `mufradat.${mK}` }, false);
        }
      }
    }

    // 6. Audit Ayahs: jalalayn, irab, and shane_nuzul
    for (const a of rukuData.ayahs || []) {
      const texts = [
        { name: 'jalalayn', val: a.jalalayn },
        { name: 'irab', val: a.irab },
        { name: 'shane_nuzul', val: a.shane_nuzul },
        { name: 'bengali_trans', val: a.translation_bn }
      ];
      for (const tItem of texts) {
        if (tItem.val) {
          checkText(tItem.val, { surah: surahId, ruku: rf, ayah: a.ayah, field: tItem.name }, true);
        }
      }
    }
  }
}

console.log('--------------------------------------------------');
console.log(`Total Surahs Audited: ${totalSurahsTested}`);
console.log(`Total Rukus Audited: ${totalRukusTested}`);
console.log(`Total Rendering & Data Failures: ${totalFailures}`);

const countsByRule = {};
for (const f of failureDetails) {
  countsByRule[f.rule] = (countsByRule[f.rule] || 0) + 1;
}
console.log('Counts by rule:', countsByRule);

if (totalFailures === 0) {
  console.log('✓ 100% PASSED: Zero unparsed Markdown artifacts, broken links, or trapped Arabic found!');
  process.exit(0);
} else {
  console.error(`✗ FAILED: Found ${totalFailures} leaks / issues:`);
  for (const f of failureDetails) {
    console.error(`  - Surah ${f.surah} / ${f.ruku || f.file} [${f.topic || f.ayah || f.section}]: ${f.rule} -> "${f.snippet}"`);
  }
  process.exit(1);
}

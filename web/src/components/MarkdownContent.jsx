import React, { useMemo } from 'react';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import { getArabicRegex } from '../utils/arabicRegex';

marked.setOptions({
  gfm: true,
  breaks: true,
});

/**
 * Normalizes Quranic ayah brackets:
 * Ensures opening bracket on the right is \ufd3f (﴿) and closing bracket on the left is \ufd3e (﴾).
 * Corrects any inverted brackets \ufd3e...\ufd3f -> \ufd3f...\ufd3e.
 */
export function normalizeQuranBrackets(text) {
  if (!text || typeof text !== 'string') return text;
  return text
    .split('\n')
    .map(line => {
      if (!line.includes('\uFD3E') && !line.includes('\uFD3F')) return line;
      const parts = line.split(/(\uFD3F[^\uFD3E\uFD3F]*?\uFD3E)/g);
      return parts
        .map((part, idx) => {
          if (idx % 2 === 1) return part;
          return part.replace(
            /\uFD3E([^\uFD3E\uFD3F]*?[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF][^\uFD3E\uFD3F]*?)\uFD3F/g,
            '\uFD3F$1\uFD3E'
          );
        })
        .join('');
    })
    .join('\n');
}

// Count ONLY actual Arabic base letters (excludes harakat U+064B..U+065F, U+0670, waqf marks, tatweel)
const BASE_AR_RE = /[\u0621-\u063A\u0641-\u064A\u0671-\u06D3]/g;
const BN_RE = /[\u0980-\u09FF]/g;
const EN_RE = /[A-Za-z]/g;

function countScripts(text) {
  if (!text) return { arBase: 0, bnCount: 0, enCount: 0 };
  return {
    arBase: (text.match(BASE_AR_RE) || []).length,
    bnCount: (text.match(BN_RE) || []).length,
    enCount: (text.match(EN_RE) || []).length,
  };
}

function splitMixedLinesWithBr(el) {
  const children = Array.from(el.childNodes);
  if (!children.some(n => n.nodeType === 1 && n.tagName === 'BR')) return false;

  const { arBase, bnCount } = countScripts(el.textContent || '');
  if (arBase < 3 || bnCount === 0) return false;

  // Group childNodes into segments split by <br>
  const segments = [];
  let current = [];
  for (const node of children) {
    if (node.nodeType === 1 && node.tagName === 'BR') {
      segments.push(current);
      current = [];
    } else {
      current.push(node);
    }
  }
  if (current.length > 0) segments.push(current);

  if (segments.length <= 1) return false;

  // Check if at least one segment is purely Arabic
  let hasPureArabicLine = false;
  const processed = segments.map(segNodes => {
    const segText = segNodes.map(n => n.textContent || '').join('').trim();
    const counts = countScripts(segText);
    const isPureAr = counts.arBase >= 3 && counts.bnCount === 0 && counts.enCount <= 2;
    if (isPureAr) hasPureArabicLine = true;
    return { segNodes, segText, isPureAr };
  });

  if (!hasPureArabicLine) return false;

  const frag = document.createDocumentFragment();
  processed.forEach(({ segNodes, segText, isPureAr }) => {
    if (!segText) return;
    const span = document.createElement('span');
    if (isPureAr) {
      span.className = 'ar-block-line font-arabic';
      span.dir = 'rtl';
      span.lang = 'ar';
    } else {
      span.className = 'bn-line';
      span.dir = 'ltr';
    }
    segNodes.forEach(n => span.appendChild(n));
    frag.appendChild(span);
  });

  el.innerHTML = '';
  el.appendChild(frag);
  return true;
}

function wrapArabic(root) {
  if (!root) return;

  // 1. Style inline code tags containing strictly Arabic text
  root.querySelectorAll('code').forEach(cd => {
    const text = cd.textContent || '';
    const { arBase, bnCount, enCount } = countScripts(text);
    if (arBase >= 1 && bnCount === 0 && enCount === 0) {
      cd.dir = 'rtl';
      cd.lang = 'ar';
      cd.classList.add('ar-code', 'font-amiri');
    }
  });

  // 2a. Split <p> or <li> elements containing <br>-separated Arabic quote + Bengali translation lines
  root.querySelectorAll('p, li').forEach(el => {
    splitMixedLinesWithBr(el);
  });

  // 2b. Apply .ar-block / .table-cell-arabic ONLY to strictly Arabic blocks (ZERO Bengali prose)
  const blockSelectors = 'p, li, div, h1, h2, h3, h4, h5, h6, td, th';
  root.querySelectorAll(blockSelectors).forEach(el => {
    if (el.tagName === 'DIV' && el.querySelector('p, blockquote, table, ul, ol')) return;
    if (el.querySelector('.ar-block-line')) return;
    const t = el.textContent || '';
    if (!t.trim()) return;

    const { arBase, bnCount, enCount } = countScripts(t);
    const minAr = (el.tagName === 'TD' || el.tagName === 'TH') ? 1 : 2;
    if (arBase >= minAr && bnCount === 0 && enCount <= 2) {
      if (el.tagName === 'TD' || el.tagName === 'TH') {
        el.classList.add('table-cell-arabic');
      } else {
        el.classList.add('ar-block', 'font-arabic', 'text-right');
      }
      el.dir = 'rtl';
      el.lang = 'ar';
      el.style.textAlign = 'right';
      el.style.direction = 'rtl';
    }
  });

  // 2c. Apply .ar-quote ONLY to blockquotes that are 100% Arabic (no Bengali text inside)
  root.querySelectorAll('blockquote').forEach(bq => {
    const t = bq.textContent || '';
    if (!t.trim()) return;
    const { arBase, bnCount, enCount } = countScripts(t);
    if (arBase >= 3 && bnCount === 0 && enCount <= 2) {
      bq.classList.add('ar-quote');
      bq.dir = 'rtl';
      bq.lang = 'ar';
    }
  });

  // Orient entire lists where all list items are strictly Arabic
  root.querySelectorAll('ul, ol').forEach(list => {
    const items = list.querySelectorAll(':scope > li');
    if (items.length > 0 && Array.from(items).every(li => li.classList.contains('ar-block'))) {
      list.dir = 'rtl';
      list.classList.add('ar-block', 'font-arabic', 'text-right');
      list.style.textAlign = 'right';
      list.style.direction = 'rtl';
    }
  });

  // 3. TreeWalker for text nodes to isolate inline Arabic inside <bdi class="ar">
  // ONLY for Arabic phrases embedded inside non-RTL (Bengali/English) contexts.
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (w.nextNode()) nodes.push(w.currentNode);

  for (const n of nodes) {
    if (n.parentElement?.closest('bdi.ar, code, pre, [dir="rtl"], .ar-block, .ar-block-line, .ar-quote, .table-cell-arabic, .uthmani-text, .font-arabic')) continue;
    const t = n.nodeValue;
    if (!t) continue;
    const AR = getArabicRegex();
    if (!AR.test(t)) continue;
    AR.lastIndex = 0;

    const frag = document.createDocumentFragment();
    let last = 0;
    let m;
    while ((m = AR.exec(t))) {
      if (m.index > last) {
        frag.append(t.slice(last, m.index));
      }
      const b = document.createElement('bdi');
      b.className = 'ar';
      b.lang = 'ar';
      b.dir = 'rtl';
      b.textContent = m[0];
      frag.append(b);
      last = m.index + m[0].length;
    }
    if (last < t.length) {
      frag.append(t.slice(last));
    }
    n.replaceWith(frag);
  }
}

function wrapTables(root) {
  if (!root) return;
  root.querySelectorAll('table').forEach(tb => {
    if (tb.parentElement && tb.parentElement.classList.contains('table-wrap')) return;
    const d = document.createElement('div');
    d.className = 'table-wrap';
    tb.replaceWith(d);
    d.append(tb);
  });
}

export function renderMarkdown(src, { inline = false } = {}) {
  if (!src) return '';
  const normalized = normalizeQuranBrackets(src);
  const html = inline ? marked.parseInline(normalized) : marked.parse(normalized);

  if (typeof document !== 'undefined') {
    const frag = DOMPurify.sanitize(html, {
      RETURN_DOM_FRAGMENT: true,
      ADD_TAGS: ['bdi', 'span', 'br', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'blockquote', 'div', 'code'],
      ADD_ATTR: ['dir', 'lang', 'class', 'target', 'rel', 'href'],
    });
    const box = document.createElement('div');
    box.append(frag);
    wrapArabic(box);
    wrapTables(box);
    return box.innerHTML;
  }

  return DOMPurify.sanitize(html, {
    ADD_TAGS: ['bdi', 'span', 'br', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'blockquote', 'div', 'code'],
    ADD_ATTR: ['dir', 'lang', 'class', 'target', 'rel', 'href'],
  });
}

export default function MarkdownContent({ content, inline = false, className = "" }) {
  const html = useMemo(() => renderMarkdown(content, { inline }), [content, inline]);

  if (!content) return null;

  const Tag = inline ? 'span' : 'div';
  const hasArabicFont = /font-(arabic|amiri)|uthmani-text/.test(className);
  const fontClass = hasArabicFont ? '' : 'font-bengali';
  return (
    <Tag
      className={`prose ${fontClass} leading-relaxed transition-colors ${className}`}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

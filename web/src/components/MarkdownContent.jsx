import React, { useMemo } from 'react';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

marked.setOptions({
  gfm: true,
  breaks: true,
});

// Arabic characters and diacritics
const A = '\\u0600-\\u06FF\\u0750-\\u077F\\uFB50-\\uFDFF\\uFE70-\\uFEFF';
const MARK = '\\u064B-\\u065F\\u0670';
const DIGITS = '0-9\\u0660-\\u0669\\u06F0-\\u06F9';
const AR_CHAR = `[${A}${MARK}]`;
const AR_INNER = `[${A}${MARK}${DIGITS}\\s،؟:؛\\-–—«»“”﴿﴾]*`;

// Paired Arabic expressions to prevent mismatched/swallowed closing brackets
const PAIRS = [
  `«${AR_INNER}${AR_CHAR}${AR_INNER}»`,
  `“${AR_INNER}${AR_CHAR}${AR_INNER}”`,
  `﴿${AR_INNER}${AR_CHAR}${AR_INNER}﴾`,
  `\\(${AR_INNER}${AR_CHAR}${AR_INNER}\\)`,
  `\\[${AR_INNER}${AR_CHAR}${AR_INNER}\\]`
].join('|');

// Bare Arabic runs (not already enclosed in paired delimiters)
const BARE = `${AR_CHAR}[${A}${MARK}${DIGITS}\\s،؟:؛\\-–—]*${AR_CHAR}|${AR_CHAR}`;

const AR = new RegExp(`(?:${PAIRS})|(?:${BARE})`, 'g');

function wrapArabic(root) {
  if (!root) return;
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (w.nextNode()) nodes.push(w.currentNode);

  for (const n of nodes) {
    if (n.parentElement?.closest('bdi.ar, code, pre')) continue;
    const t = n.nodeValue;
    if (!t) continue;
    AR.lastIndex = 0;
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
  const html = inline ? marked.parseInline(src) : marked.parse(src);

  if (typeof document !== 'undefined') {
    const frag = DOMPurify.sanitize(html, {
      RETURN_DOM_FRAGMENT: true,
      ADD_TAGS: ['bdi', 'span', 'br', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'blockquote', 'div'],
      ADD_ATTR: ['dir', 'lang', 'class', 'target', 'rel', 'href'],
    });
    const box = document.createElement('div');
    box.append(frag);
    wrapArabic(box);
    wrapTables(box);
    return box.innerHTML;
  }

  return DOMPurify.sanitize(html, {
    ADD_TAGS: ['bdi', 'span', 'br', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'blockquote', 'div'],
    ADD_ATTR: ['dir', 'lang', 'class', 'target', 'rel', 'href'],
  });
}

export default function MarkdownContent({ content, inline = false, className = "" }) {
  const html = useMemo(() => renderMarkdown(content, { inline }), [content, inline]);

  if (!content) return null;

  const Tag = inline ? 'span' : 'div';
  return (
    <Tag
      className={`prose font-bengali leading-relaxed transition-colors ${className}`}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

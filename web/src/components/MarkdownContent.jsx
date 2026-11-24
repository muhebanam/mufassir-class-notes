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
  return text.replace(
    /\uFD3E([^\uFD3E\uFD3F\r\n]*?[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF][^\uFD3E\uFD3F\r\n]*?)\uFD3F/g,
    '\uFD3F$1\uFD3E'
  );
}

function wrapArabic(root) {
  if (!root) return;

  // 1. Style inline code tags containing Arabic text
  root.querySelectorAll('code').forEach(cd => {
    const text = cd.textContent || '';
    const arReg = getArabicRegex();
    const m = text.match(arReg);
    if (m && m.join('').replace(/\s+/g, '').length >= text.replace(/\s+/g, '').length * 0.6) {
      cd.dir = 'rtl';
      cd.lang = 'ar';
      cd.classList.add('ar-code', 'font-amiri');
    }
  });

  // 2. Automatically apply .ar-block, dir="rtl", and text-right to paragraphs, lists, headings, and quotes
  // consisting primarily or purely of Arabic text so they start from the right
  const blockSelectors = 'p, blockquote, li, div, h1, h2, h3, h4, h5, h6, td, th';
  root.querySelectorAll(blockSelectors).forEach(el => {
    if (el.tagName === 'DIV' && el.querySelector('p, blockquote, table, ul, ol')) return;
    const t = el.textContent || '';
    if (!t.trim()) return;

    const arLetters = (t.match(/[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]/g) || []).length;
    const bnLetters = (t.match(/[\u0980-\u09FF]/g) || []).length;
    const enLetters = (t.match(/[a-zA-Z]/g) || []).length;
    const nonWsLen = t.replace(/\s+/g, '').length;

    // Purely or primarily Arabic:
    // Has >= 3 Arabic letters, Arabic letters exceed Bengali + English, and Arabic >= 35% of non-whitespace
    if (arLetters >= 3 && arLetters > (bnLetters + enLetters) && (arLetters / nonWsLen >= 0.35)) {
      el.classList.add('ar-block', 'text-right');
      el.dir = 'rtl';
      el.lang = 'ar';
      el.style.textAlign = 'right';
      el.style.direction = 'rtl';
    }
  });

  // Orient entire lists where list items are Arabic
  root.querySelectorAll('ul, ol').forEach(list => {
    const items = list.querySelectorAll(':scope > li');
    if (items.length > 0 && Array.from(items).every(li => li.classList.contains('ar-block'))) {
      list.dir = 'rtl';
      list.classList.add('ar-block', 'text-right');
      list.style.textAlign = 'right';
      list.style.direction = 'rtl';
    }
  });

  // 3. TreeWalker for text nodes to isolate Arabic inside <bdi class="ar">
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (w.nextNode()) nodes.push(w.currentNode);

  for (const n of nodes) {
    if (n.parentElement?.closest('bdi.ar, code, pre')) continue;
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
  return (
    <Tag
      className={`prose font-bengali leading-relaxed transition-colors ${className}`}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

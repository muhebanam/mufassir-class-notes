import React, { useMemo } from 'react';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import { getArabicRegex } from '../utils/arabicRegex';

marked.setOptions({
  gfm: true,
  breaks: true,
});

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

  // 2. Automatically apply .ar-block to paragraphs or blockquotes consisting primarily of Arabic
  root.querySelectorAll('p, blockquote').forEach(el => {
    const t = el.textContent || '';
    if (!t.trim()) return;
    const arMatches = t.match(getArabicRegex()) || [];
    const arLen = arMatches.join('').replace(/\s+/g, '').length;
    const totalLen = t.replace(/\s+/g, '').length;
    if (totalLen > 0 && arLen / totalLen >= 0.75) {
      el.classList.add('ar-block');
      el.dir = 'rtl';
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
  const html = inline ? marked.parseInline(src) : marked.parse(src);

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

import React, { useEffect, useRef } from 'react';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

// Regex matching Arabic script, Quranic brackets, quotes, and Arabic punctuation
const AR = /[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF][\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF\s\u064B-\u065F«»“”()،؟﴿﴾]*/g;

/**
 * TreeWalker DOM post-processor:
 * Finds all Arabic text runs and wraps them in isolated RTL elements (<bdi class="ar" lang="ar" dir="rtl">).
 * Ensures Quranic ornate brackets ﴿...﴾ and Arabic citations NEVER reverse in LTR contexts.
 */
function tagArabic(root) {
  if (!root) return;
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (w.nextNode()) nodes.push(w.currentNode);

  for (const n of nodes) {
    if (!n.nodeValue || !AR.test(n.nodeValue)) {
      AR.lastIndex = 0;
      continue;
    }
    AR.lastIndex = 0;

    // Skip if already inside a BDI tag or element with .ar class
    if (n.parentElement && (n.parentElement.tagName === 'BDI' || n.parentElement.classList.contains('ar'))) {
      continue;
    }

    const span = document.createElement('span');
    span.innerHTML = n.nodeValue.replace(AR, (m) => {
      const trimmed = m.trim();
      if (!trimmed) return m;
      return `<bdi class="ar" lang="ar" dir="rtl">${m}</bdi>`;
    });

    n.replaceWith(...span.childNodes);
  }
}

// Configure marked with GFM tables and line breaks
marked.setOptions({
  gfm: true,
  breaks: true,
});

export default function MarkdownContent({ content, className = "" }) {
  const containerRef = useRef(null);

  useEffect(() => {
    if (containerRef.current) {
      tagArabic(containerRef.current);
    }
  }, [content]);

  if (!content) return null;

  const rawHtml = marked.parse(content);
  const cleanHtml = DOMPurify.sanitize(rawHtml, {
    ADD_TAGS: ['bdi', 'span', 'br', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'blockquote'],
    ADD_ATTR: ['dir', 'lang', 'class', 'target', 'rel', 'href'],
  });

  return (
    <div
      ref={containerRef}
      className={`prose font-bengali leading-relaxed transition-colors ${className}`}
      dangerouslySetInnerHTML={{ __html: cleanHtml }}
    />
  );
}

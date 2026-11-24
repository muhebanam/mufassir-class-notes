import React from 'react';

export default function HighlightText({ text, query }) {
  if (!text || !query || !query.trim()) return text;
  const escaped = query.trim().replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const parts = text.split(new RegExp(`(${escaped})`, 'gi'));
  return (
    <>
      {parts.map((part, idx) =>
        part.toLowerCase() === query.trim().toLowerCase() ? (
          <mark
            key={idx}
            className="bg-emerald-200/80 dark:bg-emerald-800/80 text-inherit rounded px-0.5 font-bold"
          >
            {part}
          </mark>
        ) : (
          part
        )
      )}
    </>
  );
}

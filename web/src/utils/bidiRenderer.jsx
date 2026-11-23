import React from 'react';

/**
 * BiDi Text Renderer for Islamic & Quranic Texts
 * Ensures all ornate Quranic brackets ﴿...﴾ and quotes «...»
 * are wrapped in isolated RTL boundaries (<bdi dir="rtl">) so they
 * never render reversed or jumbled on any browser or mobile screen.
 */
export function renderBidiText(text) {
  if (!text) return null;

  // Split by Quranic verse markers ﴿...﴾ or classical quotes «...»
  const regex = /(﴿[^﴾\n]*﴾|«[^»\n]*»)/g;
  const parts = text.split(regex);

  return parts.map((part, index) => {
    if (!part) return null;

    if (part.startsWith('﴿') && part.endsWith('﴾')) {
      return (
        <bdi
          key={index}
          dir="rtl"
          className="font-amiri text-emerald-800 dark:text-emerald-300 font-semibold px-1 py-0.5 rounded bg-emerald-50/50 dark:bg-emerald-950/30 inline-block text-[1.08em] leading-normal"
        >
          {part}
        </bdi>
      );
    }

    if (part.startsWith('«') && part.endsWith('»')) {
      return (
        <bdi
          key={index}
          dir="rtl"
          className="font-amiri text-teal-800 dark:text-teal-300 font-medium px-1 inline-block text-[1.05em] leading-normal"
        >
          {part}
        </bdi>
      );
    }

    return <React.Fragment key={index}>{part}</React.Fragment>;
  });
}

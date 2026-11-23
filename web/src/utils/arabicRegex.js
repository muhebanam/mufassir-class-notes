// Arabic characters, presentation forms, and Quranic diacritics
export const A = '\\u0600-\\u06FF\\u0750-\\u077F\\uFB50-\\uFD3D\\uFD40-\\uFDFF\\uFE70-\\uFEFF';
export const MARK = '\\u064B-\\u065F\\u0670';
export const DIGITS = '0-9\\u0660-\\u0669\\u06F0-\\u06F9';
export const AR_CHAR = `[${A}${MARK}]`;
export const AR_PUNCT = '\\s،؟:؛!\\.\\-–—';

// Strictly Arabic characters, marks, digits, and allowed punctuation inside paired delimiters.
// Excludes Latin (a-zA-Z) and Bengali (\u0980-\u09FF) to prevent over-matching parenthesized references.
const IN_COMMON = `${A}${MARK}${DIGITS}${AR_PUNCT}`;

// Paired Arabic expressions: each pair prevents swallowing its own closing delimiter.
export const PAIRS = [
  `«[${IN_COMMON}“”( )[\\]]*?${AR_CHAR}[${IN_COMMON}“”( )[\\]]*?»`,
  `“[${IN_COMMON}«»( )[\\]]*?${AR_CHAR}[${IN_COMMON}«»( )[\\]]*?”`,
  `﴿[${IN_COMMON}«»“”\\(\\)\\[\\]]*?${AR_CHAR}[${IN_COMMON}«»“”\\(\\)\\[\\]]*?﴾`,
  `\\([${IN_COMMON}«»“”\\[\\]]*?${AR_CHAR}[${IN_COMMON}«»“”\\[\\]]*?\\)`,
  `\\[[${IN_COMMON}«»“”\\(\\)]*?${AR_CHAR}[${IN_COMMON}«»“”\\(\\)]*?\\]`
].join('|');

// Bare Arabic runs (not already enclosed in paired delimiters)
export const BARE = `${AR_CHAR}[${IN_COMMON}]*?${AR_CHAR}|${AR_CHAR}`;

export const AR_REGEX_PATTERN = `(?:${PAIRS})|(?:${BARE})`;

/**
 * Returns a fresh RegExp instance for Arabic matching to avoid mutable lastIndex state issues.
 */
export function getArabicRegex() {
  return new RegExp(AR_REGEX_PATTERN, 'g');
}

export const AR = getArabicRegex();

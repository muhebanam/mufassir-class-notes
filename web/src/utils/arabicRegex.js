// Arabic characters and diacritics
export const A = '\\u0600-\\u06FF\\u0750-\\u077F\\uFB50-\\uFDFF\\uFE70-\\uFEFF';
export const MARK = '\\u064B-\\u065F\\u0670';
export const DIGITS = '0-9\\u0660-\\u0669\\u06F0-\\u06F9';
export const AR_CHAR = `[${A}${MARK}]`;
export const AR_INNER = `[${A}${MARK}${DIGITS}\\s،؟:؛\\-–—«»“”﴿﴾]*`;

// Paired Arabic expressions to prevent mismatched/swallowed closing brackets
export const PAIRS = [
  `«${AR_INNER}${AR_CHAR}${AR_INNER}»`,
  `“${AR_INNER}${AR_CHAR}${AR_INNER}”`,
  `﴿${AR_INNER}${AR_CHAR}${AR_INNER}﴾`,
  `\\(${AR_INNER}${AR_CHAR}${AR_INNER}\\)`,
  `\\[${AR_INNER}${AR_CHAR}${AR_INNER}\\]`
].join('|');

// Bare Arabic runs (not already enclosed in paired delimiters)
export const BARE = `${AR_CHAR}[${A}${MARK}${DIGITS}\\s،؟:؛\\-–—]*${AR_CHAR}|${AR_CHAR}`;

export const AR_REGEX_PATTERN = `(?:${PAIRS})|(?:${BARE})`;

export function getArabicRegex() {
  return new RegExp(AR_REGEX_PATTERN, 'g');
}

export const AR = getArabicRegex();

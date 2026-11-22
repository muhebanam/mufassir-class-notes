// Bengali and Arabic numeral conversion
const bnDigits = "০১২৩৪৫৬৭৮৯";
const enDigits = "0123456789";

export function toBn(num) {
  if (num === null || num === undefined) return "";
  return String(num).replace(/[0-9]/g, (d) => bnDigits[d]);
}

export function toEn(str) {
  if (!str) return "";
  return String(str).replace(/[০-৯]/g, (d) => bnDigits.indexOf(d));
}

// Normalize Arabic text for instant searching (removes harakat, tanween, dagger alif)
export function normalizeArabic(text) {
  if (!text) return "";
  return text
    .replace(/[\u064B-\u065F\u0670\u06D6-\u06DC\u06DF-\u06E8\u06EA-\u06ED]/g, "")
    .replace(/[أإآٱ]/g, "ا")
    .replace(/[ى]/g, "ي")
    .replace(/[ة]/g, "ه")
    .trim();
}

// Normalize Bengali text for searching (removes punctuation, extra spaces)
export function normalizeBengali(text) {
  if (!text) return "";
  return text
    .toLowerCase()
    .replace(/[।,;:!?"'’‘\-–—(){}\[\]]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

// Copy text to clipboard with fallback
export async function copyToClipboard(text) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return true;
    } else {
      const textArea = document.createElement("textarea");
      textArea.value = text;
      textArea.style.position = "fixed";
      textArea.style.left = "-999999px";
      textArea.style.top = "-999999px";
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      const successful = document.execCommand("copy");
      textArea.remove();
      return successful;
    }
  } catch (err) {
    console.error("Copy failed", err);
    return false;
  }
}

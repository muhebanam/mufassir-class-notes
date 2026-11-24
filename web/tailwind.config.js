/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        paper: {
          bg: '#faf9f6',
          ink: '#1f2933',
          card: '#ffffff',
          line: '#e5e7eb',
          accent: '#0f5132',
          amber: '#b45309',
        },
        sepia: {
          bg: '#f4ecd8',
          ink: '#3e3529',
          card: '#ede2cf',
          line: '#dccdb4',
          accent: '#8b5e34',
          muted: '#6b5e4f',
        },
        academicDark: {
          bg: '#121518',
          card: '#1b2026',
          ink: '#e2e8f0',
          line: '#2d3748',
          accent: '#34d3be',
        },
        islamic: {
          emerald: '#0f5132',
          gold: '#b45309',
          teal: '#004d40',
        }
      },
      fontFamily: {
        quran: ['"Amiri Quran"', '"Scheherazade New"', '"Amiri"', 'serif'],
        amiri: ['"Amiri"', '"Scheherazade New"', '"Traditional Arabic"', '"Segoe UI"', 'serif'],
        arabic: ['"Amiri"', '"Scheherazade New"', '"Traditional Arabic"', '"Segoe UI"', 'serif'],
        bengali: ['"Noto Serif Bengali"', '"Hind Siliguri"', 'serif'],
        sans: ['"Hind Siliguri"', '"Noto Sans Bengali"', 'sans-serif'],
      },
      maxWidth: {
        'reading': '740px',
        'study': '1100px',
        'mushaf': '800px',
      }
    },
  },
  plugins: [],
}

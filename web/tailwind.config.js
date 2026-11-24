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
        sepia: {
          50: '#faf8f5',
          100: '#f5f0e6',
          200: '#ede0cc',
          300: '#e3ceb0',
          800: '#4a3b2c',
          900: '#2e2419',
        },
        islamic: {
          green: '#1b5e20',
          gold: '#c59b27',
          teal: '#004d40',
        }
      },
      fontFamily: {
        amiri: ['"Amiri Quran"', '"Scheherazade New"', 'serif'],
        arabic: ['"Amiri Quran"', '"Scheherazade New"', 'serif'],
        bengali: ['"Noto Serif Bengali"', '"Hind Siliguri"', 'sans-serif'],
      }
    },
  },
  plugins: [],
}

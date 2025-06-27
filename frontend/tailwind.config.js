/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'dhikra-green': '#059669',
        'dhikra-dark': '#064e3b',
        'dhikra-light': '#d1fae5',
      },
      fontFamily: {
        'arabic': ['Amiri', 'serif'],
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
} 
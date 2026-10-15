/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,css}", "./projects/*.html", "./*.html", "./menu.html"],
  safelist: ['invisible'],
  theme: {
    extend: {
      fontFamily: {
        'body': ['"Berlin Type"', '"IBM Plex Sans"', 'sans-serif']
      },
      aspectRatio: {
        'ipad-l': '4/3',
        'ipad11-l': '10/7',
        'ipad11-p': '7/10',
        'iphonex-l': '13/6',
        'iphonex-p': '6/13',
        'tablet-l':'128/75',
      },
      gridTemplateColumns: {
        'profile': '7rem auto',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ]
}

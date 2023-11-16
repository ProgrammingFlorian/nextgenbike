/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
    colors: {
      black: "#000000",
      gray: "#9CA3AF",
      white: "#FFFFFF",
      green: {
        100: "EFFFEF",
        500: "#09B617",
      },
      orange: {
        100: "#FFF7EF",
        500: "#FBA04C",
      },
      red: {
        100: "#FFEDED",
        500: "#FF4949",
      },
      indigo: {
        100: "#EFE7FD",
        500: "#3400E1",
      }
    },
    fontFamily: {
      sans: ['Manrope', 'sans-serif']
    }
  },
  plugins: [],
}
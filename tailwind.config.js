/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./chat_doc/app/templates/*.html",
    "./chat_doc/app/templates/**/*.html",
    "./chat_doc/app/static/src/**/*.js",
    "./chat_doc/app/static/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/typography"),
    require("daisyui")
  ],
  daisyui: {
    themes: ["light", "dark", "cupcake", "emerald", "cyberpunk", "dracula"],
  },
}

// BATCH SIZE INCREASE
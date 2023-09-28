/** @type {import("tailwindcss").Config} */
const colors = require("tailwindcss/colors")

module.exports = {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./nuxt.config.{js,ts}",
    "./node_modules/vue-tailwind-datepicker/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        teal: colors.teal,
        cyan: colors.cyan,
        rose: colors.rose,
        spring: {
            "50": "#f1f8f1",
            "100": "#dfedde",
            "200": "#bfdbbf",
            "300": "#95c098",
            "400": "#609966",
            "500": "#46834f",
            "600": "#34673c",
            "700": "#295331",
            "800": "#234229",
            "900": "#1d3722",
            "950": "#101e14",
        },
        "vtd-primary": {
            "50": "#f1f8f1",
            "100": "#dfedde",
            "200": "#bfdbbf",
            "300": "#95c098",
            "400": "#609966",
            "500": "#46834f",
            "600": "#34673c",
            "700": "#295331",
            "800": "#234229",
            "900": "#1d3722",
        }, // Light mode Datepicker color
        "vtd-secondary": colors.gray, // Dark mode Datepicker color
      },
    },
  },
  corePlugins: {
    aspectRatio: false,
  },
  plugins: [
    require("@tailwindcss/typography"),
    require("@tailwindcss/forms"),
    require("@tailwindcss/aspect-ratio"),
  ],
}

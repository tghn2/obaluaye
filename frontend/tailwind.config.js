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
        "cerise": {
            "50": "#fef2f3",
            "100": "#fde6e7",
            "200": "#fbd0d5",
            "300": "#f7aab2",
            "400": "#f27a8a",
            "500": "#ea546c",
            "600": "#d5294d",
            "700": "#b31d3f",
            "800": "#961b3c",
            "900": "#811a39",
            "950": "#48091a",
        },
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
        kashmir: {
            "50": "#f4f8fa",
            "100": "#e6eef3",
            "200": "#d2e1eb",
            "300": "#b4cddc",
            "400": "#8fb3cb",
            "500": "#749bbd",
            "600": "#6285ae",
            "700": "#5a79a5",
            "800": "#4b6082",
            "900": "#3f5069",
            "950": "#2a3241",
        },            
        "vtd-primary": {
            "50": "#f4f8fa",
            "100": "#e6eef3",
            "200": "#d2e1eb",
            "300": "#b4cddc",
            "400": "#8fb3cb",
            "500": "#749bbd",
            "600": "#6285ae",
            "700": "#5a79a5",
            "800": "#4b6082",
            "900": "#3f5069",
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

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
            "50": "#fdf2f9",
            "100": "#fbe8f4",
            "200": "#fad0ea",
            "300": "#f7aad8",
            "400": "#f076bc",
            "500": "#e74da0",
            "600": "#d93e8a",
            "700": "#b91d65",
            "800": "#991b54",
            "900": "#801b49",
            "950": "#4e0927",
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

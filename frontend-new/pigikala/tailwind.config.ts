import type { Config } from "tailwindcss";
import daisyui from "daisyui";

export default {
  darkMode: "selector",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
      fontFamily: {
        vazir: ["var(--font-vazir-matn)"],
        inter: ["var(--font-inter)"],
      },
    },
  },
  plugins: [daisyui],
  daisyui: {
    themes: ["light", "night", "dim", "dark"],
  },
} satisfies Config;

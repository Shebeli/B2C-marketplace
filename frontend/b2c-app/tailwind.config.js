import daisyui from "daisyui";
import scrollbar from "tailwind-scrollbar";

export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [scrollbar, daisyui ],
  daisyui: {
    themes: [
      "light",
      "night",
      {
        sherdark: {
          primary: "#1e40af",

          secondary: "#14532d",

          accent: "#00ffff",

          neutral: "#374151",

          "base-100": "#1f2937",

          info: "#93c5fd",

          success: "#22c55e",

          warning: "#f59e0b",

          error: "#ef4444",
        },
      },
    ],
  },
};

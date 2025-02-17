import { Vazirmatn, Inter } from "next/font/google";

export const vazirMatn = Vazirmatn({
  subsets: ["latin"],
  weight: "400",
  display: "swap",
  variable: "--font-vazir-matn",
});

export const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

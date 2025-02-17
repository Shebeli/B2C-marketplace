import type { Metadata } from "next";
import { ThemeProvider } from "next-themes";
import { inter, vazirMatn } from "./ui/fonts";
import "./ui/globals.css";

export const metadata: Metadata = {
  title: "%s | Pigikala",
  description: "Pigikala is a B2C multivendor platform.",
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" dir="rtl">
      <body
        className={`${vazirMatn.variable} font-inter ${inter.variable} font-vazir`}
      >
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}

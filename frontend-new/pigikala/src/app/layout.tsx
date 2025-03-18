import type { Metadata } from "next";
import { ThemeProvider } from "next-themes";
import { inter, vazirMatn } from "./ui/fonts";
import "./ui/globals.css";
import { Toaster } from "react-hot-toast";
import { NuqsAdapter } from "nuqs/adapters/next/app";

export const metadata: Metadata = {
  title: "%s | Pigikala",
  description: "Pigikala is a B2C multivendor platform.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" dir="rtl" suppressHydrationWarning>
      <body
        className={`font-vazir ${vazirMatn.variable}  font-inter ${inter.variable}`}
      >
        <Toaster />
        <NuqsAdapter>
          <ThemeProvider attribute="data-theme">{children}</ThemeProvider>
        </NuqsAdapter>
      </body>
    </html>
  );
}

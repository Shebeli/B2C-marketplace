import { createContext } from "react";

export interface ThemeContextType {
  theme: ThemeType;
  toggleTheme: () => void;
}

export const ThemeContext = createContext<ThemeContextType | undefined>(
  undefined
);

export const THEMES = {
  LIGHT: "light",
  DARK: "dark",
} as const;

export type ThemeType = (typeof THEMES)[keyof typeof THEMES];

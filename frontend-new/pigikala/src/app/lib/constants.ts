export interface NavbarProfileInfo {
  phone: string;
  pictureUrl: string | null;
}

export const alertTypes = ["error", "info", "success", "warning"] as const;

export interface AlertData {
  message: string;
  type: (typeof alertTypes)[number];
}

export const usernamePattern =
  /^(?=[a-zA-Z])(?=(?:[^a-zA-Z]*[a-zA-Z]){3})\w{4,}$/;

export interface colorChoice {
  name: string;
  value: string; // color hex codes
}

export interface priceRange {
  min: number;
  max: number;
}

export interface productGenericFilters {
  category: string; // has to be provided
  priceRange: priceRange;
  color: colorChoice | null;
  isAvailable: boolean;
  canDeliverToday: boolean;
}

export const defaultProductFilters = {
  category: "",
  priceRange: { min: 0, max: 1000000000 },
  color: null,
  isAvailable: false,
  canDeliverToday: false,
};

export const sortOptions = [
  "جدید ترین",
  "ارزان ترین",
  "گران ترین",
  "پربازدید ترین",
]; // hardcoded temporarily as a constant, might be variable in production.
// export type SortType = (typeof sortOptions)[number];

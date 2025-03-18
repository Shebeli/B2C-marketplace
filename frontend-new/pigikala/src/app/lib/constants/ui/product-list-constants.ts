// Product sorting
export const productSortOptions = [
  { name: "گران ترین", value: "-main_price" },
  { name: "ارزان ترین", value: "main_price" },
  { name: "بالاترین امتیاز", value: "rating" },
  { name: "جدیدترین", value: "created_at" },
  { name: "بیشترین بازدید", value: "view_count" },
  { name: "موجود در انبار", value: "in_stock" },
  { name: "بیشترین فروش", value: "total_number_sold" },
] as const;

export const sortOptions = [
  "main_price",
  "-main_price",
  "rating",
  "created_at",
  "view_count",
  "in_stock",
  "total_number_sold",
] as const;

export type ProductSort = (typeof sortOptions)[number];

export const defaultSortOption = {
  name: "جدید ترین",
  value: "created_at",
};

export const FILTER_MAX_PRICE = 1000000000;

export const defaultFilterOptions = {
  isAvailable: false,
  canDeliverToday: false,
  priceMin: 0,
  priceMax: FILTER_MAX_PRICE,
  selectedColors: [],
};
export const filterKeys = [
  "isAvailable",
  "canDeliverToday",
  "priceMin",
  "priceMax",
  "selectedColors",
] as const;

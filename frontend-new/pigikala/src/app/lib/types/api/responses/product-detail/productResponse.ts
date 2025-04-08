// Generic interfaces or types which are shared between both the APIs and UIs
// don't have API or UI as a prefix to their name, which means its used both by
// either API interfaces and UI interfaces.

export interface TechnicalDetail {
  attribute: string;
  value: string;
}

export interface ProductOwner {
  id: string;
  storeName: string;
  storeImage: string;
}

export interface Breadcrumb {
  subCategory: string;
  category: string;
  mainCategory: string;
}

interface ProductVariant {
  id: number;
  name: string;
  price: number;
  images: string[];
  color: string | "";
}

export interface ProductOwner {
  id: string;
  storeName: string;
  storeImage: string;
}

export interface ApiProductDetail {
  id: number;
  technicalDetails: TechnicalDetail[];
  variants: ProductVariant[];
  owner: ProductOwner;
  ratingAvg: number;
  ratingCount: number;
  name: string;
  description: string;
  breadCrumb: Breadcrumb;
}

import { PaginatedResponse } from "./generalResponses";

/**
 *
 */
export interface ProductListItemResponse {
  id: number;
  name: string;
  mainPrice: number;
  mainImage: string | null;
  sellerProfile: sellerInfo;
}

export interface sellerInfo {
  storeName: string;
  storeImage: string | null;
  storeUrl: string;
}

/**
 * the name of subcategories are not unique, resort to id rather than name.
 */
export interface SubCategoryResponse {
  id: number;
  name: string;
}

export interface BreadCrumbResponse {
  subCategory: string;
  category: string;
  mainCategory: string;
}

export type ProductListPaginatedResponse =
  PaginatedResponse<ProductListItemResponse>;

"use server";

import { ProductSort } from "../constants/ui/product-list-constants";
import { API_ROUTES } from "../apiRoutes";
import { ProductGenericFilters } from "../types/ui/product-list-types";
import { api } from "../fetch/fetch-wrapper";
import {
  BreadCrumbResponse,
  ProductListResponse,
} from "../types/api/responses/product-list-responses";
import { transformKeysToSnakeCase } from "../utils/product-list-helpers/product-list-helpers";

const { PRODUCT: PRODUCT_ROUTES } = API_ROUTES;

/**
 * For fetching the subcategory name based on ID
 */
export async function fetchBreadCrumb(id: number) {
  return await api.get<BreadCrumbResponse>(
    `${PRODUCT_ROUTES.SUB_CATEGORIES}${id}`
  );
}

export async function fetchProducts({
  subCategoryId,
  sort,
  genericFilters,
  page,
}: {
  subCategoryId: number;
  sort: ProductSort;
  genericFilters: Partial<ProductGenericFilters>;
  page: number;
}) {
  // construct the query params in a way that the endpoint is expecting
  const queryParams = {
    subcategory: subCategoryId,
    ordering: sort,
    page,
    ...genericFilters,
  };

  
  
  return await api.get<ProductListResponse>(PRODUCT_ROUTES.PRODUCTS_LIST, {
    params: transformKeysToSnakeCase(queryParams),
    revalidate: 60,
  });
}
  
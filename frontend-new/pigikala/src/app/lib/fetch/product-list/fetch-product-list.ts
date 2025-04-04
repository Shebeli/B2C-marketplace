"use server";

import { ProductSort } from "../../constants/ui/productListConstants";
import { API_ROUTES } from "../../apiRoutes";
import { ProductGenericFilters } from "../../types/ui/productListTypes";
import { api } from "../fetchWrapper";
import {
  BreadCrumbResponse,
  ProductListPaginatedResponse,
} from "../../types/api/responses/productListResponses";
import { transformKeysToSnakeCase } from "../../utils/product-list-helpers/productListHelpers";

const { PRODUCT: PRODUCT_ROUTES } = API_ROUTES;

/**
 * For fetching the breadcrumb name via the passed in subcategory's id.
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

  return await api.get<ProductListPaginatedResponse>(
    PRODUCT_ROUTES.PRODUCTS_LIST,
    {
      params: transformKeysToSnakeCase(queryParams),
      revalidate: 60,
    }
  );
}

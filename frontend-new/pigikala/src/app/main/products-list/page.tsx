import { productSortOptions } from "@/app/lib/constants/ui/productListConstants";
import { isFailedResponse } from "@/app/lib/fetch/fetchWrapper";
import { fetchBreadCrumb } from "@/app/lib/fetch/product-list/fetch-product-list";
import { ProductQueryParamsSchema } from "@/app/lib/schemas/productListSchemas";
import { ProductGenericFilters } from "@/app/lib/types/ui/productListTypes";
import CategoryBreadcrumb from "@/app/ui/breadcrumbs";
import ProductFilter from "@/app/ui/product-list/filter/product-filter";
import sampleColorChoices from "@/app/ui/product-list/placeholder";
import ProductListDisplay from "@/app/ui/product-list/product-list-display";
import ProductListSortDropdown from "@/app/ui/product-list/sort-dropdown";
import { BreadCrumbSkeleton, ProductsListSkeleton } from "@/app/ui/skeletons";
import { Metadata } from "next";
import { Suspense } from "react";
import "react-range-slider-input/dist/style.css";
import { ZodError } from "zod";
import { ApiError, QueryParamError } from "../customError";

export const metadata: Metadata = {
  title: "Products List",
};

export default async function ProductListPage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  let validatedParams;

  // Parse the query params and prepare the data for fetching
  try {
    const paramResults = await searchParams;
    validatedParams = ProductQueryParamsSchema.parse(paramResults);
  } catch (error) {
    throw new QueryParamError({
      details: error instanceof ZodError ? error.message : "Unknown error",
    });
  }

  // given subcategory should be valid for product list fetching
  const breadCrumbFetchResult = await fetchBreadCrumb(
    validatedParams.subCategoryId
  );
  if (isFailedResponse(breadCrumbFetchResult)) {
    throw new ApiError({
      ...breadCrumbFetchResult,
      userMessage:
        breadCrumbFetchResult.status == 404
          ? "دسته بندی مد نظر یافت نشد."
          : breadCrumbFetchResult.userMessage,
    });
  }

  // transform generic filters for fetching
  const genericFiltersData: ProductGenericFilters = {
    priceMin: validatedParams.priceMin,
    priceMax: validatedParams.priceMax,
    isAvailable: validatedParams.isAvailable,
    canDeliverToday: validatedParams.canDeliverToday,
  };

  // Get available color choices by fetching the color options for given subCategoryId
  const availableColorChoices = sampleColorChoices;

  return (
    <>
      <div className="max-w-(--breakpoint-2xl) flex flex-col px-3 py-2 mb-4 w-full gap-3">
        <Suspense fallback={<BreadCrumbSkeleton />}>
          <CategoryBreadcrumb subCategoryId={validatedParams.subCategoryId} />
        </Suspense>
        <div className="flex gap-2">
          <ProductFilter colorChoices={availableColorChoices} />
          <div className="flex-col w-full">
            <ProductListSortDropdown sortOptions={productSortOptions} />
            <Suspense
              key={JSON.stringify(validatedParams)}
              fallback={<ProductsListSkeleton />}
            >
              <ProductListDisplay
                subCategoryId={validatedParams.subCategoryId}
                sort={validatedParams.sort}
                page={validatedParams.page}
                genericFilters={genericFiltersData}
              />
            </Suspense>
          </div>
        </div>
      </div>
    </>
  );
}

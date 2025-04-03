import { productSortOptions } from "@/app/lib/constants/ui/productListConstants";
import { ProductQueryParamsSchema } from "@/app/lib/schemas/productListSchemas";
import { ProductGenericFilters } from "@/app/lib/types/ui/productListTypes";
import CategoryBreadcrumb from "@/app/ui/breadcrumbs";
import ProductFilter from "@/app/ui/product-list/filter/product-filter";
import sampleColorChoices from "@/app/ui/product-list/placeholder";
import ProductListDisplay from "@/app/ui/product-list/product-list-display";
import ProductListSortDropdown from "@/app/ui/product-list/sort-dropdown";
import { BreadCrumbSkeleton, ProductsListSkeleton } from "@/app/ui/skeletons";
import { Suspense } from "react";
import "react-range-slider-input/dist/style.css";
import { ZodError } from "zod";
import { Metadata } from "next";
import { fetchBreadCrumb } from "@/app/lib/fetch/product-list/fetch-product-list";
import { isError } from "@/app/lib/fetch/fetchWrapper";
import { details } from "@/app/ui/product-page/placeholder-data";

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
    console.error(
      "Error when parsing query params with zod in product list component",
      error instanceof ZodError ? error.format() : "Unknown error"
    );
    throw new Error(
      JSON.stringify({
        status: 400,
        message: "مشکلی در دریافت لیست کالا ها پیش آمده است",
        details: error instanceof ZodError ? error.format() : "Unknown error",
      })
    );
  }

  // validate if the given subcategory ID
  const subCategoryBreadCrumbResult = await fetchBreadCrumb(
    validatedParams.subCategoryId
  );
  if (isError(subCategoryBreadCrumbResult)) {
    throw new Error(
      JSON.stringify({
        status: 404,
        message: "دسته بندی مورد نظر یافت نشد. 😵",
        details: subCategoryBreadCrumbResult.details,
      })
    );
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

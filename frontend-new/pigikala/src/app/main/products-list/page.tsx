import { productSortOptions } from "@/app/lib/constants/ui/product-list-constants";
import { ProductQueryParamsSchema } from "@/app/lib/schemas/product-list-schemas";
import { ProductGenericFilters } from "@/app/lib/types/ui/product-list-types";
import CategoryBreadcrumb from "@/app/ui/breadcrumbs";
import ProductFilter from "@/app/ui/product-list/filter/product-filter";
import sampleColorChoices from "@/app/ui/product-list/placeholder";
import ProductListDisplay from "@/app/ui/product-list/product-list-display";
import ProductListPagination from "@/app/ui/product-list/product-list-pagination";
import ProductListSortDropdown from "@/app/ui/product-list/sort-dropdown";
import { BreadCrumbSkeleton, ProductsListSkeleton } from "@/app/ui/skeletons";
import { Suspense } from "react";
import "react-range-slider-input/dist/style.css";
import { ZodError } from "zod";

export default async function ProductListPage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  let validatedParams;

  // 1) Parse the query params and prepare the data for fetching
  // 2) Call the fetches in proper ordering
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

  // transform the filters for fetching
  const genericFiltersData: ProductGenericFilters = {
    priceMin: validatedParams.priceMin,
    priceMax: validatedParams.priceMax,
    isAvailable: validatedParams.isAvailable,
    canDeliverToday: validatedParams.canDeliverToday,
  };

  // Fetch the products

  // Get available color choices by fetching the color options for given subCategoryId
  const availableColorChoices = sampleColorChoices;

  return (
    <>
      <div className="max-w-(--breakpoint-2xl) flex flex-col p-2 w-full gap-3">
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
        <ProductListPagination />
      </div>
    </>
  );
}

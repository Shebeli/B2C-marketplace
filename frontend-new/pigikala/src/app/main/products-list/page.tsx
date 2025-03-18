import {
  fetchBreadCrumb,
  fetchProducts,
} from "@/app/lib/actions/product-list-actions";
import { productSortOptions } from "@/app/lib/constants/ui/product-list-constants";
import { isError } from "@/app/lib/fetch/fetch-wrapper";
import { ProductQueryParamsSchema } from "@/app/lib/schemas/product-list-schemas";
import { ProductGenericFilters } from "@/app/lib/types/ui/product-list-types";
import CategoryBreadcrumb from "@/app/ui/breadcrumbs";
import sampleColorChoices from "@/app/ui/product-list/placeholder";
import ProductListMain from "@/app/ui/product-list/product-list-main";
import "react-range-slider-input/dist/style.css";
import { ZodError } from "zod";

export default async function ProductListPage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  let productsListResponse;
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

  // fetch breadcrumb data
  const categoryBreadCrumbResult = await fetchBreadCrumb(
    validatedParams.subCategoryId
  );

  // transform the filters for fetching
  const genericFiltersData: ProductGenericFilters = {
    minPrice: validatedParams.minPrice,
    maxPrice: validatedParams.maxPrice,
    isAvailable: validatedParams.isAvailable,
    canDeliverToday: validatedParams.canDeliverToday,
  };

  // Fetch the products
  try {
    productsListResponse = await fetchProducts({
      subCategoryId: validatedParams.subCategoryId,
      sort: validatedParams.sort,
      page: validatedParams.page,
      genericFilters: genericFiltersData,
    });

    if (isError(productsListResponse)) {
      console.error("Error when fetching product list from the server");
      throw new Error(JSON.stringify(productsListResponse));
    }
  } catch (error) {
    console.error(
      "An unexpected error has occured when fetching product list:",
      error
    );
    throw new Error(
      JSON.stringify({
        status: 500,
        message: "یک خطای غیر منتظره پیش آمده است.",
        details: "Unexpected error",
      })
    );
  }

  // Get available color choices by fetching the color options for given subCategoryId
  const availableColorChoices = sampleColorChoices;

  return (
    <>
      <div className="max-w-(--breakpoint-2xl) flex flex-col p-2 w-full">
        <CategoryBreadcrumb breadcrumbsResult={categoryBreadCrumbResult} />
        <ProductListMain
          colorChoices={availableColorChoices}
          sortOptions={productSortOptions}
          products={productsListResponse.results}
        />
        {/* Pagination */}
        <div className="join self-center my-5">
          <input
            className="join-item btn btn-square"
            type="radio"
            name="options"
            aria-label="1"
            defaultChecked
          />
          <input
            className="join-item btn btn-square"
            type="radio"
            name="options"
            aria-label="2"
          />
          <input
            className="join-item btn btn-square"
            type="radio"
            name="options"
            aria-label="3"
          />
          <input
            className="join-item btn btn-square"
            type="radio"
            name="options"
            aria-label="4"
          />
        </div>
      </div>
    </>
  );
}

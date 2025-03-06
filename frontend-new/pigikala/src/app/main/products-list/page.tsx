import {
  fetchBreadCrumb,
  fetchProducts,
} from "@/app/lib/actions/product-list-actions";
import { productSortOptions } from "@/app/lib/constants/ui/product-list-constants";
import {
  ColorFilterOption,
  ProductGenericFilters,
} from "@/app/lib/types/ui/product-list-types";
import { isError } from "@/app/lib/fetch/fetch-wrapper";
import { ProductQueryParamsSchema } from "@/app/lib/schemas/product-list-schemas";
import CategoryBreadcrumb from "@/app/ui/breadcrumbs";
import ProductListMain from "@/app/ui/product-list/header";
import sampleColorChoices from "@/app/ui/product-list/placeholder";
import "react-range-slider-input/dist/style.css";
import { ZodError } from "zod";

export default async function ProductListPage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  let productsListResponse;
  let validatedParams;

  // parse the query params
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

  // data transformation
  const genericFiltersData: ProductGenericFilters = {
    minPrice: validatedParams.minPrice,
    maxPrice: validatedParams.maxPrice,
    isAvailable: validatedParams.isAvailable,
    canDeliverToday: validatedParams.canDeliverToday,
  };

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

  // TODO: fetch color choices from the server and validate the current selected color choices based on the fetch results
  const availableColorChoices = sampleColorChoices;
  const selectedColors = validatedParams.selectedColors;

  // Instead of array lookups, we transform the array to a set which will result in O(m+n) complexity instead of O(m*n). (m =< n)
  const selectedColorsSet = new Set(selectedColors);

  const colorFilterOptions: ColorFilterOption[] = availableColorChoices.map(
    (colorChoice) => {
      return {
        ...colorChoice,
        selected: selectedColorsSet.has(colorChoice.value),
      };
    }
  );


  return (
    <>
      <div className="max-w-screen-2xl flex flex-col p-2 w-full">
        <CategoryBreadcrumb breadcrumbsResult={categoryBreadCrumbResult} />
        <ProductListMain
          initialGenericFilters={genericFiltersData}
          initialColorFilterOptions={colorFilterOptions}
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

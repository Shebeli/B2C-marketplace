import { ProductListItemResponse } from "@/app/lib/types/api/responses/product-list-responses";
import ProductCard from "./product-card";
import { isError } from "@/app/lib/fetch/fetch-wrapper";
import { fetchProducts } from "@/app/lib/actions/product-list-actions";

export default async function ProductListDisplay({
  subCategoryId, sort, page, genericFilters
}: {
  products: ProductListItemResponse[];
}) {
  let productsListResponse;
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

  return (
    <div>
      <div className="grid 2xl:grid-cols-5 xl:grid-cols-4 lg:grid-cols-3 md:grid-cols-2 sm:grid-cols-1 gap-4 my-6">
        {products.map((product) => (
          <ProductCard
            key={product.id}
            id={product.id}
            name={product.name}
            image={product.mainImage}
            price={product.mainPrice}
            sellerName={product.seller.storeName}
            sellerPic={product.seller.storeImage}
            sellerStoreUrl={product.seller.storeUrl}
          />
        ))}
      </div>
    </div>
  );
}

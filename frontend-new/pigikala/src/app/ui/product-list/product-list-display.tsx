import ProductCard from "./product-card";
import { isError } from "@/app/lib/fetch/fetch-wrapper";
import { fetchProducts } from "@/app/lib/actions/product-list-actions";
import { ProductGenericFilters } from "@/app/lib/types/ui/product-list-types";
import { ProductSort } from "@/app/lib/constants/ui/product-list-constants";
import ProductListPagination from "./product-list-pagination";

export default async function ProductListDisplay({
  subCategoryId,
  sort,
  page,
  genericFilters,
}: {
  subCategoryId: number;
  sort: ProductSort;
  page: number;
  genericFilters: ProductGenericFilters;
}) {
  const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));

  await delay(1500);

  let productsListResponse;
  try {
    productsListResponse = await fetchProducts({
      subCategoryId: subCategoryId,
      sort: sort,
      page: page,
      genericFilters: genericFilters,
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

  const productCards = productsListResponse.results.map((product) => (
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
  ));

  return (
    <div>
      {productCards.length !== 0 ? (
        <div className="grid 2xl:grid-cols-5 xl:grid-cols-4 lg:grid-cols-3 md:grid-cols-2 sm:grid-cols-1 gap-4 my-6">
          {productCards}
        </div>
      ) : (
        <div className="card w-full self-center justify-self-center my-8">
          <div className="card-body items-center text-center flex gap-8">
            <h2 className="card-title text-3xl">کالایی یافت نشد! 😥</h2>
            <p className="text-xl">سعی در تغییر پارامتر های فیلتر خود دهید!</p>
          </div>
        </div>
      )}
      <ProductListPagination itemTotalCount={productsListResponse.count} />
    </div>
  );
}

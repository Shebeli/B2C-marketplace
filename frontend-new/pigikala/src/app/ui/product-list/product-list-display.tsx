import { ProductSort } from "@/app/lib/constants/ui/productListConstants";
import { isFailedResponse } from "@/app/lib/services/api/fetch/fetchWrapper";
import { fetchProducts } from "@/app/lib/services/api/fetch/product-list/fetchProductList";
import { ProductGenericFilters } from "@/app/lib/types/ui/productListTypes";
import { ApiError } from "@/app/main/customError";
import ProductCard from "./product-card";
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
  // artificial delay for displaying skeleton for test purposes
  const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));
  await delay(1500);

  const productsFetchResult = await fetchProducts({
    subCategoryId: subCategoryId,
    sort: sort,
    page: page,
    genericFilters: genericFilters,
  });

  if (isFailedResponse(productsFetchResult)) {
    throw new ApiError({
      ...productsFetchResult,
    });
  }

  const productCards = productsFetchResult.results.map((product) => (
    <ProductCard
      key={product.id}
      id={product.id}
      name={product.name}
      image={product.mainImage}
      price={product.mainPrice}
      sellerName={product.sellerProfile.storeName}
      sellerPic={product.sellerProfile.storeImage}
      sellerStoreUrl={product.sellerProfile.storeUrl}
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
      <ProductListPagination itemTotalCount={productsFetchResult.count} />
    </div>
  );
}

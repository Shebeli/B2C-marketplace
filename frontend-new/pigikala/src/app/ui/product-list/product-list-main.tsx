"use client";

import { ProductListItemResponse } from "@/app/lib/types/api/responses/productListResponses";
import { ColorChoice, SortChoice } from "@/app/lib/types/ui/productListTypes";
import { useState } from "react";
import { FaFilter } from "react-icons/fa6";
import ProductFilterOptions from "./filter/product-filters";
import FilterProvider from "./filter/filter-provider";
import ProductCard from "./product-card";
import ProductListSortDropdown from "./sort-dropdown";

// The generic filters are static.
export default function ProductListMain({
  colorChoices,
  sortOptions,
  products,
}: {
  colorChoices: ColorChoice[];
  sortOptions: readonly SortChoice[];
  products: ProductListItemResponse[];
}) {
  const [toggleFilters, setToggleFilters] = useState<boolean>(true);

  return (
    <FilterProvider colorChoices={colorChoices}>
      <div className="my-2 flex items-center gap-1">
        <button
          className="md:tooltip md:tooltip-left cursor-pointer btn btn- btn-circle justify-items-center"
          data-tip="فیلتر ها"
          aria-label="Toggle filters"
          onClick={() => setToggleFilters(!toggleFilters)}
        >
          <FaFilter className="size-7 text-primary" />
        </button>
      </div>
      <div className="flex gap-2">
        {/* Filter */}
        <div
          className={`overflow-hidden ${
            toggleFilters ? "w-full min-w-52 max-w-60" : "w-0 opacity-0"
          }`}
        >
          {toggleFilters && <ProductFilterOptions />}
        </div>

        {/* Sort dropdown and products */}
        <div className="flex-col">
          {/* Sort drop down*/}
          <ProductListSortDropdown sortOptions={sortOptions} />

          <div>
            <div className="grid 2xl:grid-cols-5 xl:grid-cols-4 lg:grid-cols-3 md:grid-cols-2 sm:grid-cols-1 gap-4 my-6">
              {products.map((product) => (
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
              ))}
            </div>
          </div>
        </div>
      </div>
    </FilterProvider>
  );
}

"use client";

import {
  ColorFilterOption,
  ProductGenericFilters,
  SortChoice,
} from "@/app/lib/types/ui/product-list-types";
import { ProductListItemResponse } from "@/app/lib/types/api/responses/product-list-responses";
import { useState } from "react";
import { FaFilter } from "react-icons/fa6";
import ProductFilters from "./filter";
import ProductCard from "./product-card";
import ProductListSortDropdown from "./sort-dropdown";

export default function ProductListMain({
  initialGenericFilters,
  initialColorFilterOptions,
  sortOptions,
  products,
}: {
  initialColorFilterOptions: ColorFilterOption[];
  initialGenericFilters: ProductGenericFilters;
  sortOptions: readonly SortChoice[];
  products: ProductListItemResponse[];
}) {
  const [toggleFilters, setToggleFilters] = useState<boolean>(true);

  return (
    <>
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
          className={`overflow-hidden transition-all duration-300 ease-in-out ${
            toggleFilters
              ? "w-full min-w-56 max-w-64 opacity-100 transform translate-x-0"
              : "w-0 opacity-0 transform -translate-x-20"
          }`}
        >
          {toggleFilters && (
            <ProductFilters
              initialGenericFilters={initialGenericFilters}
              initialColorFilterOptions={initialColorFilterOptions}
            />
          )}
        </div>

        <div className="flex-col">
          {/* Sort drop down*/}
          <ProductListSortDropdown sortOptions={sortOptions} />

          <div>
            <div className="grid 2xl:grid-cols-5 xl:grid-cols-4 lg:grid-cols-3 md:grid-cols-2 sm:grid-cols-1 gap-4 mt-6">
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
        </div>
      </div>
    </>
  );
}

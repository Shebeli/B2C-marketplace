"use client";

import { useState } from "react";
import { FaFilter } from "react-icons/fa6";
import ProductFilterOptions from "./product-filters";
import FilterProvider from "./filter-provider";
import { ColorChoice } from "@/app/lib/types/ui/product-list-types";

/**
 * Dynamically fetched filter options which are specific for each subcategory
 * and other dynamic options such as color choices should be passed to this component.
 */
export default function ProductFilter({
  colorChoices,
}: {
  colorChoices: ColorChoice[];
}) {
  const [toggleFilters, setToggleFilters] = useState<boolean>(false);

  return (
    <FilterProvider colorChoices={colorChoices}>
      <div className={`flex flex-col`}>
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
        <div
          className={`overflow-hidden ${
            toggleFilters ? "min-w-60" : "w-0 opacity-0"
          }`}
        >
          {toggleFilters && <ProductFilterOptions />}
        </div>
      </div>
    </FilterProvider>
  );
}

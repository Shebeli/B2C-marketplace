"use client";

import { usePathname, useSearchParams } from "next/navigation";
import { startTransition, useCallback, useEffect, useState } from "react";
import "react-range-slider-input/dist/style.css";
import { ProductColorFilter } from "../color-filter";
import PriceFilter from "./filter-price";
import FilterToggleOption from "./filter-toggle-option";
import { useFilters } from "./filterContext";
import { useRouter } from "next/navigation";
import { useTransition } from "react";

export default function ProductFilters() {
  const [isColorChoicesOpen, setIsColorChoicesOpen] = useState<boolean>(false);

  const { hasFilters, resetFilters } = useFilters();
  const { replace } = useRouter();
  const pathname = usePathname();

  const [isPending, startTransition] = useTransition();
  const searchParams = useSearchParams();

  const customResetFilters = () => {
    startTransition(resetFilters);
  };
  // const resetFilters = () => {
  //   startTransition(() => {
  //     const newSearchParams = new URLSearchParams();

  //     newSearchParams.set("subCategoryId", searchParams.get("subCategoryId")!);
  //     const currentSort = newSearchParams.get("sort");
  //     if (currentSort) {
  //       newSearchParams.set("sort", currentSort);
  //     }

  //     replace(`${pathname}?${newSearchParams}`);
  //   });
  // };
  /**
   * Checks if any query param (except 'subCategoyId' and 'sort') exists in the
   * URL's query params.
   */

  // const updateHasFilters = useCallback(() => {
  //   const paramKeys = Array.from(
  //     searchParams
  //       .keys()
  //       .filter((paramKey) => !["subCategoryId", "sort"].includes(paramKey))
  //   );

  //   setHasFilters(paramKeys.length > 0);
  // }, [searchParams]);

  // useEffect(() => {
  //   updateHasFilters();
  // }, [updateHasFilters]);

  console.log("HAS FILTERS????:", hasFilters())
  return (
    <div>
      <div className="border border-base-300 p-1">
        <div className={`m-1.5`}>
          {isPending ? (
            <button className="btn btn-circle" disabled={true}>
              <span className="loading loading-spinner"></span>
            </button>
          ) : (
            <button
              className="btn btn-soft btn-sm btn-secondary"
              onClick={customResetFilters}
              disabled={!hasFilters()}
            >
              حذف فیلتر ها
            </button>
          )}
        </div>

        <div className="flex flex-col gap-2.5">
          <div className=" border-b border-base-300">
            <div
              className={`collapse collapse-arrow ${
                isColorChoicesOpen ? "collapse-open" : "collapse-close"
              }`}
            >
              <input
                className="cursor-pointer"
                type="radio"
                name="my-accordion-2"
                onClick={() => setIsColorChoicesOpen(!isColorChoicesOpen)}
              />
              <div className={`collapse-title pr-2 font-medium`}>رنگ</div>
              {/* The conditional top padding is that for some reason, the default padding persists when the collapse is closed */}
              <div
                className={`collapse-content border-t border-base-300 ${
                  isColorChoicesOpen ? "pt-4" : ""
                }`}
              >
                <ProductColorFilter />
              </div>
            </div>
          </div>
          <PriceFilter />
          <FilterToggleOption
            filterToggle={{
              name: "موجود",
              queryParam: "isAvailable",
            }}
          />
          <FilterToggleOption
            filterToggle={{
              name: "ارسال امروز",
              queryParam: "canDeliverToday",
            }}
          />
        </div>
      </div>
    </div>
  );
}

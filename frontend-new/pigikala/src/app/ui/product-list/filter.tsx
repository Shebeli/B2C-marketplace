"use client";

import {
  ColorFilterOption,
  ProductGenericFilters,
} from "@/app/lib/types/ui/product-list-types";
import { useEffect, useState } from "react";
import RangeSlider from "react-range-slider-input";
import "react-range-slider-input/dist/style.css";
import { ProductListColorFilter } from "./color-filter";
import { usePathname, useSearchParams, useRouter } from "next/navigation";
import { useDebouncedCallback } from "use-debounce";

/**
 * Generic filters are managed and handled in this stated for updating query params.
 * Color Filter is just passed to a child component in which it handles the state by itself.
 */
export default function ProductFilters({
  initialGenericFilters,
  initialColorFilterOptions,
}: {
  initialGenericFilters: ProductGenericFilters;
  initialColorFilterOptions: ColorFilterOption[];
}) {
  const { replace } = useRouter();
  const searchParams = useSearchParams();
  const pathname = usePathname();

  const [isColorChoicesOpen, setIsColorChoicesOpen] = useState<boolean>(false);
  const [genericFilters, setGenericFilters] = useState(initialGenericFilters);

  const updateParamsGenericFilters = useDebouncedCallback(() => {
    const newSearchParams = new URLSearchParams(searchParams);

    console.log(genericFilters);
    // iterate over generic filters and set the new params
    Object.entries(genericFilters).forEach(([key, value]) => {
      if (value !== undefined) {
        newSearchParams.set(key, value.toString());
      } else {
        newSearchParams.delete(key);
      }
    });

    console.log(newSearchParams.toString());
    replace(`${pathname}?${newSearchParams.toString()}`);
  }, 500);

  //

  // Update query params with generic filters
  useEffect(() => {
    updateParamsGenericFilters();
  }, [updateParamsGenericFilters, genericFilters, searchParams]);

  return (
    <div className="border-b">
      <div className="min-w-56 border border-base-300 p-1">
        <div>
          <div>
            <a
              className="text-sm cursor-pointer link-info"
              onClick={() =>
                setGenericFilters({
                  minPrice: undefined,
                  maxPrice: undefined,
                  isAvailable: undefined,
                  canDeliverToday: undefined,
                })
              }
            >
              حذف فیلتر ها
            </a>
          </div>
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
                <ProductListColorFilter
                  initialColorFilterOptions={initialColorFilterOptions}
                />
              </div>
            </div>
          </div>
          <div className="flex flex-col gap-5 py-2 px-1.5 border-b border-base-300">
            {/* Price range slider */}
            <p className="font-medium">محدوده قیمت به تومن</p>
            <RangeSlider
              value={[
                genericFilters.minPrice ?? 0,
                genericFilters.maxPrice ?? 1000000000,
              ]}
              onInput={(e) => {
                setGenericFilters({
                  ...genericFilters,
                  minPrice: e[0],
                  maxPrice: e[1],
                });
              }}
              min={0}
              max={1000000000}
            />
            <div className="flex justify-between">
              <p>{genericFilters.maxPrice?.toLocaleString() ?? 1000000000}</p>
              <p>{genericFilters.minPrice?.toLocaleString() ?? 0}</p>
            </div>
          </div>
          <div className="form-control">
            <label className="label cursor-pointer">
              <span className="label-text font-semibold text-base ">موجود</span>
              <input
                type="checkbox"
                checked={genericFilters.isAvailable ?? false}
                onChange={() =>
                  setGenericFilters({
                    ...genericFilters,
                    isAvailable: !genericFilters.isAvailable,
                  })
                }
                className="toggle toggle-info"
              />
            </label>
          </div>
          <div className="form-control">
            <label className="label cursor-pointer">
              <span className="label-text font-semibold text-base ">
                ارسال امروز
              </span>
              <input
                type="checkbox"
                checked={genericFilters.canDeliverToday ?? false}
                onChange={() =>
                  setGenericFilters({
                    ...genericFilters,
                    canDeliverToday: !genericFilters.canDeliverToday,
                  })
                }
                className="toggle toggle-info"
              />
            </label>
          </div>
        </div>
      </div>
    </div>
  );
}

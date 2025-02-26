"use client";

import {
  defaultProductFilters,
  productGenericFilters,
} from "@/app/lib/constants";
import { useState } from "react";
import RangeSlider from "react-range-slider-input";
import "react-range-slider-input/dist/style.css";
import sampleColorChoices from "./placeholder";
import clsx from "clsx";

interface productFiltersProps {
  filters: productGenericFilters;
  setFilters: React.Dispatch<React.SetStateAction<productGenericFilters>>;
}

export default function ProductFilters({
  filters,
  setFilters,
}: productFiltersProps) {
  const [isColorChoicesOpen, setIsColorChoicesOpen] = useState<boolean>(false);

  return (
    <div className="border-b">
      <div className="min-w-56 border border-base-300 p-1">
        <div>
          <div>
            <a
              className="text-sm cursor-pointer link-info"
              onClick={() => setFilters(defaultProductFilters)}
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
              {/* The condition top padding is because for some reason, the padding persists when the collapse is closed */}
              <div
                className={`collapse-content border-t border-base-300 ${
                  isColorChoicesOpen ? "pt-4" : ""
                }`}
              >
                <div className="grid grid-cols-4 gap-1.5 border-bas-300">
                  {/* Dynamic color filters*/}
                  {sampleColorChoices.map((colorChoice) => (
                    <div
                      className={
                        "flex flex-col items-center gap-1 cursor-pointer"
                      }
                      key={colorChoice.value}
                      onClick={() => {
                        setFilters({
                          ...filters,
                          color:
                            colorChoice === filters.color ? null : colorChoice,
                        });
                      }}
                    >
                      <div
                        style={{ backgroundColor: colorChoice.value }}
                        className={clsx(
                          `size-7 rounded-md border-[2.5px] border-white ${
                            colorChoice === filters.color
                              ? "ring-[3.5px] ring-cyan-400"
                              : ""
                          }`
                        )}
                      ></div>
                      <p className="text-sm font-medium">{colorChoice.name}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
          <div className="flex flex-col gap-5 py-2 px-1.5 border-b border-base-300">
            {/* Price range slider */}
            <p className="font-medium">محدوده قیمت به تومن</p>
            <RangeSlider
              value={[filters.priceRange.min, filters.priceRange.max]}
              onInput={(e) =>
                setFilters({ ...filters, priceRange: { min: e[0], max: e[1] } })
              }
              min={0}
              max={100000000}
            />
            <div className="flex justify-between">
              <p>{filters.priceRange.max.toLocaleString()}</p>
              <p>{filters.priceRange.min.toLocaleString()}</p>
            </div>
          </div>
          <div className="form-control">
            <label className="label cursor-pointer">
              <span className="label-text font-semibold text-base ">موجود</span>
              <input
                type="checkbox"
                checked={filters.isAvailable}
                onChange={() =>
                  setFilters({
                    ...filters,
                    isAvailable: !filters.isAvailable,
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
                checked={filters.canDeliverToday}
                onChange={() =>
                  setFilters({
                    ...filters,
                    canDeliverToday: !filters.canDeliverToday,
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

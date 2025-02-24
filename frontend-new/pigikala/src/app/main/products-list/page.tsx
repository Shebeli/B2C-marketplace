"use client";

import React, { useState } from "react";
import { FaArrowDownWideShort } from "react-icons/fa6";
import RangeSlider from "react-range-slider-input";
import "react-range-slider-input/dist/style.css";

const ProductsList: React.FC = () => {
  const sortOptions = [
    "جدید ترین",
    "ارزان ترین",
    "گران ترین",
    "پربازدید ترین",
  ] as const; // hardcoded temporarily as a constant, might be variable in production.
  type SortType = (typeof sortOptions)[number];
  const [selectedSort, setSelectedSort] = useState<SortType>("جدید ترین");
  const [isColorFilterOpen, setIsColorFilterOpen] = useState<boolean>(false);
  const [priceFilter, setPriceFilter] = useState<Array<number>>([0, 50000000]);

  return (
    <div className=" max-w-screen-2xl">
      <div className=" flex gap-2 p-2">
        <div className="border-b-2 border-base-300">
          <div className="min-w-52 border-2 border-base-300 bg-base-200 p-1">
            {/* Filters */}
            <div className="">
              <div className=" border-b-2 border-base-300">
                <div
                  className={`collapse collapse-arrow cursor-pointer ${
                    isColorFilterOpen ? "collapse-open" : "collapse-close"
                  }`}
                >
                  <input
                    className=" cursor-pointer"
                    type="radio"
                    name="my-accordion-2"
                    onClick={() => setIsColorFilterOpen(!isColorFilterOpen)}
                  />
                  <div className={`collapse-title pr-2 font-medium`}>رنگ</div>
                  <div className="collapse-content">
                    <div className="grid grid-cols-4 gap-1.5">
                      {/* Dynamic color filters*/}
                      {Array(7)
                        .fill("آبی")
                        .map((color) => (
                          <div
                            className="flex flex-col items-center gap-1"
                            key={color}
                          >
                            <div className="bg-blue-400 size-7 rounded-md"></div>
                            <p className="text-sm font-medium">{color}</p>
                          </div>
                        ))}
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex flex-col gap-5 py-2 px-1.5 border-b-2 border-base-300">
                {/* Price range slider */}
                <p className="font-medium">محدوده قیمت به تومن</p>
                <RangeSlider
                  value={priceFilter}
                  onInput={setPriceFilter}
                  min={0}
                  max={100000000}
                />
                <div className="flex justify-between">
                  <p>{priceFilter[1].toLocaleString()}</p>
                  <p>{priceFilter[0].toLocaleString()}</p>
                </div>
              </div>
              <div className="form-control">
                <label className="label cursor-pointer">
                  <span className="label-text font-semibold text-base ">
                    موجود
                  </span>
                  <input type="checkbox" className="toggle toggle-info" />
                </label>
              </div>
              <div className="form-control">
                <label className="label cursor-pointer">
                  <span className="label-text font-semibold text-base ">
                    ارسال امروز
                  </span>
                  <input type="checkbox" className="toggle toggle-info" />
                </label>
              </div>
            </div>
          </div>
        </div>
        <div className="flex-col">
          <div className="border-b-2 border-base-300 pb-1.5">
            {/* Sort drop down*/}
            <div className="flex items-center">
              <FaArrowDownWideShort className="ml-1.5 size-5" />
              <span className="font-medium ml-2">مرتب سازی:</span>
              <select className="select select-primary select-sm font-medium">
                {sortOptions.map((sortOption) => (
                  <option
                    className=""
                    key={sortOption}
                    onClick={() => setSelectedSort(sortOption)}
                  >
                    {sortOption}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div>
            <div className="grid grid-cols-1 xl:grid-cols-5 lg:grid-cols-4 md:grid-cols-3 sm:grid-cols-2 gap-4 mt-6">
              {Array(25)
                .fill(null)
                .map((_, index) => (
                  <div key={index} className="card bg-base-100 shadow-lg">
                    <figure>
                      <img
                        src="https://via.placeholder.com/300"
                        alt={`Product ${index + 1}`}
                        className="rounded-lg"
                      />
                    </figure>
                    <div className="card-body">
                      <h2 className="card-title">Product {index + 1}</h2>
                      <div className="flex items-center">
                        <div className="avatar">
                          <div className="w-7 rounded-full">
                            <img src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp" />
                          </div>
                        </div>
                        <span className="text-sm mr-1.5">تک سینا</span>
                      </div>

                      <p className=" text-left text-sm">500,000 تومان</p>
                      <div className="card-actions justify-end">
                        <button className="btn btn-primary btn-sm text-sm ">
                          مشاهده محصول
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductsList;

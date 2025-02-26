"use client";

import {
  defaultProductFilters,
  productGenericFilters,
} from "@/app/lib/constants";
import ProductFilters from "@/app/ui/product-list/filter";
import sampleColorChoices from "@/app/ui/product-list/placeholder";
import Image from "next/image";
import React, { useState } from "react";
import { FaArrowDownWideShort, FaFilter } from "react-icons/fa6";
import "react-range-slider-input/dist/style.css";
import { sortOptions } from "@/app/lib/constants";
import SortDropdown from "@/app/ui/product-list/sort-dropdown";
import ProductCard from "@/app/ui/product-list/product-card";
import Breadcrumbs from "@/app/ui/breadcrumbs";

export default function ProductListPage() {
  // Sort
  const [selectedSort, setSelectedSort] = useState<string>("جدید ترین");
  const [toggleFilters, setToggleFilters] = useState<boolean>(false);

  // Filter
  const [filters, setFilters] = useState<productGenericFilters>(
    defaultProductFilters
  );

  return (
    <>
      <div className="max-w-screen-2xl flex flex-col p-2 w-full">
        <Breadcrumbs
          breadcrumbs={[
            { name: "وسایل دیجیتال", url: "/main/category/digital" },
            {
              name: "لپتاپ",
              url: "/main/category/laptop",
            },
          ]}
        />
        <div className="my-2 flex items-center gap-1">
          <button
            className="md:tooltip md:tooltip-left cursor-pointer btn btn-circle justify-items-center"
            data-tip="فیلتر ها"
            aria-label="Toggle filters"
            onClick={() => setToggleFilters(!toggleFilters)}
          >
            <FaFilter className="size-7 text-primary" />
          </button>
          <h3 className="text-lg">لپتاپ ASUS</h3>
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
              <ProductFilters filters={filters} setFilters={setFilters} />
            )}
          </div>

          <div className="flex-col">
            {/* Sort drop down*/}
            <SortDropdown
              sortOptions={sortOptions}
              setSelectedSort={setSelectedSort}
            />
            <div>
              <div className="grid 2xl:grid-cols-5 xl:grid-cols-4 lg:grid-cols-3 md:grid-cols-2 sm:grid-cols-1 gap-4 mt-6">
                {Array(25)
                  .fill(null)
                  .map((_, index) => (
                    <ProductCard
                      key={index}
                      id={index}
                      name={
                        "لپ تاپ 15.6 اینچی ایسوس مدل Vivobook 15 F1504VA-NJ826-i7 1355U 16GB 512SSD TN Fingerprint Backlit"
                      }
                      image={"/sample_images/product-main-image.webp"}
                      price={500000}
                      sellerName={"فروشگاه تک سینا"}
                      sellerPic={"/home/random-avatar.webp"}
                    />
                  ))}
              </div>
            </div>
          </div>
        </div>
        {/* Pagination */}
        <div className="join self-center my-5">
          <input
            className="join-item btn btn-square"
            type="radio"
            name="options"
            aria-label="1"
            defaultChecked
          />
          <input
            className="join-item btn btn-square"
            type="radio"
            name="options"
            aria-label="2"
          />
          <input
            className="join-item btn btn-square"
            type="radio"
            name="options"
            aria-label="3"
          />
          <input
            className="join-item btn btn-square"
            type="radio"
            name="options"
            aria-label="4"
          />
        </div>
      </div>
    </>
  );
}

import React, { useState } from "react";
import { FaArrowDownWideShort } from "react-icons/fa6";

const ProductsList: React.FC = () => {
  const sortOptions = [
    "جدید ترین",
    "ارزان ترین",
    "گران ترین",
    "پربازدید ترین",
  ] as const; // hardcoded temporarily as a constant, might be variable in production.
  type SortType = (typeof sortOptions)[number];
  const [selectedSort, setSelectedSort] = useState<SortType>("جدید ترین");

  return (
    <div className=" max-w-screen-2xl w-f">
      <div className=" flex gap-2 p-2">
        <div className="border-b-2">
          <div className="min-w-36 border-2">
            {/* Filters */}
            <div className=" ">
              <div className=" border-b-1">
                <span>رنگ</span>
              </div>
            </div>
          </div>
        </div>
        <div className="flex-col">
          <div className="border-b-2 pb-1.5">
            {/* Sort drop down*/}
            <div className="flex items-center">
              <FaArrowDownWideShort className="ml-1.5 size-5"/>
              <span className="font-medium ml-2">مرتب سازی:</span>
              <select className="select select-primary select-sm font-medium">
                {sortOptions.map((sortOption) => (
                  <option
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

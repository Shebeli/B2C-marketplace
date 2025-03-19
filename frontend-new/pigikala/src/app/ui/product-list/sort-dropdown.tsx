"use client";

import { SortChoice } from "@/app/lib/types/ui/product-list-types";
import { useQueryState } from "nuqs";
import { FaArrowDownWideShort } from "react-icons/fa6";
// import { startTransition } from "react";

export default function ProductListSortDropdown({
  sortOptions,
}: {
  sortOptions: readonly SortChoice[];
}) {
  const [sort, setSort] = useQueryState("sort", {
    shallow: false,
  });

  const handleSortChange = (sortOption: string) => {
    setSort(sortOption);
  };

  return (
    <div className="border-b border-base-300 pb-1.5">
      <div className="flex items-center">
        <FaArrowDownWideShort className="ml-1.5 size-5" />
        <span className="font-medium ml-2">مرتب سازی:</span>
        <select
          defaultValue={sort ?? "یک گزینه را انتخاب کنید"}
          className="select font-medium"
          onChange={(e) => handleSortChange(e.currentTarget.value)}
        >
          <option disabled={true}>یک گزینه را انتخاب کنید</option>
          {sortOptions.map((sortOption) => (
            <option key={sortOption.value} value={sortOption.value}>
              {sortOption.name}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}

import { useSearchParams, useRouter, usePathname } from "next/navigation";
import { FaArrowDownWideShort } from "react-icons/fa6";
import { SortChoice } from "@/app/lib/types/ui/product-list-types";
import { defaultSortOption } from "@/app/lib/constants/ui/product-list-constants";
import { useState } from "react";

export default function ProductListSortDropdown({
  sortOptions,
}: {
  sortOptions: readonly SortChoice[];
}) {
  const pathname = usePathname();
  const { replace } = useRouter();
  const searchParams = useSearchParams();
  const [sort, setSort] = useState(searchParams.get("sort"))

  const handleSortChange = (sortOption: string) => {
    const newSearchParams = new URLSearchParams(searchParams);

    newSearchParams.set("sort", sortOption);

    replace(`${pathname}?${newSearchParams.toString()}`);
  };

  return (
    <div className="border-b border-base-300 pb-1.5">
      <div className="flex items-center">
        <FaArrowDownWideShort className="ml-1.5 size-5" />
        <span className="font-medium ml-2">مرتب سازی:</span>
        <select
          defaultValue={
            sortOptions.find(
              (sortChoice) => sortChoice.name === searchParams.get("sort")
            )?.name ?? defaultSortOption.name
          }
          className="select select-primary select-sm font-medium"
          onClick={(e) => handleSortChange(e.currentTarget.value)}
        >
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

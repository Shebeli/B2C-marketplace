import { FaArrowDownWideShort } from "react-icons/fa6";

interface SortDropdownProps {
  sortOptions: string[];
  setSelectedSort: React.Dispatch<React.SetStateAction<string>>;
}

export default function SortDropdown({
  sortOptions,
  setSelectedSort,
}: SortDropdownProps) {
  return (
    <div className="border-b border-base-300 pb-1.5">
      <div className="flex items-center">
        <FaArrowDownWideShort className="ml-1.5 size-5" />
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
  );
}

import { ColorChoice } from "@/app/lib/types/ui/product-list-types";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { FilterContext } from "./filterContext";
import {
  parseAsArrayOf,
  parseAsBoolean,
  parseAsInteger,
  parseAsString,
  useQueryStates,
} from "nuqs";
import {
  defaultFilterOptions,
  FILTER_MAX_PRICE,
  filterKeys,
} from "@/app/lib/constants/ui/product-list-constants";

interface FilterProviderProps {
  children: React.ReactNode;
  colorChoices: ColorChoice[];
  initialFilters?: Record<string, string | string[]>;
}

export default function FilterProvider({
  children,
  colorChoices,
}: FilterProviderProps) {
  const [queryFilters, setQueryFilters] = useQueryStates(
    {
      isAvailable: parseAsBoolean.withDefault(defaultFilterOptions.isAvailable),
      canDeliverToday: parseAsBoolean.withDefault(defaultFilterOptions.canDeliverToday),
      minPrice: parseAsInteger.withDefault(defaultFilterOptions.minPrice),
      maxPrice: parseAsInteger.withDefault(defaultFilterOptions.maxPrice),
      selectedColors: parseAsArrayOf(parseAsString).withDefault(defaultFilterOptions.selectedColors),
    },
    {
      shallow: false,
      scroll: true,
    }
  );

  /**
   * Remove all the filter options from the query params
   * while preserving the subCategoryId and the sort option.
   */
  const resetFilters = () => {
    setQueryFilters(defaultFilterOptions);
  };

  /**
   * Returns a bool indicating whether at least one filter is
   * set or not.
   */
  const hasFilters = () => {
    return filterKeys.some((key) => {
      const currentValue = queryFilters[key];
      const defaultValue = defaultFilterOptions[key];

      if (Array.isArray(currentValue)) {
        return currentValue.length > 0;
      }

      return currentValue !== defaultValue;
    });
  };
  return (
    <FilterContext.Provider
      value={{
        queryFilters,
        setQueryFilters,
        resetFilters,
        hasFilters,
        colorChoices,
      }}
    >
      {children}
    </FilterContext.Provider>
  );
}

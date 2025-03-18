/* eslint-disable @typescript-eslint/no-explicit-any */
// idc setting the type for custom generic types
import { createContext, useContext } from "react";
import { ColorChoice } from "@/app/lib/types/ui/product-list-types";
import { SetValues, Values } from "nuqs";

interface FilterContextType {
  queryFilters: Values<any>;
  setQueryFilters: SetValues<any>;
  resetFilters: () => void;
  hasFilters: () => boolean;
  colorChoices: ColorChoice[];
}

export const FilterContext = createContext<FilterContextType | null>(null);

/**
 * Custom hook which enables managing and handling filter options in
 * different components via react context.
 *
 * @returns `activeFilters` the react state which holds all key value pairs of
 * filter options, selected sort option and the subCateoryId (subCategoryId always exists).
 *
 *  The following functions will modify the shared context state `activeFilters` and the
 *  replace current URL's query param(s):
 *
 * `updateFilter` for updating or adding a new filter option.
 *
 * `removeFilter` for removing a specific filter option.
 *
 * `resetFilters` for removing all filter options.
 */
export function useFilters(): FilterContextType {
  const context = useContext(FilterContext);
  if (!context) {
    throw new Error("useFilters must be provdied with a provider");
  }
  return context;
}

export interface ColorChoice {
  name: string; // name to be displayed
  value: string; // hex code of the color
}

/**
 * Note that multiple colors can be selected by the user, or none.
 */
export interface ColorFilterOption {
  name: string; // name to be displayed
  value: string; // color's hex code
  selected: boolean; // has the user selected the color
}

/**
 * A field having undefined value means the filter isn't provided at all.
 */
export interface ProductGenericFilters {
  minPrice: number | undefined;
  maxPrice: number | undefined;
  isAvailable: boolean | undefined;
  canDeliverToday: boolean | undefined;
}

export interface SortChoice {
  name: string; // for displaying
  value: string; // value for updating the query parameters with.
}

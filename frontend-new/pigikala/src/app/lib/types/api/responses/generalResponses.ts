// Any kind of paginated response from DRF would follow the following data shape
export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}


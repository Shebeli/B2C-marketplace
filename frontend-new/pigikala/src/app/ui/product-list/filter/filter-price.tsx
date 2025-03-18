import { parseAsInteger, useQueryState } from "nuqs";
import { useEffect, useState } from "react";
import RangeSlider from "react-range-slider-input";
import { useDebouncedCallback } from "use-debounce";

export default function PriceFilter() {
  const MAX_PRICE = 1000000000;
  // Since nuqs doesn't support debouncing, seperate states
  // localMinPrice and localMaxPrice are created so the local price changes
  // are reflected immediately in the UI, but the non-shallow query updates
  // are debounced.
  const [minPrice, setMinPrice] = useQueryState(
    "minPrice",
    parseAsInteger
      .withOptions({
        shallow: false,
        clearOnDefault: true,
      })
      .withDefault(0)
  );
  const [maxPrice, setMaxPrice] = useQueryState(
    "maxPrice",
    parseAsInteger
      .withOptions({
        shallow: false,
        clearOnDefault: true,
      })
      .withDefault(MAX_PRICE)
  );

  const [localMinPrice, setLocalMinPrice] = useState<number>(minPrice);
  const [localMaxPrice, setLocalMaxPrice] = useState<number>(maxPrice);

  // Update the localMinPrice and localMaxPrice when the query state changes.
  useEffect(() => {
    setLocalMinPrice(minPrice);
    setLocalMaxPrice(maxPrice);
  }, [minPrice, maxPrice]);

  const updatePriceQuery = useDebouncedCallback(
    (minPrice: number, maxPrice: number) => {
      setMinPrice(minPrice);
      setMaxPrice(maxPrice);
    },
    500
  );

  const handlePriceInput = (e: [number, number]) => {
    const newMinPrice = e[0];
    const newMaxPrice = e[1];
    setLocalMinPrice(newMinPrice);
    setLocalMaxPrice(newMaxPrice);
    updatePriceQuery(newMinPrice, newMaxPrice);
  };

  return (
    <div className="flex flex-col gap-5 py-2 px-1.5 border-b border-base-300">
      <p className="font-medium">محدوده قیمت به تومن</p>
      <RangeSlider
        value={[Number(localMinPrice), Number(localMaxPrice)]}
        onInput={handlePriceInput}
        min={0}
        max={1000000000}
      />
      <div className="flex justify-between">
        <p>{localMaxPrice.toLocaleString()}</p>
        <p>{localMinPrice.toLocaleString()}</p>
      </div>
    </div>
  );
}

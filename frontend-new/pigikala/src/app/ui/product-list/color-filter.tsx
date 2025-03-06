import clsx from "clsx";
import { useState } from "react";
import { ColorFilterOption } from "@/app/lib/types/ui/product-list-types";

export function ProductListColorFilter({
  initialColorFilterOptions,
}: {
  initialColorFilterOptions: ColorFilterOption[];
}) {
  const [colorFilterOptions, setColorFilterOptions] = useState(
    initialColorFilterOptions
  );

  // for updating the `selected` key of a specific colorFilterOption
  const toggleSelected = (value: string) => {
    setColorFilterOptions((prevColors) =>
      prevColors.map((prevColor) =>
        prevColor.value === value
          ? { ...prevColor, selected: !prevColor.selected }
          : prevColor
      )
    );
  };

  return (
    <div className="grid grid-cols-4 gap-y-2 border-base-300">
      {colorFilterOptions.map((colorFilterOption) => (
        <div
          className={"flex flex-col items-center gap-1 cursor-pointer"}
          key={colorFilterOption.value}
          onClick={() => toggleSelected(colorFilterOption.value)}
        >
          <div
            style={{ backgroundColor: colorFilterOption.value }}
            className={clsx(
              `size-8 rounded-md border-[2.5px] border-white ${
                colorFilterOption.selected
                  ? "ring-[3.5px] ring-cyan-400"
                  : ""
              }`
            )}
          ></div>
          <p className="text-sm font-medium">{colorFilterOption.name}</p>
        </div>
      ))}
    </div>
  );
}

import clsx from "clsx";
import { useFilters } from "./filter/filterContext";
import { parseAsArrayOf, parseAsString, useQueryState } from "nuqs";

// It is expected that the colorChoices are provided to the filter context.
export function ProductColorFilter() {
  const { colorChoices } = useFilters();
  // const selectedColors =
  //   (activeFilters["selectedColors"] as string[] | undefined) ?? [];
  const [selectedColors, setSelectedColors] = useQueryState(
    "selectedColors",
    parseAsArrayOf(parseAsString)
      .withOptions({
        shallow: false,
      })
      .withDefault([])
  );

  // Construct the new selectedColors based on whether the color is getting selected or deselected,
  // and update the filters with it.
  const handleColorClick = (clickedColor: string) => {
    let newSelectedColors;
    if (selectedColors.includes(clickedColor)) {
      newSelectedColors = selectedColors.filter(
        (selectedColor) => selectedColor !== clickedColor
      );
    } else {
      newSelectedColors = [...selectedColors, clickedColor];
    }
    setSelectedColors(newSelectedColors);
  };

  return (
    <div className="grid grid-cols-4 gap-y-2 border-base-300">
      {colorChoices.map((colorChoice) => (
        <div
          className={"flex flex-col items-center gap-1 cursor-pointer"}
          key={colorChoice.value}
          onClick={() => handleColorClick(colorChoice.value)}
        >
          <div
            style={{ backgroundColor: colorChoice.value }}
            className={clsx(
              `size-8 rounded-md border-2 border-base-100  ${
                selectedColors.includes(colorChoice.value)
                  ? "ring-[3.5px] ring-cyan-400"
                  : ""
              }`
            )}
          ></div>
          <p className="text-sm font-medium">{colorChoice.name}</p>
        </div>
      ))}
    </div>
  );
}

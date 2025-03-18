import { FilterToggle } from "@/app/lib/types/ui/product-list-types";
import { useQueryState } from "nuqs";

export default function FilterToggleOption({
  filterToggle,
}: {
  filterToggle: FilterToggle;
}) {
  const queryParam = filterToggle.queryParam;
  const [isChecked, setIsChecked] = useQueryState(queryParam, {
    parse: (value: string) => value === "true",
    defaultValue: false, // so the query param gets omitted if its false
    shallow: false,
  });

  const handleToggleChange = () => {
    setIsChecked(!isChecked);
  };

  return (
    <fieldset className="fieldset">
      <label className="fieldset-label justify-between text-base text-base-content">
        <span className="font-semibold">{filterToggle.name}</span>
        <input
          type="checkbox"
          checked={isChecked || false}
          onChange={handleToggleChange}
          className="toggle toggle-info"
        />
      </label>
    </fieldset>
  );
}

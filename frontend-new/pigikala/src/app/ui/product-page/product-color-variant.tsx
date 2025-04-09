import { ProductVariantUI } from "@/app/lib/types/ui/product-detail/productDetailsUI";

interface ProductColorProps {
  variants: ProductVariantUI[];
  selectedVariant: ProductVariantUI;
  setSelectedVariant: React.Dispatch<React.SetStateAction<ProductVariantUI>>;
}

const ProductColorVariant: React.FC<ProductColorProps> = ({
  variants,
  selectedVariant,
  setSelectedVariant,
}) => {
  return (
    <div>
      <p>رنگ انتخاب شده: {selectedVariant.colorName}</p>
      <div className="flex my-2 gap-2">
        {variants.map((variant) => (
          <button
            key={variant.id}
            className={`w-9 h-9 rounded-full hover:cursor-pointer ${
              selectedVariant === variant
                ? "ring-4 border-[3.5px] ring-cyan-500"
                : ""
            }`}
            style={{ backgroundColor: `${variant.colorValue}` }}
            onClick={() => setSelectedVariant(variant)}
          ></button>
        ))}
      </div>
    </div>
  );
};

export default ProductColorVariant;

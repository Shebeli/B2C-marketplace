import ProductFeatureCard from "./product-feature-card";

interface ProductFeature {
  attribute: string;
  value: string;
}

interface ProductFeatureProps {
  productFeatures: ProductFeature[];
}

export default function ProductFeatures({
  productFeatures,
}: ProductFeatureProps) {
  return (
    // text shouldn't be longer than about 23 letters, otherwise the text will be overflowed.
    <>
      <div className="lg:col-span-1 col-span-2 ">
        <h2 className="font-semibold text-lg mt-2 mb-1">ویژگی ها</h2>
        <div className="lg:grid grid-cols-3 flex gap-4 w-full lg:overflow-hidden overflow-scroll scrollbar-thumb-rounded-full scrollbar-track-rounded-full scrollbar-thumb-slate-700 scrollbar-track-slate-300 py-1">
          {productFeatures.map((productFeature, index) => (
            <ProductFeatureCard key={index} productFeature={productFeature} />
          ))}
        </div>
      </div>
    </>
  );
}

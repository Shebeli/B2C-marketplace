import { ProductFeatureUI } from "@/app/lib/types/ui/product-detail/productDetailsUI";

export default function ProductFeatureCard({
  productFeature,
}: {
  productFeature: ProductFeatureUI;
}) {
  return (
    <div className="card bg-base-200 shadow-md lg:min-w-[60px] min-w-[128px]">
      <div className="card-body flex p-1 text items-center">
        <h2>{productFeature.attribute}</h2>
        <p className="font-semibold">{productFeature.value}</p>
      </div>
    </div>
  );
}

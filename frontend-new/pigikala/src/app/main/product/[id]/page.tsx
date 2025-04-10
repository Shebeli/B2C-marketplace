import { getProductById } from "@/app/lib/actions/productDetailActions";
import ProductFooter from "@/app/ui/product-page/product-footer";
import ProductMain from "@/app/ui/product-page/product-main";
import ProductTabs from "@/app/ui/product-page/product-tabs";

export default async function ProductPage(props: {
  params: Promise<{ id: number }>;
}) {
  const params = await props.params;
  const id = params.id;

  const product = await getProductById(id);

  return (
    <div className="lg:px-4 max-w-(--breakpoint-2xl)">
      <ProductMain product={product} />
      <ProductFooter />
      <ProductTabs
        productId={product.id}
        description={product.description}
        technicalDetails={product.technicalDetails}
      />
    </div>
  );
}

import { notFound } from "next/navigation";

export default async function ProductPage(props: {
  params: Promise<{ id: string }>;
}) {
  const params = await props.params;
  const id = params.id;

  const product = await fetchProduct(id);

  if (!product) {
    notFound();
  }

  return  

}

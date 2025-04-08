import { getProductCommentsById } from "@/app/lib/actions/productDetailActions";
import { isFailedResponse } from "@/app/lib/services/api/fetch/fetchWrapper";
import ProductCommentCard from "./product-comment-card";

interface ProductCommentProps {
  productId: number;
}

export async function ProductComment({ productId }: ProductCommentProps) {
  const comments = await getProductCommentsById(productId);

  if (isFailedResponse(comments)) {
    return <h1>مشکلی در دریافت نظرات پیش آمده است, لطفا بعدا تلاش کنید.</h1>;
  }

  return (
    <ul className="list bg-base-100 rounded-box shadow-md">
      {comments.results.map((comment, index) => (
        <ProductCommentCard key={index} comment={comment} />
      ))}
    </ul>
  );
}

import { getProductReviewsById } from "@/app/lib/actions/productDetailActions";
import { isFailedResponse } from "@/app/lib/services/api/fetch/fetchWrapper";
import ReviewCard from "./product-review-card";

interface ProductReviewProps {
  productId: number;
}

export async function ProductReview({ productId }: ProductReviewProps) {
  const reviews = await getProductReviewsById(productId);

  if (isFailedResponse(reviews)) {
    return <h1>مشکلی در دریافت نظرات پیش آمده است, لطفا بعدا تلاش کنید.</h1>;
  }

  return (
    <ul className="list bg-base-100 rounded-box shadow-md">
      {reviews.results.map((review, index) => (
        <ReviewCard key={index} review={review} />
      ))}
    </ul>
  );
}

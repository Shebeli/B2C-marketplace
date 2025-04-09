import { Paginated } from "@/app/lib/types/api/responses/generalResponses";
import { ProductReviewAPI } from "@/app/lib/types/api/responses/product-detail/reviewsResponse";
import { API_ROUTES } from "../../../../apiRoutes";
import { ProductCommentAPI } from "../../../../types/api/responses/product-detail/commentsResponse";
import { ApiProductDetail } from "../../../../types/api/responses/product-detail/productResponse";
import { api } from "../fetchWrapper";

const { PRODUCT: PRODUCT_ROUTES, FEEDBACK: FEEDBACK_ROUTES } = API_ROUTES;

export async function fetchProduct(id: number) {
  return await api.get<ApiProductDetail>(`${PRODUCT_ROUTES.PRODUCTS}${id}`);
}

export async function fetchProductReviews(id: number) {
  return await api.get<Paginated<ProductReviewAPI>>(
    `${FEEDBACK_ROUTES.PRODUCT_REVIEWS}${id}`
  );
}

export async function fetchProductComments(id: number) {
  return await api.get<Paginated<ProductCommentAPI>>(
    `${FEEDBACK_ROUTES.PRODUCT_COMMENTS}${id}`
  );
}

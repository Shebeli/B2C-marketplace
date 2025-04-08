"use server";

import { Paginated as Paginated } from "../types/api/responses/generalResponses";
import {
  FailedResponse,
  isFailedResponse,
} from "../services/api/fetch/fetchWrapper";
import {
  fetchProduct,
  fetchProductComments,
  fetchProductReviews,
} from "../services/api/fetch/product-detail/fetchProduct";
import {
  transformCommentToUI,
  transformProductToUI,
  transformReviewToUI,
} from "../services/api/transformers/productDetailTransformer";
import { ProductDetailUI } from "../types/ui/product-detail/productDetailsUI";
import { ApiError } from "@/app/main/customError";
import { ProductReviewUI } from "../types/ui/product-detail/productReviewUI";
import { ProductCommentUI } from "../types/ui/product-detail/productCommentUI";

export async function getProductById(id: number): Promise<ProductDetailUI> {
  const fetchResult = await fetchProduct(id);

  if (isFailedResponse(fetchResult)) {
    throw new ApiError({ ...fetchResult });
  }
  return transformProductToUI(fetchResult);
}

export async function getProductCommentsById(
  id: number
): Promise<Paginated<ProductCommentUI> | FailedResponse> {
  const fetchResult = await fetchProductComments(id);

  // Let the component handle the error gracefully
  if (isFailedResponse(fetchResult)) {
    return fetchResult;
  }

  return {
    ...fetchResult,
    results: fetchResult.results.map((comment) =>
      transformCommentToUI(comment)
    ),
  };
}

export async function getProductReviewsById(
  id: number
): Promise<Paginated<ProductReviewUI> | FailedResponse> {
  const fetchResult = await fetchProductReviews(id);

  // Let the component handle the error gracefully
  if (isFailedResponse(fetchResult)) {
    return fetchResult;
  }

  return {
    ...fetchResult,
    results: fetchResult.results.map((review) => transformReviewToUI(review)),
  };
}

import { ProductCommentAPI } from "@/app/lib/types/api/responses/product-detail/commentsResponse";
import { ApiProductDetail } from "@/app/lib/types/api/responses/product-detail/productResponse";
import { ProductReviewAPI } from "@/app/lib/types/api/responses/product-detail/reviewsResponse";
import { ProductCommentUI } from "@/app/lib/types/ui/product-detail/productCommentUI";
import { ProductDetailUI } from "@/app/lib/types/ui/product-detail/productDetailsUI";
import { ProductReviewUI } from "@/app/lib/types/ui/product-detail/productReviewUI";
import {
  translateColorToPersian
} from "@/app/lib/utils/colorsTranslation";
import { toRelativePersianTime } from "@/app/lib/utils/time";

export function transformProductToUI(
  product: ApiProductDetail
): ProductDetailUI {
  return {
    ...product,
    productFeatures: product.technicalDetails.slice(0, 9),
    variants: product.variants.map((variant) => {
      return {
        id: variant.id,
        name: variant.name,
        images: variant.images,
        price: variant.price,
        colorValue: variant.color ?? null,
        colorName: translateColorToPersian(variant.color),
      };
    }),
  };
}

export function transformReviewToUI(review: ProductReviewAPI): ProductReviewUI {
  return {
    ...review,
    createdRelativeTime: toRelativePersianTime(review.createdAt),
    updatedRelativeTime: toRelativePersianTime(review.updatedAt),
  };
}

export function transformCommentToUI(
  comment: ProductCommentAPI
): ProductCommentUI {
  return {
    ...comment,
    createdRelativeTime: toRelativePersianTime(comment.createdAt),
    updatedRelativeTime: toRelativePersianTime(comment.updatedAt),
  };
}

import { TechnicalDetail } from "@/app/lib/types/api/responses/product-detail/productResponse";
import { Suspense } from "react";
import { ReviewSkeleton } from "../skeletons";
import { ProductComment } from "./product-comment";
import ProductTechnicalDetails from "./product-detail";
import { ProductReview } from "./product-review";

interface ProductTabProps {
  productId: number;
  technicalDetails: TechnicalDetail[];
  description: string;
}

export default function ProductTabs({
  productId,
  technicalDetails,
  description,
}: ProductTabProps) {
  return (
    <div>
      <div className="tabs tabs-lift my-8">
        <input
          type="radio"
          defaultChecked
          name="product-tab"
          className="tab border-primary"
          aria-label="معرفی"
        />
        <div className="tab-content bg-base-100 border-base-300 p-6">
          <p>{description}</p>
        </div>
        <input
          type="radio"
          name="product-tab"
          className="tab"
          aria-label="مشخصات فنی"
        />
        <div className="tab-content bg-base-100 border-base-300 p-6">
          <ProductTechnicalDetails technicalDetails={technicalDetails} />
        </div>
        <input
          type="radio"
          name="product-tab"
          className="tab"
          aria-label="نظرات و بررسی ها"
        />
        <div className="tab-content bg-base-100 border-base-300 p-6">
          <Suspense fallback={<ReviewSkeleton />}>
            <ProductReview productId={productId} />
          </Suspense>
        </div>
        <input
          type="radio"
          name="product-tab"
          className="tab"
          aria-label="سوالات"
        />
        <div className="tab-content bg-base-100 border-base-300 p-6">
          <Suspense fallback={<ReviewSkeleton />}>
            <ProductComment productId={productId} />
          </Suspense>
        </div>
      </div>
    </div>
  );
}

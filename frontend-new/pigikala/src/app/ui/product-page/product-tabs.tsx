import { Suspense } from "react";
import { ReviewSkeleton } from "../skeletons";
import { ProductComment } from "./product-comment";
import ProductTechnicalDetails from "./product-detail";
import { ProductReview } from "./product-review";
import { TechnicalDetail } from "@/app/lib/types/api/responses/product-detail/productResponse";

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
    <div
      role="tablist"
      className="tabs tabs-lifted place-self-center w-full my-8 shadow-lg"
    >
      <input
        type="radio"
        name="technical_detail_tab"
        role="tab"
        className="tab"
        aria-label="مشخصات"
      />
      <div
        role="tabpanel"
        className="tab-content bg-base-100 border-secondary rounded-box p-6 border-r-8 "
      >
        <ProductTechnicalDetails technicalDetails={technicalDetails} />
      </div>

      <input
        type="radio"
        name="description_tab"
        role="tab"
        className="tab"
        aria-label="معرفی"
        defaultChecked
      />
      <div
        role="tabpanel"
        className="tab-content bg-base-100 border-r-8 border-primary from-base-200 to-base-300 rounded-box p-6 "
      >
        <p className="max-w-(--breakpoint-2xl) leading-7 text-sm font-medium">
          {description}
        </p>
      </div>

      <input
        type="radio"
        name="reviews_tab"
        role="tab"
        className="tab "
        aria-label="نظرات و بررسی"
      />
      <div
        role="tabpanel"
        className="tab-content bg-base-100 border-accent border-r-8 rounded-box p-8 text-red-500 font-bold text-2xl"
      >
        <Suspense fallback={<ReviewSkeleton />}>
          <ProductReview productId={productId} />
        </Suspense>
      </div>
      <input
        type="radio"
        name="comments_tab"
        role="tab"
        className="tab "
        aria-label="سوالات"
      />
      <div
        role="tabpanel"
        className="tab-content bg-base-100 border-accent border-r-8 rounded-box p-8 text-red-500 font-bold text-2xl"
      >
        <Suspense fallback={<ReviewSkeleton />}>
          <ProductComment productId={productId} />
        </Suspense>
      </div>
    </div>
  );
}

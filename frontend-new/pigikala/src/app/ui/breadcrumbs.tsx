import { BreadCrumbResponse } from "../lib/types/api/responses/product-list-responses";
import { ApiResponse, isError } from "../lib/fetch/fetch-wrapper";

export default function CategoryBreadcrumb({
  breadcrumbsResult,
}: {
  breadcrumbsResult: ApiResponse<BreadCrumbResponse>;
}) {
  return isError(breadcrumbsResult) ? (
    <div className="text-sm pt-2 pb-1">
      <p className="text-error font-semibold italic"> خطا در دریافت بردکرامپ ⚠️ </p>
    </div>
  ) : (
    <div className="breadcrumbs text-sm pt-2 pb-1">
      <ul>
        <li>{breadcrumbsResult.mainCategory}</li>
        <li>{breadcrumbsResult.category}</li>
        <li>{breadcrumbsResult.subCategory}</li>
      </ul>
    </div>
  );
}

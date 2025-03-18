import { fetchBreadCrumb } from "../lib/actions/product-list-actions";
import { isError } from "../lib/fetch/fetch-wrapper";

export default async function CategoryBreadcrumb({
  subCategoryId,
}: {
  subCategoryId: number;
}) {
  // fetch breadcrumb data
  const categoryBreadCrumbResult = await fetchBreadCrumb(subCategoryId);

  return isError(categoryBreadCrumbResult) ? (
    <div className="text-sm pt-2 pb-1">
      <p className="text-error font-semibold italic">
        {" "}
        خطا در دریافت بردکرامپ ⚠️{" "}
      </p>
    </div>
  ) : (
    <div className="breadcrumbs text-sm pt-2 pb-1">
      <ul>
        <li>{categoryBreadCrumbResult.mainCategory}</li>
        <li>{categoryBreadCrumbResult.category}</li>
        <li>{categoryBreadCrumbResult.subCategory}</li>
      </ul>
    </div>
  );
}

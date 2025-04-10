export function NavbarProfileSkeleton() {
  return <div className="skeleton w-10 h-10 rounded-full "></div>;
}

export function ProductsListItemSkeleton() {
  return (
    <div className="flex card flex-col gap-4">
      <div className="card-body gap-4">
        <div className="skeleton min-h-44 min-w-40 max-w-60 "></div>
        <div className="flex items-center gap-4">
          <div className="skeleton h-8 w-8 shrink-0 rounded-full"></div>
          <div className="flex flex-col gap-4">
            <div className="skeleton h-4 w-12"></div>
            <div className="skeleton h-4 w-28"></div>
          </div>
        </div>
        <div className="card-actions justify-end">
          <button className="btn w-2/5 btn-sm skeleton"></button>
        </div>
      </div>
    </div>
  );
}

export function ProductsListSkeleton() {
  return (
    <div>
      <div className="grid 2xl:grid-cols-5 xl:grid-cols-4 lg:grid-cols-3 md:grid-cols-2 sm:grid-cols-1 gap-4 my-6">
        {Array(20)
          .fill(null)
          .map((_, index) => (
            <ProductsListItemSkeleton key={index} />
          ))}
      </div>
    </div>
  );
}

export function BreadCrumbSkeleton() {
  return <div className="skeleton w-12 h-4 rounded-3xl"></div>;
}

export function ReviewCardSkeleton() {
  return (
    <li className="skeleton list-row">
      <div className="skeleton size-8"></div>
      <div>
        <div className="skeleton text-xs uppercase font-semibold opacity-60"></div>
      </div>
      <p className="skeleton list-col-wrap text-xs"></p>
    </li>
  );
}

export function ReviewSkeleton() {
  return (
    <ul className="skeleton list bg-base-100 rounded-box shadow-md">
      {Array(20)
        .fill(null)
        .map((_, index) => (
          <ReviewCardSkeleton key={index} />
        ))}
    </ul>
  );
}

export function ProductSkeleton() {
  return (
    <div className="sm:grid max-w-(--breakpoint-2xl)  sm:grid-cols-3 flex flex-col items-center  justify-between content-between place-content-between gap-8 w-11/12 p-4">
      {/* Breadcrumb and the title*/}
      <div className="flex flex-col items-center sm:place-self-end gap-2  col-span-3">
        {/* BreadCrumb */}
        <div className="flex gap-1">
          <div className="skeleton w-16 h-4 "></div>
          <div className="skeleton w-16 h-4 "></div>
          <div className="skeleton w-16 h-4 "></div>
        </div>
        {/* Product title */}
        <div className="skeleton w-[200px] h-4"></div>
      </div>
      {/* Product Image and subimages */}
      <div className="flex flex-col gap-2 h-[247px] max-w-[350px]  items-center w-full">
        <div className="skeleton w-full h-10/12"></div>
        <div className="flex gap-1.5 w-full  h-2/12">
          <div className="flex-1 h-full skeleton"></div>
          <div className="flex-1 h-full skeleton"></div>
          <div className="flex-1 h-full skeleton"></div>
          <div className="flex-1 h-full skeleton"></div>
          <div className="flex-1 h-full skeleton"></div>
        </div>
      </div>
      {/* Product middle text info */}
      <div className="flex-col gap-3 hidden md:flex self-start">
        <div className="h-4 w-64 skeleton"></div>
        <div className="h-4 w-20 skeleton"></div>
        <div className="h-4 w-20 skeleton"></div>
        <div className="h-4 w-20 skeleton"></div>
        <div className="flex gap-1">
          <div className="h-8 w-8 rounded-full skeleton"></div>
          <div className="h-8 w-8 rounded-full skeleton"></div>
          <div className="h-8 w-8 rounded-full skeleton"></div>
        </div>
      </div>
      {/* Add to cart button */}
      <div className="flex flex-col w-[200px] justify-between h-full items-end justify-self-end col-start-3">
        <div className="w-full h-9/12 skeleton"></div>
        <div className="btn w-full skeleton "></div>
      </div>
    </div>
  );
}

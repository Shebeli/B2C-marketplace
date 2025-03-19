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

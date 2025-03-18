export function NavbarProfileSkeleton() {
  return <div className="skeleton w-10 h-10 rounded-full "></div>;
}

export function ProductsListSkeleton() {
  return (
    <div className="grid 2xl:grid-cols-5 xl:grid-cols-4 lg:grid-cols-3 md:grid-cols-2 sm:grid-cols-1 gap-4 my-6 skeleton">
      <div className="card bg-base-100 shadow-lg">
        <figure className="mx-8 min-h-52 min-w-52" />
        <div className="card-body">
          <div className="flex items-center">
            <div className="avatar">
              <div className="w-7 rounded-full skeleton"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export function BreadCrumbSkeleton() {
  return <div className="skeleton w-12 h-4 rounded-3xl"></div>;
}

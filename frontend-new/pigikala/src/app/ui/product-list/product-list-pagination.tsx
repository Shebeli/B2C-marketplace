"use client";

import { parseAsInteger, useQueryState } from "nuqs";
import Pagination from "rc-pagination";
import "rc-pagination/assets/index.css";

export default function ProductListPagination({
  itemTotalCount,
}: {
  itemTotalCount: number;
}) {
  const [page, setPage] = useQueryState(
    "page",
    parseAsInteger
      .withOptions({
        shallow: false,
        history: "push",
      })
      .withDefault(1)
  );

  const handlePageChange = (selectedPage: number) => {
    setPage(selectedPage);
  };

  if (itemTotalCount / 20 <= 1) return null;

  return (
    <Pagination
      pageSize={20}
      total={itemTotalCount}
      current={page}
      onChange={handlePageChange}
      className="place-self-center flex gap-1"
    />
  );
}

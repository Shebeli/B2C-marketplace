"use client";

import { useEffect } from "react";
import { ErrorInfo } from "../lib/fetch/fetchWrapper";
import DeadFaceIcon from "../ui/deadFaceIcon";
import Link from "next/link";

export default function Error({
  error,
}: {
  error: ErrorInfo & { digest?: string };
}) {
  useEffect(() => {
    console.error(error.details);
  }, [error]);
  console.log(error)
  return (
    <div className="flex flex-col gap-4 items-center my-8">
      <DeadFaceIcon width={160} height={160} />
      <h1 className="text-3xl">{error.status} hi</h1>
      <h2 className="text-3xl">یک خطایی پیش آمده است!</h2>

      <Link href="/">
        <button className="btn btn-lg btn-error rounded-xl">بازگشت به صفحه اصلی</button>
      </Link>
    </div>
  );
}

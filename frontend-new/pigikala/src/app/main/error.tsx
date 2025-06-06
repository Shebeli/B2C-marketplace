"use client";

import Link from "next/link";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useEffect } from "react";
import DeadFaceIcon from "../ui/deadFaceIcon";

export default function Error({
  error,
}: {
  error: Error & { digest?: string };
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  const searchParams = useSearchParams();
  const { replace } = useRouter();
  const pathname = usePathname();
  let errorData;
  try {
    errorData = JSON.parse(error.message);
  } catch {
    errorData = {
      status: 500,
      userMessage: "یک خطای داخلی پیش آمده است.",
      details: "Error in parsing error.message data in error.tsx boundary.",
    };
  }

  const handleQueryParamReset = () => {
    const params = new URLSearchParams();

    const currentSubCategoryId = searchParams.get("subCategoryId");
    if (currentSubCategoryId) {
      params.set("subCategoryId", currentSubCategoryId);
    }

    replace(`${pathname}?${params.toString()}`);
  };

  return (
    <div className="flex flex-col gap-3 items-center my-8">
      <DeadFaceIcon width={160} height={160} />
      <h1 className="text-4xl text-secondary font-semibold italic">
        {" "}
        {errorData.status}
      </h1>
      <h2 className="text-2xl mb-2">{errorData.userMessage}</h2>
      {errorData.type === "QueryParamError" ? (
        <button
          className="btn btn-lg btn-primary rounded-xl"
          onClick={handleQueryParamReset}
        >
          ریست پارامتر های جست و جو
        </button>
      ) : (
        <Link href="/">
          <button className="btn btn-lg btn-primary rounded-xl">
            بازگشت به صفحه اصلی
          </button>
        </Link>
      )}
    </div>
  );
}

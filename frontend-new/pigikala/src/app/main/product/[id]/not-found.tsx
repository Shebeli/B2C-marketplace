"use client";

import DeadFaceIcon from "@/app/ui/deadFaceIcon";
import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex flex-col gap-3 items-center my-8">
      <DeadFaceIcon width={160} height={160} />
      <h1 className="text-4xl text-secondary font-semibold italic">404</h1>
      <h2 className="text-2xl mb-2">محصول مورد نظر یافت نشد.</h2>
      <Link href="/">
        <button className="btn btn-lg btn-primary rounded-xl">
          بازگشت به صفحه اصلی
        </button>
      </Link>
    </div>
  );
}

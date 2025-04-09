"use client";

import { useEffect, useRef } from "react";

export default function HomeModal() {
  const welcomeModalRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const hasSeenModal = localStorage.getItem("homeModalSeen");
    if (!hasSeenModal) {
      welcomeModalRef.current?.showModal();
    }
  }, []);

  return (
    <dialog ref={welcomeModalRef} id="my_modal_3" className="modal">
      <div className="modal-box border-[6px] border-info">
        <button
          onClick={() => {
            localStorage.setItem("homeModalSeen", "true");
            welcomeModalRef.current?.close();
          }}
          className="btn btn-sm btn-ghost btn-circle absolute right-2 top-2"
        >
          ✕
        </button>
        <h3 className="font-bold text-lg mt-4">
          {" "}
          خوش آمدید! <span className="text-3xl">😊</span>
        </h3>
        <ul className="py-4 flex flex-col gap-6 font-medium">
          <li>
            تمامی اطلاعات، نمادها و نشان‌های موجود در این پروژه صرفاً برای تکمیل
            نمونه‌کار ارائه شده‌اند و هیچ‌گونه اعتبار رسمی ندارند.
          </li>
          <li>
            در این پروژه، هدف اصلی صرفاً پرداختن به جزئیات نبوده است؛ بلکه تلاش
            شده تا تمامی ویژگی‌های کلیدی و مهم به بهترین شکل ممکن پیاده‌سازی
            شوند و از پرداختن به امکانات غیرضروری پرهیز شود.
          </li>
          <li>
            شایان ذکر است که تمرکز اصلی این پروژه بر توسعه بخش بک‌اند بوده و این
            بخش با جزئیات بیشتری نسبت به فرانت‌اند تکمیل شده است. به همین دلیل،
            برخی از ویژگی‌های اپلیکیشن در سمت فرانت‌اند، به دلیل حجم بالای
            پروژه، هنوز در حال پیاده سازی هستند.
          </li>
        </ul>
      </div>
    </dialog>
  );
}

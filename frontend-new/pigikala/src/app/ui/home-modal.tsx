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
            این آپ در حالت لوکال می باشد و تمام داده ها موجود در آن غیر واقعی می
            باشد صرفا جهت تست و نمونه در این حالت قرار دارد.
          </li>

          <li>
            شایان ذکر است که بخش فرانت در حال تکمیل می باشد, و تمام نمونه کالا
            ها, نظرات, و دیگر داده های موجود در این آپ بصورت رندوم تولید شده
            اند.
          </li>
          <li>
            سرویس دریافت اس ام اس جهت ثبت نام / ورود در محیط لوکال, در ترمینال
            سرویس سلری کد را چاپ میکند.
          </li>
        </ul>
      </div>
    </dialog>
  );
}

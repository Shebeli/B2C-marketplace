import {
  FaHeadset,
  FaCreditCard,
  FaTruck,
  FaCalendarCheck,
} from "react-icons/fa6";

export default function ProductFooter() {
  return (
    <div className="flex gap-16 max-w-(--breakpoint-2xl)  place-self-center justify-between border-y-2 border-base-300 p-4 px-8 mt-8 w-full">
      <div className="bg-base flex flex-col items-center gap-2 ">
        <FaHeadset className="text-4xl" />
        <p>پشتیبانی 24 ساعته</p>
      </div>
      <div className="bg-base flex flex-col items-center gap-2">
        <FaCreditCard className="text-4xl" />
        <p> امکان پرداخت در محل </p>
      </div>
      <div className="bg-base flex flex-col items-center gap-2">
        <FaTruck className="text-4xl" />
        <p>تحویل به موقع</p>
      </div>
      <div className="bg-base flex flex-col items-center gap-2">
        <FaCalendarCheck className="text-4xl" />
        <p>7 روز ضمانت بازگشت کالا</p>
      </div>
    </div>
  );
}

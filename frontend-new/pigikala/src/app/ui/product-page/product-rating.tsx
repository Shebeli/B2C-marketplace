import { FaStar } from "react-icons/fa6";

export default function ProductRating({
  rating,
  buyersCount,
}: {
  rating: number;
  buyersCount: number;
}) {
  return (
    <div className="flex gap-1">
      <FaStar className=" text-yellow-300" />
      <p className="font-light text-sm">
        {rating} امتیاز ( از {buyersCount} خریدار)
      </p>
    </div>
  );
}

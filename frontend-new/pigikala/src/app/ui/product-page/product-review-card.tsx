import { ProductReviewUI } from "@/app/lib/types/ui/product-detail/productReviewUI";
import Image from "next/image";
import { DEFAULT_PROFILE_IMAGE_URL } from "@/app/lib/constants/assets";
import { FaRegThumbsDown, FaRegThumbsUp } from "react-icons/fa6";

interface ReviewCardProps {
  review: ProductReviewUI;
}

export default function ReviewCard({ review }: ReviewCardProps) {
  return (
    <li className="list-row border-y-[1px] border-x-[1px] border-base-300 my-0.5">
      <div></div>
      <div>
        <div className="flex items-end gap-2">
          <Image
            width={32}
            height={32}
            alt={`${review.reviewedBy.fullName} Profile Picture`}
            className="size-8 rounded-box"
            src={review.reviewedBy.profilePicture ?? DEFAULT_PROFILE_IMAGE_URL}
          />
          <div className="text-xs mb-2">{review.reviewedBy.fullName}</div>
        </div>
        <div className="font-semibold mt-2">
          <span className="flex items-center gap-x-2">
            <div className="rating">
              {/* DaisyUI rating component */}
              {Array(5)
                .fill(null)
                .map((_, index) => (
                  <div
                    key={index}
                    className="mask mask-star-2 size-3.5 bg-orange-400"
                    aria-label={`${index + 1} star`}
                    aria-current={review.rating === index + 1}
                  ></div>
                ))}
            </div>{" "}
            <h1>{review.title}</h1>
          </span>
        </div>
      </div>
      <p className="list-col-wrap text-xs">{review.description}</p>
      <button className="btn btn-sm btn-square btn-ghost">
        <FaRegThumbsUp className="size-4" />
      </button>
      <button className="btn btn-sm btn-square btn-ghost">
        <FaRegThumbsDown className="size-4" />
      </button>
    </li>
  );
}

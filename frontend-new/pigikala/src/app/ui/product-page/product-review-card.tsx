import { ProductReviewUI } from "@/app/lib/types/ui/product-detail/productReviewUI";
import Image from "next/image";
import { DEFAULT_PROFILE_IMAGE_URL } from "@/app/lib/constants/assets";

interface ReviewCardProps {
  review: ProductReviewUI;
}

export default function ReviewCard({ review }: ReviewCardProps) {
  return (
    <li className="list-row">
      <div>
        <Image
          alt={`${review.reviewedBy.fullName} Profile Picture`}
          className="size-8 rounded-box"
          src={review.reviewedBy.profilePicture ?? DEFAULT_PROFILE_IMAGE_URL}
        />
      </div>
      <div>
        <div>{review.reviewedBy.fullName}</div>
        <div className="text-xs uppercase font-semibold opacity-60">
          {review.title}
        </div>
      </div>
      <p className="list-col-wrap text-xs">{review.description}</p>
      <button className="btn btn-square btn-ghost">
        <svg
          className="size-[1.2em]"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
        >
          <g
            strokeLinejoin="round"
            strokeLinecap="round"
            strokeWidth="2"
            fill="none"
            stroke="currentColor"
          >
            <path d="M6 3L20 12 6 21 6 3z"></path>
          </g>
        </svg>
      </button>
      <button className="btn btn-square btn-ghost">
        <svg
          className="size-[1.2em]"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
        >
          <g
            strokeLinejoin="round"
            strokeLinecap="round"
            strokeWidth="2"
            fill="none"
            stroke="currentColor"
          >
            <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path>
          </g>
        </svg>
      </button>
    </li>
  );
}

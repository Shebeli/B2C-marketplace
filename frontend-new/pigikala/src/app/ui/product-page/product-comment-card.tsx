import { DEFAULT_PROFILE_IMAGE_URL } from "@/app/lib/constants/assets";
import { ProductCommentUI } from "@/app/lib/types/ui/product-detail/productCommentUI";
import Image from "next/image";

interface CommentCard {
  comment: ProductCommentUI;
}

export default function ProductCommentCard({ comment }: CommentCard) {
  return (
    <li className="list-row">
      <div>
        <Image
          alt={`${comment.commentedBy.fullName} Profile Picture`}
          className="size-8 rounded-box"
          src={comment.commentedBy.profilePicture ?? DEFAULT_PROFILE_IMAGE_URL}
        />
      </div>
      <div>
        <div>{comment.commentedBy.fullName}</div>
        <div className="text-xs uppercase font-semibold opacity-60">
          {comment.title}
        </div>
      </div>
      <p className="list-col-wrap text-xs">{comment.description}</p>
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

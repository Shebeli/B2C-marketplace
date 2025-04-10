import { DEFAULT_PROFILE_IMAGE_URL } from "@/app/lib/constants/assets";
import { ProductCommentUI } from "@/app/lib/types/ui/product-detail/productCommentUI";
import Image from "next/image";

interface CommentCard {
  comment: ProductCommentUI;
}

export default function ProductCommentCard({ comment }: CommentCard) {
  return (
    <li className="list-row border-y-[1px] border-x-[1px] border-base-300 my-0.5">
      <div></div>
      <div>
        <div className="flex items-end gap-2">
          <Image
            width={32}
            height={32}
            alt={`${comment.commentedBy.fullName} Profile Picture`}
            className="size-8 rounded-box"
            src={
              comment.commentedBy.profilePicture ?? DEFAULT_PROFILE_IMAGE_URL
            }
          />
          <div className="text-xs mb-2">{comment.commentedBy.fullName}</div>
        </div>
        <div className="font-semibold mt-2">
          <span className="flex items-center gap-x-2">
            <h1>{comment.title}</h1>
          </span>
        </div>
      </div>
      <p className="list-col-wrap text-xs">{comment.description}</p>
      <button className="btn btn-sm btn-secondary place-self-end">Reply</button>
    </li>
  );
}

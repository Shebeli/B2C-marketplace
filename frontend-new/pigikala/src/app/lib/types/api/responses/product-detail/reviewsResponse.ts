import { Paginated } from "../generalResponses";

export interface ProductReviewAPI {
  id: number;
  rating: number;
  title: string;
  description: string;
  createdAt: string;
  updatedAt: string;
  reviewedBy: {
    id: number;
    fullName: string;
    profilePicture: string | null;
  };
}

export type ProductReviewPaginatedAPI = Paginated<ProductReviewAPI>;

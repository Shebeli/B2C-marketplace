export interface ProductReviewUI {
  id: number;
  rating: number;
  title: string;
  description: string;
  createdRelativeTime: string;
  updatedRelativeTime: string;
  reviewedBy: {
    id: number;
    fullName: string;
    profilePicture: string | null;
  };
}

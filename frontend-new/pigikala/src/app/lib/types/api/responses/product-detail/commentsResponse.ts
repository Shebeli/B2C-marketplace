
interface ProductCommenter {
  id: number;
  fullName: string;
  profilePicture: string | null;
}

export interface ProductCommentAPI {
  id: number;
  title: string;
  description: string;
  createdAt: string;
  updatedAt: string;
  commentedBy: ProductCommenter;
}


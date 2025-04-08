export interface ProductCommentUI {
    id: number;
    title: string;
    description: string;
    createdRelativeTime: string;
    updatedRelativeTime: string;
    commentedBy: {
      id: number;
      fullName: string;
      profilePicture: string | null;
    };
  }
  
export type Post = {
  id: string;
  author: string;
  title: string;
  createdAt: string;
  imageLink?: string;
  reactions: number;
  comments: { id: string;authorId: string; authorName: string; text: string }[];
};


export type GetPostsData = {
  posts: Post[];
};
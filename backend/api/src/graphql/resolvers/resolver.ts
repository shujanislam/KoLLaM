import { IResolvers } from "@graphql-tools/utils";
import { GraphQLScalarType, Kind } from "graphql";
import Post, { IPost } from "../../models/Post";

export const resolvers: IResolvers = {
  // Custom scalar for Date
  Date: new GraphQLScalarType({
    name: "Date",
    description: "Custom Date scalar type",
    serialize(value: unknown) {
      return (value as Date).toISOString(); // send to client
    },
    parseValue(value: unknown) {
      return new Date(value as string); // from client
    },
    parseLiteral(ast) {
      if (ast.kind === Kind.STRING) return new Date(ast.value);
      return null;
    },
  }),

  Query: {
    posts: async (): Promise<IPost[]> => {
      return await Post.find();
    },

    getPost: async (_parent, { id }: { id: string }): Promise<IPost | null> => {
      return await Post.findById(id);
    },
  },

  Mutation: {
    createPost: async (
      _parent,
      { title, content, image_link, author }: { title: string; content: string; image_link: string; author: string }
    ): Promise<IPost> => {
      const newPost = new Post({
        title,
        content,
        image_link,
        author,
        createdAt: new Date(),
      });
      await newPost.save();
      return newPost;
    },

    deletePost: async (_parent, { id }: { id: string }): Promise<IPost | null> => {
      const deleted = await Post.findByIdAndDelete(id);
      return deleted;
    },
  },
};

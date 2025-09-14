"use client";

import Image from "next/image";
import { gql } from '@apollo/client';
import { useQuery, useMutation } from "@apollo/client/react";
import { useState } from "react";

// --- GraphQL Queries/Mutations ---
const GET_POSTS = gql`
  query GetPosts {
    posts {
      id
      title
      author
      createdAt
    }
  }
`;

const CREATE_POST = gql`
  mutation CreatePost(
    $title: String!
    $image_link: String!
    $content: String!
    $author: String!
  ) {
    createPost(
      title: $title
      image_link: $image_link
      content: $content
      author: $author
    ) {
      id
      title
    }
  }
`;

// --- React Component ---
export default function FeedPage() {
  const [title, setTitle] = useState("");
  const [imageLink, setImageLink] = useState("");
  const [content, setContent] = useState("");
  const [author, setAuthor] = useState("");

  const { data, loading: loadingPosts, error: errorPosts } = useQuery(GET_POSTS);
  const [createPost, { loading: creating, error: errorCreate }] = useMutation(CREATE_POST, {
    refetchQueries: [{ query: GET_POSTS }],
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await createPost({
      variables: { title, image_link: imageLink, content, author },
    });
    setTitle("");
    setImageLink("");
    setContent("");
    setAuthor("");
  };

  return (
    <div className="max-w-3xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Create New Post</h1>
      <form className="flex flex-col gap-2 mb-8" onSubmit={handleSubmit}>
        <input
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="border p-2 rounded"
        />
        <input
          placeholder="Image Link"
          value={imageLink}
          onChange={(e) => setImageLink(e.target.value)}
          className="border p-2 rounded"
        />
        <textarea
          placeholder="Content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="border p-2 rounded"
        />
        <input
          placeholder="Author"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
          className="border p-2 rounded"
        />
        <button
          type="submit"
          disabled={creating}
          className="bg-green-500 text-white p-2 rounded mt-2"
        >
          {creating ? "Creating..." : "Create Post"}
        </button>
        {errorCreate && <p className="text-red-500">{errorCreate.message}</p>}
      </form>

      <h2 className="text-2xl font-bold mb-4">All Posts</h2>
      {loadingPosts ? (
        <p>Loading posts...</p>
      ) : errorPosts ? (
        <p className="text-red-500">{errorPosts.message}</p>
      ) : (
        <ul className="space-y-4">
          {data?.posts?.map((post: any) => (
            <li key={post.id} className="border p-4 rounded shadow">
              <h3 className="font-semibold">{post.title}</h3>
              <p className="text-sm text-gray-600">By {post.author}</p>
              <p className="text-xs text-gray-400">{post.createdAt}</p>

              <div className="mt-2">
                <Image
                  src={
                    post.image_link?.startsWith("http")
                      ? post.image_link
                      : "/fallback.jpg" // put a fallback image inside /public/
                  }
                  alt={post.title}
                  width={600}
                  height={400}
                  className="rounded"
                />
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

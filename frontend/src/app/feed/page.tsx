"use client";

import Image from "next/image";
import { gql } from '@apollo/client';
import { useQuery, useMutation } from "@apollo/client/react";
import { useState } from "react";
import { motion } from "framer-motion";
import Navbar from '../components/Navbar.tsx';

// --- GraphQL Queries/Mutations ---
const GET_POSTS = gql`
  query GetPosts {
    posts {
      id
      title
      image_link
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
<>
  <Navbar />
<div className="max-w-5xl mx-auto p-6">
      {/* --- Create Post Form --- */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-white p-6 rounded-2xl shadow-xl mb-10"
      >
        <h1 className="text-3xl font-extrabold text-purple-700 mb-6">
          ✍️ Create New Post
        </h1>

        <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
          <input
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="border p-3 rounded-lg shadow-sm focus:ring-2 focus:ring-purple-400 outline-none"
          />
          <input
            placeholder="Image Link"
            value={imageLink}
            onChange={(e) => setImageLink(e.target.value)}
            className="border p-3 rounded-lg shadow-sm focus:ring-2 focus:ring-purple-400 outline-none"
          />
          <textarea
            placeholder="Content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="border p-3 rounded-lg shadow-sm h-28 focus:ring-2 focus:ring-purple-400 outline-none"
          />
          <input
            placeholder="Author"
            value={author}
            onChange={(e) => setAuthor(e.target.value)}
            className="border p-3 rounded-lg shadow-sm focus:ring-2 focus:ring-purple-400 outline-none"
          />
          <button
            type="submit"
            disabled={creating}
            className="bg-gradient-to-r from-purple-600 to-pink-500 text-white py-3 rounded-lg font-semibold shadow hover:opacity-90 transition"
          >
            {creating ? "Creating..." : "🚀 Create Post"}
          </button>
          {errorCreate && (
            <p className="text-red-500 font-medium">{errorCreate.message}</p>
          )}
        </form>
      </motion.div>

      {/* --- Posts Feed --- */}
      <h2 className="text-3xl font-extrabold text-purple-700 mb-6">📰 All Posts</h2>

      {loadingPosts ? (
        <p>Loading posts...</p>
      ) : errorPosts ? (
        <p className="text-red-500">{errorPosts.message}</p>
      ) : (
        <motion.ul
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.6 }}
          className="space-y-6"
        >
          {data?.posts?.map((post: any, idx: number) => (
            <motion.li
              key={post.id}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1, duration: 0.5 }}
              className="bg-white border rounded-xl shadow-lg p-6 hover:shadow-2xl transition"
            >
              <h3 className="text-2xl font-bold text-gray-800 mb-2">
                {post.title}
              </h3>
              <p className="text-sm text-gray-500 mb-1">By {post.author}</p>
              <p className="text-xs text-gray-400 mb-4">{post.createdAt}</p>
              <div className="mt-2 rounded-lg overflow-hidden">
                <Image
                  src={
                    post.image_link?.startsWith("http")
                      ? post.image_link
                      : "/fallback.jpg"
                  }
                  alt={post.title}
                  width={800}
                  height={500}
                  className="rounded-lg object-cover"
                />
              </div>
            </motion.li>
          ))}
        </motion.ul>
      )}
    </div>
</>
  );
}

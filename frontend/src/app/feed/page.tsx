"use client";

import Image from "next/image";
import { gql } from '@apollo/client';
import { useQuery, useMutation } from "@apollo/client/react";
import {GetPostsData, Post} from "@/app/feed/data"
import { useState } from "react";
import {Heart,MessageCircle} from 'lucide-react'

// --- GraphQL Queries/Mutations ---
// i have changed the query accoding to the data needed but db have to be changed too
const GET_POSTS = gql`
  query GetPosts {
    posts {
      id
      title
      image_link
      author
      createdAt
      reactions
      comments
      image_link
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
  //const [author, setAuthor] = useState(""); can get from user profile
  const [showModal, setShowModal] = useState(false);
  const [photo, setPhoto] = useState<string | null>(null);
  const [photoPreview, setPhotoPreview] = useState<string | null>(null);
  const { data, loading: loadingPosts, error: errorPosts } = useQuery<GetPostsData>(GET_POSTS);
  const [createPost, { loading: creating, error: errorCreate }] = useMutation(CREATE_POST, {
    refetchQueries: [{ query: GET_POSTS }],
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await createPost({
      variables: { 
        title: title || "Photo Post", 
        image_link: imageLink, 
        content: content,
        author: "Anonymous" //get from user profile
      },
    });
    setShowModal(false);
    setTitle("");
    setContent("");
    setImageLink("");
    setPhotoPreview(null);
    setPhoto(null);
  };

  function handlePhotoChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (file && file.type.startsWith("image/")) {
      const reader = new FileReader();
      reader.onload = () => setPhotoPreview(reader.result as string);
      reader.readAsDataURL(file);
      setPhoto(file.name);
    } else {
      setPhoto(null);
      setPhotoPreview(null);
      setImageLink("");
    }
  }

  /* if (loadingPosts) {
    return <p>Loading posts...</p>;
  }

  if (errorPosts) {
    return <p className="text-red-500">{errorPosts.message}</p>;
  } */

  return (
    <div className="flex flex-col gap-4 bg-gradient-to-br from-gray-50 via-white to-gray-100 min-h-screen p-2 sm:p-4 rounded-2xl">
      {/* have to add Trending Section to see top posts */}
      
      <button
        onClick={() => setShowModal(true)}
        className="self-end px-5 py-2 bg-black text-white rounded-full shadow hover:bg-gray-800 transition font-semibold mb-2"
      >
        Create New Post
      </button>

      {/* Button for new post */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
          <div className="bg-white rounded-xl shadow-lg p-6 w-full max-w-lg relative animate-fade-in">
            <button
              className="absolute top-2 right-2 text-gray-400 hover:text-gray-700 text-2xl font-bold"
              onClick={() => setShowModal(false)}
              aria-label="Close"
            >

              
            </button>
            <h2 className="text-xl font-bold text-black mb-4">Create New Post</h2>
            <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
              <input
                className="border rounded px-2 py-1 text-black"
                placeholder="Post title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
              <textarea
                className="border rounded px-2 py-1 min-h-[80px] text-black"
                placeholder="Write something..."
                value={content}
                onChange={(e) => setContent(e.target.value)}
              />
              <input
                className="text-black"
                type="file"
                accept="image/*"
                onChange={handlePhotoChange}
              />
              {photoPreview && (
                <img src={photoPreview} alt="Preview" className="max-h-60 object-contain rounded" />
              )}
              <button
                type="submit"
                className="bg-black text-white px-4 py-2 rounded disabled:opacity-50"
                disabled={!content && !photoPreview}
              >
                Post
              </button>
            </form>
            <div className="text-xs text-gray-500 mt-2">You can upload only text, only photo, or both combined.</div>
          </div>
        </div>
      )}

      <ul className="space-y-4">
        {data?.posts.map((post: Post) => (
          <li key={post.id} className="bg-white rounded-lg shadow flex border border-gray-100 hover:shadow-lg transition overflow-hidden">
            {/* Left actions column */}
            <div className="flex flex-col items-center justify-start px-2 py-4 bg-gray-50 border-r border-gray-100 min-w-[48px]">
              <button className="text-gray-400 hover:text-pink-500 mb-2" title="Like" disabled>
                <Heart/>
              </button>
              <span className="font-semibold text-gray-700 text-sm mb-2">{post.reactions}</span>
              <button className="text-gray-400 hover:text-blue-500" title="Comment" disabled>
                <MessageCircle/>
              </button>
              <span className="font-semibold text-gray-700 text-sm">{post.comments.length}</span>
            </div>
            {/* Main post content */}
            <div className="flex-1 flex flex-col gap-2 p-4">
              <div className="flex items-center gap-2 mb-1">
                <a href={`/posts/${post.id}`} className="text-lg font-bold text-gray-900 hover:underline truncate flex-1">{post.title || "Photo Post"}</a>
                <span className="text-xs text-gray-400">By {post.author}</span>

              </div>
              {post.image_link && (
                <div className="w-full flex justify-center items-center">
                  <Image 
                    src={post.image_link?.startsWith("http") ? post.image_link : "/fallback.jpg"}
                    alt={post.title || "Post image"} 
                    width={400}
                    height={400}
                    className="rounded-md border border-gray-200 shadow-sm w-full h-auto max-h-[400px] object-contain bg-gray-100" 
                    style={{maxWidth:'100%'}} 
                  />
                </div>
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

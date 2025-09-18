"use client";

import Link from "next/link";
import { motion } from "framer-motion";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-purple-100 via-white to-pink-100 p-6">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center max-w-3xl"
      >
        <h1 className="text-5xl font-extrabold text-purple-800 drop-shadow mb-4">
          KoLLaM: Where Tradition Meets AI
        </h1>
        <p className="text-lg text-gray-700 mb-6">
          Generate unique Kolam designs, evaluate them with AI based on real
          rules, and share your creativity with the community.
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/feed"
            className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg shadow"
          >
            Explore Kolams
          </Link>
          <Link
            href="/generate"
            className="bg-pink-500 hover:bg-pink-600 text-white px-6 py-3 rounded-lg shadow"
          >
            Generate Now
          </Link>
        </div>
      </motion.div>

      {/* Features Section */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5, duration: 0.8 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20 max-w-5xl"
      >
        <div className="p-6 bg-white rounded-2xl shadow-lg text-center">
          <h2 className="text-xl font-bold mb-2">🎨 Kolam Generator</h2>
          <p className="text-gray-600">
            Create stunning Kolam designs instantly with AI-powered generation.
          </p>
        </div>

        <div className="p-6 bg-white rounded-2xl shadow-lg text-center">
          <h2 className="text-xl font-bold mb-2">🤖 AI Evaluation</h2>
          <p className="text-gray-600">
            Get instant feedback on your Kolam&apos;s authenticity and design
            quality.
          </p>
        </div>

        <div className="p-6 bg-white rounded-2xl shadow-lg text-center">
          <h2 className="text-xl font-bold mb-2">🌐 Social Sharing</h2>
          <p className="text-gray-600">
            Share your Kolams with the world and explore community creations.
          </p>
        </div>
      </motion.div>
    </main>
  );
}

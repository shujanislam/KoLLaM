"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import Navbar from "./components/Navbar";

export default function Home() {
  return (
    <>
      <Navbar />
      <main className="relative min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-white via-purple-50 to-pink-50 overflow-hidden">
        {/* Background Kolam Accent */}
        <div className="absolute inset-0 opacity-5 bg-[url('/kolam-bg.svg')] bg-center bg-no-repeat bg-cover pointer-events-none" />

        {/* Hero Section */}
        <motion.section
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="relative z-10 text-center max-w-4xl px-6"
        >
          <h1 className="text-6xl md:text-7xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-purple-700 via-pink-600 to-orange-400 drop-shadow-sm">
            KoLLaM
          </h1>
          <p className="mt-6 text-lg md:text-xl text-gray-700 leading-relaxed">
            A platform where{" "}
            <span className="font-semibold text-purple-700">tradition</span>{" "}
            meets{" "}
            <span className="font-semibold text-pink-600">technology</span>.  
            Generate Kolam designs, evaluate them with AI, and share your
            creativity with the world.
          </p>
          <div className="mt-8 flex gap-4 justify-center">
            <Link
              href="/feed"
              className="px-6 py-3 rounded-xl font-semibold text-white bg-gradient-to-r from-purple-600 to-pink-500 shadow-lg hover:opacity-90 transition"
            >
              Explore Kolams
            </Link>
            <Link
              href="/generate"
              className="px-6 py-3 rounded-xl font-semibold text-white bg-gradient-to-r from-pink-500 to-orange-400 shadow-lg hover:opacity-90 transition"
            >
              Generate Now
            </Link>
          </div>
        </motion.section>

        {/* Features Section */}
        <motion.section
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.9 }}
          className="relative z-10 grid grid-cols-1 md:grid-cols-3 gap-10 mt-24 max-w-6xl px-6"
        >
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="p-10 rounded-3xl bg-white/80 backdrop-blur-md border border-purple-100 shadow-xl text-left"
          >
            <h2 className="text-2xl font-bold text-purple-700 mb-4">
              🎨 Kolam Generator
            </h2>
            <p className="text-gray-600">
              Instantly create mesmerizing Kolam designs with our AI-powered
              generator that blends math, art, and tradition.
            </p>
          </motion.div>

          <motion.div
            whileHover={{ scale: 1.05 }}
            className="p-10 rounded-3xl bg-white/80 backdrop-blur-md border border-pink-100 shadow-xl text-left"
          >
            <h2 className="text-2xl font-bold text-pink-600 mb-4">
              🤖 AI Evaluation
            </h2>
            <p className="text-gray-600">
              Get real-time feedback on authenticity, symmetry, and design rules
              behind your Kolam.
            </p>
          </motion.div>

          <motion.div
            whileHover={{ scale: 1.05 }}
            className="p-10 rounded-3xl bg-white/80 backdrop-blur-md border border-orange-100 shadow-xl text-left"
          >
            <h2 className="text-2xl font-bold text-orange-500 mb-4">
              🌐 Community Sharing
            </h2>
            <p className="text-gray-600">
              Share your designs, explore others&apos; creations, and become a
              part of a global Kolam culture.
            </p>
          </motion.div>
        </motion.section>
      </main>
    </>
  );
}

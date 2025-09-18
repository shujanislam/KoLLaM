"use client";

import Link from "next/link";
import { motion } from "framer-motion";

export default function Navbar() {
  return (
    <motion.nav
      initial={{ y: -40, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6 }}
      className="w-full bg-white/80 backdrop-blur-md shadow-md border-b border-purple-100"
    >
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo / Brand */}
        <Link
          href="/"
          className="text-2xl font-extrabold bg-gradient-to-r from-purple-600 to-pink-500 bg-clip-text text-transparent tracking-tight"
        >
          KoLLaM
        </Link>

        {/* Nav Links */}
        <div className="flex gap-8 text-gray-700 font-medium">
          <Link
            href="/generate"
            className="hover:text-purple-600 transition-colors"
          >
            🎨 Generate
          </Link>
          <Link
            href="/evaluate"
            className="hover:text-purple-600 transition-colors"
          >
            🤖 Evaluate
          </Link>
          <Link
            href="/feed"
            className="hover:text-purple-600 transition-colors"
          >
            🌐 Community
          </Link>
        </div>
      </div>
    </motion.nav>
  );
}

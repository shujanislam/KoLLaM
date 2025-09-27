"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { useState } from "react";
import { Menu, X } from "lucide-react";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <motion.nav
      initial={{ y: -40, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6 }}
      className="fixed top-0 left-0 w-full z-50 bg-white/70 backdrop-blur-lg border-b border-purple-100 shadow-sm"
    >
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo / Brand */}
        <Link
          href="/"
          className="text-3xl font-extrabold bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 bg-clip-text text-transparent tracking-tight"
        >
          KoLLaM
        </Link>

        {/* Desktop Nav Links */}
        <div className="hidden md:flex gap-10 text-gray-700 font-medium">
          {[
            { href: "/generate", label: "Generate" },
            { href: "/evaluate", label: "Evaluate" },
            { href: "/feed", label: "Community" },
          ].map((link, i) => (
            <motion.div
              key={i}
              whileHover={{ scale: 1.05 }}
              className="relative group"
            >
              <Link
                href={link.href}
                className="hover:text-purple-600 transition-colors"
              >
                {link.label}
              </Link>
              <span className="absolute left-0 -bottom-1 w-0 h-[2px] bg-gradient-to-r from-purple-600 to-pink-500 group-hover:w-full transition-all"></span>
            </motion.div>
          ))}
        </div>

        {/* Mobile Menu Button */}
        <button
          className="md:hidden text-gray-700"
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? <X size={28} /> : <Menu size={28} />}
        </button>
      </div>

      {/* Mobile Nav Links */}
      {isOpen && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="md:hidden bg-white/90 backdrop-blur-lg shadow-md border-t border-purple-100 px-6 py-4 flex flex-col gap-4"
        >
          <Link href="/generate" className="hover:text-purple-600">
            🎨 Generate
          </Link>
          <Link href="/evaluate" className="hover:text-purple-600">
            🤖 Evaluate
          </Link>
          <Link href="/feed" className="hover:text-purple-600">
            🌐 Community
          </Link>
        </motion.div>
      )}
    </motion.nav>
  );
}

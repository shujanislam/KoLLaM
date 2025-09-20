import { ReactNode } from "react";

export default function PostsLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-white flex flex-col items-center w-full">
      <div className="w-full max-w-2xl md:max-w-5xl lg:max-w-7xl px-2 sm:px-6 md:px-12 py-8">
      <h1 className="text-4xl font-extrabold mb-8 text-gray-900 text-center tracking-tight scroll-m-20  text-balance">KolamGram</h1>
        {children}
      </div>
    </div>
  );
}

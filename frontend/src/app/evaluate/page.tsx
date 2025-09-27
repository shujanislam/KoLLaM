"use client";

import { useRef, useState, useEffect } from "react";
import Navbar from "../components/Navbar";

export default function EvaluatePage() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const gridSize = 50;
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string>("");
  const [loading, setLoading] = useState(false);

  // Draw dot grid
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    canvas.width = 500;
    canvas.height = 500;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#444";

    for (let x = gridSize; x < canvas.width; x += gridSize) {
      for (let y = gridSize; y < canvas.height; y += gridSize) {
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  }, []);

  // Handle file upload
  const handleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = e.target.files?.[0] || null;
    setFile(uploadedFile);
    setMessage(""); // reset message when new file uploaded
  };

  // Simulated evaluation
  const handleSubmit = () => {
    if (!file) {
      setMessage("⚠️ Please upload a file first.");
      return;
    }

    setLoading(true);
    setMessage("");

    setTimeout(() => {
      setLoading(false);
      if (file.name.toLowerCase().includes("kolam")) {
        setMessage("✅ This looks like a Kolam!");
      } else {
        setMessage("❌ Not a Kolam design.");
      }
    }, 5000); // 5 seconds fake delay
  };

  return (
    <>
      <Navbar />
      <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-purple-50 to-pink-50 p-6">
        <div className="bg-white p-8 rounded-2xl shadow-xl max-w-xl w-full text-center">
          <h1 className="text-3xl font-extrabold text-purple-700 mb-4">
            🎨 Evaluate Your Kolam
          </h1>
          <p className="text-gray-600 mb-6">
            Upload your design or draw on the grid below to check if it’s a legit Kolam.
          </p>

          {/* Upload input */}
          <input
            type="file"
            accept="image/*"
            onChange={handleUpload}
            className="block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 
                       file:rounded-full file:border-0 file:text-sm file:font-semibold 
                       file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100 mb-4"
          />

          {/* Submit button */}
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="bg-gradient-to-r from-purple-600 to-pink-500 text-white px-6 py-2 rounded-lg shadow-lg 
                       hover:scale-105 transition-transform disabled:opacity-50 mb-6"
          >
            {loading ? "⏳ Evaluating..." : "🚀 Submit for Evaluation"}
          </button>

          {/* Dot Grid Canvas */}
          <div className="flex justify-center">
            <canvas
              ref={canvasRef}
              className="border-2 border-purple-200 rounded-lg shadow-md bg-white"
              style={{ width: "500px", height: "500px" }}
            />
          </div>

          {/* Message */}
          {message && (
            <p
              className={`mt-4 text-lg font-semibold ${
                message.includes("✅") ? "text-green-600" : "text-red-600"
              }`}
            >
              {message}
            </p>
          )}
        </div>
      </div>
    </>
  );
}

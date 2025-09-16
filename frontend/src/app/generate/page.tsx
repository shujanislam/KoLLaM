"use client";
import { useState } from "react";

export default function KolamGenerator() {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [size, setSize] = useState<number>(8); // default value

  const handleGenerate = async () => {
    const res = await fetch("http://localhost:8081/generate-kolam", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ size }), // send size to backend
    });

    if (!res.ok) {
      console.error("Error generating kolam:", await res.text());
      return;
    }

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    setImageUrl(url);
  };

  return (
    <div className="p-4">
      <div className="flex items-center gap-2 mb-4">
        <input
          type="number"
          value={size}
          onChange={(e) => setSize(Number(e.target.value))}
          className="border p-2 rounded w-24"
          placeholder="Size"
          min={2}
          max={50}
        />
        <button
          onClick={handleGenerate}
          className="bg-green-500 text-white px-4 py-2 rounded"
        >
          Generate Kolam
        </button>
      </div>

      {imageUrl && (
        <div className="mt-4">
          <img
            src={imageUrl}
            alt="Generated Kolam"
            className="rounded shadow"
          />
        </div>
      )}
    </div>
  );
}

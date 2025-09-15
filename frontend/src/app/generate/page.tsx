"use client";
import { useState } from "react";

export default function KolamGenerator() {
  const [imageUrl, setImageUrl] = useState<string | null>(null);

  const handleGenerate = async () => {
    const res = await fetch("http://localhost:8081/generate-kolam", {
      method: "POST",
    });

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    setImageUrl(url);
  };

  return (
    <div className="p-4">
      <button 
        onClick={handleGenerate} 
        className="bg-green-500 text-white px-4 py-2 rounded"
      >
        Generate Kolam
      </button>

      {imageUrl && (
        <div className="mt-4">
          <img src={imageUrl} alt="Generated Kolam" className="rounded shadow" />
        </div>
      )}
    </div>
  );
}

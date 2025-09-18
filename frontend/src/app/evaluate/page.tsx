"use client";

import { useEffect, useRef, useState } from "react";
import Navbar from '../components/Navbar';
import KulSvg from '../../savage/kul.svg';
import LuSvg from '../../savage/lu.svg';

// Define shape types
type ShapeType = 'kul' | 'lu' | 'freehand';

interface Shape {
  type: ShapeType;
  x: number;
  y: number;
  size: number;
  color: string;
}

export default function DrawPage() {
  const gridSize = 70;
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [lastPosition, setLastPosition] = useState({ x: 0, y: 0 });
  const [selectedShape, setSelectedShape] = useState<ShapeType>('freehand');
  const [shapes, setShapes] = useState<Shape[]>([]);
  const [brushSize, setBrushSize] = useState(2);
  const [brushColor, setBrushColor] = useState('#000000');
  const [svgImages, setSvgImages] = useState<{ [key: string]: HTMLImageElement }>({});
  const [draggedShapeIndex, setDraggedShapeIndex] = useState<number | null>(null);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const [originalShapePosition, setOriginalShapePosition] = useState<{ x: number, y: number } | null>(null);
  const [backgroundImage, setBackgroundImage] = useState<HTMLImageElement | null>(null);
  const [showGrid, setShowGrid] = useState(true);
  const [evaluationStatus, setEvaluationStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

  useEffect(() => {
    const svgsToLoad = {
      kul: KulSvg.src,
      lu: LuSvg.src,
    };

    Object.entries(svgsToLoad).forEach(([name, src]) => {
      const img = new Image();
      img.src = src as string;
      img.onload = () => {
        setSvgImages((prev) => ({ ...prev, [name]: img }));
      };
    });
  }, []);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const context = canvas.getContext('2d');
    if (!context) return;

    canvas.width = 800;
    canvas.height = 600;
    context.strokeStyle = brushColor;
    context.lineWidth = brushSize;
    context.lineCap = 'round';
    context.lineJoin = 'round';

    redrawCanvas();
  }, [brushSize, brushColor, backgroundImage, shapes]);

  const drawGrid = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
    ctx.beginPath();
    ctx.strokeStyle = '#e0e0e0';
    ctx.lineWidth = 0.5;

    for (let x = 0; x <= width; x += gridSize) {
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
    }

    for (let y = 0; y <= height; y += gridSize) {
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
    }

    ctx.stroke();
  };

  // New function to draw imported SVG
  const drawSVGShape = (ctx: CanvasRenderingContext2D, x: number, y: number, size: number, color: string, type: 'kul' | 'lu') => {
    const svgImage = svgImages[type];
    if (!svgImage) return;

    // Save current context
    ctx.save();

    // Apply color filter if needed (this is a simplified approach)
    if (color !== '#000000') {
      ctx.globalCompositeOperation = 'source-over';
    }

    // Calculate scaled size
    const scaledWidth = size;
    const scaledHeight = size;

    // Draw the SVG image
    ctx.drawImage(
      svgImage,
      x - scaledWidth / 2,
      y - scaledHeight / 2,
      scaledWidth,
      scaledHeight
    );

    // Restore context
    ctx.restore();
  };

  const drawShape = (shape: Shape) => {
    const canvas = canvasRef.current;
    const context = canvas?.getContext('2d');
    if (!canvas || !context) return;

    switch (shape.type) {
      case 'kul':
      case 'lu':
        drawSVGShape(context, shape.x, shape.y, shape.size, shape.color, shape.type);
        break;
    }
  };

  const redrawCanvas = () => {
    const canvas = canvasRef.current;
    const context = canvas?.getContext('2d');
    if (!canvas || !context) return;

    context.clearRect(0, 0, canvas.width, canvas.height);

    if (backgroundImage) {
      context.drawImage(backgroundImage, 0, 0, canvas.width, canvas.height);
    }

    if (showGrid) {
      drawGrid(context, canvas.width, canvas.height);
    }

    const draggedShape = draggedShapeIndex !== null ? shapes[draggedShapeIndex] : null;

    shapes.forEach((shape, index) => {
      if (index !== draggedShapeIndex) {
        drawShape(shape);
      }
    });

    if (draggedShape) {
      drawShape(draggedShape);
    }
  };

  const isPointInShape = (px: number, py: number, shape: Shape) => {
    const size = shape.size;
    // Simple bounding box collision for all shapes for now
    return px >= shape.x - size / 2 && px <= shape.x + size / 2 &&
           py >= shape.y - size / 2 && py <= shape.y + size / 2;
  };

  const snapToGrid = (coord: number, gridSize: number) => {
    return Math.floor(coord / gridSize) * gridSize + gridSize / 2;
  };

  const startDrawing = (event: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    if (selectedShape === 'freehand') {
      setIsDrawing(true);
      setLastPosition({ x, y });
      return;
    }

    // Check if clicking on an existing shape to drag it
    let clickedShapeIndex = -1;
    for (let i = shapes.length - 1; i >= 0; i--) {
      if (isPointInShape(x, y, shapes[i])) {
        clickedShapeIndex = i;
        break;
      }
    }

    if (clickedShapeIndex !== -1) {
      setDraggedShapeIndex(clickedShapeIndex);
      setIsDrawing(true);
      setOriginalShapePosition({
        x: shapes[clickedShapeIndex].x,
        y: shapes[clickedShapeIndex].y
      });
      setDragOffset({
        x: x - shapes[clickedShapeIndex].x,
        y: y - shapes[clickedShapeIndex].y
      });
    } else {
      // If not clicking on a shape, add a new one
      const snappedX = snapToGrid(x, gridSize);
      const snappedY = snapToGrid(y, gridSize);

      const isOccupied = shapes.some(s => s.x === snappedX && s.y === snappedY);

      if (!isOccupied) {
        const newShape: Shape = {
          type: selectedShape,
          x: snappedX,
          y: snappedY,
          size: gridSize * 0.8,
          color: brushColor
        };
        setShapes(prev => [...prev, newShape]);
      }
    }
  };

  const draw = (event: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isDrawing) return;

    const canvas = canvasRef.current;
    const context = canvas?.getContext('2d');
    if (!canvas || !context) return;

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    if (draggedShapeIndex !== null) {
      const newShapes = [...shapes];
      newShapes[draggedShapeIndex] = {
        ...newShapes[draggedShapeIndex],
        x: x - dragOffset.x,
        y: y - dragOffset.y
      };
      setShapes(newShapes);
      redrawCanvas();
    } else if (selectedShape === 'freehand') {
      context.strokeStyle = brushColor;
      context.lineWidth = brushSize;
      context.beginPath();
      context.moveTo(lastPosition.x, lastPosition.y);
      context.lineTo(x, y);
      context.stroke();
      setLastPosition({ x, y });
    }
  };

  const stopDrawing = () => {
    if (draggedShapeIndex !== null && originalShapePosition) {
      const newShapes = [...shapes];
      const shape = newShapes[draggedShapeIndex];

      const snappedX = snapToGrid(shape.x, gridSize);
      const snappedY = snapToGrid(shape.y, gridSize);

      const isOccupied = shapes.some((s, index) => 
        index !== draggedShapeIndex && s.x === snappedX && s.y === snappedY
      );

      if (isOccupied) {
        // Revert to original position
        shape.x = originalShapePosition.x;
        shape.y = originalShapePosition.y;
      } else {
        // Snap to new position
        shape.x = snappedX;
        shape.y = snappedY;
      }
      
      setShapes(newShapes);
      redrawCanvas();
    }
    setIsDrawing(false);
    setDraggedShapeIndex(null);
    setOriginalShapePosition(null);
  };

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    const context = canvas?.getContext('2d');
    if (!canvas || !context) return;

    context.clearRect(0, 0, canvas.width, canvas.height);
    setShapes([]);
    setBackgroundImage(null);
    setShowGrid(true);
  };

  const undoLastShape = () => {
    if (shapes.length > 0) {
      setShapes(prev => prev.slice(0, -1));
    }
  };

  const evaluateKolam = async () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    setEvaluationStatus('loading');
    canvas.toBlob(async (blob) => {
      if (!blob) {
        setEvaluationStatus('error');
        return;
      }

      const formData = new FormData();
      formData.append('image', blob, 'kolam.png');

      try {
        const response = await fetch('http://localhost:8081/api/evaluate', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          setEvaluationStatus('success');
          console.log('Evaluation successful:', await response.json());
        } else {
          setEvaluationStatus('error');
          console.error('Evaluation failed:', response.statusText);
        }
      } catch (error) {
        setEvaluationStatus('error');
        console.error('Error during evaluation:', error);
      }
    });
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        if (e.target?.result) {
          const img = new Image();
          img.onload = () => {
            setBackgroundImage(img);
            setShowGrid(false); // Hide grid when background is set
          };
          img.src = e.target.result as string;
        }
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <>
      <Navbar />
      <div className="min-h-screen bg-gradient-to-b from-white via-purple-50 to-pink-50 flex flex-col items-center justify-center p-6">
        <div className="bg-white/80 backdrop-blur-lg p-8 rounded-3xl shadow-2xl border border-purple-100 max-w-6xl">
          <h1 className="text-3xl font-extrabold text-center text-purple-700 mb-6 tracking-tight">
            🎨 Draw & Evaluate Your Kolam
          </h1>
          
          <div className="mb-6 p-4 bg-gray-50 rounded-xl">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Shape Tools</label>
                <div className="grid grid-cols-3 gap-2">
                  {(['freehand', 'kul', 'lu'] as ShapeType[]).map((shape) => (
                    <button
                      key={shape}
                      onClick={() => setSelectedShape(shape)}
                      className={`p-2 text-xs rounded ${
                        selectedShape === shape
                          ? 'bg-purple-600 text-white'
                          : 'bg-white border border-gray-300 hover:bg-gray-50'
                      }`}
                      disabled={(shape === 'kul' && !svgImages.kul) || (shape === 'lu' && !svgImages.lu)}
                    >
                      {shape === 'freehand' ? '✏️' :
                       shape === 'kul' ? (svgImages.kul ? 'K' : '⏳') :
                       shape === 'lu' ? (svgImages.lu ? 'L' : '⏳') : '●'}
                    </button>
                  ))}
                </div>
                {Object.keys(svgImages).length < 2 && (
                  <p className="text-xs text-gray-500 mt-1">Loading SVG shapes...</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Line Width: {brushSize}px
                </label>
                <input
                  type="range"
                  min="1"
                  max="10"
                  value={brushSize}
                  onChange={(e) => setBrushSize(Number(e.target.value))}
                  className="w-full"
                />
                <p className="text-xs text-gray-500 mt-1">For freehand drawing only</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Color</label>
                <div className="flex gap-2">
                  <input
                    type="color"
                    value={brushColor}
                    onChange={(e) => setBrushColor(e.target.value)}
                    className="w-12 h-8 rounded border"
                  />
                  <div className="flex gap-1">
                    {['#000000', '#FF0000', '#00FF00', '#0000FF', '#FFD700'].map(color => (
                      <button
                        key={color}
                        onClick={() => setBrushColor(color)}
                        className="w-6 h-6 rounded border-2 border-gray-300"
                        style={{ backgroundColor: color }}
                      />
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="mb-4 flex gap-4 justify-center flex-wrap items-center">
            <button
              onClick={undoLastShape}
              className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg shadow transition-colors"
            >
              Undo Last
            </button>
            <input
              type="file"
              id="imageUpload"
              accept="image/*"
              onChange={handleImageUpload}
              className="hidden"
            />
            <label
              htmlFor="imageUpload"
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg shadow transition-colors cursor-pointer"
            >
              Upload Image
            </label>
            <button
              onClick={clearCanvas}
              className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg shadow transition-colors"
            >
              Clear Canvas
            </button>
            <button
              onClick={evaluateKolam}
              className="bg-gradient-to-r from-purple-600 to-pink-500 text-white px-6 py-2 rounded-lg shadow-lg hover:scale-105 transition-transform disabled:opacity-50"
              disabled={evaluationStatus === 'loading'}
            >
              {evaluationStatus === 'loading' ? 'Evaluating...' : 'Evaluate Kolam'}
            </button>
          </div>

          {evaluationStatus === 'success' && <p className="text-center text-green-600 mb-4">Evaluation successful!</p>}
          {evaluationStatus === 'error' && <p className="text-center text-red-600 mb-4">Evaluation failed. Please try again.</p>}

          <canvas
            ref={canvasRef}
            onMouseDown={startDrawing}
            onMouseMove={draw}
            onMouseUp={stopDrawing}
            onMouseLeave={stopDrawing}
            className="border-2 border-purple-200 rounded-lg shadow-md bg-white cursor-crosshair mx-auto block"
            style={{ width: "800px", height: "600px" }}
          />
          
          <p className="text-center text-gray-600 mt-4 text-sm">
            Selected: <span className="font-semibold">{selectedShape}</span> | 
            Line Width: <span className="font-semibold">{brushSize}px</span> | 
            Shapes drawn: <span className="font-semibold">{shapes.length}</span>
            {Object.keys(svgImages).length === 2 && <span className="text-green-600"> | SVGs Loaded ✓</span>}
          </p>
        </div>
      </div>
    </>
  );
}
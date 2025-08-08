import React, { useEffect } from "react";
import { Navigate, useParams } from "react-router-dom";
import {
  branchedCanvas,
  branchedToolCanvas,
  helloCanvas,
  weatherCanvas,
} from "../api/mockData";
import { CanvasView } from "../components/CanvasView";
import { useCanvasStore } from "../store/canvasStore";
import { CanvasData } from "../types";

const CANVAS_REGISTRY: Record<string, CanvasData> = {
  [helloCanvas.canvas_id]: helloCanvas,
  [weatherCanvas.canvas_id]: weatherCanvas,
  [branchedCanvas.canvas_id]: branchedCanvas,
  [branchedToolCanvas.canvas_id]: branchedToolCanvas,
};

export const CanvasPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { setCanvas, clear } = useCanvasStore();
  const canvas = useCanvasStore(s => s.canvas);
  const isLoading = useCanvasStore(s => s.isLoading);
  const error = useCanvasStore(s => s.error);

  useEffect(() => {
    if (id) {
      const data = CANVAS_REGISTRY[id];
      if (data) {
        setCanvas(data);
      } else {
        clear();
      }
    }
  }, [id, setCanvas, clear]);

  if (!id) {
    return <Navigate to="/" replace />;
  }

  if (isLoading) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-500">
        Loading canvas...
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex-1 flex items-center justify-center text-red-500">
        Error: {error}
      </div>
    );
  }

  if (!canvas || !CANVAS_REGISTRY[id]) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-500">
        Canvas not found
      </div>
    );
  }

  return <CanvasView data={canvas} />;
};

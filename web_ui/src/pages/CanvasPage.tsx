import React, { useEffect } from "react";
import { useParams } from "react-router-dom";
import { canvasExampleService } from "../api/canvasExampleService";
import canvasService from "../api/canvasService";
import { CanvasView } from "../components/CanvasView";
import { config } from "../config";
import { useCanvasStore } from "../store/canvasStore";

export const CanvasPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { setCanvas, clear } = useCanvasStore();
  const canvas = useCanvasStore(s => s.canvas);
  const isLoading = useCanvasStore(s => s.isLoading);
  const error = useCanvasStore(s => s.error);

  useEffect(() => {
    if (id) {
      // Use example service when in gh-page mode, otherwise use regular API service
      const fetchCanvas =
        config.build.mode === "gh-page"
          ? canvasExampleService.fetchExample(id)
          : canvasService.fetchCanvas(id);

      fetchCanvas
        .then(data => {
          if (data) {
            setCanvas(data);
          } else {
            console.error("Canvas not found");
            clear();
          }
        })
        .catch(err => {
          console.error("Failed to fetch canvas:", err);
          clear();
        });
    } else {
      clear();
    }
  }, [id, setCanvas, clear]);
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

  if (!canvas) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-500">
        Canvas not found
      </div>
    );
  }

  return (
    <CanvasView
      canvas={canvas}
      showControls={true}
      showMiniMap={true}
      showPanel={true}
    />
  );
};

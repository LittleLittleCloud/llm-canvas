import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { canvasService } from "../api/canvasService";
import { CanvasGallery } from "../components/CanvasGallery";
import { CanvasSummary } from "../types";

export const GalleryPage: React.FC = () => {
  const navigate = useNavigate();
  const [canvasSummaries, setCanvasSummaries] = useState<CanvasSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadCanvases = async () => {
      try {
        setLoading(true);
        const response = await canvasService.listCanvases();
        setCanvasSummaries(response.canvases);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load canvases"
        );
      } finally {
        setLoading(false);
      }
    };

    loadCanvases();
  }, []);

  const handleOpenCanvas = (id: string) => {
    navigate(`/canvas/${encodeURIComponent(id)}`);
  };

  if (loading) {
    return (
      <div className="p-8 text-center text-gray-500 text-sm">
        Loading canvases...
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 text-center text-red-500 text-sm">Error: {error}</div>
    );
  }

  return (
    <CanvasGallery
      canvasSummaries={canvasSummaries}
      onOpen={handleOpenCanvas}
    />
  );
};

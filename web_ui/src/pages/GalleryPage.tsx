import React from "react";
import { useNavigate } from "react-router-dom";
import {
  branchedCanvas,
  branchedToolCanvas,
  helloCanvas,
  weatherCanvas,
} from "../api/mockData";
import { CanvasGallery } from "../components/CanvasGallery";
import { CanvasData } from "../types";

const CANVAS_REGISTRY: Record<string, CanvasData> = {
  [helloCanvas.canvas_id]: helloCanvas,
  [weatherCanvas.canvas_id]: weatherCanvas,
  [branchedCanvas.canvas_id]: branchedCanvas,
  [branchedToolCanvas.canvas_id]: branchedToolCanvas,
};

export const GalleryPage: React.FC = () => {
  const navigate = useNavigate();

  const handleOpenCanvas = (id: string) => {
    navigate(`/canvas/${encodeURIComponent(id)}`);
  };

  return (
    <CanvasGallery
      canvases={Object.values(CANVAS_REGISTRY)}
      onOpen={handleOpenCanvas}
    />
  );
};

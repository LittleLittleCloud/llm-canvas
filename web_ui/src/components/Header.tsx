import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useCanvasStore } from "../store/canvasStore";

export const Header: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const canvas = useCanvasStore(s => s.canvas);

  const isCanvasPage = location.pathname.startsWith("/canvas/");

  return (
    <header className="p-4 bg-indigo-600 text-white font-semibold shadow flex items-center justify-between">
      <h1 className="cursor-pointer" onClick={() => navigate("/")}>
        LLM Canvas
      </h1>
      {isCanvasPage && canvas && (
        <div className="text-xs opacity-75 font-mono">{canvas.canvas_id}</div>
      )}
    </header>
  );
};

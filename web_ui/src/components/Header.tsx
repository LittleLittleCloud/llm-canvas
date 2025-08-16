import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useCanvasStore } from "../store/canvasStore";
import { LLMCanvasPrimaryLogo } from "./Logo";
import { ServerStatusIndicator } from "./ServerStatusIndicator";

export const Header: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const canvas = useCanvasStore(s => s.canvas);

  const isCanvasPage = location.pathname.startsWith("/canvas/");

  return (
    <header className="p-4 bg-indigo-600 text-white font-semibold shadow flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <div className="cursor-pointer" onClick={() => navigate("/")}>
          <LLMCanvasPrimaryLogo />
        </div>
        <ServerStatusIndicator />
      </div>
      <div className="flex items-center space-x-4">
        {isCanvasPage && canvas && (
          <div className="text-xs opacity-75 font-mono">{canvas.canvas_id}</div>
        )}
      </div>
    </header>
  );
};

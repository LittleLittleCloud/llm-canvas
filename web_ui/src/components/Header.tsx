import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useCanvasStore } from "../store/canvasStore";
import { LLMCanvasPrimaryLogo } from "./Logo";
import { ServerStatusIndicator } from "./ServerStatusIndicator";
import { ThemeToggle } from "./ThemeToggle";

export const Header: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const canvas = useCanvasStore(s => s.canvas);

  const isCanvasPage = location.pathname.startsWith("/canvas/");

  return (
    <header className="p-4 bg-indigo-600 dark:bg-gray-800 text-white font-semibold shadow flex items-center justify-between transition-colors duration-200">
      <div className="flex items-center space-x-3">
        <div className="cursor-pointer" onClick={() => navigate("/")}>
          <LLMCanvasPrimaryLogo />
        </div>
        <ServerStatusIndicator />
      </div>
      <div className="flex items-center space-x-4">
        <nav className="flex items-center space-x-4">
          <button
            onClick={() => navigate("/")}
            className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
              location.pathname === "/"
                ? "bg-white/20 text-white"
                : "text-white/80 hover:text-white hover:bg-white/10"
            }`}
          >
            Gallery
          </button>
          <button
            onClick={() => navigate("/docs")}
            className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
              location.pathname === "/docs"
                ? "bg-white/20 text-white"
                : "text-white/80 hover:text-white hover:bg-white/10"
            }`}
          >
            Documentation
          </button>
        </nav>
        <ThemeToggle />
        {isCanvasPage && canvas && (
          <div className="text-xs opacity-75 font-mono">{canvas.canvas_id}</div>
        )}
      </div>
    </header>
  );
};

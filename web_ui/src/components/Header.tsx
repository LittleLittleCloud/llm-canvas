import { Github } from "lucide-react";
import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import config from "../config";
import { LLMCanvasPrimaryLogo } from "./Logo";
import { ServerStatusIndicator } from "./ServerStatusIndicator";
import { ThemeToggle } from "./ThemeToggle";
import { Button } from "./ui/button";

export const Header: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const isGithubMode = config.build.mode === "gh-page";

  return (
    <header className="p-4 bg-indigo-600 dark:bg-gray-800 text-white font-semibold shadow flex items-center justify-between transition-colors duration-200">
      <div className="flex items-center space-x-3">
        <div className="cursor-pointer" onClick={() => navigate("/")}>
          <LLMCanvasPrimaryLogo />
        </div>
        {isGithubMode && (
          <Button
            onClick={() => navigate("/gallery")}
            variant="ghost"
            size="sm"
            className="text-white hover:text-white hover:bg-white/10"
          >
            Gallery
          </Button>
        )}
      </div>
      <div className="flex items-center space-x-2">
        {!isGithubMode && <ServerStatusIndicator />}
        <Button
          asChild
          variant="ghost"
          size="icon"
          className="text-white/80 hover:text-white hover:bg-white/10"
        >
          <a
            href="https://github.com/LittleLittleCloud/llm-canvas"
            target="_blank"
            rel="noopener noreferrer"
            title="View on GitHub"
          >
            <Github className="w-5 h-5" />
          </a>
        </Button>
        <ThemeToggle />
      </div>
    </header>
  );
};

import { Moon, Sun } from "lucide-react";
import React from "react";
import { useThemeStore } from "../store/themeStore";
import { Button } from "./ui/button";

export const ThemeToggle: React.FC = () => {
  const { actualTheme, setTheme } = useThemeStore();

  // Display icon based on actual theme (sun for light, moon for dark)
  const getDisplayIcon = () => {
    return actualTheme === "light" ? (
      <Sun className="w-4 h-4" />
    ) : (
      <Moon className="w-4 h-4" />
    );
  };

  const getDisplayLabel = () => {
    return actualTheme === "light" ? "Light" : "Dark";
  };

  const handleThemeChange = () => {
    if (actualTheme === "dark") {
      setTheme("light");
    } else {
      setTheme("dark");
    }
  };

  return (
    <Button
      onClick={handleThemeChange}
      variant="ghost"
      size="sm"
      className="flex items-center text-white/80 hover:text-white hover:bg-white/10 dark:text-gray-300 dark:hover:text-white transition-colors duration-200"
      title={`Current theme: ${getDisplayLabel()}. Click to cycle themes.`}
    >
      {getDisplayIcon()}
    </Button>
  );
};

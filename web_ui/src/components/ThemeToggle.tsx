import { Monitor, Moon, Sun } from "lucide-react";
import React from "react";
import { Theme, useThemeStore } from "../store/themeStore";
import { Button } from "./ui/button";

export const ThemeToggle: React.FC = () => {
  const { theme, setTheme } = useThemeStore();

  const themes: { value: Theme; icon: React.ReactNode; label: string }[] = [
    { value: "light", icon: <Sun className="w-4 h-4" />, label: "Light" },
    { value: "dark", icon: <Moon className="w-4 h-4" />, label: "Dark" },
    { value: "system", icon: <Monitor className="w-4 h-4" />, label: "System" },
  ];

  const currentTheme = themes.find(t => t.value === theme);

  const handleThemeChange = () => {
    const currentIndex = themes.findIndex(t => t.value === theme);
    const nextIndex = (currentIndex + 1) % themes.length;
    setTheme(themes[nextIndex].value);
  };

  return (
    <Button
      onClick={handleThemeChange}
      variant="ghost"
      size="sm"
      className="flex items-center space-x-2 text-white/80 hover:text-white hover:bg-white/10 dark:text-gray-300 dark:hover:text-white transition-colors duration-200"
      title={`Current theme: ${currentTheme?.label}. Click to cycle themes.`}
    >
      {currentTheme?.icon}
      <span className="hidden sm:inline">{currentTheme?.label}</span>
    </Button>
  );
};

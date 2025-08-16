import { useThemeStore } from "../store/themeStore";

export const useTheme = () => {
  const { theme, actualTheme, setTheme, toggleTheme } = useThemeStore();

  return {
    theme,
    actualTheme,
    setTheme,
    toggleTheme,
    isDark: actualTheme === "dark",
    isLight: actualTheme === "light",
  };
};

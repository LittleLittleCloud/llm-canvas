import { useMemo } from "react";

/**
 * Custom hook to detect if the build mode is GitHub Pages
 * @returns boolean - true if build mode is "gh-page", false otherwise
 */
export const useIsGithubPages = (): boolean => {
  const isGithubPages = useMemo(() => {
    return import.meta.env.VITE_BUILD_MODE === "gh-page";
  }, []);

  return isGithubPages;
};

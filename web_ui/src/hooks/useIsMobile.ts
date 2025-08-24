import { useEffect, useState } from "react";

/**
 * Custom hook to detect if the current screen size is mobile
 * @param breakpoint - The breakpoint in pixels to consider as mobile (default: 768px)
 * @returns boolean indicating if the current screen is mobile size
 */
export const useIsMobile = (breakpoint: number = 768): boolean | undefined => {
  const [isMobile, setIsMobile] = useState<boolean | undefined>(undefined);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth <= breakpoint);
    };

    // Initial check
    checkMobile();

    // Add resize event listener
    window.addEventListener("resize", checkMobile);

    // Cleanup event listener
    return () => window.removeEventListener("resize", checkMobile);
  }, [breakpoint]);

  return isMobile;
};

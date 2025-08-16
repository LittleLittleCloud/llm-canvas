import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";

export type Theme = "light" | "dark" | "system";

export interface ThemeState {
  theme: Theme;
  actualTheme: "light" | "dark";
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
}

const getSystemTheme = (): "light" | "dark" => {
  if (typeof window === "undefined") return "light";
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
};

const getActualTheme = (theme: Theme): "light" | "dark" => {
  if (theme === "system") {
    return getSystemTheme();
  }
  return theme;
};

const applyTheme = (actualTheme: "light" | "dark") => {
  if (typeof document === "undefined") return;

  const root = document.documentElement;
  root.classList.remove("light", "dark");
  root.classList.add(actualTheme);
};

export const useThemeStore = create<ThemeState>()(
  devtools(
    persist(
      (set, get) => {
        // Listen for system theme changes
        if (typeof window !== "undefined") {
          const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
          mediaQuery.addEventListener("change", () => {
            const { theme } = get();
            if (theme === "system") {
              const newActualTheme = getActualTheme(theme);
              set({ actualTheme: newActualTheme });
              applyTheme(newActualTheme);
            }
          });
        }

        return {
          theme: "system",
          actualTheme: getSystemTheme(),
          setTheme: (theme: Theme) => {
            const actualTheme = getActualTheme(theme);
            set({ theme, actualTheme });
            applyTheme(actualTheme);
          },
          toggleTheme: () => {
            const { theme } = get();
            let newTheme: Theme;

            if (theme === "light") {
              newTheme = "dark";
            } else if (theme === "dark") {
              newTheme = "light";
            } else {
              // If system, toggle to the opposite of current system theme
              const systemTheme = getSystemTheme();
              newTheme = systemTheme === "light" ? "dark" : "light";
            }

            const actualTheme = getActualTheme(newTheme);
            set({ theme: newTheme, actualTheme });
            applyTheme(actualTheme);
          },
        };
      },
      {
        name: "theme-store",
        onRehydrateStorage: () => state => {
          if (state) {
            // Apply theme on hydration
            applyTheme(state.actualTheme);
          }
        },
      }
    ),
    {
      name: "theme-store",
    }
  )
);

import react from "@vitejs/plugin-react";
import { copyFileSync, existsSync } from "fs";
import { resolve } from "path";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  console.log("Build mode:", env.VITE_BUILD_MODE);

  const isGithubPages = env.VITE_BUILD_MODE === "gh-page";

  return {
    base: isGithubPages ? "/llm-canvas/" : "/",
    plugins: [
      react(),
      // Custom plugin to handle GitHub Pages specific files
      isGithubPages && {
        name: "github-pages-spa",
        configResolved(config: import("vite").ResolvedConfig) {
          // Use the GitHub Pages specific HTML template
          config.build.rollupOptions.input = resolve(
            __dirname,
            "index.gh-pages.html"
          );
        },
        writeBundle() {
          // Copy 404.html to dist folder for GitHub Pages SPA support
          const distDir = resolve(__dirname, "dist");
          const srcFile = resolve(__dirname, "public", "404.html");
          const destFile = resolve(distDir, "404.html");

          if (existsSync(srcFile)) {
            copyFileSync(srcFile, destFile);
            console.log("Copied 404.html for GitHub Pages SPA support");
          }
        },
      },
    ].filter(Boolean),
    server: {
      port: 5173,
    },
  };
});

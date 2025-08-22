import react from "@vitejs/plugin-react";
import { copyFileSync, existsSync, writeFileSync } from "fs";
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
          const distDir = resolve(__dirname, "dist");

          // Copy index.gh-pages.html to index.html
          const ghPagesIndexSrc = resolve(distDir, "index.gh-pages.html");
          const indexDest = resolve(distDir, "index.html");

          if (existsSync(ghPagesIndexSrc)) {
            copyFileSync(ghPagesIndexSrc, indexDest);
            console.log(
              "Copied index.gh-pages.html to index.html for GitHub Pages"
            );
          }

          // Copy 404.html to dist folder for GitHub Pages SPA support
          const srcFile = resolve(__dirname, "public", "404.html");
          const destFile = resolve(distDir, "404.html");

          if (existsSync(srcFile)) {
            copyFileSync(srcFile, destFile);
            console.log("Copied 404.html for GitHub Pages SPA support");
          }

          // Generate sitemap.xml and robots.txt for GitHub Pages
          try {
            // Canonical site URL, can be overridden via env
            const siteUrl = (
              env.VITE_SITE_URL ||
              "https://littlelittlecloud.github.io/llm-canvas"
            ).replace(/\/$/, "");

            // Known public routes for the SPA when hosted on GH Pages
            const routes = ["/", "/gallery"]; // dynamic routes like /canvas/:id are omitted

            const now = new Date().toISOString();
            const urls = routes
              .map(
                r =>
                  `  <url>\n    <loc>${siteUrl}${r === "/" ? "/" : r}</loc>\n    <changefreq>weekly<\/changefreq>\n    <priority>${r === "/" ? "1.0" : "0.8"}<\/priority>\n    <lastmod>${now}<\/lastmod>\n  <\/url>`
              ) // keep pretty formatting
              .join("\n");

            const sitemap = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n<\/urlset>\n`;
            writeFileSync(resolve(distDir, "sitemap.xml"), sitemap, "utf-8");
            console.log("Generated sitemap.xml");

            const robots = `User-agent: *\nAllow: /\n\nSitemap: ${siteUrl}/sitemap.xml\n`;
            writeFileSync(resolve(distDir, "robots.txt"), robots, "utf-8");
            console.log("Generated robots.txt");
          } catch (err) {
            console.warn("Failed to generate sitemap/robots:", err);
          }
        },
      },
    ].filter(Boolean),
    server: {
      port: 5173,
    },
  };
});

import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  console.log("Build mode:", env.VITE_BUILD_MODE);
  return {
    base: env.VITE_BUILD_MODE === "gh-page" ? "/llm-canvas/" : "/",
    plugins: [react()],
    server: {
      port: 5173,
    },
  };
});

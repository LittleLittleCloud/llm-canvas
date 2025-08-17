// Configuration for different environments

// Check if we're in development mode
const isDevelopment = import.meta.env.VITE_DEV_MODE === "true";

type BuildMode = "gh-page" | "local"; // gh-page: github page, local: local server

const isGithubPage = import.meta.env.VITE_BUILD_MODE === "gh-page";

export const config: {
  api: {
    baseUrl: string;
  };
  sse: {
    endpoint: string;
  };
  dev: {
    enableDevTools: boolean;
    enableMockData: boolean;
  };
  build: {
    mode: BuildMode;
  };
} = {
  // API configuration
  api: {
    // Read from environment variable first, fallback to localhost in development
    baseUrl: import.meta.env.VITE_BASE_URL || "",
  },

  // WebSocket/SSE configuration
  sse: {
    endpoint: "/stream",
  },

  // Development flags
  dev: {
    enableDevTools: isDevelopment,
    enableMockData: false, // Set to true to use mock data instead of API
  },

  build: {
    mode: isGithubPage ? "gh-page" : "local",
  },
};

export default config;

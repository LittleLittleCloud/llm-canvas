// Configuration for different environments

// Check if we're in development mode
const isDevelopment = import.meta.env.VITE_DEV_MODE === "true";

export const config = {
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
};

export default config;

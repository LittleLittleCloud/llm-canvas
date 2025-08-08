// Configuration for different environments

// Check if we're in development mode
const isDevelopment = window.location.hostname === 'localhost' || window.location.port === '5173';

export const config = {
  // API configuration
  api: {
    // Default to port 8000 for FastAPI in development
    baseUrl: isDevelopment ? 'http://127.0.0.1:8000' : '',
  },
  
  // WebSocket/SSE configuration  
  sse: {
    endpoint: '/stream',
  },
  
  // Development flags
  dev: {
    enableDevTools: isDevelopment,
    enableMockData: false, // Set to true to use mock data instead of API
  },
};

export default config;

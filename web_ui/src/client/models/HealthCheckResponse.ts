/**
 * Response type for GET /api/v1/health
 */
export type HealthCheckResponse = {
  status: "healthy";
  server_type: "local" | "cloud";
  timestamp: number | null;
};

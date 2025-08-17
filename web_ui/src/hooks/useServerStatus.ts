import { useCallback, useEffect, useState } from "react";
import { canvasService } from "../api/canvasService";
import type { HealthCheckResponse } from "../client";

export type ServerStatus = "healthy" | "error" | "loading";

interface UseServerStatusReturn {
  status: ServerStatus;
  lastChecked: Date | null;
  serverType: "local" | "cloud" | null;
  error: string | null;
  checkStatus: () => Promise<void>;
}

export const useServerStatus = (
  intervalMs: number = 30000
): UseServerStatusReturn => {
  const [status, setStatus] = useState<ServerStatus>("loading");
  const [lastChecked, setLastChecked] = useState<Date | null>(null);
  const [serverType, setServerType] = useState<"local" | "cloud" | null>(null);
  const [error, setError] = useState<string | null>(null);

  const checkStatus = useCallback(async () => {
    try {
      setStatus("loading");
      setError(null);

      const response: HealthCheckResponse = await canvasService.healthCheck();

      if (response.status === "healthy") {
        setStatus("healthy");
        setServerType(response.server_type);
        setLastChecked(new Date());
      } else {
        setStatus("error");
        setError("Server returned non-healthy status");
      }
    } catch (err) {
      setStatus("error");
      setServerType(null);
      setError(
        err instanceof Error ? err.message : "Failed to check server status"
      );
    }
  }, []);

  useEffect(() => {
    // Check status immediately
    checkStatus();

    // Set up interval for periodic checks
    const interval = setInterval(checkStatus, intervalMs);

    return () => clearInterval(interval);
  }, [checkStatus, intervalMs]);

  return {
    status,
    lastChecked,
    serverType,
    error,
    checkStatus,
  };
};

import type { CanvasSummary } from "./CanvasSummary";

/**
 * SSE event data for canvas creation.
 */
export type SSECanvasCreatedEvent = {
  type: "canvas_created";
  timestamp: number;
  data: CanvasSummary;
};

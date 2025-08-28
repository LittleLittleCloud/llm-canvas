import type { CanvasSummary } from "./CanvasSummary";

/**
 * SSE event data for canvas updates.
 */
export type SSECanvasUpdatedEvent = {
  type: "canvas_updated";
  timestamp: number;
  data: CanvasSummary;
};

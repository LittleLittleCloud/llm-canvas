import type { SSECanvasDeletedEventData } from "./SSECanvasDeletedEventData";

/**
 * SSE event data for canvas deletion.
 */
export type SSECanvasDeletedEvent = {
  type: "canvas_deleted";
  timestamp: number;
  data: SSECanvasDeletedEventData;
};

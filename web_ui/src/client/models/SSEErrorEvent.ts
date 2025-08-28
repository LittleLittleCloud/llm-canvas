import type { SSEErrorEventData } from "./SSEErrorEventData";

/**
 * SSE error event for stream errors.
 */
export type SSEErrorEvent = {
  type: "error";
  timestamp: number;
  data: SSEErrorEventData;
};

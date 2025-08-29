import type { SSEMessageDeletedEventData } from "./SSEMessageDeletedEventData";

/**
 * SSE event data for message deletion.
 */
export type SSEMessageDeletedEvent = {
  type: "message_deleted";
  timestamp: number;
  canvas_id: string;
  data: SSEMessageDeletedEventData;
};

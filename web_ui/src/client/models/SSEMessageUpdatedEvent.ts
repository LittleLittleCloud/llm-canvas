import type { MessageNode } from "./MessageNode";

/**
 * SSE event data for message updates.
 */
export type SSEMessageUpdatedEvent = {
  type: "message_updated";
  timestamp: number;
  canvas_id: string;
  data: MessageNode;
};

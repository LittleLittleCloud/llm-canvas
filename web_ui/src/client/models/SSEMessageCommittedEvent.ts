import type { MessageNode } from "./MessageNode";

/**
 * SSE event data for message commits.
 */
export type SSEMessageCommittedEvent = {
  type: "message_committed";
  timestamp: number;
  canvas_id: string;
  data: MessageNode;
};

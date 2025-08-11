import type { MessageNode } from "./MessageNode";

/**
 * Event data for canvas message updates.
 */
export type CanvasUpdateMessageEvent = {
  event_type: "update_message";
  canvas_id: string;
  timestamp: number;
  data: MessageNode;
};

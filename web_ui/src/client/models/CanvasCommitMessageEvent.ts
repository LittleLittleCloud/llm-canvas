import type { MessageNode } from "./MessageNode";

/**
 * Event data for canvas message commits.
 */
export type CanvasCommitMessageEvent = {
  event_type: "commit_message";
  canvas_id: string;
  timestamp: number;
  data: MessageNode;
};

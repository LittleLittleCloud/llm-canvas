import type { Message } from "./Message";

/**
 * Node in the canvas conversation graph.
 */
export type MessageNode = {
  id: string;
  message: Message;
  parent_id: string | null;
  child_ids: Array<string>;
  meta: Record<string, unknown> | null;
};

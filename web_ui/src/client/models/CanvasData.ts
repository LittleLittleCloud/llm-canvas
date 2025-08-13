import type { MessageNode } from "./MessageNode";

/**
 * Complete canvas data structure.
 */
export type CanvasData = {
  title: string | null;
  last_updated: number | null;
  description: string | null;
  canvas_id: string;
  created_at: number;
  nodes: Record<string, MessageNode>;
};

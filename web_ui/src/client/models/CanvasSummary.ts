/**
 * Summary information about a canvas.
 */
export type CanvasSummary = {
  canvas_id: string;
  created_at: number;
  root_ids: Array<string>;
  node_count: number;
  title: string | null;
  description: string | null;
  meta: Record<string, unknown>;
};

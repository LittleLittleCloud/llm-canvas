import type { CanvasSummary } from "./CanvasSummary";

/**
 * Response type for GET /api/v1/canvas/list
 */
export type CanvasListResponse = {
  canvases: Array<CanvasSummary>;
};

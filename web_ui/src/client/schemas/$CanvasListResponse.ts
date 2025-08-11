export const $CanvasListResponse = {
  description: `Response type for GET /api/v1/canvas/list`,
  properties: {
    canvases: {
      type: "array",
      contains: {
        type: "CanvasSummary",
      },
      isRequired: true,
    },
  },
} as const;

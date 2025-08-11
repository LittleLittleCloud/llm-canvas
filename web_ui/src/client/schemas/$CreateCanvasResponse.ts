export const $CreateCanvasResponse = {
  description: `Response type for POST /api/v1/canvas`,
  properties: {
    canvas_id: {
      type: "string",
      isRequired: true,
    },
    message: {
      type: "string",
      isRequired: true,
    },
  },
} as const;

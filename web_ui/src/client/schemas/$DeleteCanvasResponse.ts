export const $DeleteCanvasResponse = {
  description: `Response type for DELETE /api/v1/canvas/{canvas_id}`,
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

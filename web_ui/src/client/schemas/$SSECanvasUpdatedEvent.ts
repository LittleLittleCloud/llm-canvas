export const $SSECanvasUpdatedEvent = {
  description: `SSE event data for canvas updates.`,
  properties: {
    type: {
      type: '"canvas_updated"',
      isRequired: true,
    },
    timestamp: {
      type: "number",
      isRequired: true,
    },
    data: {
      type: "CanvasSummary",
      isRequired: true,
    },
  },
} as const;

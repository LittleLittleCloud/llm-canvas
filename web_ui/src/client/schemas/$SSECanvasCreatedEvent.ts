export const $SSECanvasCreatedEvent = {
  description: `SSE event data for canvas creation.`,
  properties: {
    type: {
      type: '"canvas_created"',
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

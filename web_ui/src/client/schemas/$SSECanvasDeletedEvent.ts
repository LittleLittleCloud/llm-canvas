export const $SSECanvasDeletedEvent = {
  description: `SSE event data for canvas deletion.`,
  properties: {
    type: {
      type: '"canvas_deleted"',
      isRequired: true,
    },
    timestamp: {
      type: "number",
      isRequired: true,
    },
    data: {
      type: "SSECanvasDeletedEventData",
      isRequired: true,
    },
  },
} as const;

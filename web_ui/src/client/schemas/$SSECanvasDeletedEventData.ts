export const $SSECanvasDeletedEventData = {
  description: `Data payload for canvas deleted events.`,
  properties: {
    canvas_id: {
      type: "string",
      isRequired: true,
    },
  },
} as const;

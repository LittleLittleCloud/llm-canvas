export const $CanvasUpdateMessageEvent = {
  description: `Event data for canvas message updates.`,
  properties: {
    event_type: {
      type: '"update_message"',
      isRequired: true,
    },
    canvas_id: {
      type: "string",
      isRequired: true,
    },
    timestamp: {
      type: "number",
      isRequired: true,
    },
    data: {
      type: "MessageNode",
      isRequired: true,
    },
  },
} as const;

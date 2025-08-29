export const $SSEMessageUpdatedEvent = {
  description: `SSE event data for message updates.`,
  properties: {
    type: {
      type: '"message_updated"',
      isRequired: true,
    },
    timestamp: {
      type: "number",
      isRequired: true,
    },
    canvas_id: {
      type: "string",
      isRequired: true,
    },
    data: {
      type: "MessageNode",
      isRequired: true,
    },
  },
} as const;

export const $SSEMessageDeletedEvent = {
  description: `SSE event data for message deletion.`,
  properties: {
    type: {
      type: '"message_deleted"',
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
      type: "SSEMessageDeletedEventData",
      isRequired: true,
    },
  },
} as const;

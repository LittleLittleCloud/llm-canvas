export const $SSEMessageCommittedEvent = {
  description: `SSE event data for message commits.`,
  properties: {
    type: {
      type: '"message_committed"',
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

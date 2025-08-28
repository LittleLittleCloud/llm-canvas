export const $SSEErrorEvent = {
  description: `SSE error event for stream errors.`,
  properties: {
    type: {
      type: '"error"',
      isRequired: true,
    },
    timestamp: {
      type: "number",
      isRequired: true,
    },
    data: {
      type: "SSEErrorEventData",
      isRequired: true,
    },
  },
} as const;

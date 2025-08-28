export const $SSEErrorEventData = {
  description: `Data payload for error events.`,
  properties: {
    error: {
      type: "string",
      isRequired: true,
    },
  },
} as const;

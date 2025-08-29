export const $SSEMessageDeletedEventData = {
  description: `Data payload for message deleted events.`,
  properties: {
    message_id: {
      type: "string",
      isRequired: true,
    },
  },
} as const;

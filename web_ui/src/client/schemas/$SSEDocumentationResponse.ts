export const $SSEDocumentationResponse = {
  description: `Response type for GET /api/v1/sse/documentation`,
  properties: {
    events: {
      type: "array",
      contains: {
        type: "any-of",
        contains: [
          {
            type: "SSECanvasCreatedEvent",
          },
          {
            type: "SSECanvasUpdatedEvent",
          },
          {
            type: "SSECanvasDeletedEvent",
          },
          {
            type: "SSEHeartbeatEvent",
          },
          {
            type: "SSEErrorEvent",
          },
          {
            type: "SSEMessageCommittedEvent",
          },
          {
            type: "SSEMessageUpdatedEvent",
          },
          {
            type: "SSEMessageDeletedEvent",
          },
        ],
      },
      isRequired: true,
    },
  },
} as const;

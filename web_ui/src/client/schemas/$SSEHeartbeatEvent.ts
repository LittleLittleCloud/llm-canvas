export const $SSEHeartbeatEvent = {
  description: `SSE heartbeat event to keep connections alive.`,
  properties: {
    type: {
      type: '"heartbeat"',
      isRequired: true,
    },
    timestamp: {
      type: "number",
      isRequired: true,
    },
  },
} as const;

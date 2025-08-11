export const $HealthCheckResponse = {
  description: `Response type for GET /api/v1/health`,
  properties: {
    status: {
      type: '"healthy"',
      isRequired: true,
    },
    server_type: {
      type: "Enum",
      isRequired: true,
    },
    timestamp: {
      type: "any-of",
      contains: [
        {
          type: "number",
        },
        {
          type: "null",
        },
      ],
      isRequired: true,
    },
  },
} as const;

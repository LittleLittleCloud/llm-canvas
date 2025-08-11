export const $ToolUseBlockParam = {
  properties: {
    id: {
      type: "string",
      isRequired: true,
    },
    input: {
      properties: {},
      isRequired: true,
    },
    name: {
      type: "string",
      isRequired: true,
    },
    type: {
      type: '"tool_use"',
      isRequired: true,
    },
    cache_control: {
      type: "any-of",
      contains: [
        {
          type: "CacheControlEphemeralParam",
        },
        {
          type: "null",
        },
      ],
    },
  },
} as const;

export const $ToolResultBlockParam = {
  properties: {
    tool_use_id: {
      type: "string",
      isRequired: true,
    },
    type: {
      type: '"tool_result"',
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
    content: {
      type: "any-of",
      contains: [
        {
          type: "string",
        },
        {
          type: "array",
          contains: {
            type: "any-of",
            contains: [
              {
                type: "TextBlockParam",
              },
              {
                type: "ImageBlockParam",
              },
              {
                type: "SearchResultBlockParam",
              },
            ],
          },
        },
      ],
    },
    is_error: {
      type: "boolean",
    },
  },
} as const;

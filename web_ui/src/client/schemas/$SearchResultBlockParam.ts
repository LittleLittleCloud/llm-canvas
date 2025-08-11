export const $SearchResultBlockParam = {
  properties: {
    content: {
      type: "array",
      contains: {
        type: "TextBlockParam",
      },
      isRequired: true,
    },
    source: {
      type: "string",
      isRequired: true,
    },
    title: {
      type: "string",
      isRequired: true,
    },
    type: {
      type: '"search_result"',
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
    citations: {
      type: "CitationsConfigParam",
    },
  },
} as const;

export const $ImageBlockParam = {
  properties: {
    source: {
      type: "any-of",
      contains: [
        {
          type: "Base64ImageSourceParam",
        },
        {
          type: "URLImageSourceParam",
        },
      ],
      isRequired: true,
    },
    type: {
      type: '"image"',
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

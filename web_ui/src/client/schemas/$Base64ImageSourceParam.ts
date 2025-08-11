export const $Base64ImageSourceParam = {
  properties: {
    data: {
      type: "any-of",
      contains: [
        {
          type: "string",
        },
        {
          type: "string",
          format: "path",
        },
      ],
      isRequired: true,
    },
    media_type: {
      type: "Enum",
      isRequired: true,
    },
    type: {
      type: '"base64"',
      isRequired: true,
    },
  },
} as const;

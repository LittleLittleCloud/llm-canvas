export const $URLImageSourceParam = {
  properties: {
    type: {
      type: '"url"',
      isRequired: true,
    },
    url: {
      type: "string",
      isRequired: true,
    },
  },
} as const;

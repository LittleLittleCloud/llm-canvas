export const $Message = {
  description: `Message structure for canvas conversations.`,
  properties: {
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
                type: "ToolUseBlockParam",
              },
              {
                type: "ToolResultBlockParam",
              },
              {
                type: "ImageBlockParam",
              },
            ],
          },
        },
      ],
      isRequired: true,
    },
    role: {
      type: "Enum",
      isRequired: true,
    },
  },
} as const;

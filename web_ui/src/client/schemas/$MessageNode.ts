export const $MessageNode = {
  description: `Node in the canvas conversation graph.`,
  properties: {
    id: {
      type: "string",
      isRequired: true,
    },
    message: {
      type: "Message",
      isRequired: true,
    },
    parent_id: {
      type: "any-of",
      contains: [
        {
          type: "string",
        },
        {
          type: "null",
        },
      ],
      isRequired: true,
    },
    child_ids: {
      type: "array",
      contains: {
        type: "string",
      },
      isRequired: true,
    },
    meta: {
      type: "any-of",
      contains: [
        {
          type: "dictionary",
          contains: {
            properties: {},
          },
        },
        {
          type: "null",
        },
      ],
      isRequired: true,
    },
  },
} as const;

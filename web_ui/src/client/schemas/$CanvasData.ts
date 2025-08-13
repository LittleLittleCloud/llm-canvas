export const $CanvasData = {
  description: `Complete canvas data structure.`,
  properties: {
    title: {
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
    last_updated: {
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
    description: {
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
    canvas_id: {
      type: "string",
      isRequired: true,
    },
    created_at: {
      type: "number",
      isRequired: true,
    },
    nodes: {
      type: "dictionary",
      contains: {
        type: "MessageNode",
      },
      isRequired: true,
    },
  },
} as const;

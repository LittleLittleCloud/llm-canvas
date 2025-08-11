export const $CanvasSummary = {
  description: `Summary information about a canvas.`,
  properties: {
    canvas_id: {
      type: "string",
      isRequired: true,
    },
    created_at: {
      type: "number",
      isRequired: true,
    },
    root_ids: {
      type: "array",
      contains: {
        type: "string",
      },
      isRequired: true,
    },
    node_count: {
      type: "number",
      isRequired: true,
    },
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
    meta: {
      type: "dictionary",
      contains: {
        properties: {},
      },
      isRequired: true,
    },
  },
} as const;

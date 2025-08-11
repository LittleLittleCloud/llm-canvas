export const $CitationContentBlockLocationParam = {
  properties: {
    cited_text: {
      type: "string",
      isRequired: true,
    },
    document_index: {
      type: "number",
      isRequired: true,
    },
    document_title: {
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
    end_block_index: {
      type: "number",
      isRequired: true,
    },
    start_block_index: {
      type: "number",
      isRequired: true,
    },
    type: {
      type: '"content_block_location"',
      isRequired: true,
    },
  },
} as const;

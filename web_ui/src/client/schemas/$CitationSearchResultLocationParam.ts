export const $CitationSearchResultLocationParam = {
  properties: {
    cited_text: {
      type: "string",
      isRequired: true,
    },
    end_block_index: {
      type: "number",
      isRequired: true,
    },
    search_result_index: {
      type: "number",
      isRequired: true,
    },
    source: {
      type: "string",
      isRequired: true,
    },
    start_block_index: {
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
    type: {
      type: '"search_result_location"',
      isRequired: true,
    },
  },
} as const;

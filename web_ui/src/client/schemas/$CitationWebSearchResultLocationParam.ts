export const $CitationWebSearchResultLocationParam = {
  properties: {
    cited_text: {
      type: "string",
      isRequired: true,
    },
    encrypted_index: {
      type: "string",
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
      type: '"web_search_result_location"',
      isRequired: true,
    },
    url: {
      type: "string",
      isRequired: true,
    },
  },
} as const;

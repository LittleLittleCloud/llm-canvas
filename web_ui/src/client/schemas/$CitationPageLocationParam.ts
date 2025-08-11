export const $CitationPageLocationParam = {
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
    end_page_number: {
      type: "number",
      isRequired: true,
    },
    start_page_number: {
      type: "number",
      isRequired: true,
    },
    type: {
      type: '"page_location"',
      isRequired: true,
    },
  },
} as const;

export const $CitationCharLocationParam = {
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
    end_char_index: {
      type: "number",
      isRequired: true,
    },
    start_char_index: {
      type: "number",
      isRequired: true,
    },
    type: {
      type: '"char_location"',
      isRequired: true,
    },
  },
} as const;

export const $TextBlockParam = {
  properties: {
    text: {
      type: "string",
      isRequired: true,
    },
    type: {
      type: '"text"',
      isRequired: true,
    },
    cache_control: {
      type: "any-of",
      contains: [
        {
          type: "CacheControlEphemeralParam",
        },
        {
          type: "null",
        },
      ],
    },
    citations: {
      type: "any-of",
      contains: [
        {
          type: "array",
          contains: {
            type: "any-of",
            contains: [
              {
                type: "CitationCharLocationParam",
              },
              {
                type: "CitationPageLocationParam",
              },
              {
                type: "CitationContentBlockLocationParam",
              },
              {
                type: "CitationWebSearchResultLocationParam",
              },
              {
                type: "CitationSearchResultLocationParam",
              },
            ],
          },
        },
        {
          type: "null",
        },
      ],
    },
  },
} as const;

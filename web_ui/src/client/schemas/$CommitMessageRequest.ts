export const $CommitMessageRequest = {
  properties: {
    data: {
      type: "CanvasCommitMessageEvent",
      isRequired: true,
    },
  },
} as const;

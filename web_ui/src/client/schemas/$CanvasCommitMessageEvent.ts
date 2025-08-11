export const $CanvasCommitMessageEvent = {
  description: `Event data for canvas message commits.`,
  properties: {
    event_type: {
      type: '"commit_message"',
      isRequired: true,
    },
    canvas_id: {
      type: "string",
      isRequired: true,
    },
    timestamp: {
      type: "number",
      isRequired: true,
    },
    data: {
      type: "MessageNode",
      isRequired: true,
    },
  },
} as const;

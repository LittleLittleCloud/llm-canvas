export const $CreateMessageResponse = {
  description: `Response type for POST /api/v1/canvas/{canvas_id}/messages`,
  properties: {
    message_id: {
      type: "string",
      isRequired: true,
    },
    canvas_id: {
      type: "string",
      isRequired: true,
    },
    message: {
      type: "string",
      isRequired: true,
    },
  },
} as const;

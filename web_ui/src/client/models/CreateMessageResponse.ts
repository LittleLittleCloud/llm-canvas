/**
 * Response type for POST /api/v1/canvas/{canvas_id}/messages
 */
export type CreateMessageResponse = {
  message_id: string;
  canvas_id: string;
  message: string;
};

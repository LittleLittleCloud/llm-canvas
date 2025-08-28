/**
 * SSE heartbeat event to keep connections alive.
 */
export type SSEHeartbeatEvent = {
  type: "heartbeat";
  timestamp: number;
};

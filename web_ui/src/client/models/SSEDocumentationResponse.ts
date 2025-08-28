import type { SSECanvasCreatedEvent } from "./SSECanvasCreatedEvent";
import type { SSECanvasDeletedEvent } from "./SSECanvasDeletedEvent";
import type { SSECanvasUpdatedEvent } from "./SSECanvasUpdatedEvent";
import type { SSEErrorEvent } from "./SSEErrorEvent";
import type { SSEHeartbeatEvent } from "./SSEHeartbeatEvent";
import type { SSEMessageCommittedEvent } from "./SSEMessageCommittedEvent";
import type { SSEMessageDeletedEvent } from "./SSEMessageDeletedEvent";
import type { SSEMessageUpdatedEvent } from "./SSEMessageUpdatedEvent";

/**
 * Response type for GET /api/v1/sse/documentation
 */
export type SSEDocumentationResponse = {
  events: Array<
    | SSECanvasCreatedEvent
    | SSECanvasUpdatedEvent
    | SSECanvasDeletedEvent
    | SSEHeartbeatEvent
    | SSEErrorEvent
    | SSEMessageCommittedEvent
    | SSEMessageUpdatedEvent
    | SSEMessageDeletedEvent
  >;
};

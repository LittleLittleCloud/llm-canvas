import type { CanvasListResponse } from "../models/CanvasListResponse";
import type { CommitMessageRequest } from "../models/CommitMessageRequest";
import type { CreateCanvasRequest } from "../models/CreateCanvasRequest";
import type { CreateCanvasResponse } from "../models/CreateCanvasResponse";
import type { CreateMessageResponse } from "../models/CreateMessageResponse";
import type { DeleteCanvasResponse } from "../models/DeleteCanvasResponse";
import type { GetCanvasResponse } from "../models/GetCanvasResponse";
import type { HealthCheckResponse } from "../models/HealthCheckResponse";
import type { SSEDocumentationResponse } from "../models/SSEDocumentationResponse";
import type { UpdateMessageRequest } from "../models/UpdateMessageRequest";
import type { CancelablePromise } from "../core/CancelablePromise";
import { OpenAPI } from "../core/OpenAPI";
import { request as __request } from "../core/request";

export type TDataGetCanvasApiV1CanvasGet = {
  /**
   * Canvas UUID
   */
  canvasId: string;
};
export type TDataCreateCanvasApiV1CanvasPost = {
  requestBody: CreateCanvasRequest;
};
export type TDataDeleteCanvasApiV1CanvasCanvasIdDelete = {
  /**
   * Canvas UUID to delete
   */
  canvasId: string;
};
export type TDataCommitMessageApiV1CanvasCanvasIdMessagesPost = {
  /**
   * Canvas UUID
   */
  canvasId: string;
  requestBody: CommitMessageRequest;
};
export type TDataUpdateMessageApiV1CanvasCanvasIdMessagesMessageIdPut = {
  /**
   * Canvas UUID
   */
  canvasId: string;
  /**
   * Message ID to update
   */
  messageId: string;
  requestBody: UpdateMessageRequest;
};
export type TDataCanvasMessageSseApiV1CanvasCanvasIdSseGet = {
  /**
   * Canvas UUID
   */
  canvasId: string;
};

export class V1Service {
  /**
   * Health Check
   * Health check endpoint to verify server is running.
   * @returns HealthCheckResponse Successful Response
   * @throws ApiError
   */
  public static healthCheckApiV1HealthGet(): CancelablePromise<HealthCheckResponse> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/health",
    });
  }

  /**
   * Sse Documentation
   * SSE documentation endpoint that describes available event types.
   *
   * You should never call this, this endpoint is to make openapi generator happy
   * @returns SSEDocumentationResponse Successful Response
   * @throws ApiError
   */
  public static sseDocumentationApiV1SseDocumentationGet(): CancelablePromise<SSEDocumentationResponse> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/sse/documentation",
    });
  }

  /**
   * List Canvases
   * List all available canvases.
   * Returns:
   * CanvasListResponse with list of canvas summaries
   * @returns CanvasListResponse Successful Response
   * @throws ApiError
   */
  public static listCanvasesApiV1CanvasListGet(): CancelablePromise<CanvasListResponse> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/canvas/list",
    });
  }

  /**
   * Get Canvas
   * Get a full canvas by ID.
   * Args:
   * canvas_id: Canvas UUID to retrieve
   * Returns:
   * CanvasData on success
   * Raises:
   * HTTPException: 404 if canvas not found
   * @returns GetCanvasResponse Successful Response
   * @throws ApiError
   */
  public static getCanvasApiV1CanvasGet(
    data: TDataGetCanvasApiV1CanvasGet
  ): CancelablePromise<GetCanvasResponse> {
    const { canvasId } = data;
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/canvas",
      query: {
        canvas_id: canvasId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Create Canvas
   * Create a new canvas.
   * Args:
   * request: Canvas creation request with optional title and description
   * Returns:
   * CreateCanvasResponse with the canvas ID and success message
   * @returns CreateCanvasResponse Successful Response
   * @throws ApiError
   */
  public static createCanvasApiV1CanvasPost(
    data: TDataCreateCanvasApiV1CanvasPost
  ): CancelablePromise<CreateCanvasResponse> {
    const { requestBody } = data;
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/canvas",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Delete Canvas
   * Delete a canvas by ID.
   * Args:
   * canvas_id: Canvas UUID to delete
   * Returns:
   * DeleteCanvasResponse with success message
   * Raises:
   * HTTPException: 404 if canvas not found
   * @returns DeleteCanvasResponse Successful Response
   * @throws ApiError
   */
  public static deleteCanvasApiV1CanvasCanvasIdDelete(
    data: TDataDeleteCanvasApiV1CanvasCanvasIdDelete
  ): CancelablePromise<DeleteCanvasResponse> {
    const { canvasId } = data;
    return __request(OpenAPI, {
      method: "DELETE",
      url: "/api/v1/canvas/{canvas_id}",
      path: {
        canvas_id: canvasId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Commit Message
   * Commit a new message to a canvas.
   * Args:
   * canvas_id: Canvas UUID to add message to
   * request: Canvas commit message event data
   * Returns:
   * CreateMessageResponse with the message ID and success message
   * Raises:
   * HTTPException: 404 if canvas not found
   * @returns CreateMessageResponse Successful Response
   * @throws ApiError
   */
  public static commitMessageApiV1CanvasCanvasIdMessagesPost(
    data: TDataCommitMessageApiV1CanvasCanvasIdMessagesPost
  ): CancelablePromise<CreateMessageResponse> {
    const { canvasId, requestBody } = data;
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/canvas/{canvas_id}/messages",
      path: {
        canvas_id: canvasId,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Update Message
   * Update an existing message in a canvas.
   * Args:
   * canvas_id: Canvas UUID containing the message
   * message_id: Message ID to update
   * request: Canvas update message event data
   * Returns:
   * CreateMessageResponse with the message ID and success message
   * Raises:
   * HTTPException: 404 if canvas or message not found
   * @returns CreateMessageResponse Successful Response
   * @throws ApiError
   */
  public static updateMessageApiV1CanvasCanvasIdMessagesMessageIdPut(
    data: TDataUpdateMessageApiV1CanvasCanvasIdMessagesMessageIdPut
  ): CancelablePromise<CreateMessageResponse> {
    const { canvasId, messageId, requestBody } = data;
    return __request(OpenAPI, {
      method: "PUT",
      url: "/api/v1/canvas/{canvas_id}/messages/{message_id}",
      path: {
        canvas_id: canvasId,
        message_id: messageId,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }

  /**
   * Canvas Sse
   * Server-Sent Events endpoint for global canvas updates.
   *
   * Sends events when canvases are created, updated, or deleted.
   * Events include:
   * - canvas_created: When a new canvas is created
   * - canvas_updated: When a canvas is updated
   * - canvas_deleted: When a canvas is deleted
   *
   * Returns:
   * StreamingResponse with SSE events
   * @returns unknown Successful Response
   * @throws ApiError
   */
  public static canvasSseApiV1CanvasSseGet(): CancelablePromise<unknown> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/canvas/sse",
    });
  }

  /**
   * Canvas Message Sse
   * Server-Sent Events endpoint for canvas message updates.
   *
   * Sends events when messages are added, updated, or deleted in a specific canvas.
   * Events include:
   * - message_committed: When a new message is added to the canvas
   * - message_updated: When an existing message is updated
   * - message_deleted: When a message is deleted
   *
   * Args:
   * canvas_id: Canvas UUID to stream events for
   * Returns:
   * StreamingResponse with SSE events
   * Raises:
   * HTTPException: 404 if canvas not found
   * @returns unknown Successful Response
   * @throws ApiError
   */
  public static canvasMessageSseApiV1CanvasCanvasIdSseGet(
    data: TDataCanvasMessageSseApiV1CanvasCanvasIdSseGet
  ): CancelablePromise<unknown> {
    const { canvasId } = data;
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/canvas/{canvas_id}/sse",
      path: {
        canvas_id: canvasId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
}

import {
  OpenAPI,
  V1Service,
  type CanvasData,
  type CanvasListResponse,
  type CommitMessageRequest,
  type CreateCanvasRequest,
  type CreateCanvasResponse,
  type CreateMessageResponse,
  type DeleteCanvasResponse,
  type UpdateMessageRequest,
} from "../client";
import { config } from "../config";

class CanvasService {
  constructor() {
    // Configure the OpenAPI client with the base URL
    this.configureClient();
  }

  private configureClient(): void {
    OpenAPI.BASE = config.api.baseUrl;
    OpenAPI.HEADERS = {
      "Content-Type": "application/json",
    };
  }

  async fetchCanvas(canvasId?: string): Promise<CanvasData> {
    if (!canvasId) {
      throw new Error("Canvas ID is required");
    }

    const response = await V1Service.getCanvasApiV1CanvasGet({
      canvasId,
    });
    return response.data;
  }

  async listCanvases(): Promise<CanvasListResponse> {
    return V1Service.listCanvasesApiV1CanvasListGet();
  }

  async createCanvas(
    request: CreateCanvasRequest
  ): Promise<CreateCanvasResponse> {
    return V1Service.createCanvasApiV1CanvasPost({
      requestBody: request,
    });
  }

  async deleteCanvas(canvasId: string): Promise<DeleteCanvasResponse> {
    return V1Service.deleteCanvasApiV1CanvasCanvasIdDelete({
      canvasId,
    });
  }

  async commitMessage(
    canvasId: string,
    request: CommitMessageRequest
  ): Promise<CreateMessageResponse> {
    return V1Service.commitMessageApiV1CanvasCanvasIdMessagesPost({
      canvasId,
      requestBody: request,
    });
  }

  async updateMessage(
    canvasId: string,
    messageId: string,
    request: UpdateMessageRequest
  ): Promise<CreateMessageResponse> {
    return V1Service.updateMessageApiV1CanvasCanvasIdMessagesMessageIdPut({
      canvasId,
      messageId,
      requestBody: request,
    });
  }

  async healthCheck() {
    return V1Service.healthCheckApiV1HealthGet();
  }
}

// Export a singleton instance
export const canvasService = new CanvasService();
export default canvasService;

import { config } from "../config";
import { CanvasData, CanvasListResponse } from "../types";

class CanvasService {
  private getApiBaseUrl(): string {
    return config.api.baseUrl;
  }

  private async apiCall(
    endpoint: string,
    options?: RequestInit
  ): Promise<Response> {
    const baseUrl = this.getApiBaseUrl();
    const url = `${baseUrl}${endpoint}`;

    const response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });

    if (!response.ok) {
      throw new Error(
        `API call failed: ${response.status} ${response.statusText}`
      );
    }

    return response;
  }

  async fetchCanvas(canvasId?: string): Promise<CanvasData> {
    if (!canvasId) {
      throw new Error("Canvas ID is required");
    }
    const endpoint = `/api/v1/canvas?id=${canvasId}`;
    const response = await this.apiCall(endpoint);
    return response.json();
  }

  async listCanvases(): Promise<CanvasListResponse> {
    const endpoint = `/api/v1/canvas/list`;
    const response = await this.apiCall(endpoint);
    return response.json();
  }
}

// Export a singleton instance
export const canvasService = new CanvasService();
export default canvasService;

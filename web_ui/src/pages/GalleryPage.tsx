import React, { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { canvasService } from "../api/canvasService";
import { CanvasGallery } from "../components/CanvasGallery";
import { config } from "../config";
import {
  CanvasSummary,
  SSECanvasCreatedEvent,
  SSECanvasDeletedEvent,
  SSECanvasUpdatedEvent,
  SSEErrorEvent,
} from "../types";

export const GalleryPage: React.FC = () => {
  const navigate = useNavigate();
  const [canvasSummaries, setCanvasSummaries] = useState<CanvasSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sseConnected, setSseConnected] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);

  const loadCanvases = async () => {
    try {
      const response = await canvasService.listCanvases();
      setCanvasSummaries(response.canvases);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load canvases");
    }
  };

  // SSE event handlers
  const handleSSEEvent = (event: MessageEvent) => {
    console.log("SSE event received:", event.data);
    try {
      const data = JSON.parse(event.data);
      console.log("SSE event received:", data);

      switch (data.type) {
        case "canvas_created": {
          console.log("Canvas created:", data);
          const createdEvent = data as SSECanvasCreatedEvent;
          setCanvasSummaries(prev => [createdEvent.data, ...prev]);
          break;
        }
        case "canvas_deleted": {
          const deletedEvent = data as SSECanvasDeletedEvent;
          setCanvasSummaries(prev =>
            prev.filter(
              canvas => canvas.canvas_id !== deletedEvent.data.canvas_id
            )
          );
          break;
        }
        case "canvas_updated": {
          const updatedEvent = data as SSECanvasUpdatedEvent;
          setCanvasSummaries(prev =>
            prev.map(canvas =>
              canvas.canvas_id === updatedEvent.data.canvas_id
                ? updatedEvent.data
                : canvas
            )
          );
          break;
        }
        case "heartbeat": {
          // Handle heartbeat to keep connection alive
          console.debug("SSE heartbeat received");
          break;
        }
        case "error": {
          const errorEvent = data as SSEErrorEvent;
          console.error("SSE error:", errorEvent.data);
          setError(`SSE error: ${errorEvent.data.error || "Unknown error"}`);
          break;
        }
        default:
          console.warn("Unknown SSE event type:", data.type);
      }
    } catch (err) {
      console.error("Failed to parse SSE event:", err);
    }
  };

  const connectSSE = () => {
    // Close existing connection if any
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    const sseUrl = `${config.api.baseUrl}/api/v1/canvas/sse`;
    const eventSource = new EventSource(sseUrl);
    eventSourceRef.current = eventSource;

    eventSource.onopen = () => {
      console.log("SSE connection opened");
      setSseConnected(true);
      setError(null);
    };
    eventSource.addEventListener("canvas_created", event => {
      const data = JSON.parse(event.data);
      console.log("Canvas created:", data);
      setCanvasSummaries(prev => [data.data, ...prev]);
    });
    eventSource.addEventListener("canvas_deleted", event => {
      const data = JSON.parse(event.data);
      console.log("Canvas deleted:", data);
      setCanvasSummaries(prev =>
        prev.filter(canvas => canvas.canvas_id !== data.data.canvas_id)
      );
    });
    eventSource.addEventListener("canvas_updated", event => {
      const data = JSON.parse(event.data);
      console.log("Canvas updated:", data);
      setCanvasSummaries(prev =>
        prev.map(canvas =>
          canvas.canvas_id === data.data.canvas_id ? data.data : canvas
        )
      );
    });
    eventSource.onerror = err => {
      console.error("SSE connection error:", err);
      setSseConnected(false);
      setError("Lost connection to server. Retrying...");
    };

    return eventSource;
  };

  useEffect(() => {
    const loadCanvasesWrapper = async () => {
      setLoading(true);
      await loadCanvases();
      setLoading(false);
    };

    // Load canvases immediately
    loadCanvasesWrapper();

    // Set up SSE connection
    const eventSource = connectSSE();
    eventSourceRef.current = eventSource;

    // Cleanup on component unmount
    return () => {
      if (eventSourceRef.current) {
        console.log("Closing SSE connection");
        eventSourceRef.current.close();
        eventSourceRef.current = null;
      }
      setSseConnected(false);
    };
  }, []);

  const handleOpenCanvas = (id: string) => {
    navigate(`/canvas/${encodeURIComponent(id)}`);
  };

  const handleCreateCanvas = async (title?: string, description?: string) => {
    try {
      const response = await canvasService.createCanvas({
        title: title || null,
        description: description || null,
      });
      // SSE will handle updating the canvas list automatically
      // Optionally navigate to the new canvas
      if (response.canvas_id) {
        navigate(`/canvas/${encodeURIComponent(response.canvas_id)}`);
      }
    } catch (err) {
      throw new Error(
        err instanceof Error ? err.message : "Failed to create canvas"
      );
    }
  };

  const handleDeleteCanvas = async (canvasId: string) => {
    try {
      await canvasService.deleteCanvas(canvasId);
      setCanvasSummaries(prev =>
        prev.filter(canvas => canvas.canvas_id !== canvasId)
      );
    } catch (err) {
      throw new Error(
        err instanceof Error ? err.message : "Failed to delete canvas"
      );
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50">
        <div className="p-8">
          <div className="max-w-6xl mx-auto">
            <div className="flex justify-between items-center mb-12">
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                  Canvas Gallery
                </h1>
                <p className="text-gray-600 mt-2">
                  Loading your canvases...
                  {!sseConnected && " (Connecting to live updates...)"}
                </p>
              </div>
              <button
                disabled
                className="px-6 py-3 bg-gray-300 text-gray-500 font-medium rounded-xl cursor-not-allowed"
              >
                <svg
                  className="w-5 h-5 mr-2 inline"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 4v16m8-8H4"
                  />
                </svg>
                Create Canvas
              </button>
            </div>
            <div className="flex items-center justify-center py-20">
              <div className="text-center">
                <div className="mx-auto w-16 h-16 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-full flex items-center justify-center mb-4">
                  <svg
                    className="w-8 h-8 text-indigo-600 animate-spin"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                </div>
                <p className="text-gray-600">Loading canvases...</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50">
        <div className="p-8">
          <div className="max-w-6xl mx-auto">
            <div className="flex justify-between items-center mb-12">
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                  Canvas Gallery
                </h1>
                <p className="text-red-600 mt-2">
                  Failed to load canvases
                  {!sseConnected && " • Live updates disconnected"}
                </p>
              </div>
              <button
                onClick={() => {
                  loadCanvases();
                  // Also try to reconnect SSE if needed
                  if (!sseConnected) {
                    connectSSE();
                  }
                }}
                className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-medium rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-all duration-200"
              >
                <svg
                  className="w-5 h-5 mr-2 inline"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
                Retry
              </button>
            </div>
            <div className="flex items-center justify-center py-20">
              <div className="text-center">
                <div className="mx-auto w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mb-4">
                  <svg
                    className="w-8 h-8 text-red-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Something went wrong
                </h3>
                <p className="text-red-600 mb-4">{error}</p>
                <button
                  onClick={() => {
                    loadCanvases();
                    // Also try to reconnect SSE if needed
                    if (!sseConnected) {
                      connectSSE();
                    }
                  }}
                  className="inline-flex items-center px-4 py-2 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors"
                >
                  Try again
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <CanvasGallery
      canvasSummaries={canvasSummaries}
      onOpen={handleOpenCanvas}
      onCreate={handleCreateCanvas}
      onDelete={handleDeleteCanvas}
      showCreateButton={true}
      showDeleteButton={true}
    />
  );
};

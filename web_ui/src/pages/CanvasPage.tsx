import React, { useCallback, useEffect, useRef } from "react";
import { useParams } from "react-router-dom";
import canvasService from "../api/canvasService";
import { CanvasView } from "../components/CanvasView";
import { config } from "../config";
import { useCanvasStore } from "../store/canvasStore";
import {
  SSEErrorEvent,
  SSEMessageCommittedEvent,
  SSEMessageUpdatedEvent,
} from "../types";

export const CanvasPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { setCanvas, clear, updateMessage } = useCanvasStore();
  const canvas = useCanvasStore(s => s.canvas);
  const isLoading = useCanvasStore(s => s.isLoading);
  const error = useCanvasStore(s => s.error);
  const eventSourceRef = useRef<EventSource | null>(null);

  // SSE connection setup
  const connectSSE = useCallback(
    (canvasId: string) => {
      // Close existing connection if any
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }

      const sseUrl = `${config.api.baseUrl}/api/v1/canvas/${encodeURIComponent(canvasId)}/sse`;
      const eventSource = new EventSource(sseUrl);
      eventSourceRef.current = eventSource;

      eventSource.onopen = () => {
        console.log(`SSE connection opened for canvas ${canvasId}`);
      };

      eventSource.addEventListener("message_committed", event => {
        try {
          const data = JSON.parse(event.data) as SSEMessageCommittedEvent;
          console.log("Message committed:", data);

          // Get the current canvas from the store to avoid stale closure
          const currentCanvas = useCanvasStore.getState().canvas;

          // Update the canvas store with the new message
          if (currentCanvas && data.canvas_id === currentCanvas.canvas_id) {
            // Add the new message to the canvas
            const updatedNodes = { ...currentCanvas.nodes };
            updatedNodes[data.data.id] = data.data;

            // Update parent's child_ids if this message has a parent
            if (data.data.parent_id && updatedNodes[data.data.parent_id]) {
              const parentNode = updatedNodes[data.data.parent_id];
              if (!parentNode.child_ids.includes(data.data.id)) {
                updatedNodes[data.data.parent_id] = {
                  ...parentNode,
                  child_ids: [...parentNode.child_ids, data.data.id],
                };
              }
            }

            setCanvas({
              ...currentCanvas,
              nodes: updatedNodes,
            });
          }
        } catch (err) {
          console.error("Failed to parse message_committed event:", err);
        }
      });

      eventSource.addEventListener("message_updated", event => {
        try {
          const data = JSON.parse(event.data) as SSEMessageUpdatedEvent;
          console.log("Message updated:", data);

          // Get the current canvas from the store to avoid stale closure
          const currentCanvas = useCanvasStore.getState().canvas;

          // Update the canvas store with the updated message
          if (currentCanvas && data.canvas_id === currentCanvas.canvas_id) {
            updateMessage(data.data.id, data.data);
          }
        } catch (err) {
          console.error("Failed to parse message_updated event:", err);
        }
      });

      eventSource.addEventListener("heartbeat", () => {
        console.debug("SSE heartbeat received for canvas", canvasId);
      });

      eventSource.addEventListener("error", event => {
        try {
          const data = JSON.parse(
            (event as MessageEvent).data
          ) as SSEErrorEvent;
          console.error("SSE error:", data.data);
        } catch {
          // If we can't parse the error event, it's likely a connection error
          console.error("SSE connection error for canvas", canvasId);
        }
      });

      eventSource.onerror = () => {
        console.error("SSE connection error for canvas", canvasId);
      };

      return eventSource;
    },
    [setCanvas, updateMessage]
  );

  useEffect(() => {
    if (id) {
      canvasService
        .fetchCanvas(id)
        .then(data => {
          if (data) {
            setCanvas(data);
          } else {
            console.error("Canvas not found");
            clear();
          }
        })
        .catch(err => {
          console.error("Failed to fetch canvas:", err);
          clear();
        });
      connectSSE(id);
    } else {
      clear();
    }
  }, [id, setCanvas, updateMessage]);

  if (isLoading) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-500">
        Loading canvas...
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex-1 flex items-center justify-center text-red-500">
        Error: {error}
      </div>
    );
  }

  if (!canvas) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-500">
        Canvas not found
      </div>
    );
  }

  return (
    <CanvasView
      canvas={canvas}
      showControls={true}
      showMiniMap={true}
      showPanel={true}
    />
  );
};

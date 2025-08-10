"""API endpoints for llm_canvas.

Provides API endpoints defined in doc/server/api.md:
"""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any

from fastapi import HTTPException, Path, Query
from fastapi.responses import JSONResponse, StreamingResponse

if TYPE_CHECKING:  # Only for type checkers
    from collections.abc import Generator

    from .canvas_registry import CanvasRegistry
    from .types import (
        CanvasCommitMessageEvent,
        CanvasListResponse,
        CanvasSummary,
        CanvasUpdateMessageEvent,
        CreateCanvasRequest,
        CreateCanvasResponse,
        CreateMessageResponse,
        DeleteCanvasResponse,
        ErrorResponse,
    )


logger = logging.getLogger(__name__)
API_PREFIX = "/api/v1"


def setup_api_routes(app: Any, registry: CanvasRegistry) -> None:
    """Set up API routes on the FastAPI app."""

    @app.get(f"{API_PREFIX}/canvas/list")
    def list_canvases() -> CanvasListResponse:
        """List all available canvases.

        Returns:
            CanvasListResponse with list of canvas summaries
        """
        items: list[CanvasSummary] = [c.to_summary() for c in registry.list()]
        return {"canvases": items}

    @app.get(f"{API_PREFIX}/canvas")
    def get_canvas(canvas_id: str = Query(..., description="Canvas UUID")) -> Any:
        """Get a full canvas by ID.

        Args:
            canvas_id: Canvas UUID to retrieve

        Returns:
            CanvasData on success

        Raises:
            HTTPException: 404 if canvas not found
        """
        logger.info(f"Fetching canvas {canvas_id}")
        c = registry.get(canvas_id)
        if not c:
            error_response: ErrorResponse = {"error": "canvas_not_found", "message": "Canvas not found"}
            raise HTTPException(
                status_code=404,
                detail=error_response,
            )
        return JSONResponse(c.to_canvas_data())

    @app.post(f"{API_PREFIX}/canvas")
    def create_canvas(request: CreateCanvasRequest) -> CreateCanvasResponse:
        """Create a new canvas.

        Args:
            request: Canvas creation request with optional title and description

        Returns:
            CreateCanvasResponse with the canvas ID and success message
        """
        from .canvas import Canvas

        canvas = Canvas(title=request.get("title"), description=request.get("description"))
        registry.add(canvas)
        logger.info(f"Created canvas {canvas.canvas_id}")

        return {"canvas_id": canvas.canvas_id, "message": "Canvas created successfully"}

    @app.delete(f"{API_PREFIX}/canvas/{{canvas_id}}")
    def delete_canvas(canvas_id: str = Path(..., description="Canvas UUID to delete")) -> DeleteCanvasResponse:
        """Delete a canvas by ID.

        Args:
            canvas_id: Canvas UUID to delete

        Returns:
            DeleteCanvasResponse with success message

        Raises:
            HTTPException: 404 if canvas not found
        """
        removed = registry.remove(canvas_id)
        if not removed:
            error_response: ErrorResponse = {"error": "canvas_not_found", "message": "Canvas not found"}
            raise HTTPException(
                status_code=404,
                detail=error_response,
            )

        logger.info(f"Deleted canvas {canvas_id}")
        return {"canvas_id": canvas_id, "message": "Canvas deleted successfully"}

    @app.post(f"{API_PREFIX}/canvas/{{canvas_id}}/messages")
    def commit_message(
        request: CanvasCommitMessageEvent,
        canvas_id: str = Path(..., description="Canvas UUID"),
    ) -> CreateMessageResponse:
        """Commit a new message to a canvas.

        Args:
            canvas_id: Canvas UUID to add message to
            request: Canvas commit message event data

        Returns:
            CreateMessageResponse with the message ID and success message

        Raises:
            HTTPException: 404 if canvas not found
        """

        canvas = registry.get(canvas_id)
        if not canvas:
            error_response: ErrorResponse = {"error": "canvas_not_found", "message": "Canvas not found"}
            raise HTTPException(
                status_code=404,
                detail=error_response,
            )
        node_data = request["data"]
        node_id = request["data"]["id"]
        # check if the node id already exist
        if canvas.get_node(node_id):
            error_response: ErrorResponse = {"error": "node_already_exists", "message": "Node already exists"}
            raise HTTPException(
                status_code=400,
                detail=error_response,
            )

        # Commit the message to the canvas
        canvas._nodes[node_data["id"]] = node_data
        logger.info(f"Committed message {node_data['id']} to canvas {canvas_id}")

        return {
            "message_id": node_data["id"],
            "canvas_id": canvas_id,
            "message": "Message committed successfully",
        }

    @app.put(f"{API_PREFIX}/canvas/{{canvas_id}}/messages/{{message_id}}")
    def update_message(
        canvas_id: str = Path(..., description="Canvas UUID"),
        message_id: str = Path(..., description="Message ID to update"),
        request: CanvasUpdateMessageEvent = ...,
    ) -> CreateMessageResponse:
        """Update an existing message in a canvas.

        Args:
            canvas_id: Canvas UUID containing the message
            message_id: Message ID to update
            request: Canvas update message event data

        Returns:
            CreateMessageResponse with the message ID and success message

        Raises:
            HTTPException: 404 if canvas or message not found
        """
        from .types import Message

        canvas = registry.get(canvas_id)
        if not canvas:
            error_response: ErrorResponse = {"error": "canvas_not_found", "message": "Canvas not found"}
            raise HTTPException(
                status_code=404,
                detail=error_response,
            )

        # Check if message exists
        if canvas.get_node(message_id) is None:
            error_response: ErrorResponse = {"error": "message_not_found", "message": "Message not found"}
            raise HTTPException(
                status_code=404,
                detail=error_response,
            )

        # Extract message data from the event
        node_data = request["data"]
        updated_message: Message = node_data["message"]

        # Update the message in the canvas
        canvas.update_message(message_id, updated_message, meta=node_data["meta"])
        logger.info(f"Updated message {message_id} in canvas {canvas_id}")

        return {
            "message_id": message_id,
            "canvas_id": canvas_id,
            "message": "Message updated successfully",
        }

    # ---- (Future) Streaming SSE placeholder for spec alignment ----
    @app.get(f"{API_PREFIX}/canvas/stream")
    def stream(canvas_id: str = Query(..., description="Canvas UUID")) -> Any:
        """Stream canvas updates via Server-Sent Events.

        Args:
            canvas_id: Canvas UUID to stream

        Returns:
            StreamingResponse with SSE events

        Raises:
            HTTPException: 404 if canvas not found
        """
        c = registry.get(canvas_id)
        if not c:
            error_response: ErrorResponse = {"error": "canvas_not_found", "message": "Canvas not found"}
            raise HTTPException(
                status_code=404,
                detail=error_response,
            )

        def event_stream() -> Generator[str, None, None]:  # simple snapshot for now
            yield f"event: snapshot\ndata: {json.dumps(c.to_canvas_data())}\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

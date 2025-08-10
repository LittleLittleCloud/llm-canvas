"""API endpoints for llm_canvas.

Provides API endpoints defined in doc/server/api.md:
"""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any

from fastapi import HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse

if TYPE_CHECKING:  # Only for type checkers
    from collections.abc import Generator

    from .canvas_registry import CanvasRegistry
    from .types import CanvasListResponse, CanvasSummary, ErrorResponse


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

"""API endpoints for llm_canvas.

Provides API endpoints defined in doc/server/api.md:
- GET /api/v1/canvas/list
- GET /api/v1/canvas/get?id=...
- GET /api/v1/canvas/stream?id=...
"""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # Only for type checkers
    from collections.abc import Generator

    from .canvas import CanvasSummary
    from .canvasRegistry import CanvasRegistry
from fastapi import HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse

logger = logging.getLogger(__name__)
API_PREFIX = "/api/v1"


def setup_api_routes(app: Any, registry: CanvasRegistry) -> None:
    """Set up API routes on the FastAPI app."""

    @app.get(f"{API_PREFIX}/canvas/list")
    def list_canvases() -> dict:
        items: list[CanvasSummary] = [c.to_summary() for c in registry.list()]
        return {"canvases": items}

    @app.get(f"{API_PREFIX}/canvas")
    def get_canvas(canvas_id: str = Query(..., description="Canvas UUID")) -> Any:
        logger.info(f"Fetching canvas {canvas_id}")
        c = registry.get(canvas_id)
        if not c:
            raise HTTPException(
                status_code=404,
                detail={"error": "canvas_not_found", "message": "Canvas not found"},
            )
        return JSONResponse(c.to_canvas_data())

    # ---- (Future) Streaming SSE placeholder for spec alignment ----
    @app.get(f"{API_PREFIX}/canvas/stream")
    def stream(canvas_id: str = Query(..., description="Canvas UUID")) -> Any:
        c = registry.get(canvas_id)
        if not c:
            raise HTTPException(
                status_code=404,
                detail={"error": "canvas_not_found", "message": "Canvas not found"},
            )

        def event_stream() -> Generator[str, None, None]:  # simple snapshot for now
            yield f"event: snapshot\ndata: {json.dumps(c.to_canvas_data())}\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

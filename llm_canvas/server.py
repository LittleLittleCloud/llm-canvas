"""FastAPI server module for llm_canvas.

Provides API endpoints defined in doc/server/api.md:
- GET /api/v1/canvas/list
- GET /api/v1/canvas/get?id=...

Also serves the single-page web UI (if built) from the package static directory.
"""

from __future__ import annotations

import argparse
import logging
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any, List

from ._mockData import MOCK_CANVASES
from .canvas import Canvas
from .canvasRegistry import CanvasRegistry

try:  # pragma: no cover - optional dependency
    from fastapi import FastAPI, HTTPException, Query
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse, StreamingResponse
    from fastapi.staticfiles import StaticFiles
except ImportError:  # pragma: no cover
    FastAPI = None  # type: ignore

if TYPE_CHECKING:  # Only for type checkers
    from fastapi import FastAPI as _FastAPI  # noqa: F401

    from .canvas import CanvasSummary

logger = logging.getLogger(__name__)
API_PREFIX = "/api/v1"


# ---- App Factory ----


def _base_app() -> Any:
    if FastAPI is None:  # pragma: no cover
        raise RuntimeError(
            "FastAPI not installed. Install extra: uv add 'llm-canvas[server]'"
        )
    app = FastAPI(title="llm_canvas", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


def create_app_registry(registry: CanvasRegistry) -> Any:
    app = _base_app()

    # ---- API Endpoints ----
    @app.get(f"{API_PREFIX}/canvas/list")
    def list_canvases() -> dict:
        items: List[CanvasSummary] = []
        for c in registry.list():
            items.append(
                {
                    "canvas_id": c.canvas_id,
                    "created_at": c.created_at,
                    "root_ids": list(c._roots),  # internal but fine for summary
                    "node_count": len(c._nodes),
                    "meta": {"last_updated": registry.last_updated(c.canvas_id)},
                    "title": c.title,
                    "description": c.description,
                }
            )
        return {"canvases": items}

    @app.get(f"{API_PREFIX}/canvas")
    def get_canvas(id: str = Query(..., description="Canvas UUID")):
        logger.info(f"Fetching canvas {id}")
        c = registry.get(id)
        if not c:
            raise HTTPException(
                status_code=404,
                detail={"error": "canvas_not_found", "message": "Canvas not found"},
            )
        return JSONResponse(c.to_canvas_data())

    # ---- (Future) Streaming SSE placeholder for spec alignment ----
    @app.get(f"{API_PREFIX}/canvas/stream")
    def stream(id: str = Query(..., description="Canvas UUID")):
        c = registry.get(id)
        if not c:
            raise HTTPException(
                status_code=404,
                detail={"error": "canvas_not_found", "message": "Canvas not found"},
            )

        def event_stream():  # simple snapshot for now
            import json

            yield f"event: snapshot\ndata: {json.dumps(c.to_canvas_data())}\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    # ---- Static Frontend Serving ----
    static_dir = Path(__file__).parent / "static"
    if static_dir.exists():
        app.mount(
            "/assets", StaticFiles(directory=static_dir / "assets"), name="assets"
        )

        @app.get("/")
        def serve_index():
            from fastapi.responses import FileResponse

            return FileResponse(static_dir / "index.html")

    return app


def create_app_single(canvas: Canvas) -> Any:
    """Create a FastAPI app for a single canvas instance."""
    registry = CanvasRegistry()
    registry.add(canvas)
    return create_app_registry(registry)


# ---- CLI ----


def main() -> None:  # pragma: no cover - CLI utility
    parser = argparse.ArgumentParser(description="Serve llm_canvas API / UI")
    parser.add_argument("--host", default="127.0.0.1", help="Host to serve on")
    parser.add_argument("--port", type=int, default=8000, help="Port to serve on")
    args = parser.parse_args()

    registry = CanvasRegistry()

    # Load mock canvases for development/testing
    for canvas_id, canvas_data in MOCK_CANVASES.items():
        # Create canvas manually from data since we removed from_dict
        c = Canvas(
            canvas_id=canvas_data["canvas_id"],
            title=canvas_data.get("title"),
            description=canvas_data.get("description"),
        )
        c.created_at = canvas_data.get("created_at", time.time())

        # Manually populate nodes
        for nid, node_data in canvas_data.get("nodes", {}).items():
            c._nodes[nid] = {
                "id": node_data.get("id", nid),
                "content": node_data.get("content", {}),
                "parent_id": node_data.get("parent_id"),
                "child_ids": node_data.get("child_ids", []),
                "meta": node_data.get("meta", {}),
            }
        c._roots = list(canvas_data.get("root_ids", []))

        registry.add(c)
        print(f"Loaded mock canvas: {canvas_id} - {c.title}")

    app = create_app_registry(registry)

    try:
        import uvicorn

        print(f"Starting server at http://{args.host}:{args.port}")
        uvicorn.run(app, host=args.host, port=args.port)
    except ImportError:
        print("uvicorn not installed. Install with: uv add 'llm-canvas[server]'")


if __name__ == "__main__":  # pragma: no cover
    main()

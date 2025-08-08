"""FastAPI server module for llm_canvas.

Provides API endpoints defined in doc/server/api.md:
- GET /api/v1/canvas/list
- GET /api/v1/canvas/get?id=...

Also serves the single-page web UI (if built) from the package static directory.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from .canvas import Canvas

try:  # pragma: no cover - optional dependency
    from fastapi import FastAPI, HTTPException, Query
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse, StreamingResponse
    from fastapi.staticfiles import StaticFiles
except ImportError:  # pragma: no cover
    FastAPI = None  # type: ignore

if TYPE_CHECKING:  # Only for type checkers
    from fastapi import FastAPI as _FastAPI  # noqa: F401

API_PREFIX = "/api/v1"


# ---- Canvas Registry (simple in-memory) ----
class CanvasRegistry:
    """Stores canvases in-memory. Placeholder for future persistence layer."""

    def __init__(self):
        self._canvases: Dict[str, Canvas] = {}
        self._last_updated: Dict[str, float] = {}

    def add(self, canvas: Canvas):
        self._canvases[canvas.canvas_id] = canvas
        self._last_updated[canvas.canvas_id] = time.time()

    def get(self, canvas_id: str) -> Optional[Canvas]:
        return self._canvases.get(canvas_id)

    def list(self) -> List[Canvas]:
        return list(self._canvases.values())

    def touch(self, canvas_id: str):
        if canvas_id in self._last_updated:
            self._last_updated[canvas_id] = time.time()

    def last_updated(self, canvas_id: str) -> Optional[float]:
        return self._last_updated.get(canvas_id)


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


def create_app_single(canvas: Canvas) -> Any:
    """Create an app exposing API for a single canvas (legacy behavior)."""
    registry = CanvasRegistry()
    registry.add(canvas)
    return create_app_registry(registry)


def create_app_registry(registry: CanvasRegistry) -> Any:
    app = _base_app()

    # ---- API Endpoints ----
    @app.get(f"{API_PREFIX}/canvas/list")
    def list_canvases():
        items = []
        for c in registry.list():
            items.append(
                {
                    "canvas_id": c.canvas_id,
                    "created_at": c.created_at,
                    "root_ids": list(c._roots),  # internal but fine for summary
                    "node_count": len(c._nodes),
                    "meta": {"last_updated": registry.last_updated(c.canvas_id)},
                }
            )
        return {"canvases": items}

    @app.get(f"{API_PREFIX}/canvas/get")
    def get_canvas(id: str = Query(..., description="Canvas UUID")):
        c = registry.get(id)
        if not c:
            raise HTTPException(
                status_code=404,
                detail={"error": "canvas_not_found", "message": "Canvas not found"},
            )
        return JSONResponse(c.to_dict())

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
            yield f"event: snapshot\ndata: {c.to_json()}\n\n"

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


# ---- CLI ----


def main():  # pragma: no cover - CLI utility
    parser = argparse.ArgumentParser(description="Serve llm_canvas API / UI")
    parser.add_argument(
        "--canvas", action="append", help="Path to canvas JSON file (can be repeated)"
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host to serve on")
    parser.add_argument("--port", type=int, default=8000, help="Port to serve on")
    args = parser.parse_args()

    registry = CanvasRegistry()
    if args.canvas:
        for path in args.canvas:
            p = Path(path)
            if p.exists():
                c = Canvas.load(str(p))
                registry.add(c)
                print(f"Loaded canvas {c.canvas_id} from {path}")
            else:
                print(f"File not found: {path} - skipping")
    else:
        # Provide a fresh empty canvas for convenience
        c = Canvas()
        registry.add(c)
        print(f"Created new canvas {c.canvas_id}")

    app = create_app_registry(registry)

    try:
        import uvicorn

        print(f"Starting server at http://{args.host}:{args.port}")
        uvicorn.run(app, host=args.host, port=args.port)
    except ImportError:
        print("uvicorn not installed. Install with: uv add 'llm-canvas[server]'")


if __name__ == "__main__":  # pragma: no cover
    main()

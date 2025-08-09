"""FastAPI server module for llm_canvas.

Provides API endpoints defined in doc/server/api.md:
- GET /api/v1/canvas/list
- GET /api/v1/canvas/get?id=...

Also serves the single-page web UI (if built) from the package static directory.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ._api import setup_api_routes
from ._local_server import create_local_server
from ._mockData import MOCK_CANVASES
from .canvas import Canvas
from .canvasRegistry import CanvasRegistry

try:  # pragma: no cover - optional dependency
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
except ImportError:  # pragma: no cover
    FastAPI = None  # type: ignore[assignment]

if TYPE_CHECKING:  # Only for type checkers
    from fastapi import FastAPI as _FastAPI  # noqa: F401

logger = logging.getLogger(__name__)


# ---- App Factory ----


def _base_app() -> Any:
    if FastAPI is None:  # pragma: no cover
        error_msg = "FastAPI not installed. Install extra: uv add 'llm-canvas[server]'"
        raise RuntimeError(error_msg)
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

    # Set up API routes
    setup_api_routes(app, registry)

    # ---- Static Frontend Serving ----
    static_dir = Path(__file__).parent / "static"
    if static_dir.exists():
        app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")

        @app.get("/")
        def serve_index() -> Any:
            from fastapi.responses import FileResponse

            return FileResponse(static_dir / "index.html")

    return app


# ---- CLI ----


def main() -> None:  # pragma: no cover - CLI utility
    parser = argparse.ArgumentParser(description="Serve llm_canvas API / UI")
    parser.add_argument("--host", default="127.0.0.1", help="Host to serve on")
    parser.add_argument("--port", type=int, default=8000, help="Port to serve on")
    parser.add_argument("--local", action="store_true", help="Start as local server with session-based storage (default)")
    parser.add_argument("--log-level", default="info", choices=["debug", "info", "warning", "error"], help="Set logging level")
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper()), format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Use local server by default or when explicitly requested
    if True:  # Default to local server for now
        logger.info("Starting LLM Canvas Local Server (Free & Open Source)")
        logger.warning("⚠️  LOCAL SERVER LIMITATION: No data persistence")
        logger.warning("   • Data is lost when server restarts")
        logger.warning("   • No backup or recovery mechanisms")
        logger.warning("   • Session-based storage only")
        logger.info("   For permanent storage, consider cloud plans")

        app = create_local_server()
    else:
        # Fallback to original app creation method
        registry = CanvasRegistry()

        # Load mock canvases for development/testing
        for canvas_id, canvas_data in MOCK_CANVASES.items():
            c = Canvas.from_canvas_data(canvas_data)
            registry.add(c)
            logger.info(f"Loaded mock canvas: {canvas_id} - {c.title}")

        app = create_app_registry(registry)

    try:
        import uvicorn

        logger.info(f"Server starting at http://{args.host}:{args.port}")
        logger.info("Open your browser to start visualizing LLM conversations!")
        uvicorn.run(app, host=args.host, port=args.port, log_level=args.log_level)
    except ImportError:
        logger.exception("uvicorn not installed. Install with: uv add 'llm-canvas[server]'")


if __name__ == "__main__":  # pragma: no cover
    main()

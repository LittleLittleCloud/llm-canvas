"""Local server implementation for llm_canvas.

This module provides the free & open source local server that:
- Runs entirely in the user's local environment
- Provides complete privacy control
- Uses session-based storage only (no data persistence)
- Includes warnings about data limitations
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ._api import setup_api_routes
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


def create_local_server() -> Any:
    """Create a local server app with session-based storage and appropriate warnings.

    This is the free & open source local deployment that:
    - Runs entirely in the user's local environment
    - Provides complete privacy control
    - Uses session-based storage only (no data persistence)
    - Includes warnings about data limitations
    """
    if FastAPI is None:  # pragma: no cover
        error_msg = "FastAPI not installed. Install extra: uv add 'llm-canvas[server]'"
        raise RuntimeError(error_msg)

    app = FastAPI(
        title="LLM Canvas Local Server",
        version="0.1.0",
        description="Free & Open Source LLM Canvas Local Server - Session-based storage only",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Create in-memory registry for session-based storage
    registry = CanvasRegistry()

    # Load mock canvases for development/testing
    for canvas_id, canvas_data in MOCK_CANVASES.items():
        c = Canvas.from_canvas_data(canvas_data)
        registry.add(c)
        logger.info(f"Loaded mock canvas: {canvas_id} - {c.title}")

    # Set up API routes
    setup_api_routes(app, registry)

    # Add a warning endpoint about data persistence
    @app.get("/api/v1/server/info")
    def server_info() -> dict[str, Any]:
        """Provide information about the local server capabilities and limitations."""
        return {
            "server_type": "local",
            "version": "0.1.0",
            "features": {
                "real_time_visualization": True,
                "conversation_branches": True,
                "tool_call_display": True,
                "multi_format_support": True,
                "api_integration": True,
            },
            "limitations": {"data_persistence": False, "cross_session_storage": False, "backup_recovery": False},
            "warnings": ["Data is lost when server restarts", "No backup or recovery mechanisms", "Session-based storage only"],
            "upgrade_info": {
                "cloud_plans_available": True,
                "cloud_features": ["permanent data storage", "cross-device access", "team collaboration"],
            },
        }

    # ---- Static Frontend Serving ----
    static_dir = Path(__file__).parent / "static"
    if static_dir.exists():
        app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")

        @app.get("/")
        def serve_index() -> Any:
            from fastapi.responses import FileResponse

            return FileResponse(static_dir / "index.html")

    return app


def start_local_server(host: str = "127.0.0.1", port: int = 8000, log_level: str = "info") -> None:
    """Start a local LLM Canvas server with session-based storage.

    Args:
        host: Host to serve on (default: 127.0.0.1)
        port: Port to serve on (default: 8000)
        log_level: Logging level (debug, info, warning, error)
    """
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()), format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logger.info("Starting LLM Canvas Local Server (Free & Open Source)")
    logger.warning("⚠️  LOCAL SERVER LIMITATION: No data persistence")
    logger.warning("   • Data is lost when server restarts")
    logger.warning("   • No backup or recovery mechanisms")
    logger.warning("   • Session-based storage only")
    logger.info("   For permanent storage, consider cloud plans")

    app = create_local_server()

    try:
        import uvicorn

        logger.info(f"Server starting at http://{host}:{port}")
        logger.info("Open your browser to start visualizing LLM conversations!")
        uvicorn.run(app, host=host, port=port, log_level=log_level)
    except ImportError:
        logger.exception("uvicorn not installed. Install with: uv add 'llm-canvas[server]'")

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
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from ._api import v1_router

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
        separate_input_output_schemas=False,  # Disable separate schemas for input/output
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

    # Set up API routes
    app.include_router(v1_router)

    # ---- Static Frontend Serving ----
    static_dir = Path(__file__).parent / "static"
    if static_dir.exists():
        app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")

        @app.get("/")
        def serve_index() -> Any:
            return FileResponse(static_dir / "index.html")

        # Catch-all route for SPA routing - must be after API routes
        @app.get("/{full_path:path}")
        def serve_spa(full_path: str) -> Any:
            # For non-API routes, serve the index.html to let frontend router handle it
            if not full_path.startswith("api/"):
                return FileResponse(static_dir / "index.html")
            # If it's an API route that doesn't exist, let FastAPI handle the 404
            raise HTTPException(status_code=404, detail="Not found")

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

    app = create_local_server()

    try:
        logger.info(f"Server starting at http://{host}:{port}")
        logger.info("Open your browser to start visualizing LLM conversations!")
        uvicorn.run(app, host=host, port=port, log_level=log_level)
    except ImportError:
        logger.exception("uvicorn not installed. Install with: uv add 'llm-canvas[server]'")

"""Server module for llm_canvas.

This module provides server creation functions that work with an existing registry.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .canvas_registry import CanvasRegistry

try:  # pragma: no cover - optional dependency
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
except ImportError:  # pragma: no cover
    FastAPI = None  # type: ignore[assignment]


def create_app_registry(registry: CanvasRegistry) -> Any:
    """Create a FastAPI app with the given registry.

    Args:
        registry: The canvas registry to use for the app

    Returns:
        FastAPI application instance

    Raises:
        RuntimeError: If FastAPI is not installed
    """
    if FastAPI is None:  # pragma: no cover
        error_msg = "FastAPI not installed. Install extra: uv add 'llm-canvas[server]'"
        raise RuntimeError(error_msg)

    from pathlib import Path

    from ._api import setup_api_routes
    from .types import HealthCheckResponse

    app = FastAPI(
        title="LLM Canvas Server",
        version="0.1.0",
        description="LLM Canvas Server with custom registry",
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

    # Set up API routes with the provided registry
    setup_api_routes(app, registry)

    # Add a health check endpoint
    @app.get("/api/v1/health")
    def health_check() -> HealthCheckResponse:
        """Health check endpoint to verify server is running."""
        return {
            "status": "healthy",
            "server_type": "local",
            "timestamp": None,
        }

    # ---- Static Frontend Serving ----
    static_dir = Path(__file__).parent / "static"
    if static_dir.exists():
        from fastapi.staticfiles import StaticFiles

        app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")

        @app.get("/")
        def serve_index() -> Any:
            from fastapi.responses import FileResponse

            return FileResponse(static_dir / "index.html")

    return app

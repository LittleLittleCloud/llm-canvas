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

from fastapi import FastAPI
from fastapi import FastAPI as _FastAPI  # noqa: F401
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

from ._api import v1_router

logger = logging.getLogger(__name__)


def custom_openapi_schema(app: FastAPI) -> dict[str, Any]:
    """Generate custom OpenAPI schema without Input/Output variants."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="LLM Canvas API",
        version="0.1.0",
        description="RESTful API for LLM Canvas operations",
        routes=app.routes,
    )

    # Fix duplicate schema titles by ensuring unique names
    if "components" in openapi_schema and "schemas" in openapi_schema["components"]:
        schemas = openapi_schema["components"]["schemas"]

        # Remove Input/Output variants and merge them into single schemas
        schemas_to_remove = []
        schemas_to_add = {}

        for schema_name, schema_def in schemas.items():
            if schema_name.endswith(("-Input", "-Output")):
                base_name = schema_name.replace("-Input", "").replace("-Output", "")

                # Use the base name without suffix as the title
                if "title" in schema_def:
                    schema_def["title"] = base_name

                # Keep the first variant we see (usually Input), discard others
                if base_name not in schemas_to_add:
                    schemas_to_add[base_name] = schema_def

                schemas_to_remove.append(schema_name)

        # Remove old variants
        for schema_name in schemas_to_remove:
            del schemas[schema_name]

        # Add cleaned schemas
        schemas.update(schemas_to_add)

        # Update all references to point to the cleaned schema names
        def update_refs(obj: Any) -> Any:
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key == "$ref" and isinstance(value, str):
                        for old_name in schemas_to_remove:
                            if old_name in value:
                                base_name = old_name.replace("-Input", "").replace("-Output", "")
                                obj[key] = value.replace(old_name, base_name)
                    else:
                        update_refs(value)
            elif isinstance(obj, list):
                for item in obj:
                    update_refs(item)

        update_refs(openapi_schema)

    app.openapi_schema = openapi_schema
    return app.openapi_schema


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

    # Set custom OpenAPI schema to eliminate Input/Output variants
    app.openapi = lambda: custom_openapi_schema(app)

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

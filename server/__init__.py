"""LLM Canvas Server - FastAPI server components."""

from .api import (
    CreateCanvasRequest,
    CreateCanvasResponse,
    CreateMessageResponse,
    DeleteCanvasResponse,
    DeleteMessageResponse,
    ErrorResponse,
    HealthCheckResponse,
    StreamEventData,
    UpdateCanvasRequest,
    v1_router,
)
from .registry import CanvasRegistry, get_local_registry
from .server import create_local_server as create_app
from .server import start_local_server

__all__ = [
    # Registry exports
    "CanvasRegistry",
    # API exports
    "CreateCanvasRequest",
    "CreateCanvasResponse",
    "CreateMessageResponse",
    "DeleteCanvasResponse",
    "DeleteMessageResponse",
    "ErrorResponse",
    "HealthCheckResponse",
    "StreamEventData",
    "UpdateCanvasRequest",
    # Server exports
    "create_app",
    "get_local_registry",
    "start_local_server",
    "v1_router",
]

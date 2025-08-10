# Core classes and utilities
from .canvas import Canvas
from .canvas_client import CanvasClient
from .canvas_registry import CanvasRegistry

# All type definitions
from .types import (
    BranchInfo,
    CanvasCommitMessageEvent,
    CanvasData,
    CanvasDeleteMessageEvent,
    CanvasEvent,
    CanvasListResponse,
    CanvasSummary,
    CanvasUpdateMessageEvent,
    CreateCanvasRequest,
    CreateCanvasResponse,
    CreateMessageRequest,
    CreateMessageResponse,
    DeleteCanvasResponse,
    DeleteMessageResponse,
    ErrorResponse,
    HealthCheckResponse,
    Message,
    MessageBlock,
    MessageNode,
    StreamEventData,
    TextBlockParam,
    ToolResultBlockParam,
    ToolUseBlockParam,
    UpdateCanvasRequest,
    UpdateMessageRequest,
)

# Server functions (optional dependency)
try:
    from ._local_server import start_local_server
except ImportError:
    start_local_server = None  # type: ignore[assignment]

# Default canvas client instance for convenience
canvas_client = CanvasClient()

__all__ = [
    "BranchInfo",
    "Canvas",
    "CanvasClient",
    "CanvasCommitMessageEvent",
    "CanvasData",
    "CanvasDeleteMessageEvent",
    "CanvasEvent",
    "CanvasListResponse",
    "CanvasRegistry",
    "CanvasSummary",
    "CanvasUpdateMessageEvent",
    "CreateCanvasRequest",
    "CreateCanvasResponse",
    "CreateMessageRequest",
    "CreateMessageResponse",
    "DeleteCanvasResponse",
    "DeleteMessageResponse",
    "ErrorResponse",
    "HealthCheckResponse",
    "Message",
    "MessageBlock",
    "MessageNode",
    "StreamEventData",
    "TextBlockParam",
    "ToolResultBlockParam",
    "ToolUseBlockParam",
    "UpdateCanvasRequest",
    "UpdateMessageRequest",
    "canvas_client",
    "start_local_server",
]

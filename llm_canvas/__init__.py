from .canvas import (
    Canvas,
    CanvasData,
    CanvasSummary,
    Message,
    MessageBlock,
    MessageNode,
    TextBlockParam,
    ToolResultBlockParam,
    ToolUseBlockParam,
)
from .canvasClient import CanvasClient
from .canvasRegistry import CanvasRegistry

# Server functions (optional dependency)
try:
    from ._local_server import start_local_server
except ImportError:
    start_local_server = None  # type: ignore[assignment]

# Default canvas client instance for convenience
canvas_client = CanvasClient()

__all__ = [
    "Canvas",
    "CanvasClient",
    "CanvasData",
    "CanvasRegistry",
    "CanvasSummary",
    "Message",
    "MessageBlock",
    "MessageNode",
    "TextBlockParam",
    "ToolResultBlockParam",
    "ToolUseBlockParam",
    "canvas_client",  # Default instance
    "start_local_server",  # Local server function
]

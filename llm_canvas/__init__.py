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
]

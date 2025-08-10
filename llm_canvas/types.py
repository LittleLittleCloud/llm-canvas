"""Type definitions for llm_canvas.

This module contains all TypedDict definitions used throughout the llm_canvas package,
including API request/response types and core data structures.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypedDict

if TYPE_CHECKING:
    from collections.abc import Iterable

from anthropic.types import TextBlockParam, ToolResultBlockParam, ToolUseBlockParam

# ---- Core Data Types ----

type UnSupportedBlockParam = Any  # Placeholder for unsupported block types
# Union type for message blocks matching TypeScript
MessageBlock = TextBlockParam | ToolUseBlockParam | ToolResultBlockParam | Any


class Message(TypedDict):
    """Message structure for canvas conversations."""

    content: str | Iterable[MessageBlock]
    role: Literal["user", "assistant", "system"]


class MessageNode(TypedDict):
    """Node in the canvas conversation graph."""

    id: str
    message: Message
    parent_id: str | None
    child_ids: list[str]
    meta: dict[str, Any] | None


class CanvasSummary(TypedDict):
    """Summary information about a canvas."""

    canvas_id: str
    created_at: float
    root_ids: list[str]
    node_count: int
    title: str | None
    description: str | None
    meta: dict[str, Any]


class CanvasData(TypedDict):
    """Complete canvas data structure."""

    title: str | None
    last_updated: float | None
    description: str | None
    canvas_id: str
    created_at: float
    root_ids: list[str]
    nodes: dict[str, MessageNode]


type CanvasEventType = Literal["commit_message", "update_message", "delete_message"]


class CanvasCommitMessageEvent(TypedDict):
    """Event data for canvas message commits."""

    event_type: Literal["commit_message"]
    canvas_id: str
    timestamp: float
    data: MessageNode


class CanvasUpdateMessageEvent(TypedDict):
    """Event data for canvas message updates."""

    event_type: Literal["update_message"]
    canvas_id: str
    timestamp: float
    data: MessageNode


class CanvasDeleteMessageEvent(TypedDict):
    """Event data for canvas message deletions."""

    event_type: Literal["delete_message"]
    canvas_id: str
    timestamp: float
    data: str  # Node ID that was deleted


type CanvasEvent = CanvasCommitMessageEvent | CanvasUpdateMessageEvent | CanvasDeleteMessageEvent


class BranchInfo(TypedDict):
    """Information about a canvas branch."""

    name: str
    description: str | None
    head_node_id: str | None
    created_at: float


# ---- API Response TypedDict Definitions ----


class HealthCheckResponse(TypedDict):
    """Response type for GET /api/v1/health"""

    status: Literal["healthy"]
    server_type: Literal["local", "cloud"]
    timestamp: float | None


class CanvasListResponse(TypedDict):
    """Response type for GET /api/v1/canvas/list"""

    canvases: list[CanvasSummary]


class ErrorResponse(TypedDict):
    """Standard error response format"""

    error: str
    message: str


class StreamEventData(TypedDict):
    """Data structure for SSE stream events"""

    event: str
    data: str


# ---- API Request TypedDict Definitions (for future endpoints) ----


class CreateCanvasRequest(TypedDict, total=False):
    """Request type for POST /api/v1/canvas (future endpoint)"""

    title: str | None
    description: str | None


class UpdateCanvasRequest(TypedDict, total=False):
    """Request type for PUT /api/v1/canvas/{canvas_id} (future endpoint)"""

    title: str | None
    description: str | None


class CreateMessageRequest(TypedDict):
    """Request type for POST /api/v1/canvas/{canvas_id}/messages (future endpoint)"""

    content: str
    role: str
    parent_id: str | None
    meta: dict[str, Any] | None


class UpdateMessageRequest(TypedDict, total=False):
    """Request type for PUT /api/v1/canvas/{canvas_id}/messages/{message_id} (future endpoint)"""

    content: str
    meta: dict[str, Any] | None


# ---- API Response TypedDict Definitions for future endpoints ----


class CreateCanvasResponse(TypedDict):
    """Response type for POST /api/v1/canvas (future endpoint)"""

    canvas_id: str
    message: str


class DeleteCanvasResponse(TypedDict):
    """Response type for DELETE /api/v1/canvas/{canvas_id} (future endpoint)"""

    canvas_id: str
    message: str


class CreateMessageResponse(TypedDict):
    """Response type for POST /api/v1/canvas/{canvas_id}/messages (future endpoint)"""

    message_id: str
    canvas_id: str
    message: str


class DeleteMessageResponse(TypedDict):
    """Response type for DELETE /api/v1/canvas/{canvas_id}/messages/{message_id} (future endpoint)"""

    message_id: str
    canvas_id: str
    message: str


# ---- Re-export anthropic types for convenience ----
if TYPE_CHECKING:
    __all__ = [
        "BranchInfo",
        "CanvasCommitMessageEvent",
        "CanvasData",
        "CanvasDeleteMessageEvent",
        "CanvasEvent",
        "CanvasEventType",
        "CanvasListResponse",
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
        "UnSupportedBlockParam",
        "UpdateCanvasRequest",
        "UpdateMessageRequest",
    ]

"""Private type definitions for llm_canvas server-side events.

This module contains all TypedDict definitions used internally by the SSE system,
keeping them private to the server implementation.
"""

from __future__ import annotations

from typing import Literal, TypedDict, Union

from llm_canvas.types import CanvasSummary, MessageNode

# ---- SSE Event Types ----

SSEEventType = Literal[
    "canvas_created",
    "canvas_updated",
    "canvas_deleted",
    "message_committed",
    "message_updated",
    "message_deleted",
    "heartbeat",
    "error",
]


class SSEEventBase(TypedDict):
    """Base structure for all SSE events."""

    type: SSEEventType
    timestamp: float


class SSECanvasCreatedEvent(TypedDict):
    """SSE event data for canvas creation."""

    type: Literal["canvas_created"]
    timestamp: float
    data: CanvasSummary


class SSECanvasUpdatedEvent(TypedDict):
    """SSE event data for canvas updates."""

    type: Literal["canvas_updated"]
    timestamp: float
    data: CanvasSummary


class SSECanvasDeletedEventData(TypedDict):
    """Data payload for canvas deleted events."""

    canvas_id: str


class SSECanvasDeletedEvent(TypedDict):
    """SSE event data for canvas deletion."""

    type: Literal["canvas_deleted"]
    timestamp: float
    data: SSECanvasDeletedEventData


class SSEMessageCommittedEvent(TypedDict):
    """SSE event data for message commits."""

    type: Literal["message_committed"]
    timestamp: float
    canvas_id: str
    data: MessageNode


class SSEMessageUpdatedEvent(TypedDict):
    """SSE event data for message updates."""

    type: Literal["message_updated"]
    timestamp: float
    canvas_id: str
    data: MessageNode


class SSEMessageDeletedEventData(TypedDict):
    """Data payload for message deleted events."""

    message_id: str


class SSEMessageDeletedEvent(TypedDict):
    """SSE event data for message deletion."""

    type: Literal["message_deleted"]
    timestamp: float
    canvas_id: str
    data: SSEMessageDeletedEventData


class SSEHeartbeatEvent(TypedDict):
    """SSE heartbeat event to keep connections alive."""

    type: Literal["heartbeat"]
    timestamp: float


class SSEErrorEventData(TypedDict):
    """Data payload for error events."""

    error: str


class SSEErrorEvent(TypedDict):
    """SSE error event for stream errors."""

    type: Literal["error"]
    timestamp: float
    data: SSEErrorEventData


# Union type for all SSE global canvas events
SSEGlobalEvent = Union[SSECanvasCreatedEvent, SSECanvasUpdatedEvent, SSECanvasDeletedEvent, SSEHeartbeatEvent, SSEErrorEvent]

# Union type for all SSE canvas-specific message events
SSECanvasEvent = Union[
    SSEMessageCommittedEvent, SSEMessageUpdatedEvent, SSEMessageDeletedEvent, SSEHeartbeatEvent, SSEErrorEvent
]

# Union type for all SSE events
SSEEvent = Union[SSEGlobalEvent, SSECanvasEvent]

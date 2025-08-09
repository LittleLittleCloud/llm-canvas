from __future__ import annotations

import logging
import threading
import time
import uuid
from typing import TYPE_CHECKING, Any, Callable, Literal, TypedDict

if TYPE_CHECKING:
    from collections.abc import Iterable

from anthropic.types import TextBlockParam, ToolResultBlockParam, ToolUseBlockParam

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---- Data Models ----

type UnSupportedBlockParam = Any  # Placeholder for unsupported block types
# Union type for message blocks matching TypeScript
MessageBlock = TextBlockParam | ToolUseBlockParam | ToolResultBlockParam | Any


class Message(TypedDict):
    content: str | Iterable[MessageBlock]
    role: Literal["user", "assistant", "system"]


class MessageNode(TypedDict):
    id: str
    content: Message
    parent_id: str | None
    child_ids: list[str]
    meta: dict[str, Any] | None


class CanvasSummary(TypedDict):
    canvas_id: str
    created_at: float
    root_ids: list[str]
    node_count: int
    title: str | None
    description: str | None
    meta: dict[str, Any]


class CanvasData(TypedDict):
    title: str | None
    last_updated: float | None
    description: str | None
    canvas_id: str
    created_at: float
    root_ids: list[str]
    nodes: dict[str, MessageNode]


class CanvasEvent(TypedDict):
    event_type: Literal["message_added", "message_updated", "canvas_updated"]
    canvas_id: str
    timestamp: float
    data: dict[str, Any]


class Canvas:
    """Represents a DAG of message nodes (LLM conversation branches)."""

    def __init__(
        self,
        canvas_id: str | None = None,
        title: str | None = None,
        description: str | None = None,
    ) -> None:
        self.canvas_id = canvas_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.created_at = time.time()
        self._nodes: dict[str, MessageNode] = {}
        self._roots: list[str] = []
        self._server_thread = None
        self._server_running = False

        # Event system
        self._event_listeners: list[Callable[[CanvasEvent], None]] = []
        self._event_lock = threading.Lock()

    # ---- Event System ----
    def add_event_listener(self, listener: Callable[[CanvasEvent], None]) -> None:
        """Add an event listener that will be called when canvas events occur."""
        with self._event_lock:
            self._event_listeners.append(listener)

    def remove_event_listener(self, listener: Callable[[CanvasEvent], None]) -> None:
        """Remove an event listener."""
        with self._event_lock:
            if listener in self._event_listeners:
                self._event_listeners.remove(listener)

    def _emit_event(self, event: CanvasEvent) -> None:
        """Emit an event to all registered listeners."""
        with self._event_lock:
            listeners = list(self._event_listeners)  # Create a copy for thread safety

        for listener in listeners:
            try:
                listener(event)
            except Exception as e:
                logger.exception(f"Error in event listener: {e}")

    # ---- Public API ----
    def add_message(
        self,
        message: Message,
        parent_node: MessageNode | None = None,
        meta: dict[str, Any] | None = None,
        node_id: str | None = None,
    ) -> MessageNode:
        node_id = node_id or str(uuid.uuid4())

        node: MessageNode = {
            "id": node_id,
            "content": message,
            "parent_id": parent_node["id"] if parent_node else None,
            "child_ids": [],
            "meta": meta or {"timestamp": time.time()},
        }
        self._nodes[node_id] = node
        if parent_node:
            parent_node["child_ids"].append(node_id)
        else:
            self._roots.append(node_id)

        # Emit SSE event
        event: CanvasEvent = {
            "event_type": "message_added",
            "canvas_id": self.canvas_id,
            "timestamp": time.time(),
            "data": {"node": node, "canvas_data": self.to_canvas_data()},
        }
        self._emit_event(event)

        return node

    def get_node(self, node_id: str) -> MessageNode | None:
        return self._nodes.get(node_id)

    def iter_nodes(self) -> Iterable[MessageNode]:
        return self._nodes.values()

    def to_summary(self) -> CanvasSummary:
        """Create a summary representation of the canvas."""
        return {
            "canvas_id": self.canvas_id,
            "created_at": self.created_at,
            "root_ids": list(self._roots),
            "node_count": len(self._nodes),
            "title": self.title,
            "description": self.description,
            "meta": {"last_updated": time.time()},
        }

    def to_canvas_data(self) -> CanvasData:
        """Convert the canvas to CanvasData format."""

        return {
            "canvas_id": self.canvas_id,
            "created_at": self.created_at,
            "root_ids": list(self._roots),
            "nodes": dict(self._nodes),
            "title": self.title,
            "description": self.description,
            "last_updated": time.time(),
        }

    def run(
        self, host: str = "127.0.0.1", port: int = 8000, background: bool = False
    ) -> None:
        """Start the web UI / API server for this canvas.

        The FastAPI application has been moved to llm_canvas.server. This method now
        creates a single-canvas registry and launches the server.
        """
        try:
            from .server import create_app_single  # Lazy import
        except Exception as e:  # pragma: no cover
            raise RuntimeError(
                "Server components not available. Install extras: uv add 'llm-canvas[server]'"
            ) from e

        app = create_app_single(self)

        if background:
            import threading
            import time as _t

            def run_server() -> None:
                try:
                    import uvicorn

                    self._server_running = True
                    uvicorn.run(app, host=host, port=port, log_level="warning")
                except ImportError:
                    logger.warning("uvicorn not available - server not started")
                finally:
                    self._server_running = False

            self._server_thread = threading.Thread(target=run_server, daemon=True)
            self._server_thread.start()
            logger.info(
                "🚀 Web UI/API started in background at http://%s:%s", host, port
            )
            _t.sleep(1)  # Give server time to start
        else:
            try:
                import uvicorn

                logger.info("🚀 Starting Web UI/API at http://%s:%s", host, port)
                uvicorn.run(app, host=host, port=port)
            except ImportError:
                logger.exception("uvicorn not available - install with: uv add uvicorn")

    def wait_for_server(self) -> None:
        """Block execution until the background server stops.

        This is useful when running the server in background mode and you want
        to keep the main thread alive. Call this after canvas.run(background=True).
        """
        if self._server_thread is None:
            logger.warning(
                "No background server running. Use canvas.run(background=True) first."
            )
            return

        try:
            logger.info("Server running in background. Press Ctrl+C to stop.")
            while self._server_running and self._server_thread.is_alive():
                time.sleep(0.1)
        except KeyboardInterrupt:
            logger.info("Shutting down server...")
            self._server_running = False

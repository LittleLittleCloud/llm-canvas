from __future__ import annotations

import json
import logging
import time
import uuid
from typing import Any, Dict, Iterable, List, Literal, Optional, TypedDict, Union

from anthropic.types import TextBlockParam, ToolResultBlockParam, ToolUseBlockParam

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---- Data Models ----


# Union type for message blocks matching TypeScript
MessageBlock = Union[TextBlockParam, ToolUseBlockParam, ToolResultBlockParam]


class Message(TypedDict):
    content: Union[str, List[MessageBlock]]
    role: Literal["user", "assistant", "system"]


class MessageNode(TypedDict):
    id: str
    content: Message
    parent_id: Optional[str]
    child_ids: List[str]
    meta: Optional[Dict[str, Any]]


class CanvasSummary(TypedDict):
    canvas_id: str
    created_at: float
    root_ids: List[str]
    node_count: int
    title: Optional[str]
    description: Optional[str]
    meta: Dict[str, Any]


class Canvas:
    """Represents a DAG of message nodes (LLM conversation branches)."""

    def __init__(
        self,
        canvas_id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ):
        self.canvas_id = canvas_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.created_at = time.time()
        self._nodes: Dict[str, MessageNode] = {}
        self._roots: List[str] = []
        self._server_thread = None
        self._server_running = False

    # ---- Public API ----
    def add_message(
        self,
        content: Any,
        role: Literal["user", "assistant", "system"] = "user",
        parent_node: Optional[MessageNode] = None,
        meta: Optional[Dict[str, Any]] = None,
        id: Optional[str] = None,
    ) -> MessageNode:
        node_id = id or str(uuid.uuid4())

        # Create the Message object
        message: Message = {
            "content": content if isinstance(content, (str, list)) else str(content),
            "role": role,
        }

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
        return node

    def get_node(self, node_id: str) -> Optional[MessageNode]:
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

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "canvas_id": self.canvas_id,
            "created_at": self.created_at,
            "root_ids": list(self._roots),
            "nodes": {nid: dict(n) for nid, n in self._nodes.items()},
        }
        if self.title is not None:
            result["title"] = self.title
        if self.description is not None:
            result["description"] = self.description
        return result

    def to_json(self, **json_kwargs) -> str:
        return json.dumps(self.to_dict(), **json_kwargs)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Canvas":
        canvas = cls(
            canvas_id=data["canvas_id"],
            title=data.get("title"),
            description=data.get("description"),
        )
        canvas.created_at = data.get("created_at", time.time())
        for nid, nd in data.get("nodes", {}).items():
            # Ensure the node has all required fields with defaults
            node: MessageNode = {
                "id": nd.get("id", nid),
                "role": nd.get("role", "user"),
                "content": nd.get("content", []),
                "parent_id": nd.get("parent_id"),
                "child_ids": nd.get("child_ids", []),
                "meta": nd.get("meta", {}),
            }
            canvas._nodes[nid] = node
        canvas._roots = list(data.get("root_ids", []))
        return canvas

    @classmethod
    def from_json(cls, raw: str) -> "Canvas":
        return cls.from_dict(json.loads(raw))

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: str) -> "Canvas":
        with open(path, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))

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

            def run_server():
                try:
                    import uvicorn

                    self._server_running = True
                    uvicorn.run(app, host=host, port=port, log_level="warning")
                except ImportError:
                    print("uvicorn not available - server not started")
                finally:
                    self._server_running = False

            self._server_thread = threading.Thread(target=run_server, daemon=True)
            self._server_thread.start()
            print(f"🚀 Web UI/API started in background at http://{host}:{port}")
            _t.sleep(1)  # Give server time to start
        else:
            try:
                import uvicorn

                print(f"🚀 Starting Web UI/API at http://{host}:{port}")
                uvicorn.run(app, host=host, port=port)
            except ImportError:
                print("uvicorn not available - install with: uv add uvicorn")

    def wait_for_server(self) -> None:
        """Block execution until the background server stops.

        This is useful when running the server in background mode and you want
        to keep the main thread alive. Call this after canvas.run(background=True).
        """
        if self._server_thread is None:
            print(
                "No background server running. Use canvas.run(background=True) first."
            )
            return

        try:
            print("Server running in background. Press Ctrl+C to stop.")
            while self._server_running and self._server_thread.is_alive():
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nShutting down server...")
            self._server_running = False

    # ---- Internal helpers ----
    def _normalize_content(self, content: Any) -> List[Dict[str, Any]]:
        # Basic normalization; can expand later for multi-part
        if isinstance(content, list):
            # assume already list of blocks
            return content
        if isinstance(content, str):
            return [{"type": "text", "text": content}]
        # Fallback to repr
        return [{"type": "text", "text": repr(content)}]


# Server (FastAPI) implementation moved to llm_canvas.server

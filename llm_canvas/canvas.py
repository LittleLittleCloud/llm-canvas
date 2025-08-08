from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---- Data Models ----


@dataclass
class MessageNode:
    id: str
    role: str
    content: List[Dict[str, Any]]
    parent_id: Optional[str] = None
    child_ids: List[str] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class Canvas:
    """Represents a DAG of message nodes (LLM conversation branches)."""

    def __init__(self, canvas_id: Optional[str] = None):
        self.canvas_id = canvas_id or str(uuid.uuid4())
        self.created_at = time.time()
        self._nodes: Dict[str, MessageNode] = {}
        self._roots: List[str] = []
        self._server_thread = None
        self._server_running = False

    # ---- Public API ----
    def add_message(
        self,
        content: Any,
        role: str = "user",
        parent_node: Optional[MessageNode] = None,
        meta: Optional[Dict[str, Any]] = None,
        id: Optional[str] = None,
    ) -> MessageNode:
        node_id = id or str(uuid.uuid4())
        normalized_content = self._normalize_content(content)
        node = MessageNode(
            id=node_id,
            role=role,
            content=normalized_content,
            parent_id=parent_node.id if parent_node else None,
            meta=meta or {"timestamp": time.time()},
        )
        self._nodes[node_id] = node
        if parent_node:
            parent_node.child_ids.append(node_id)
        else:
            self._roots.append(node_id)
        return node

    def get_node(self, node_id: str) -> Optional[MessageNode]:
        return self._nodes.get(node_id)

    def iter_nodes(self) -> Iterable[MessageNode]:
        return self._nodes.values()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "canvas_id": self.canvas_id,
            "created_at": self.created_at,
            "root_ids": list(self._roots),
            "nodes": {nid: n.to_dict() for nid, n in self._nodes.items()},
        }

    def to_json(self, **json_kwargs) -> str:
        return json.dumps(self.to_dict(), **json_kwargs)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Canvas":
        canvas = cls(canvas_id=data["canvas_id"])
        canvas.created_at = data.get("created_at", time.time())
        for nid, nd in data.get("nodes", {}).items():
            node = MessageNode(**nd)
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

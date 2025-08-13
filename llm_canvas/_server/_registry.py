from __future__ import annotations

from llm_canvas.canvas_registry import CanvasRegistry

_local_registry: CanvasRegistry | None = None


def get_local_registry() -> CanvasRegistry:
    global _local_registry

    if _local_registry is None:
        _local_registry = CanvasRegistry()

    return _local_registry

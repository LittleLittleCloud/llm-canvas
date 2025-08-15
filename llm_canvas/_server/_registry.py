from __future__ import annotations

from typing import Union

from llm_canvas.canvas_registry import CanvasRegistry

_local_registry: Union[CanvasRegistry, None] = None


def get_local_registry() -> CanvasRegistry:
    global _local_registry  # noqa: PLW0603

    if _local_registry is None:
        _local_registry = CanvasRegistry()

    return _local_registry

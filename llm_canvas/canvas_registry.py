"""Canvas Registry for managing multiple canvas instances."""

from __future__ import annotations

import time
from typing import Union

from llm_canvas.canvas import Canvas


class CanvasRegistry:
    """Simple in-memory registry for managing Canvas instances."""

    def __init__(self) -> None:
        self._canvases: dict[str, Canvas] = {}
        self._last_updated: dict[str, float] = {}

    def add(self, canvas: Canvas) -> None:
        """Add a canvas to the registry."""
        self._canvases[canvas.canvas_id] = canvas
        self._last_updated[canvas.canvas_id] = time.time()

    def get(self, canvas_id: str) -> Union[Canvas, None]:
        """Get a canvas by ID."""
        return self._canvases.get(canvas_id)

    def list(self) -> list[Canvas]:
        """List all canvases in the registry."""
        return list(self._canvases.values())

    def remove(self, canvas_id: str) -> bool:
        """Remove a canvas from the registry.

        Returns True if removed, False if not found.
        """
        if canvas_id in self._canvases:
            del self._canvases[canvas_id]
            if canvas_id in self._last_updated:
                del self._last_updated[canvas_id]
            return True
        return False

    def touch(self, canvas_id: str) -> None:
        """Update the last_updated timestamp for a canvas."""
        if canvas_id in self._last_updated:
            self._last_updated[canvas_id] = time.time()

    def last_updated(self, canvas_id: str) -> Union[float, None]:
        """Get the last updated timestamp for a canvas."""
        return self._last_updated.get(canvas_id)

"""Shared Canvas Client - Singleton instance for all examples.

This module provides a singleton CanvasClient instance that can be shared
across all example scripts, allowing them to connect to a common canvas server.
The server must be started manually by the user.
"""

from __future__ import annotations

from llm_canvas.canvas_client import CanvasClient

# Global singleton instance
_client_instance: CanvasClient | None = None


def get_canvas_client() -> CanvasClient:
    """Get the singleton CanvasClient instance.

    Returns:
        The shared CanvasClient instance
    """
    global _client_instance  # noqa: PLW0603
    if _client_instance is None:
        _client_instance = CanvasClient()
        print("🔗 Created shared CanvasClient instance")
    return _client_instance

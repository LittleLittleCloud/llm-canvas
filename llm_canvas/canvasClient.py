"""Canvas Client - A high-level interface for managing canvases and running the server.

This module provides a simplified, one-stop solution for users to:
- Create and manage multiple canvases
- Add canvases to a registry
- Run the web UI/API server
- Handle canvas operations in a unified way
"""

from __future__ import annotations

import logging
import threading
import time
from typing import TYPE_CHECKING

from .canvas import Canvas

if TYPE_CHECKING:
    from .canvas import CanvasData, CanvasSummary

from .canvasRegistry import CanvasRegistry

logger = logging.getLogger(__name__)


class CanvasClient:
    """High-level client for managing canvases and running the server.

    This class provides a unified interface for:
    - Creating and managing multiple canvases
    - Running the web UI/API server
    - Handling canvas operations

    Example:
        client = CanvasClient()
        canvas = client.create_canvas("My Chat", "A conversation about AI")
        client.add_message(canvas.canvas_id, "Hello!", "user")
        client.run_server(background=True)
    """

    def __init__(self) -> None:
        self.registry = CanvasRegistry()
        self._server_thread: threading.Thread | None = None
        self._server_running = False

    def create_canvas(
        self,
        title: str | None = None,
        description: str | None = None,
        canvas_id: str | None = None,
    ) -> Canvas:
        """Create a new canvas and add it to the registry.

        Args:
            title: Optional title for the canvas
            description: Optional description for the canvas
            canvas_id: Optional custom canvas ID (auto-generated if not provided)

        Returns:
            The created Canvas instance
        """
        canvas = Canvas(canvas_id=canvas_id, title=title, description=description)
        self.registry.add(canvas)
        logger.info("Created canvas: %s - %s", canvas.canvas_id, canvas.title)
        return canvas

    def get_canvas(self, canvas_id: str) -> Canvas | None:
        """Get a canvas by ID.

        Args:
            canvas_id: The canvas ID to retrieve

        Returns:
            The Canvas instance if found, None otherwise
        """
        return self.registry.get(canvas_id)

    def list_canvases(self) -> list[Canvas]:
        """List all canvases in the registry.

        Returns:
            List of all Canvas instances
        """
        return self.registry.list()

    def get_canvas_summaries(self) -> list[CanvasSummary]:
        """Get summaries of all canvases.

        Returns:
            List of CanvasSummary objects
        """
        summaries = []
        for canvas in self.registry.list():
            summary = canvas.to_summary()
            # Update with registry's last_updated time
            if registry_updated := self.registry.last_updated(canvas.canvas_id):
                summary["meta"]["last_updated"] = registry_updated
            summaries.append(summary)
        return summaries

    def get_canvas_data(self, canvas_id: str) -> CanvasData | None:
        """Get canvas data in the standard format.

        Args:
            canvas_id: The canvas ID to retrieve

        Returns:
            CanvasData if found, None otherwise
        """
        canvas = self.registry.get(canvas_id)
        if not canvas:
            return None
        return canvas.to_canvas_data()

    def remove_canvas(self, canvas_id: str) -> bool:
        """Remove a canvas from the registry.

        Args:
            canvas_id: The canvas ID to remove

        Returns:
            True if removed successfully, False if not found
        """
        removed = self.registry.remove(canvas_id)
        if removed:
            logger.info("Removed canvas: %s", canvas_id)
        return removed

    def run_server(
        self,
        host: str = "127.0.0.1",
        port: int = 8000,
        background: bool = False,
    ) -> None:
        """Run the web UI/API server for all canvases in the registry.

        Args:
            host: The host to bind to (default: "127.0.0.1")
            port: The port to bind to (default: 8000)
            background: Whether to run in background (default: False)
        """
        try:
            from .server import create_app_registry
        except Exception as e:
            msg = (
                "Server components not available. "
                "Install extras: uv add 'llm-canvas[server]'"
            )
            raise RuntimeError(msg) from e

        app = create_app_registry(self.registry)

        if background:

            def run_server() -> None:
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
            time.sleep(1)  # Give server time to start
        else:
            try:
                import uvicorn

                print(f"🚀 Starting Web UI/API at http://{host}:{port}")
                print(f"Managing {len(self.registry.list())} canvas(es)")
                uvicorn.run(app, host=host, port=port)
            except ImportError:
                print("uvicorn not available - install with: uv add uvicorn")

    def wait_for_server(self) -> None:
        """Block execution until the background server stops.

        This is useful when running the server in background mode and you want
        to keep the main thread alive. Call this after run_server(background=True).
        """
        if self._server_thread is None:
            print(
                "No background server running. Use run_server(background=True) first."
            )
            return

        try:
            print("Server running in background. Press Ctrl+C to stop.")
            while self._server_running and self._server_thread.is_alive():
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nShutting down server...")
            self._server_running = False

    def is_server_running(self) -> bool:
        """Check if the background server is running.

        Returns:
            True if server is running in background, False otherwise
        """
        return self._server_running

    def __len__(self) -> int:
        """Return the number of canvases in the registry."""
        return len(self.registry.list())

    def __repr__(self) -> str:
        """Return a string representation of the client."""
        return f"CanvasClient(canvases={len(self)}, server_running={self.is_server_running()})"

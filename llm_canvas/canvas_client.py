"""Canvas Client - A high-level interface for managing canvases and running the server.

This module provides a simplified, one-stop solution for users to:
- Create and manage multiple canvases
- Add canvases to a registry
- Run the web UI/API server
- Handle canvas operations in a unified way
"""

from __future__ import annotations

import json
import logging
import threading
from typing import TYPE_CHECKING
from urllib.error import URLError
from urllib.request import Request, urlopen

from llm_canvas.types import CanvasCommitMessageEvent, CanvasUpdateMessageEvent, HealthCheckResponse

from .canvas import Canvas

if TYPE_CHECKING:
    from .canvas import CanvasData, CanvasSummary
    from .types import CanvasEvent

from .canvas_registry import CanvasRegistry

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
    """

    def __init__(self, server_host: str = "127.0.0.1", server_port: int = 8000) -> None:
        self.registry = CanvasRegistry()
        self._server_thread: threading.Thread | None = None
        self._server_running = False
        self.server_host = server_host
        self.server_port = server_port

        # Event tracking for canvases
        self._event_lock = threading.Lock()

        if not self.check_server_health():
            self._prompt_user_to_start_server()

    def _on_canvas_event(self, event: CanvasEvent) -> None:
        """Internal event handler that forwards canvas events to registered listeners and calls API endpoints."""
        # Call API endpoints for commit and update events if server is available
        if self._ensure_server_running():
            try:
                if event["event_type"] == "commit_message":
                    self._call_commit_message_api(event)
                elif event["event_type"] == "update_message":
                    self._call_update_message_api(event)
                # Ignore delete_message events for now
            except Exception:
                logger.exception("Error calling API endpoint for canvas event")

    def _call_commit_message_api(self, event: CanvasCommitMessageEvent) -> None:
        """Call the commit message API endpoint."""
        canvas_id = event["canvas_id"]

        url = f"http://{self.server_host}:{self.server_port}/api/v1/canvas/{canvas_id}/messages"

        try:
            # Use the event data directly as the request body
            json_data = json.dumps(event).encode()

            # Create the request
            req = Request(url, data=json_data, headers={"Content-Type": "application/json"})
            req.get_method = lambda: "POST"

            with urlopen(req, timeout=10) as response:
                if response.status == 200:
                    logger.debug("Successfully called commit message API for canvas %s", canvas_id)
                else:
                    logger.warning("Failed to call commit message API: HTTP %s", response.status)

        except (URLError, OSError, TimeoutError) as e:
            logger.warning("Failed to call commit message API: %s", e)

    def _call_update_message_api(self, event: CanvasUpdateMessageEvent) -> None:
        """Call the update message API endpoint."""
        canvas_id = event["canvas_id"]
        message_id = event["data"]["id"]

        url = f"http://{self.server_host}:{self.server_port}/api/v1/canvas/{canvas_id}/messages/{message_id}"

        try:
            # Use the event data directly as the request body
            json_data = json.dumps(event).encode()

            # Create the request
            req = Request(url, data=json_data, headers={"Content-Type": "application/json"})
            req.get_method = lambda: "PUT"

            with urlopen(req, timeout=10) as response:
                if response.status == 200:
                    logger.debug("Successfully called update message API for canvas %s", canvas_id)
                else:
                    logger.warning("Failed to call update message API: HTTP %s", response.status)

        except (URLError, OSError, TimeoutError) as e:
            logger.warning("Failed to call update message API: %s", e)

    def _setup_canvas_event_tracking(self, canvas: Canvas) -> None:
        """Set up event tracking for a canvas by adding our event listener."""
        canvas.add_event_listener(self._on_canvas_event)

    def check_server_health(self) -> bool:
        """Check if the server is running and healthy.

        Returns:
            True if server is running and healthy, False otherwise
        """
        try:
            from urllib.error import URLError
            from urllib.request import urlopen

            url = f"http://{self.server_host}:{self.server_port}/api/v1/health"
            # Security: Ensure we only allow http/https schemes
            if not url.startswith(("http://", "https://")):
                return False

            with urlopen(url, timeout=2) as response:
                if response.status == 200:  # noqa: PLR2004
                    import json

                    data: HealthCheckResponse = json.loads(response.read().decode())
                    return data["status"] == "healthy"
                return False

        except (URLError, OSError, TimeoutError):
            # Any exception means server is not reachable
            return False

    def _prompt_user_to_start_server(self) -> None:
        """Prompt user to start the server manually."""
        print("❌ Canvas server is not running!")
        print("\n📋 To start the local canvas server, run one of these commands:")
        print(f"   llm-canvas server --host {self.server_host} --port {self.server_port}")
        print("   llm-canvas server  # (uses default host and port)")
        print("\n📖 For more information, see: doc/start_canvas_server.md")
        print(f"\n🌐 Once started, the server will be available at: http://{self.server_host}:{self.server_port}")

    def _ensure_server_running(self) -> bool:
        """Ensure server is running, prompt user if not.

        Returns:
            True if server is running, False if user needs to start it manually
        """
        if self.check_server_health():
            return True

        self._prompt_user_to_start_server()
        return False

    def create_canvas(
        self,
        title: str | None = None,
        description: str | None = None,
    ) -> Canvas:
        """Create a new canvas and add it to the registry.

        Args:
            title: Optional title for the canvas
            description: Optional description for the canvas

        Returns:
            The created Canvas instance

        Raises:
            RuntimeError: If server is not running and user needs to start it manually
        """
        if not self._ensure_server_running():
            error_msg = "Canvas server is not running. Please start the server manually using 'llm-canvas server'."
            raise RuntimeError(error_msg)

        # Call API to create canvas
        url = f"http://{self.server_host}:{self.server_port}/api/v1/canvas"
        request_data = {}
        if title is not None:
            request_data["title"] = title
        if description is not None:
            request_data["description"] = description

        try:
            req = Request(
                url, data=json.dumps(request_data).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST"
            )

            with urlopen(req, timeout=10) as response:
                if response.status == 200:
                    response_data = json.loads(response.read().decode())
                    created_canvas_id = response_data["canvas_id"]

                    # Fetch the full canvas data
                    canvas = self.get_canvas(created_canvas_id)
                    if canvas:
                        logger.info("Created canvas via API: %s - %s", created_canvas_id, title)
                        return canvas

                    msg = f"Failed to retrieve created canvas {created_canvas_id}"
                    raise RuntimeError(msg)

                msg = f"Failed to create canvas: HTTP {response.status}"
                raise RuntimeError(msg)

        except (URLError, OSError, TimeoutError) as e:
            msg = f"Failed to create canvas via API: {e}"
            raise RuntimeError(msg) from e

    def get_canvas(self, canvas_id: str) -> Canvas | None:
        """Get a canvas by ID.

        Args:
            canvas_id: The canvas ID to retrieve

        Returns:
            The Canvas instance if found, None otherwise
        """
        # Call API to get canvas
        url = f"http://{self.server_host}:{self.server_port}/api/v1/canvas?canvas_id={canvas_id}"

        try:
            with urlopen(url, timeout=10) as response:
                if response.status == 200:
                    canvas_data = json.loads(response.read().decode())
                    # Convert API response to Canvas object
                    canvas = Canvas.from_canvas_data(canvas_data)
                    self._setup_canvas_event_tracking(canvas)
                    return canvas
                if response.status == 404:
                    return None
                logger.warning("Failed to get canvas %s: HTTP %s", canvas_id, response.status)
                return None

        except (URLError, OSError, TimeoutError) as e:
            logger.warning("Failed to get canvas %s via API: %s", canvas_id, e)
            return None

    def list_canvases(self) -> list[Canvas]:
        """List all canvases in the registry.

        Returns:
            List of all Canvas instances
        """
        if not self._ensure_server_running():
            return self.registry.list()

        # Call API to get canvas list and then fetch each canvas
        url = f"http://{self.server_host}:{self.server_port}/api/v1/canvas/list"

        try:
            with urlopen(url, timeout=10) as response:
                if response.status == 200:
                    response_data = json.loads(response.read().decode())
                    canvases = []
                    for summary in response_data["canvases"]:
                        canvas = self.get_canvas(summary["canvas_id"])
                        if canvas:
                            canvases.append(canvas)
                    return canvases
                logger.warning("Failed to list canvases: HTTP %s", response.status)
                return []

        except (URLError, OSError, TimeoutError) as e:
            logger.warning("Failed to list canvases via API: %s", e)
            return []

    def get_canvas_summaries(self) -> list[CanvasSummary]:
        """Get summaries of all canvases.

        Returns:
            List of CanvasSummary objects
        """
        if not self._ensure_server_running():
            summaries = []
            for canvas in self.registry.list():
                summary = canvas.to_summary()
                # Update with registry's last_updated time
                if registry_updated := self.registry.last_updated(canvas.canvas_id):
                    summary["meta"]["last_updated"] = registry_updated
                summaries.append(summary)
            return summaries

        # Call API to get canvas summaries
        url = f"http://{self.server_host}:{self.server_port}/api/v1/canvas/list"

        try:
            with urlopen(url, timeout=10) as response:
                if response.status == 200:
                    response_data = json.loads(response.read().decode())
                    return response_data["canvases"]  # type: ignore[no-any-return]
                logger.warning("Failed to get canvas summaries: HTTP %s", response.status)
                return []

        except (URLError, OSError, TimeoutError) as e:
            logger.warning("Failed to get canvas summaries via API: %s", e)
            return []

    def get_canvas_data(self, canvas_id: str) -> CanvasData | None:
        """Get canvas data in the standard format.

        Args:
            canvas_id: The canvas ID to retrieve

        Returns:
            CanvasData if found, None otherwise
        """
        if not self._ensure_server_running():
            canvas = self.registry.get(canvas_id)
            if not canvas:
                return None
            return canvas.to_canvas_data()

        # Call API to get canvas data
        url = f"http://{self.server_host}:{self.server_port}/api/v1/canvas?canvas_id={canvas_id}"

        try:
            with urlopen(url, timeout=10) as response:
                if response.status == 200:
                    return json.loads(response.read().decode())  # type: ignore[no-any-return]
                if response.status == 404:
                    return None
                logger.warning("Failed to get canvas data %s: HTTP %s", canvas_id, response.status)
                return None

        except (URLError, OSError, TimeoutError) as e:
            logger.warning("Failed to get canvas data %s via API: %s", canvas_id, e)
            return None

    def remove_canvas(self, canvas_id: str) -> bool:
        """Remove a canvas from the registry.

        Args:
            canvas_id: The canvas ID to remove

        Returns:
            True if removed successfully, False if not found
        """
        if not self._ensure_server_running():
            removed = self.registry.remove(canvas_id)
            if removed:
                logger.info("Removed canvas: %s", canvas_id)
            return removed

        # Call API to delete canvas
        url = f"http://{self.server_host}:{self.server_port}/api/v1/canvas/{canvas_id}"

        try:
            req = Request(url, method="DELETE")
            with urlopen(req, timeout=10) as response:
                if response.status == 200:
                    logger.info("Removed canvas via API: %s", canvas_id)
                    return True
                if response.status == 404:
                    return False
                logger.warning("Failed to remove canvas %s: HTTP %s", canvas_id, response.status)
                return False

        except (URLError, OSError, TimeoutError) as e:
            logger.warning("Failed to remove canvas %s via API: %s", canvas_id, e)
            return False

    def __len__(self) -> int:
        """Return the number of canvases in the registry."""
        return len(self.registry.list())

    def __repr__(self) -> str:
        """Return a string representation of the client."""
        return f"CanvasClient(canvases={len(self)})"

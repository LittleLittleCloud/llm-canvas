"""Canvas Client - A high-level interface for managing canvases and running the server.

This module provides a simplified, one-stop solution for users to:
- Create and manage multiple canvases
- Add canvases to a registry
- Run the web UI/API server
- Handle canvas operations in a unified way
"""

# ruff: noqa: BLE001
# ruff: noqa: TRY301, TRY300

from __future__ import annotations

import logging
import threading
from typing import Union

from httpx import Timeout

from llm_canvas.canvas_registry import CanvasRegistry
from llm_canvas.types import CanvasCommitMessageEvent, CanvasEvent, CanvasUpdateMessageEvent
from llm_canvas_generated_client.llm_canvas_api_client import Client
from llm_canvas_generated_client.llm_canvas_api_client.api.v1 import (
    commit_message_api_v1_canvas_canvas_id_messages_post as commit_message_api,
)
from llm_canvas_generated_client.llm_canvas_api_client.api.v1 import (
    create_canvas_api_v1_canvas_post as create_canvas_api,
)
from llm_canvas_generated_client.llm_canvas_api_client.api.v1 import (
    delete_canvas_api_v1_canvas_canvas_id_delete as delete_canvas_api,
)
from llm_canvas_generated_client.llm_canvas_api_client.api.v1 import (
    get_canvas_api_v1_canvas_get as get_canvas_api,
)
from llm_canvas_generated_client.llm_canvas_api_client.api.v1 import (
    health_check_api_v1_health_get as health_check_api,
)
from llm_canvas_generated_client.llm_canvas_api_client.api.v1 import (
    list_canvases_api_v1_canvas_list_get as list_canvases_api,
)
from llm_canvas_generated_client.llm_canvas_api_client.api.v1 import (
    update_message_api_v1_canvas_canvas_id_messages_message_id_put as update_message_api,
)
from llm_canvas_generated_client.llm_canvas_api_client.models.canvas_commit_message_event import (
    CanvasCommitMessageEvent as GeneratedCanvasCommitMessageEvent,
)
from llm_canvas_generated_client.llm_canvas_api_client.models.canvas_update_message_event import (
    CanvasUpdateMessageEvent as GeneratedCanvasUpdateMessageEvent,
)
from llm_canvas_generated_client.llm_canvas_api_client.models.commit_message_request import (
    CommitMessageRequest,
)
from llm_canvas_generated_client.llm_canvas_api_client.models.create_canvas_request import CreateCanvasRequest
from llm_canvas_generated_client.llm_canvas_api_client.models.create_canvas_response import CreateCanvasResponse
from llm_canvas_generated_client.llm_canvas_api_client.models.http_validation_error import HTTPValidationError
from llm_canvas_generated_client.llm_canvas_api_client.models.update_message_request import UpdateMessageRequest

from .canvas import Canvas, CanvasData, CanvasSummary

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
        self._server_thread: Union[threading.Thread, None] = None
        self._server_running = False
        self.server_host = server_host
        self.server_port = server_port
        # Initialize the API client
        base_url = f"http://{server_host}:{server_port}"
        self._api_client = Client(base_url=base_url, timeout=Timeout(10.0))

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

        try:
            request = CommitMessageRequest(data=GeneratedCanvasCommitMessageEvent.from_dict(event))
            response = commit_message_api.sync(canvas_id=canvas_id, client=self._api_client, body=request)

            if response:
                logger.debug("Successfully called commit message API for canvas %s", canvas_id)
            else:
                logger.warning("Failed to call commit message API")

        except Exception as e:
            logger.warning("Failed to call commit message API: %s", e)

    def _call_update_message_api(self, event: CanvasUpdateMessageEvent) -> None:
        """Call the update message API endpoint."""
        canvas_id = event["canvas_id"]
        message_id = event["data"]["id"]

        try:
            request = UpdateMessageRequest(GeneratedCanvasUpdateMessageEvent.from_dict(event))
            response = update_message_api.sync(
                canvas_id=canvas_id, message_id=message_id, client=self._api_client, body=request
            )

            if response:
                logger.debug("Successfully called update message API for canvas %s", canvas_id)
            else:
                logger.warning("Failed to call update message API")

        except Exception as e:
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
            response = health_check_api.sync(client=self._api_client)
        except Exception:
            # Any exception means server is not reachable
            return False
        else:
            return response is not None and response.status == "healthy"

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
        title: Union[str, None] = None,
        description: Union[str, None] = None,
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
        try:
            request = CreateCanvasRequest(title=title, description=description)
            response = create_canvas_api.sync(client=self._api_client, body=request)

            if isinstance(response, CreateCanvasResponse):
                created_canvas_id = response.canvas_id

                # Fetch the full canvas data
                canvas = self.get_canvas(created_canvas_id)
                if canvas:
                    logger.info("Created canvas via API: %s - %s", created_canvas_id, title)
                    return canvas

                msg = f"Failed to retrieve created canvas {created_canvas_id}"
                raise RuntimeError(msg)

            msg = "Failed to create canvas: No response from API"
            raise RuntimeError(msg)

        except Exception as e:
            msg = f"Failed to create canvas via API: {e}"
            raise RuntimeError(msg) from e

    def get_canvas(self, canvas_id: str) -> Union[Canvas, None]:
        """Get a canvas by ID.

        Args:
            canvas_id: The canvas ID to retrieve

        Returns:
            The Canvas instance if found, None otherwise
        """
        # Call API to get canvas
        try:
            canvas_data_response = get_canvas_api.sync(client=self._api_client, canvas_id=canvas_id)

            if not isinstance(canvas_data_response, HTTPValidationError) and canvas_data_response is not None:
                # Convert API response to Canvas object
                canvas = Canvas.from_canvas_data(
                    CanvasData(
                        title=canvas_data_response.data.title,
                        description=canvas_data_response.data.description,
                        created_at=canvas_data_response.data.created_at,
                        last_updated=canvas_data_response.data.last_updated,
                        nodes=canvas_data_response.data.nodes.to_dict(),
                        canvas_id=canvas_data_response.data.canvas_id,
                    )
                )
                self._setup_canvas_event_tracking(canvas)
                return canvas
            return None

        except Exception as e:
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
        try:
            response = list_canvases_api.sync(client=self._api_client)

            if response:
                canvases = []
                for summary in response.canvases:
                    canvas = self.get_canvas(summary.canvas_id)
                    if canvas:
                        canvases.append(canvas)
                return canvases
            logger.warning("Failed to list canvases: No response from API")
            return []

        except Exception as e:
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
        try:
            response = list_canvases_api.sync(client=self._api_client)

            if response:
                return [
                    {
                        "canvas_id": c.canvas_id,
                        "created_at": c.created_at,
                        "root_ids": c.root_ids,
                        "node_count": c.node_count,
                        "title": c.title,
                        "description": c.description,
                        "meta": c.meta.to_dict() if c.meta else {},
                    }
                    for c in response.canvases
                ]
            logger.warning("Failed to get canvas summaries: No response from API")
            return []

        except Exception as e:
            logger.warning("Failed to get canvas summaries via API: %s", e)
            return []

    def get_canvas_data(self, canvas_id: str) -> Union[CanvasData, None]:
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
        try:
            canvas_data_response = get_canvas_api.sync(client=self._api_client, canvas_id=canvas_id)
            if not isinstance(canvas_data_response, HTTPValidationError) and canvas_data_response is not None:
                return CanvasData(
                    canvas_id=canvas_data_response.data.canvas_id,
                    title=canvas_data_response.data.title,
                    description=canvas_data_response.data.description,
                    created_at=canvas_data_response.data.created_at,
                    last_updated=canvas_data_response.data.last_updated,
                    nodes=canvas_data_response.data.nodes.to_dict(),
                )
            return None

        except Exception as e:
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
        try:
            response = delete_canvas_api.sync(canvas_id=canvas_id, client=self._api_client)

            if response:
                logger.info("Removed canvas via API: %s", canvas_id)
                return True
            return False

        except Exception as e:
            logger.warning("Failed to remove canvas %s via API: %s", canvas_id, e)
            return False

    def __len__(self) -> int:
        """Return the number of canvases in the registry."""
        return len(self.registry.list())

    def __repr__(self) -> str:
        """Return a string representation of the client."""
        return f"CanvasClient(canvases={len(self)})"

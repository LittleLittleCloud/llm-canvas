from __future__ import annotations

import logging
import threading
import time
import uuid
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from collections.abc import Iterable

from .types import (
    BranchInfo,
    CanvasCommitMessageEvent,
    CanvasData,
    CanvasEvent,
    CanvasSummary,
    CanvasUpdateMessageEvent,
    Message,
    MessageNode,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

        # Branch management
        self._branches: dict[str, BranchInfo] = {}
        self._current_branch = "main"
        self._initialize_main_branch()

        # Event system
        self._event_listeners: list[Callable[[CanvasEvent], None]] = []
        self._event_lock = threading.Lock()

    def _initialize_main_branch(self) -> None:
        """Initialize the main branch."""
        self._branches["main"] = {
            "name": "main",
            "description": "Main conversation thread",
            "head_node_id": None,
            "created_at": self.created_at,
        }

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
    def commit_message(self, message: Message, meta: dict[str, Any] | None = None) -> MessageNode:
        """
        Commit a message to the current branch HEAD.

        Args:
            message: The message to commit
            meta: Optional metadata for the message

        Returns:
            The created MessageNode
        """
        current_branch = self._branches[self._current_branch]
        parent_node = None

        # Get the current HEAD node if it exists
        if current_branch["head_node_id"]:
            parent_node = self._nodes[current_branch["head_node_id"]]

        # Add the message using the existing add_message method
        node = self._add_message(message, parent_node["id"] if parent_node else None, meta)

        # Update the current branch HEAD
        current_branch["head_node_id"] = node["id"]

        return node

    def checkout(
        self,
        name: str,
        description: str | None = None,
        create_if_not_exists: bool = False,
        commit_message: MessageNode | None = None,
    ) -> None:
        """
        Switch to a branch, optionally creating it if it doesn't exist.

        Args:
            name: Branch name to switch to
            description: Description for new branch (if creating)
            create_if_not_exists: Whether to create the branch if it doesn't exist
            commit_message: Starting point for new branch (defaults to current HEAD)
        """
        if name not in self._branches:
            if not create_if_not_exists:
                raise ValueError(f"Branch '{name}' does not exist")

            # Determine the starting point for the new branch
            head_node_id = None
            if commit_message:
                head_node_id = commit_message["id"]
            elif self._current_branch in self._branches:
                head_node_id = self._branches[self._current_branch]["head_node_id"]

            # Create the new branch
            self._branches[name] = {
                "name": name,
                "description": description or f"Branch {name}",
                "head_node_id": head_node_id,
                "created_at": time.time(),
            }

        # Switch to the branch
        self._current_branch = name

    def list_branches(self) -> list[BranchInfo]:
        """
        List all branches with their latest commit information.

        Returns:
            List of branch information including name and latest commit
        """
        branches = []
        for branch in self._branches.values():
            branches.append(branch)

        return branches

    def delete_branch(self, name: str) -> None:
        """
        Delete a branch.

        Args:
            name: Name of the branch to delete

        Raises:
            ValueError: If trying to delete the main branch or current branch
        """
        if name == self._current_branch:
            raise ValueError("Cannot delete the current branch. Switch to another branch first.")

        if name not in self._branches:
            raise ValueError(f"Branch '{name}' does not exist")

        del self._branches[name]

    def get_current_branch(self) -> str:
        """Get the name of the current branch."""
        return self._current_branch

    def get_head_node(self, branch_name: str | None = None) -> MessageNode | None:
        """
        Get the HEAD node of a branch.

        Args:
            branch_name: Branch name (defaults to current branch)

        Returns:
            The HEAD MessageNode or None if no HEAD exists
        """
        branch_name = branch_name or self._current_branch
        if branch_name not in self._branches:
            raise ValueError(f"Branch '{branch_name}' does not exist")

        branch = self._branches[branch_name]
        if branch["head_node_id"]:
            return self._nodes.get(branch["head_node_id"])
        return None

    def _add_message(
        self,
        message: Message,
        parent_node_id: str | None = None,
        meta: dict[str, Any] | None = None,
        node_id: str | None = None,
    ) -> MessageNode:
        node_id = node_id or str(uuid.uuid4())
        _meta = {"timestamp": time.time()}

        if meta is not None:
            _meta.update(meta)
        node: MessageNode = {
            "id": node_id,
            "message": message,
            "parent_id": parent_node_id if parent_node_id else None,
            "child_ids": [],
            "meta": _meta,
        }
        self._nodes[node_id] = node
        if parent_node_id:
            self._nodes[parent_node_id]["child_ids"].append(node_id)
            self.update_message(parent_node_id, self._nodes[parent_node_id])
        else:
            self._roots.append(node_id)

        # Emit SSE event
        event: CanvasCommitMessageEvent = {
            "event_type": "commit_message",
            "canvas_id": self.canvas_id,
            "timestamp": time.time(),
            "data": node,
        }
        self._emit_event(event)

        return node

    def update_message(self, node_id: str, updated_message_node: MessageNode) -> MessageNode:
        """
        Update an existing message in the canvas.

        Args:
            node_id: The ID of the message node to update
            message: The new message content
            meta: Optional metadata to update (will be merged with existing meta)

        Returns:
            The updated MessageNode

        Raises:
            ValueError: If the node with the given ID doesn't exist
        """
        if node_id not in self._nodes:
            raise ValueError(f"Node with ID '{node_id}' does not exist")

        self._nodes[node_id] = updated_message_node

        # Emit update event
        event: CanvasUpdateMessageEvent = {
            "event_type": "update_message",
            "canvas_id": self.canvas_id,
            "timestamp": time.time(),
            "data": self._nodes[node_id],
        }
        self._emit_event(event)

        return self._nodes[node_id]

    @property
    def nodes(self) -> dict[str, MessageNode]:
        """Get all nodes in the canvas."""
        return self._nodes

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

    @classmethod
    def from_canvas_data(cls, data: CanvasData) -> Canvas:
        """Create a Canvas instance from CanvasData."""
        canvas = cls(
            canvas_id=data["canvas_id"],
            title=data.get("title"),
            description=data.get("description"),
        )

        # Set the creation time from the data
        canvas.created_at = data["created_at"]

        # Load all nodes
        canvas._nodes = dict(data["nodes"])

        # Set root node IDs
        canvas._roots = list(data["root_ids"])

        return canvas

from __future__ import annotations

import logging
import threading
import time
import uuid
from collections.abc import Iterable
from typing import Any, Callable, Union

from llm_canvas.types import (
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


class Branch:
    """Represents a branch within a canvas for linear chat history."""

    def __init__(self, canvas: Canvas, branch_info: BranchInfo) -> None:
        self._canvas = canvas
        self._branch_info = branch_info

    @property
    def name(self) -> str:
        """Get the branch name."""
        return self._branch_info["name"]

    @property
    def description(self) -> Union[str, None]:
        """Get the branch description."""
        return self._branch_info["description"]

    @property
    def branch_info(self) -> BranchInfo:
        """Get the branch information."""
        return self._branch_info

    @property
    def head_node_id(self) -> Union[str, None]:
        """Get the HEAD node ID of this branch."""
        return self._branch_info["head_node_id"]

    def commit_message(self, message: Message, meta: Union[dict[str, Any], None] = None) -> MessageNode:
        """
        Commit a message to this branch.

        Args:
            message: The message to commit
            meta: Optional metadata for the message

        Returns:
            The created MessageNode
        """
        parent_node = None

        # Get the current HEAD node if it exists
        if self._branch_info["head_node_id"]:
            parent_node = self._canvas.get_node(self._branch_info["head_node_id"])

        # Add the message using the canvas's internal method
        node = self._canvas.add_message(message, parent_node["id"] if parent_node else None, meta)

        # Update this branch's HEAD
        self._branch_info["head_node_id"] = node["id"]

        return node

    def update_message(self, node_id: str, updated_message_node: MessageNode) -> MessageNode:
        """
        Update an existing message in this branch.

        Args:
            node_id: The ID of the message node to update
            updated_message_node: The updated message node

        Returns:
            The updated MessageNode

        Raises:
            ValueError: If the node with the given ID doesn't exist
        """
        return self._canvas.update_message(node_id, updated_message_node)

    def get_head_node(self) -> Union[MessageNode, None]:
        """
        Get the HEAD node of this branch.

        Returns:
            The HEAD MessageNode or None if no HEAD exists
        """
        if self._branch_info["head_node_id"]:
            return self._canvas.get_node(self._branch_info["head_node_id"])
        return None

    def merge_from(
        self,
        source_branch_names: Union[str, list[str]],
        merge_message: Message,
    ) -> MessageNode:
        """
        Merge one or more branches into this branch.

        Args:
            source_branch_names: Name(s) of the branch(es) to merge from (string or list of strings)
            merge_message: Merge commit message (required)

        Returns:
            The merge commit MessageNode
        """
        return self._canvas.merge(
            source_branch_names=source_branch_names,
            merge_message=merge_message,
            target_branch_name=self.name,
        )


class Canvas:
    """Represents a DAG of message nodes (LLM conversation branches)."""

    def __init__(
        self,
        canvas_id: Union[str, None] = None,
        title: Union[str, None] = None,
        description: Union[str, None] = None,
    ) -> None:
        self.canvas_id = canvas_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.created_at = time.time()
        self._nodes: dict[str, MessageNode] = {}

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
            listener(event)

    # ---- Public API ----
    def commit_message(self, message: Message, meta: Union[dict[str, Any], None] = None) -> MessageNode:
        """
        DEPRECATED: Use branch.commit_message() instead.
        Commit a message to the current branch HEAD.

        Args:
            message: The message to commit
            meta: Optional metadata for the message

        Returns:
            The created MessageNode
        """
        logger.warning("Canvas.commit_message() is deprecated. Use branch.commit_message() instead.")
        current_branch = self.checkout(name=self._current_branch)
        return current_branch.commit_message(message, meta)

    def checkout(
        self,
        name: Union[str, None] = None,
        description: Union[str, None] = None,
        create_if_not_exists: bool = False,
        commit_message: Union[MessageNode, None] = None,
    ) -> Branch:
        """
        Switch to a branch or checkout a specific message (detached head).

        Args:
            name: Branch name to switch to (None for detached head when commit_message is provided)
            description: Description for new branch (if creating)
            create_if_not_exists: Whether to create the branch if it doesn't exist
            commit_message: MessageNode to checkout or starting point for new branch

        Returns:
            Branch object for the checked out branch

        Examples:
            # Checkout to a branch
            branch = canvas.checkout(name="main")

            # Create a new branch from current HEAD
            branch = canvas.checkout(name="feature", create_if_not_exists=True)

            # Create a new branch from a specific message
            branch = canvas.checkout(name="feature", commit_message=some_message, create_if_not_exists=True)

            # Checkout to a specific message (detached head)
            branch = canvas.checkout(commit_message=some_message)
        """
        # Handle detached head checkout (when commit_message is provided without name)
        if commit_message and not name:
            message_id = commit_message["id"]
            if message_id not in self._nodes:
                raise ValueError(f"Message with ID '{message_id}' does not exist")

            # Create a temporary branch info for detached head
            detached_branch_info: BranchInfo = {
                "name": f"detached-{message_id[:8]}",
                "description": f"Detached HEAD at {message_id}",
                "head_node_id": message_id,
                "created_at": time.time(),
            }
            return Branch(self, detached_branch_info)

        # Handle regular branch checkout
        if not name:
            raise ValueError("Either name or commit_message must be provided")

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

        # Return a Branch object
        return Branch(self, self._branches[name])

    def list_branches(self) -> list[BranchInfo]:
        """
        List all branches with their latest commit information.

        Returns:
            List of branch information including name and latest commit
        """
        return list(self._branches.values())

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

    def merge(
        self,
        source_branch_names: Union[str, list[str]],
        merge_message: Message,
        target_branch_name: str,
    ) -> MessageNode:
        """
        Merge one or more branches into another using explicit merge strategy.

        Args:
            source_branch_names: Name(s) of the branch(es) to merge from (string or list of strings)
            merge_message: Merge commit message (required)
            target_branch_name: Name of the branch to merge into (required)

        Returns:
            The merge commit MessageNode

        Raises:
            ValueError: If branches don't exist or merge is not possible

        The merge creates an explicit merge commit that references all source branches,
        preserving the full conversation history and branch structure.
        """
        # Normalize source_branch_names to a list
        if isinstance(source_branch_names, str):
            source_branch_names = [source_branch_names]

        if not source_branch_names:
            raise ValueError("At least one source branch must be specified")

        # Validate all source branches
        for source_branch_name in source_branch_names:
            if source_branch_name not in self._branches:
                raise ValueError(f"Source branch '{source_branch_name}' does not exist")

        # Validate target branch
        if target_branch_name not in self._branches:
            raise ValueError(f"Target branch '{target_branch_name}' does not exist")

        # Get target branch
        target_branch = self._branches[target_branch_name]
        target_head_id = target_branch["head_node_id"]

        # Collect source branch information
        source_branches = []
        source_head_ids = []

        for source_branch_name in source_branch_names:
            source_branch = self._branches[source_branch_name]
            source_head_id = source_branch["head_node_id"]

            if not source_head_id:
                raise ValueError(f"Source branch '{source_branch_name}' has no commits")

            source_branches.append(source_branch)
            source_head_ids.append(source_head_id)

        # Create explicit merge commit that references all branches
        merge_node = self.add_message(
            message=merge_message,
            parent_node_id=target_head_id,
        )

        # Add all source HEADs as additional parents (for visualization)
        for source_head_id in source_head_ids:
            if source_head_id and source_head_id in self._nodes:
                source_node = self._nodes[source_head_id]
                if merge_node["id"] not in source_node["child_ids"]:
                    source_node["child_ids"].append(merge_node["id"])
                    self.update_message(source_head_id, source_node)

        # Update target branch HEAD
        target_branch["head_node_id"] = merge_node["id"]

        return merge_node

    def add_message(
        self,
        message: Message,
        parent_node_id: Union[str, None] = None,
        meta: Union[dict[str, Any], None] = None,
        node_id: Union[str, None] = None,
    ) -> MessageNode:
        node_id = node_id or str(uuid.uuid4())
        _meta = {"timestamp": time.time()}

        if meta is not None:
            _meta.update(meta)
        node: MessageNode = MessageNode(
            id=node_id,
            message=message,
            parent_id=parent_node_id if parent_node_id else None,
            child_ids=[],
            meta=_meta,
        )
        self._nodes[node_id] = node
        if parent_node_id:
            self._nodes[parent_node_id]["child_ids"].append(node_id)
            self.update_message(parent_node_id, self._nodes[parent_node_id])

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

    def get_node(self, node_id: str) -> Union[MessageNode, None]:
        return self._nodes.get(node_id)

    def iter_nodes(self) -> Iterable[MessageNode]:
        return self._nodes.values()

    def to_summary(self) -> CanvasSummary:
        """Create a summary representation of the canvas."""

        # find all root nodes
        # a root node is a node that has no parent
        root_ids = [node_id for node_id, node in self._nodes.items() if node["parent_id"] is None]
        return {
            "canvas_id": self.canvas_id,
            "created_at": self.created_at,
            "root_ids": root_ids,
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

        return canvas

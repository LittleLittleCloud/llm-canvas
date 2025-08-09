"""Tests for Canvas API implementation."""

import pytest

from llm_canvas import canvas_client
from llm_canvas.canvas import Canvas


class TestCanvasAPI:
    """Test suite for Canvas API functionality."""

    @pytest.fixture
    def canvas(self) -> Canvas:
        """Create a test canvas."""
        return canvas_client.create_canvas(title="Test Canvas", description="A canvas for testing the API")

    def test_create_canvas(self, canvas: Canvas) -> None:
        """Test canvas creation."""
        assert canvas.canvas_id is not None
        assert canvas.title == "Test Canvas"
        assert canvas.description == "A canvas for testing the API"
        assert canvas.get_current_branch() == "main"

    def test_commit_message(self, canvas: Canvas) -> None:
        """Test committing messages to canvas."""
        # Add user message
        user_msg = canvas.commit_message({"content": "Hello, world!", "role": "user"})
        assert user_msg["id"] is not None
        assert user_msg["message"]["content"] == "Hello, world!"
        assert user_msg["message"]["role"] == "user"

        # Add assistant message
        assistant_msg = canvas.commit_message({"content": "Hello! How can I help you today?", "role": "assistant"})
        assert assistant_msg["id"] is not None
        assert assistant_msg["message"]["content"] == "Hello! How can I help you today?"
        assert assistant_msg["message"]["role"] == "assistant"

        # Verify parent-child relationship
        assert assistant_msg["parent_id"] == user_msg["id"]

    def test_list_branches(self, canvas: Canvas) -> None:
        """Test listing branches."""
        # Initially should have only main branch
        branches = canvas.list_branches()
        assert len(branches) == 1
        assert branches[0]["name"] == "main"
        assert branches[0]["description"] == "Main conversation thread"

    def test_checkout_existing_branch(self, canvas: Canvas) -> None:
        """Test checking out to existing branch."""
        canvas.checkout("main")
        assert canvas.get_current_branch() == "main"

    def test_checkout_new_branch(self, canvas: Canvas) -> None:
        """Test creating and checking out new branch."""
        canvas.checkout(name="Alternative Path", description="Testing alternative conversation path", create_if_not_exists=True)
        assert canvas.get_current_branch() == "Alternative Path"

        # Verify branch was created
        branches = canvas.list_branches()
        branch_names = [b["name"] for b in branches]
        assert "Alternative Path" in branch_names

    def test_checkout_nonexistent_branch_without_create(self, canvas: Canvas) -> None:
        """Test checking out to non-existent branch without create flag."""
        with pytest.raises(ValueError, match="Branch 'nonexistent' does not exist"):
            canvas.checkout("nonexistent")

    def test_branch_from_specific_message(self, canvas: Canvas) -> None:
        """Test creating branch from specific message."""
        # Add a message to main
        user_msg = canvas.commit_message({"content": "Hello, main branch!", "role": "user"})

        # Create branch from that message
        canvas.checkout(
            name="From Hello",
            description="Branch starting from the hello message",
            create_if_not_exists=True,
            commit_message=user_msg,
        )

        # Verify we're on the new branch
        assert canvas.get_current_branch() == "From Hello"

        # Verify HEAD is the specified message
        head = canvas.get_head_node()
        assert head is not None
        assert head["id"] == user_msg["id"]

    def test_head_operations(self, canvas: Canvas) -> None:
        """Test HEAD node operations."""
        # Initially no HEAD
        head = canvas.get_head_node()
        assert head is None

        # Add message and check HEAD
        msg = canvas.commit_message({"content": "First message", "role": "user"})
        head = canvas.get_head_node()
        assert head is not None
        assert head["id"] == msg["id"]

        # Test getting HEAD of specific branch
        main_head = canvas.get_head_node("main")
        assert main_head is not None
        assert main_head["id"] == msg["id"]

    def test_head_operations_invalid_branch(self, canvas: Canvas) -> None:
        """Test HEAD operations with invalid branch."""
        with pytest.raises(ValueError, match="Branch 'invalid' does not exist"):
            canvas.get_head_node("invalid")

    def test_delete_branch(self, canvas: Canvas) -> None:
        """Test branch deletion."""
        # Create a branch to delete
        canvas.checkout(name="To Delete", description="Branch to be deleted", create_if_not_exists=True)

        # Switch back to main
        canvas.checkout("main")

        # Delete the branch
        canvas.delete_branch("To Delete")

        # Verify it's gone
        branches = canvas.list_branches()
        branch_names = [b["name"] for b in branches]
        assert "To Delete" not in branch_names

    def test_cannot_delete_current_branch(self, canvas: Canvas) -> None:
        """Test that current branch cannot be deleted."""
        with pytest.raises(ValueError, match="Cannot delete the current branch"):
            canvas.delete_branch("main")

    def test_cannot_delete_nonexistent_branch(self, canvas: Canvas) -> None:
        """Test deleting non-existent branch raises error."""
        with pytest.raises(ValueError, match="Branch 'nonexistent' does not exist"):
            canvas.delete_branch("nonexistent")

    def test_complex_branching_scenario(self, canvas: Canvas) -> None:
        """Test complex branching scenario with multiple branches and messages."""
        # Add initial message to main
        hello_main = canvas.commit_message({"content": "Hello, main branch!", "role": "user"})

        # Create alternative path
        canvas.checkout(name="Alternative Path", description="Exploring different responses", create_if_not_exists=True)
        canvas.commit_message({"content": "Hello, alternative branch!", "role": "user"})

        # Create branch from specific message
        canvas.checkout(
            name="Branch from Hello",
            description="New path from the hello message",
            create_if_not_exists=True,
            commit_message=hello_main,
        )
        canvas.commit_message({"content": "This is a different direction!", "role": "user"})

        # Verify all branches exist
        branches = canvas.list_branches()
        branch_names = [b["name"] for b in branches]
        assert "main" in branch_names
        assert "Alternative Path" in branch_names
        assert "Branch from Hello" in branch_names
        assert len(branches) == 3

        # Verify each branch has the expected latest message
        for branch in branches:
            assert branch["head_node_id"] is not None
            head_node_message = canvas.get_head_node(branch["name"])
            assert head_node_message is not None
            if branch["name"] == "main":
                assert head_node_message["message"]["content"] == "Hello, main branch!"
            elif branch["name"] == "Alternative Path":
                assert head_node_message["message"]["content"] == "Hello, alternative branch!"
            elif branch["name"] == "Branch from Hello":
                assert head_node_message["message"]["content"] == "This is a different direction!"

    def test_message_metadata(self, canvas: Canvas) -> None:
        """Test message metadata handling."""
        custom_meta = {"custom_field": "value", "priority": "high"}
        msg = canvas.commit_message({"content": "Message with metadata", "role": "user"}, meta=custom_meta)

        # Check that custom metadata is preserved along with timestamp
        assert msg["meta"] is not None
        assert "timestamp" in msg["meta"]
        assert msg["meta"]["custom_field"] == "value"
        assert msg["meta"]["priority"] == "high"

    def test_update_message(self, canvas: Canvas) -> None:
        """Test updating existing messages."""
        # Create a message to update
        original_msg = canvas.commit_message({"content": "Original content", "role": "user"})
        original_id = original_msg["id"]

        # Update the message content
        updated_msg = canvas.update_message(original_id, {"content": "Updated content", "role": "user"})

        # Verify the update was applied
        assert updated_msg["id"] == original_id
        assert updated_msg["message"]["content"] == "Updated content"
        assert updated_msg["message"]["role"] == "user"

        # Verify the node was updated in the canvas
        retrieved_msg = canvas.get_node(original_id)
        assert retrieved_msg is not None
        assert retrieved_msg["message"]["content"] == "Updated content"

        # Verify metadata includes last_updated timestamp
        assert retrieved_msg["meta"] is not None
        assert "last_updated" in retrieved_msg["meta"]
        assert "timestamp" in retrieved_msg["meta"]  # Original timestamp should still exist

    def test_update_message_with_metadata(self, canvas: Canvas) -> None:
        """Test updating message with additional metadata."""
        # Create a message to update
        original_msg = canvas.commit_message({"content": "Original content", "role": "assistant"})
        original_id = original_msg["id"]

        # Update with custom metadata
        updated_msg = canvas.update_message(
            original_id,
            {"content": "Updated content with metadata", "role": "assistant"},
            meta={"updated_by": "test", "version": 2},
        )

        # Verify the update and metadata
        assert updated_msg["message"]["content"] == "Updated content with metadata"
        assert updated_msg["meta"] is not None
        assert updated_msg["meta"]["updated_by"] == "test"
        assert updated_msg["meta"]["version"] == 2
        assert "last_updated" in updated_msg["meta"]
        assert "timestamp" in updated_msg["meta"]  # Original timestamp preserved

    def test_update_message_preserves_structure(self, canvas: Canvas) -> None:
        """Test that updating a message preserves the graph structure."""
        # Create a conversation chain
        msg1 = canvas.commit_message({"content": "First message", "role": "user"})
        msg2 = canvas.commit_message({"content": "Second message", "role": "assistant"})
        msg3 = canvas.commit_message({"content": "Third message", "role": "user"})

        # Update the middle message
        canvas.update_message(msg2["id"], {"content": "Updated second message", "role": "assistant"})

        # Verify structure is preserved
        updated_msg2 = canvas.get_node(msg2["id"])
        assert updated_msg2 is not None
        assert updated_msg2["parent_id"] == msg1["id"]
        assert msg3["id"] in updated_msg2["child_ids"]

        # Verify content was updated
        assert updated_msg2["message"]["content"] == "Updated second message"

    def test_update_nonexistent_message(self, canvas: Canvas) -> None:
        """Test updating a message that doesn't exist raises error."""
        with pytest.raises(ValueError, match="Node with ID 'nonexistent-id' does not exist"):
            canvas.update_message("nonexistent-id", {"content": "This should fail", "role": "user"})

    def test_update_message_preserves_metadata(self, canvas: Canvas) -> None:
        """Test that updating preserves existing metadata while adding new."""
        # Create message with initial metadata
        original_msg = canvas.commit_message(
            {"content": "Original content", "role": "user"}, meta={"initial_field": "initial_value", "priority": "low"}
        )

        # Update with additional metadata
        canvas.update_message(
            original_msg["id"],
            {"content": "Updated content", "role": "user"},
            meta={"new_field": "new_value", "priority": "high"},
        )  # Override priority

        # Verify metadata merging
        updated_msg = canvas.get_node(original_msg["id"])
        assert updated_msg is not None
        assert updated_msg["meta"] is not None
        assert updated_msg["meta"]["initial_field"] == "initial_value"  # Preserved
        assert updated_msg["meta"]["new_field"] == "new_value"  # Added
        assert updated_msg["meta"]["priority"] == "high"  # Overridden
        assert "last_updated" in updated_msg["meta"]  # Auto-added
        assert "timestamp" in updated_msg["meta"]  # Original preserved

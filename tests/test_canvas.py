"""Tests for Canvas API implementation."""

import uuid

import pytest

from llm_canvas.canvas import Canvas
from llm_canvas.types import Message, MessageNode


class TestCanvasAPI:
    """Test suite for Canvas API functionality."""

    @pytest.fixture
    def canvas(self) -> Canvas:
        """Create a test canvas."""
        canvas_id = str(uuid.uuid4())
        return Canvas(canvas_id=canvas_id, title="Test Canvas", description="A canvas for testing the API")

    def test_create_canvas(self, canvas: Canvas) -> None:
        """Test canvas creation."""
        assert canvas.canvas_id is not None
        assert canvas.title == "Test Canvas"
        assert canvas.description == "A canvas for testing the API"

    def test_commit_message(self, canvas: Canvas) -> None:
        """Test committing messages to canvas using branch API."""
        # Get main branch
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)

        # Add user message
        user_msg = main_branch.commit_message({"content": "Hello, world!", "role": "user"})
        assert user_msg["id"] is not None
        assert user_msg["message"]["content"] == "Hello, world!"
        assert user_msg["message"]["role"] == "user"

        # Add assistant message
        assistant_msg = main_branch.commit_message({"content": "Hello! How can I help you today?", "role": "assistant"})
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
        branch = canvas.checkout("main")
        assert branch.name == "main"

    def test_checkout_new_branch(self, canvas: Canvas) -> None:
        """Test creating and checking out new branch."""
        branch = canvas.checkout(
            name="Alternative Path", description="Testing alternative conversation path", create_if_not_exists=True
        )
        assert branch.name == "Alternative Path"
        assert branch.description == "Testing alternative conversation path"

        # Verify branch was created
        branches = canvas.list_branches()
        branch_names = [b["name"] for b in branches]
        assert "Alternative Path" in branch_names

    def test_checkout_nonexistent_branch_without_create(self, canvas: Canvas) -> None:
        """Test checking out to non-existent branch without create flag."""
        with pytest.raises(ValueError, match="Branch 'nonexistent' does not exist"):
            canvas.checkout("nonexistent")

    def test_checkout_detached_head(self, canvas: Canvas) -> None:
        """Test checking out to a specific message (detached head)."""
        # Get main branch and create some messages
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)
        msg1 = main_branch.commit_message({"content": "First message", "role": "user"})
        main_branch.commit_message({"content": "Second message", "role": "assistant"})

        # Checkout to first message (detached head)
        detached_branch = canvas.checkout(commit_message=msg1)

        # Verify we're in detached head state
        assert detached_branch.name.startswith("detached-")
        assert detached_branch.head_node_id == msg1["id"]
        assert detached_branch.description is not None
        assert "Detached HEAD" in detached_branch.description

        # Verify we can commit to detached head
        new_msg = detached_branch.commit_message({"content": "New message from detached head", "role": "user"})
        assert new_msg["parent_id"] == msg1["id"]
        assert detached_branch.head_node_id == new_msg["id"]

    def test_branch_from_specific_message(self, canvas: Canvas) -> None:
        """Test creating branch from specific message."""
        # Get main branch and add a message
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)
        user_msg = main_branch.commit_message({"content": "Hello, main branch!", "role": "user"})

        # Create branch from that message
        branch = canvas.checkout(
            name="From Hello",
            description="Branch starting from the hello message",
            create_if_not_exists=True,
            commit_message=user_msg,
        )

        # Verify HEAD is the specified message
        head = branch.get_head_node()
        assert head is not None
        assert head["id"] == user_msg["id"]

    def test_head_operations(self, canvas: Canvas) -> None:
        """Test HEAD node operations."""
        # Get main branch
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)

        # Initially no HEAD
        head = main_branch.get_head_node()
        assert head is None

        # Add message and check HEAD
        msg = main_branch.commit_message({"content": "First message", "role": "user"})
        head = main_branch.get_head_node()
        assert head is not None
        assert head["id"] == msg["id"]

    def test_head_operations_invalid_branch(self, canvas: Canvas) -> None:
        """Test HEAD operations with invalid branch."""
        with pytest.raises(ValueError, match="Branch 'invalid' does not exist"):
            canvas.checkout("invalid")

    def test_delete_branch(self, canvas: Canvas) -> None:
        """Test branch deletion."""
        # Create a branch to delete
        branch = canvas.checkout(name="To Delete", description="Branch to be deleted", create_if_not_exists=True)
        assert branch.name == "To Delete"

        # Switch back to main
        main_branch = canvas.checkout("main")
        assert main_branch.name == "main"

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
        # Get main branch and add initial message
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)
        hello_main = main_branch.commit_message({"content": "Hello, main branch!", "role": "user"})

        # Create alternative path
        alt_branch = canvas.checkout(
            name="Alternative Path", description="Exploring different responses", create_if_not_exists=True
        )
        alt_branch.commit_message({"content": "Hello, alternative branch!", "role": "user"})

        # Create branch from specific message
        hello_branch = canvas.checkout(
            name="Branch from Hello",
            description="New path from the hello message",
            create_if_not_exists=True,
            commit_message=hello_main,
        )
        hello_branch.commit_message({"content": "This is a different direction!", "role": "user"})

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
            head_node_message = canvas.nodes[branch["head_node_id"]]
            assert head_node_message is not None
            if branch["name"] == "main":
                assert head_node_message["message"]["content"] == "Hello, main branch!"
            elif branch["name"] == "Alternative Path":
                assert head_node_message["message"]["content"] == "Hello, alternative branch!"
            elif branch["name"] == "Branch from Hello":
                assert head_node_message["message"]["content"] == "This is a different direction!"

    def test_message_metadata(self, canvas: Canvas) -> None:
        """Test message metadata handling."""
        # Get main branch
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)

        custom_meta = {"custom_field": "value", "priority": "high"}
        msg = main_branch.commit_message({"content": "Message with metadata", "role": "user"}, meta=custom_meta)

        # Check that custom metadata is preserved along with timestamp
        assert msg["meta"] is not None
        assert "timestamp" in msg["meta"]
        assert msg["meta"]["custom_field"] == "value"
        assert msg["meta"]["priority"] == "high"

    def test_update_message(self, canvas: Canvas) -> None:
        """Test updating existing messages."""
        # Get main branch and create a message to update
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)
        original_msg = main_branch.commit_message({"content": "Original content", "role": "user"})
        original_id = original_msg["id"]
        updated_content = "Updated content"
        updated_msg_node = original_msg.copy()
        updated_msg_node["message"]["content"] = updated_content

        # Update the message content using branch
        updated_msg = main_branch.update_message(original_id, updated_msg_node)

        # Verify the update was applied
        assert updated_msg["id"] == original_id
        assert updated_msg["message"]["content"] == "Updated content"
        assert updated_msg["message"]["role"] == "user"

        # Verify the node was updated in the canvas
        retrieved_msg = canvas.get_node(original_id)
        assert retrieved_msg is not None
        assert retrieved_msg["message"]["content"] == "Updated content"

        # Verify metadata includes timestamp
        assert retrieved_msg["meta"] is not None
        assert "timestamp" in retrieved_msg["meta"]  # Original timestamp should still exist

    def test_update_message_with_metadata(self, canvas: Canvas) -> None:
        """Test updating message with additional metadata."""
        # Get main branch and create a message to update
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)
        original_msg = main_branch.commit_message({"content": "Original content", "role": "assistant"})
        original_id = original_msg["id"]

        # Update with custom metadata - create updated message node
        updated_msg_node = original_msg.copy()
        updated_msg_node["message"]["content"] = "Updated content with metadata"
        assert original_msg["meta"] is not None
        updated_msg_node["meta"] = {**original_msg["meta"], "updated_by": "test", "version": 2}

        # Update using branch
        updated_msg = main_branch.update_message(original_id, updated_msg_node)

        # Verify the update and metadata
        assert updated_msg["message"]["content"] == "Updated content with metadata"
        assert updated_msg["meta"] is not None
        assert updated_msg["meta"]["updated_by"] == "test"
        assert updated_msg["meta"]["version"] == 2
        assert "timestamp" in updated_msg["meta"]  # Original timestamp preserved

    def test_update_message_preserves_structure(self, canvas: Canvas) -> None:
        """Test that updating a message preserves the graph structure."""
        # Get main branch and create a conversation chain
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)
        msg1 = main_branch.commit_message({"content": "First message", "role": "user"})
        msg2 = main_branch.commit_message({"content": "Second message", "role": "assistant"})
        msg3 = main_branch.commit_message({"content": "Third message", "role": "user"})

        # Update the middle message
        updated_msg2_node = msg2.copy()
        updated_msg2_node["message"]["content"] = "Updated second message"
        main_branch.update_message(msg2["id"], updated_msg2_node)

        # Verify structure is preserved
        updated_msg2 = canvas.get_node(msg2["id"])
        assert updated_msg2 is not None
        assert updated_msg2["parent_id"] == msg1["id"]
        assert msg3["id"] in updated_msg2["child_ids"]

        # Verify content was updated
        assert updated_msg2["message"]["content"] == "Updated second message"

    def test_update_nonexistent_message(self, canvas: Canvas) -> None:
        """Test updating a message that doesn't exist raises error."""
        # Get main branch
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)

        # Create a dummy message node for the update
        dummy_msg_node: MessageNode = {
            "id": "nonexistent-id",
            "message": {"content": "This should fail", "role": "user"},
            "parent_id": None,
            "child_ids": [],
            "meta": {"timestamp": 0},
        }

        with pytest.raises(ValueError, match="Node with ID 'nonexistent-id' does not exist"):
            main_branch.update_message("nonexistent-id", dummy_msg_node)

    def test_update_message_preserves_metadata(self, canvas: Canvas) -> None:
        """Test that updating preserves existing metadata while adding new."""
        # Get main branch and create message with initial metadata
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)
        original_msg = main_branch.commit_message(
            {"content": "Original content", "role": "user"}, meta={"initial_field": "initial_value", "priority": "low"}
        )

        # Update with additional metadata
        updated_msg_node: MessageNode = original_msg.copy()
        updated_msg_node["message"]["content"] = "Updated content"
        assert updated_msg_node["meta"] is not None
        assert original_msg["meta"] is not None
        updated_msg_node["meta"] = {
            **original_msg["meta"],
            "new_field": "new_value",
            "priority": "high",  # Override priority
        }
        main_branch.update_message(original_msg["id"], updated_msg_node)

        # Verify metadata merging
        updated_msg = canvas.get_node(original_msg["id"])
        assert updated_msg is not None
        assert updated_msg["meta"] is not None
        assert updated_msg["meta"]["initial_field"] == "initial_value"  # Preserved
        assert updated_msg["meta"]["new_field"] == "new_value"  # Added
        assert updated_msg["meta"]["priority"] == "high"  # Overridden
        assert "timestamp" in updated_msg["meta"]  # Original preserved

    def test_merge_single_branch(self, canvas: Canvas) -> None:
        """Test merging a single branch.

        Graph structure:
        Before merge:
            main:    M1 ── M2 (HEAD)
            feature: F1 ── F2 (HEAD)

        After merge:
            main:    M1 ── M2 ── MERGE (HEAD)
                              ┌─────┘
            feature: F1 ── F2 ──┘
        """
        # Create main branch with messages
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)
        main_branch.commit_message({"content": "Main message 1", "role": "user"})
        main_msg2 = main_branch.commit_message({"content": "Main message 2", "role": "assistant"})

        # Create feature branch with messages
        feature_branch = canvas.checkout(name="feature", create_if_not_exists=True)
        feature_branch.commit_message({"content": "Feature message 1", "role": "user"})
        feature_msg2 = feature_branch.commit_message({"content": "Feature message 2", "role": "assistant"})

        # Merge feature into main
        merge_message: Message = {"role": "system", "content": "Merge feature branch into main"}
        merge_node = canvas.merge("feature", merge_message, "main")

        # Verify merge node properties
        assert merge_node["message"]["content"] == "Merge feature branch into main"
        assert merge_node["message"]["role"] == "system"
        assert merge_node["parent_id"] == main_msg2["id"]  # Target branch HEAD

        # Verify graph structure - merge node should be child of both heads
        assert merge_node["id"] in canvas.nodes[main_msg2["id"]]["child_ids"]
        assert merge_node["id"] in canvas.nodes[feature_msg2["id"]]["child_ids"]

        # Verify main branch HEAD was updated
        main_branch_updated = canvas.checkout("main")
        assert main_branch_updated.head_node_id == merge_node["id"]

    def test_merge_multiple_branches(self, canvas: Canvas) -> None:
        """Test merging multiple branches at once.

        Graph structure:
        Before merge:
            main:     M1 (HEAD)
            feature1: F1 (HEAD)
            feature2: F2 (HEAD)
            feature3: F3 (HEAD)

        After merge:
            main:     M1 ── MERGE (HEAD)
                        ┌────┘
            feature1: F1 ──┘
                        ┌────┘
            feature2: F2 ──┘
                        ┌────┘
            feature3: F3 ──┘
        """
        # Create main branch
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)
        main_msg = main_branch.commit_message({"content": "Main message", "role": "user"})

        # Create first feature branch
        feature1_branch = canvas.checkout(name="feature1", create_if_not_exists=True)
        feature1_msg = feature1_branch.commit_message({"content": "Feature 1 message", "role": "assistant"})

        # Create second feature branch
        feature2_branch = canvas.checkout(name="feature2", create_if_not_exists=True)
        feature2_msg = feature2_branch.commit_message({"content": "Feature 2 message", "role": "assistant"})

        # Create third feature branch
        feature3_branch = canvas.checkout(name="feature3", create_if_not_exists=True)
        feature3_msg = feature3_branch.commit_message({"content": "Feature 3 message", "role": "assistant"})

        # Merge all features into main
        merge_message: Message = {"role": "system", "content": "Merge multiple feature branches"}
        merge_node = canvas.merge(["feature1", "feature2", "feature3"], merge_message, "main")

        # Verify all source branches are connected to merge node
        assert merge_node["id"] in canvas.nodes[feature1_msg["id"]]["child_ids"]
        assert merge_node["id"] in canvas.nodes[feature2_msg["id"]]["child_ids"]
        assert merge_node["id"] in canvas.nodes[feature3_msg["id"]]["child_ids"]
        assert merge_node["id"] in canvas.nodes[main_msg["id"]]["child_ids"]

    def test_branch_merge_from_single(self, canvas: Canvas) -> None:
        """Test using Branch.merge_from() with single branch."""
        # Create branches with messages
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)
        main_branch.commit_message({"content": "Main content", "role": "user"})

        feature_branch = canvas.checkout(name="feature", create_if_not_exists=True)
        feature_branch.commit_message({"content": "Feature content", "role": "assistant"})

        # Use branch method to merge
        merge_message: Message = {"role": "system", "content": "Merge using branch method"}
        merge_node = main_branch.merge_from("feature", merge_message)

        # Verify merge worked correctly
        assert merge_node["message"]["content"] == "Merge using branch method"

        # Verify main branch HEAD was updated
        assert main_branch.head_node_id == merge_node["id"]

    def test_branch_merge_from_multiple(self, canvas: Canvas) -> None:
        """Test using Branch.merge_from() with multiple branches."""
        # Create branches
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)
        main_branch.commit_message({"content": "Main content", "role": "user"})

        # Create multiple feature branches
        for i in range(1, 4):
            branch = canvas.checkout(name=f"feature{i}", create_if_not_exists=True)
            branch.commit_message({"content": f"Feature {i} content", "role": "assistant"})

        # Merge all features using branch method
        merge_message: Message = {"role": "system", "content": "Merge multiple features using branch method"}
        merge_node = main_branch.merge_from(["feature1", "feature2", "feature3"], merge_message)

        assert main_branch.head_node_id is not None
        assert merge_node["id"] == main_branch.head_node_id

    def test_merge_validation_errors(self, canvas: Canvas) -> None:
        """Test merge validation errors."""
        # Create valid branches
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)
        empty_branch = canvas.checkout(name="empty", create_if_not_exists=True)
        main_branch.commit_message({"content": "Main content", "role": "user"})

        feature_branch = canvas.checkout(name="feature", create_if_not_exists=True)
        feature_branch.commit_message({"content": "Feature content", "role": "assistant"})

        merge_message: Message = {"role": "system", "content": "Test merge"}

        # Test non-existent source branch
        with pytest.raises(ValueError, match="Source branch 'nonexistent' does not exist"):
            canvas.merge("nonexistent", merge_message, "main")

        # Test non-existent target branch
        with pytest.raises(ValueError, match="Target branch 'nonexistent' does not exist"):
            canvas.merge("feature", merge_message, "nonexistent")

        # Test empty source branches list
        with pytest.raises(ValueError, match="At least one source branch must be specified"):
            canvas.merge([], merge_message, "main")

        # Test source branch with no commits
        with pytest.raises(ValueError, match="Source branch 'empty' has no commits"):
            canvas.merge(empty_branch.name, merge_message, "main")

    def test_merge_multiple_with_mixed_valid_invalid(self, canvas: Canvas) -> None:
        """Test merging multiple branches with some invalid ones."""
        # Create valid branches
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)
        main_branch.commit_message({"content": "Main content", "role": "user"})

        feature_branch = canvas.checkout(name="feature", create_if_not_exists=True)
        feature_branch.commit_message({"content": "Feature content", "role": "assistant"})

        merge_message: Message = {"role": "system", "content": "Test merge"}

        # Test with one valid and one invalid branch
        with pytest.raises(ValueError, match="Source branch 'nonexistent' does not exist"):
            canvas.merge(["feature", "nonexistent"], merge_message, "main")

    def test_merge_preserves_conversation_history(self, canvas: Canvas) -> None:
        """Test that merge preserves full conversation history.

        Graph structure:
        Before merge:
            main:    Q ── Initial_Answer (HEAD)
                     │
            feature: └── Alternative_Answer ── Follow_up (HEAD)

        After merge:
            main:    Q ── Initial_Answer ── MERGE (HEAD)
                     │                       ┌─────┘
            feature: └── Alternative_Answer ── Follow_up ──┘
        """
        # Create a complex conversation tree
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)
        msg1 = main_branch.commit_message({"content": "Question", "role": "user"})
        msg2 = main_branch.commit_message({"content": "Initial answer", "role": "assistant"})

        # Create feature branch from msg1
        feature_branch = canvas.checkout(name="feature", create_if_not_exists=True, commit_message=msg1)
        msg3 = feature_branch.commit_message({"content": "Alternative answer", "role": "assistant"})
        msg4 = feature_branch.commit_message({"content": "Follow-up", "role": "user"})

        # Merge feature into main
        merge_message: Message = {"role": "system", "content": "Combine answers"}
        merge_node = canvas.merge("feature", merge_message, "main")

        # Verify all messages are still accessible
        assert canvas.nodes[msg1["id"]] is not None
        assert canvas.nodes[msg2["id"]] is not None
        assert canvas.nodes[msg3["id"]] is not None
        assert canvas.nodes[msg4["id"]] is not None
        assert canvas.nodes[merge_node["id"]] is not None

        # Verify relationships are preserved
        assert msg2["parent_id"] == msg1["id"]
        assert msg3["parent_id"] == msg1["id"]
        assert msg4["parent_id"] == msg3["id"]

        # Verify merge connects to both branches
        assert merge_node["parent_id"] == msg2["id"]  # Target branch HEAD
        assert merge_node["id"] in canvas.nodes[msg4["id"]]["child_ids"]  # Source branch HEAD

    def test_merge_backward_compatibility(self, canvas: Canvas) -> None:
        """Test that merge API maintains backward compatibility with string input."""
        # Create branches
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)
        main_branch.commit_message({"content": "Main content", "role": "user"})

        feature_branch = canvas.checkout(name="feature", create_if_not_exists=True)
        feature_msg = feature_branch.commit_message({"content": "Feature content", "role": "assistant"})

        # Test string input (single branch)
        merge_message: Message = {"role": "system", "content": "Backward compatible merge"}
        merge_node = canvas.merge("feature", merge_message, "main")

        assert merge_node["id"] in canvas.nodes[feature_msg["id"]]["child_ids"]

    def test_merge_updates_target_branch_head(self, canvas: Canvas) -> None:
        """Test that merge properly updates target branch HEAD.

        Graph structure:
        Before merge:
            main:    Original_Main (HEAD)
            feature: Feature_Content (HEAD)

        After merge:
            main:    Original_Main ── MERGE ── After_Merge (HEAD)
                                       ┌─────┘
            feature: Feature_Content ──┘
        """
        # Create branches
        main_branch = canvas.checkout(name="main", create_if_not_exists=True)
        original_main_msg = main_branch.commit_message({"content": "Original main", "role": "user"})

        feature_branch = canvas.checkout(name="feature", create_if_not_exists=True)
        feature_branch.commit_message({"content": "Feature content", "role": "assistant"})

        # Verify initial HEAD
        assert main_branch.head_node_id == original_main_msg["id"]

        # Perform merge
        merge_message: Message = {"role": "system", "content": "Update HEAD test"}
        merge_node = canvas.merge("feature", merge_message, "main")

        # Verify main branch HEAD was updated
        main_branch_after = canvas.checkout("main")
        assert main_branch_after.head_node_id == merge_node["id"]

        # Verify we can continue committing to main after merge
        new_msg = main_branch_after.commit_message({"content": "After merge", "role": "user"})
        assert new_msg["parent_id"] == merge_node["id"]
        assert main_branch_after.head_node_id == new_msg["id"]

#!/usr/bin/env python3
"""
Legacy test script for Canvas API implementation.

For comprehensive testing, use pytest:
    python -m pytest tests/

This script is kept for quick manual testing and demonstration.
"""

import os
import sys

from llm_canvas.canvas import Canvas

# Add the current directory to Python path to import llm_canvas
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # noqa: PTH120

from llm_canvas import canvas_client


def test_canvas_api() -> Canvas:
    """Test the Canvas API implementation."""
    print("Testing Canvas API Implementation")
    print("=" * 50)

    # 1. Create a new canvas
    print("\n1. Creating a new canvas...")
    canvas = canvas_client.create_canvas(title="Test Canvas", description="A canvas for testing the API")
    print(f"✓ Created canvas: {canvas.canvas_id}")
    print(f"  Title: {canvas.title}")
    print(f"  Description: {canvas.description}")
    print(f"  Current branch: {canvas.get_current_branch()}")

    # 2. Add messages to the canvas
    print("\n2. Adding messages...")
    user_msg = canvas.commit_message({"content": "Hello, world!", "role": "user"})
    print(f"✓ Added user message: {user_msg['id']}")

    assistant_msg = canvas.commit_message({"content": "Hello! How can I help you today?", "role": "assistant"})
    print(f"✓ Added assistant message: {assistant_msg['id']}")

    # 3. Test branch operations
    print("\n3. Testing branch operations...")

    # List current branches
    branches = canvas.list_branches()
    print(f"✓ Current branches: {len(branches)}")
    for branch in branches:
        print(f"  - {branch['name']}: {branch['description']}")
        if branch["latest_commit_message"]:
            print(f"    Latest: {branch['latest_commit_message']['content'][:50]}...")

    # Create a new branch
    canvas.checkout(name="Alternative Path", description="Testing alternative conversation path", create_if_not_exists=True)
    print(f"✓ Switched to branch: {canvas.get_current_branch()}")

    # Add message to new branch
    alt_msg = canvas.commit_message({"content": "This is an alternative path!", "role": "user"})
    print(f"✓ Added message to alternative branch: {alt_msg['id']}")

    # Create branch from specific message
    canvas.checkout(
        name="From Hello",
        description="Branch starting from the hello message",
        create_if_not_exists=True,
        commit_message=user_msg,
    )
    print(f"✓ Created branch from specific message: {canvas.get_current_branch()}")

    final_msg = canvas.commit_message({"content": "Starting from hello message!", "role": "assistant"})
    print(f"✓ Added message to new branch: {final_msg['id']}")

    # 4. Final branch listing
    print("\n4. Final branch structure...")
    branches = canvas.list_branches()
    for branch in branches:
        print(f"Branch: {branch['name']}")
        if branch["latest_commit"]:
            print(f"  Latest: {branch['latest_commit']['content']}")
        print()

    # 5. Test HEAD operations
    print("5. Testing HEAD operations...")
    head_node = canvas.get_head_node()
    if head_node:
        print(f"✓ Current HEAD: {head_node['content']['content']}")
    else:
        print("✗ No HEAD found")

    # Switch back to main and check HEAD
    canvas.checkout("main")
    main_head = canvas.get_head_node("main")
    if main_head:
        print(f"✓ Main branch HEAD: {main_head['content']['content']}")
    else:
        print("✗ No HEAD found for main branch")

    # 6. Test deletion
    print("\n6. Testing branch deletion...")
    try:
        canvas.delete_branch("Alternative Path")
        print("✓ Successfully deleted 'Alternative Path' branch")
    except Exception as e:
        print(f"✗ Error deleting branch: {e}")

    try:
        canvas.delete_branch("main")
        print("✗ Should not be able to delete main branch")
    except ValueError as e:
        print(f"✓ Correctly prevented deleting main branch: {e}")

    print("\n" + "=" * 50)
    print("Canvas API test completed!")

    return canvas


if __name__ == "__main__":
    test_canvas = test_canvas_api()

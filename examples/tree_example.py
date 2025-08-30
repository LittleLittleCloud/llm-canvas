"""Tree Visualization Example

This example demonstrates basic recursive tree drawing functionality for Canvas branches.
It shows the hierarchical structure of branches and their message counts.
"""

from __future__ import annotations

import asyncio
import time

from examples.shared_client import get_canvas_client
from llm_canvas.canvas import Branch, Canvas


def draw_binary_tree(canvas: Canvas, branch_name: str, depth: int = 0) -> None:
    """
    Draw a binary tree structure in the Canvas.

    Args:
        canvas: The Canvas object to draw on
        value: The value to display at the current node
        depth: The current depth in the tree (used for indentation)
    """
    current_branch = canvas.checkout(name=branch_name, create_if_not_exists=True)
    # commit message

    time.sleep(0.1)
    current_branch.commit_message(
        {
            "role": "user",
            "content": current_branch.name,
        }
    )

    if depth <= 0:
        return

    left_branch_name = f"{branch_name}-left"
    canvas.checkout(name=left_branch_name, create_if_not_exists=True)
    draw_binary_tree(canvas, left_branch_name, depth - 1)
    canvas.checkout(name=branch_name)

    right_branch_name = f"{current_branch.name}-right"
    canvas.checkout(name=right_branch_name, create_if_not_exists=True)
    draw_binary_tree(canvas, right_branch_name, depth - 1)

    # restore back to the previous branch
    canvas.checkout(name=current_branch.name)


async def draw_branch_async(canvas: Canvas, branch_name: str, depth: int) -> None:
    """
    Async helper function to draw a single branch.

    Args:
        canvas: The Canvas object to draw on
        branch_name: Name of the branch to create and draw
        depth: The depth to draw to
    """
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, draw_binary_tree, canvas, branch_name, depth)


async def draw_binary_tree_async(canvas: Canvas, current_branch: Branch, depth: int = 0) -> None:
    """
    Draw a binary tree structure in the Canvas with async parallel branch creation.

    Args:
        canvas: The Canvas object to draw on
        depth: The current depth in the tree (used for indentation)
    """
    await asyncio.sleep(0.5)
    current_branch.commit_message(
        {
            "role": "user",
            "content": current_branch.name,
        }
    )

    if depth <= 0:
        return

    left_branch_name = f"{current_branch.name}-left"
    left_branch = canvas.checkout(
        name=left_branch_name, create_if_not_exists=True, commit_message=current_branch.get_head_node()
    )
    right_branch_name = f"{current_branch.name}-right"
    right_branch = canvas.checkout(
        name=right_branch_name, create_if_not_exists=True, commit_message=current_branch.get_head_node()
    )
    await asyncio.sleep(0.5)

    await asyncio.gather(
        draw_binary_tree_async(canvas, left_branch, depth - 1),
        draw_binary_tree_async(canvas, right_branch, depth - 1),
    )

    # restore back to the current branch
    canvas.checkout(name=current_branch.name)


if __name__ == "__main__":
    canvas_client = get_canvas_client()

    print("\nDrawing binary tree with async parallel...")
    canvas = canvas_client.create_canvas(title="Binary Tree Async Parallel")
    start_time = time.time()
    asyncio.run(draw_binary_tree_async(canvas, canvas.current_branch, 5))
    async_time = time.time() - start_time
    print(f"Async parallel execution took {async_time:.2f} seconds")

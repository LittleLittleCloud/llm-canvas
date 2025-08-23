"""Claude Image Analysis Canvas Example

This example demonstrates Claude's vision capabilities by comparing two images
and creating a simple one-turn conversation in the canvas.

The example showcases how to use ImageBlockParam to send multiple images to Claude
and visualize the comparison process in the canvas.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from examples.claude.utils import llm_call
from examples.shared_client import get_canvas_client
from llm_canvas.types import Message

if TYPE_CHECKING:
    from anthropic.types import ImageBlockParam, TextBlockParam


def create_image_comparison_message() -> Message:
    """Create a message comparing two images using URL sources."""

    text_block_1: TextBlockParam = {"type": "text", "text": "Image 1:"}

    image_block_1: ImageBlockParam = {
        "type": "image",
        "source": {
            "type": "url",
            "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
        },
    }

    text_block_2: TextBlockParam = {"type": "text", "text": "Image 2:"}

    image_block_2: ImageBlockParam = {
        "type": "image",
        "source": {"type": "url", "url": "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg"},
    }

    text_block_question: TextBlockParam = {"type": "text", "text": "How are these images different?"}

    return Message(content=[text_block_1, image_block_1, text_block_2, image_block_2, text_block_question], role="user")


if __name__ == "__main__":
    canvas_client = get_canvas_client()
    canvas = canvas_client.create_canvas(
        title="Image Comparison Canvas",
        description="""
        This canvas demonstrates Claude's image comparison capabilities.

        The example shows a simple one-turn conversation where Claude compares
        two insect images (an ant and a bee) and explains their differences.

        This showcases how to use ImageBlockParam with URL sources to send
        multiple images in a single message to Claude for comparison analysis.
        """,
    )

    system_prompt = "You are a helpful assistant that provides image comparisons. Respond only in English."

    # Create the main branch
    main_branch = canvas.checkout("main")

    # Create and commit the image comparison message
    comparison_message = create_image_comparison_message()
    main_branch.commit_message(
        message={
            "role": "system",
            "content": system_prompt,
        }
    )
    main_branch.commit_message(message=comparison_message)

    # Get Claude's response comparing the images
    print("Asking Claude to compare the two insect images...")
    response = llm_call(comparison_message, system_prompt=system_prompt)
    print(f"Claude's response: {response}")

    # Commit Claude's response
    response_message = Message(content=response, role="assistant")
    main_branch.commit_message(message=response_message)

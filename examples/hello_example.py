"""Simple Hello Canvas Example

This example demonstrates the basic usage of the Canvas API to create
a simple conversation between a user and an assistant using the shared
CanvasClient instance.
"""

import time

from examples.shared_client import get_canvas_client
from llm_canvas.canvas import Message


def create_hello_canvas() -> None:
    """Create a simple hello conversation canvas."""
    # Get the shared client
    client = get_canvas_client()

    # Create a new canvas via the client
    canvas = client.create_canvas(title="Hello Canvas", description="A simple hello conversation example")

    print("🚀 Creating Hello Canvas example...")
    print(f"Canvas ID: {canvas.canvas_id}")

    # Create the user message
    user_message: Message = {"role": "user", "content": [{"type": "text", "text": "Hello model"}]}

    # Commit the user message to the canvas
    print("📝 Adding user message: 'Hello model'")
    canvas.commit_message(user_message)

    # Simulate a brief pause (like processing time)
    time.sleep(0.2)

    # Create the assistant response
    assistant_message: Message = {"role": "assistant", "content": [{"type": "text", "text": "Model reply"}]}

    # Commit the assistant response
    print("🤖 Adding assistant response: 'Model reply'")
    canvas.commit_message(assistant_message)

    print("✅ Hello Canvas example completed! Canvas available at server.")


if __name__ == "__main__":
    create_hello_canvas()

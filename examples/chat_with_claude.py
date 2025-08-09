"""Example usage of CanvasClient - a one-stop solution for canvas management.

This example demonstrates how to use CanvasClient to:
- Create and manage multiple canvases
- Add messages to canvases
- Run the web UI/API server
- Handle canvas operations in a unified way
"""

import os
from typing import TYPE_CHECKING

from anthropic import Anthropic

if TYPE_CHECKING:
    from anthropic.types import MessageParam

from llm_canvas import CanvasClient

anthropic_client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),  # This is the default and can be omitted
)


def main() -> None:
    # Create a canvas client
    client = CanvasClient()

    # Create multiple canvases
    chat_canvas = client.create_canvas(title="AI Assistant Chat", description="A conversation with an AI assistant")
    # Run the server in background
    print("\n🚀 Starting server...")

    print("\n✅ Server is running at http://127.0.0.1:8000")
    print("   - View all canvases: http://127.0.0.1:8000")
    print("   - API endpoint: http://127.0.0.1:8000/api/v1/canvas/list")
    print(f"   - Specific canvas: http://127.0.0.1:8000/api/v1/canvas?id={chat_canvas.canvas_id}")
    client.run_server(background=True)
    parent_node = None
    chat_history: list[MessageParam] = []
    while True:
        user_input = input("You: ")
        chat_history.append({"role": "user", "content": user_input})
        # Add user message to chat canvas
        parent_node = chat_canvas._add_message({"role": "user", "content": user_input}, parent_node)

        if user_input.lower() in ["exit", "quit"]:
            break

        response = anthropic_client.messages.create(
            model="claude-4-sonnet-20250514",
            max_tokens=1024,
            messages=chat_history,
        )

        parent_node = chat_canvas._add_message(
            response.to_dict(),
            parent_node,
        )
        chat_history.append(
            {
                "role": "assistant",
                "content": response.content,
            }
        )

    # Print summary
    print("\n📊 Canvas Client Summary:")
    print(f"Total canvases: {len(client)}")
    print(f"Server running: {client.is_server_running()}")

    print("\n📋 Canvas List:")
    for canvas in client.list_canvases():
        print(f"  • {canvas.title} ({canvas.canvas_id})")

    # Get canvas summaries
    print("\n📝 Canvas Summaries:")
    for summary in client.get_canvas_summaries():
        print(f"  • {summary['title']}: {summary['node_count']} nodes")

    print("\n👋 Press Ctrl+C to shut down the server...")
    client.wait_for_shutdown()


if __name__ == "__main__":
    main()

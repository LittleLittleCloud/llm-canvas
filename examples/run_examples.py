"""Example Runner - Demonstrates the shared CanvasClient functionality.

This script runs all examples and shows how they share a common CanvasClient
instance and server, allowing users to view all canvases in a single interface.
"""

from __future__ import annotations

from examples.hello_example import create_hello_canvas
from examples.investment_decision_example import investment_decision
from examples.shared_client import get_canvas_client
from examples.vacation_planning_example import create_vacation_planning
from examples.weather_tool_example import weather_inquiry


def run_all_examples() -> None:
    """Run all examples using the shared CanvasClient."""
    print("🚀 Canvas Examples with Shared Client")
    print("=" * 50)

    # Check if server is running first
    if not get_canvas_client().check_server_health():
        print("❌ Canvas server is not running!")
        print("\n📋 Please start the canvas server first:")
        print("   llm-canvas server")
        print("\n📖 For more information, see: doc/start_canvas_server.md")
        print("🌐 Once started, run this script again.")
        return

    print("✅ Canvas server is running")
    print("\n📋 Running all examples...")

    # Run each example with error handling
    examples = [
        ("Hello Canvas", create_hello_canvas),
        ("Weather Tool", weather_inquiry),
        ("Vacation Planning", create_vacation_planning),
        ("Investment Decision", investment_decision),
    ]

    successful_examples = 0
    for name, example_func in examples:
        print("\n" + "=" * 30)
        print(f"Running {name} example...")
        try:
            example_func()
            successful_examples += 1
        except RuntimeError as e:
            print(f"❌ Error in {name}: {e}")
            print("Please check that the canvas server is running properly.")

    # Show final status
    print("\n" + "=" * 50)
    print(f"🎉 Completed {successful_examples}/{len(examples)} examples!")

    print("\n🌐 View all canvases at: http://127.0.0.1:8000")
    print("   The server will continue running in the background.")
    print("   Press Ctrl+C when ready to stop.")

    # Keep the script running so server stays active
    try:
        client = get_canvas_client()
        client.wait_for_server()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")


def run_single_example(example_name: str) -> None:
    """Run a single example by name.

    Args:
        example_name: Name of the example to run
                     ('hello', 'weather', 'vacation', 'investment')
    """
    # Check if server is running first
    client = get_canvas_client()
    if not client.check_server_health():
        print("❌ Canvas server is not running!")
        print("\n📋 Please start the canvas server first:")
        print("   llm-canvas server")
        print("\n📖 For more information, see: doc/start_canvas_server.md")
        print("🌐 Once started, run this script again.")
        return

    examples = {
        "hello": create_hello_canvas,
        "weather": weather_inquiry,
        "vacation": create_vacation_planning,
        "investment": investment_decision,
    }

    if example_name not in examples:
        print(f"❌ Unknown example: {example_name}")
        print(f"Available examples: {', '.join(examples.keys())}")
        return

    print(f"🚀 Running {example_name} example...")
    try:
        examples[example_name]()
        print("\n🌐 Canvas available at: http://127.0.0.1:8000")
    except RuntimeError as e:
        print(f"❌ Error: {e}")
        print("\n📋 Please start the canvas server first:")
        print("   llm-canvas server")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        run_single_example(sys.argv[1])
    else:
        run_all_examples()

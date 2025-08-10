"""Test script to verify the server health check functionality."""

from examples.shared_client import get_canvas_client


def test_server_health():
    """Test the server health check functionality."""
    client = get_canvas_client()

    print("🔍 Testing server health check...")

    # Test server health
    is_healthy = client.check_server_health()

    if is_healthy:
        print("✅ Server is running and healthy!")
        print(f"🌐 Server URL: http://{client.server_host}:{client.server_port}")

        # Try to create a canvas
        try:
            canvas = client.create_canvas("Test Canvas", "Testing server connection")
            print(f"✅ Successfully created canvas: {canvas.canvas_id}")
        except RuntimeError as e:
            print(f"❌ Error creating canvas: {e}")
    else:
        print("❌ Server is not running or not healthy")
        print("\n📋 To start the server, run:")
        print("   llm-canvas server")
        print("\n📖 For more information, see: doc/start_canvas_server.md")


if __name__ == "__main__":
    test_server_health()

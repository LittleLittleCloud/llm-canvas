# CanvasClient - One-Stop Canvas Management

The `CanvasClient` class provides a high-level, user-friendly interface for managing canvases and running the web UI/API server. It's designed to be the primary entry point for most users.

## Quick Start

```python
from llm_canvas import CanvasClient

# Create a client
client = CanvasClient()

# Create a canvas
canvas = client.create_canvas("My Chat", "A conversation about AI")

# Add messages
user_msg_id = client.add_message(canvas.canvas_id, "Hello!", "user")
client.add_message(canvas.canvas_id, "Hi there! How can I help?", "assistant", parent_node_id=user_msg_id)

# Run the web UI
client.run_server()  # Blocks until server stops
# OR
client.run_server(background=True)  # Runs in background
client.wait_for_server()  # Block until server stops
```

## Features

### Canvas Management

- **Create canvases**: `create_canvas(title, description, canvas_id)`
- **List canvases**: `list_canvases()`
- **Get canvas**: `get_canvas(canvas_id)`
- **Remove canvas**: `remove_canvas(canvas_id)`
- **Get summaries**: `get_canvas_summaries()`

### Message Management

- **Add messages**: `add_message(canvas_id, content, role, parent_node_id, meta, message_id)`
- **Support for branching**: Specify `parent_node_id` to create conversation branches
- **Rich content**: Support for text, tool use, and tool result blocks

### Server Management

- **Run server**: `run_server(host, port, background)`
- **Background mode**: Run server in background thread
- **Wait for server**: `wait_for_server()` to block until server stops
- **Check status**: `is_server_running()`

### Convenience Features

- **Example canvas**: `create_example_canvas(title)` creates a pre-filled example
- **Registry access**: Built-in `CanvasRegistry` for managing multiple canvases
- **Automatic timestamps**: Registry tracks last update times

## Example Usage

### Basic Chat Application

```python
from llm_canvas import CanvasClient

client = CanvasClient()

# Create a conversation
chat = client.create_canvas("AI Chat", "Conversation with AI assistant")

# Add messages
user_msg = client.add_message(chat.canvas_id, "What is machine learning?", "user")
ai_msg = client.add_message(
    chat.canvas_id,
    "Machine learning is a subset of AI that enables computers to learn from data...",
    "assistant",
    parent_node_id=user_msg
)

# Create branches
client.add_message(chat.canvas_id, "Can you give me examples?", "user", parent_node_id=ai_msg)
client.add_message(chat.canvas_id, "How does it differ from AI?", "user", parent_node_id=ai_msg)

# Start the web UI
client.run_server(port=8080)
```

### Multi-Canvas Application

```python
from llm_canvas import CanvasClient

client = CanvasClient()

# Create multiple canvases for different purposes
research = client.create_canvas("Research Notes", "Collecting research findings")
brainstorm = client.create_canvas("Brainstorming", "Creative ideas session")
chat = client.create_canvas("AI Assistant", "General chat with AI")

# Add content to each
client.add_message(research.canvas_id, "Key findings from paper XYZ:", "user")
client.add_message(brainstorm.canvas_id, "Ideas for new features:", "user")
client.add_message(chat.canvas_id, "Hello AI!", "user")

# Run server to manage all canvases
print(f"Managing {len(client)} canvases")
client.run_server(background=True)

# Keep adding content while server runs
client.add_message(research.canvas_id, "Finding 1: Performance improved by 20%", "user")

# Server will serve all canvases at:
# http://localhost:8000/api/v1/canvas/list
# http://localhost:8000/api/v1/canvas?id=<canvas_id>
```

### Tool Integration Example

```python
from llm_canvas import CanvasClient

client = CanvasClient()
canvas = client.create_canvas("Tool Demo", "Demonstrating tool usage")

# User asks a question
user_msg = client.add_message(canvas.canvas_id, "What's the weather like?", "user")

# Assistant uses a tool
tool_msg = client.add_message(
    canvas.canvas_id,
    [
        {"type": "text", "text": "I'll check the weather for you."},
        {
            "type": "tool_use",
            "id": "weather_001",
            "name": "get_weather",
            "input": {"location": "San Francisco"}
        }
    ],
    "assistant",
    parent_node_id=user_msg
)

# Tool result
result_msg = client.add_message(
    canvas.canvas_id,
    [
        {
            "type": "tool_result",
            "tool_use_id": "weather_001",
            "content": '{"temperature": 72, "condition": "sunny"}'
        }
    ],
    "user",
    parent_node_id=tool_msg
)

# Assistant responds with weather info
client.add_message(
    canvas.canvas_id,
    "It's 72°F and sunny in San Francisco!",
    "assistant",
    parent_node_id=result_msg
)

client.run_server()
```

## API Reference

### CanvasClient

#### Constructor

```python
client = CanvasClient()
```

#### Methods

**Canvas Management:**

- `create_canvas(title=None, description=None, canvas_id=None) -> Canvas`
- `get_canvas(canvas_id: str) -> Optional[Canvas]`
- `list_canvases() -> List[Canvas]`
- `get_canvas_summaries() -> List[CanvasSummary]`
- `remove_canvas(canvas_id: str) -> bool`

**Message Management:**

- `add_message(canvas_id, content, role="user", parent_node_id=None, meta=None, message_id=None) -> Optional[str]`
- `get_canvas_data(canvas_id: str) -> Optional[CanvasData]`

**Server Management:**

- `run_server(host="127.0.0.1", port=8000, background=False) -> None`
- `wait_for_server() -> None`
- `is_server_running() -> bool`

**Convenience:**

- `create_example_canvas(title="Example Chat") -> Canvas`
- `__len__() -> int` (number of canvases)
- `__repr__() -> str`

## Benefits over Direct Canvas Usage

1. **Simplified API**: One class handles canvas creation, message management, and server operations
2. **Built-in Registry**: Automatic management of multiple canvases
3. **Unified Server**: Single server instance serves all canvases
4. **Better Error Handling**: Graceful handling of missing canvases and other errors
5. **Convenience Methods**: Pre-built examples and common operations
6. **Background Server**: Easy background server management with proper threading

The `CanvasClient` is the recommended way to use the llm_canvas library for most applications.

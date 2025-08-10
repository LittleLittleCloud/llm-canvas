# llm_canvas

Visualize LLM conversations (branches, retries, tool calls) in a browser.

## Quick Start with uv

### Installation

```bash
# Install uv (if not already installed)
# Windows: irm https://astral.sh/uv/install.ps1 | iex
# macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh

# Install llm_canvas
uv add llm-canvas[server]
```

### Python SDK

```python
from llm_canvas import Canvas

canvas = Canvas()
user = canvas.add_message("Plan a 3 day trip to Paris", role="user")
assistant_txt = "Day 1: Visit the Louvre..."
canvas.add_message(assistant_txt, role="assistant", parent_node=user)
canvas.save("trip.json")
```

### Serve with Web UI

```bash
# Option 1: Using CLI command
uv run llm-canvas-serve --canvas trip.json

# Option 2: Using uvicorn directly
uv run uvicorn llm_canvas.server:main --reload

# Option 3: From Python
python -c "
from llm_canvas import Canvas
from llm_canvas.canvas import create_app
import uvicorn

canvas = Canvas.load('trip.json')  # or Canvas() for empty
app = create_app(canvas)
uvicorn.run(app, port=8000)
"
```

## Development

### Build from Source

```bash
# Clone and build
git clone <your-repo>
cd llm_canvas

# Windows
./build.ps1

# macOS/Linux
./build.sh

# Manual steps
uv sync --extra server --extra dev
cd web_ui && npm ci && npm run build && cd ..
cp -r web_ui/dist llm_canvas/static
uv build
```

### Development Server

```bash
# Backend with auto-reload
uv run uvicorn llm_canvas.server:main --reload --port 8000

# Frontend dev server (separate terminal)
cd web_ui
npm run dev  # runs on port 5173
```

### Package and Distribute

```bash
uv build                    # Creates wheel in dist/
uv publish                  # Publish to PyPI (requires auth)
uv pip install dist/*.whl   # Install local wheel
```

## Examples

The `examples/` directory contains several demonstrations of the Canvas API:

### Starting the Canvas Server

Before running any examples, you must start the canvas server manually:

```bash
# Start the local canvas server
llm-canvas server

# Or specify host and port
llm-canvas server --host 127.0.0.1 --port 8000
```

For more details, see: `doc/start_canvas_server.md`

### Running Examples with Shared Client

All examples use a shared `CanvasClient` instance that connects to the running server:

```bash
# Run all examples at once (recommended)
python -m examples.run_examples

# Run a specific example
python -m examples.run_examples hello     # Simple conversation
python -m examples.run_examples weather   # Tool usage example
python -m examples.run_examples vacation  # Branched conversations
python -m examples.run_examples investment # Complex branching + tools

# Run individual examples
python -m examples.hello_example
python -m examples.weather_tool_example
python -m examples.vacation_planning_example
python -m examples.investment_decision_example
```

### Example Features

- **Hello Example**: Basic user-assistant conversation
- **Weather Tool**: Demonstrates tool calls and results
- **Vacation Planning**: Shows conversation branching (Japan vs Italy)
- **Investment Decision**: Complex example with branching + multiple tool calls

All examples connect to the canvas server at `http://127.0.0.1:8000` where you can view and interact with all created canvases in a single interface. If the server is not running, the examples will prompt you to start it manually.

## Features

- 🌳 **Tree View**: Visualize conversation branches and forks
- 🔄 **Real-time Updates**: SSE streaming for live canvas updates
- 🎨 **Rich Content**: Support for text, code, images (extensible)
- 📦 **Easy Integration**: Simple Python API for any LLM client
- 🚀 **Self-contained**: Bundled web UI, no external dependencies

## License

MIT

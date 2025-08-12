# LLM Canvas Project Structure

This project has been reorganized into separate components for better modularity:

## Project Structure

```
├── client/                 # High-level Canvas client
│   ├── __init__.py
│   ├── canvas.py           # Canvas class
│   ├── canvas_client.py    # CanvasClient class
│   ├── canvas_registry.py  # CanvasRegistry class
│   └── types.py           # Type definitions
├── server/                 # FastAPI server components
│   ├── __init__.py
│   ├── api.py             # API endpoints
│   ├── cli.py             # CLI interface
│   ├── registry.py        # Local registry implementation
│   ├── server.py          # FastAPI app creation
│   ├── canvas.py          # Canvas class (server copy)
│   └── types.py           # Type definitions (server copy)
├── generated_client/       # Auto-generated OpenAPI client
│   └── __init__.py        # (Generated files will be here)
├── web_ui/                # Frontend React application
├── llm_canvas/            # Main package (imports from above)
├── examples/              # Example scripts
├── tests/                 # Test suite
└── scripts/               # Build and generation scripts
```

## Installation

```bash
# Install the complete package (server + client)
pip install llm-canvas

# Or install with specific components
pip install llm-canvas[server]  # Server components
pip install llm-canvas[client]  # Client components only
```

## Usage

### Server

```python
from server import create_app

app = create_app()
```

### Client

```python
from client import CanvasClient

client = CanvasClient()
```

### Combined (as before)

```python
import llm_canvas

# All components available through main package
client = llm_canvas.CanvasClient()
app = llm_canvas.create_app()
```

## Development

### Generate OpenAPI Client

```bash
# Generate the OpenAPI schema and Python client
uv run python scripts/generate_client.py
```

This will:

1. Generate the OpenAPI schema to `schemas/openapi.json`
2. Generate the Python client to `generated_client/`
3. Update dependencies accordingly

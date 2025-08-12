# LLM Canvas Project Structure

This project is organized into separate components for better modularity and maintainability:

## Project Structure

```
├── llm_canvas/             # Main package
│   ├── __init__.py
│   ├── client/            # High-level Canvas client
│   │   ├── __init__.py
│   │   ├── canvas.py      # Canvas class
│   │   └── canvas_client.py # CanvasClient class
│   └── server/            # FastAPI server components
│       ├── __init__.py
│       ├── api.py         # API endpoints
│       ├── canvas_registry.py # Canvas registry implementation
│       ├── cli.py         # CLI interface
│       ├── registry.py    # Local registry implementation
│       ├── server.py      # FastAPI app creation
│       └── types.py       # Type definitions
├── generated_client/       # Auto-generated OpenAPI client
│   └── __init__.py        # (Generated files will be here)
├── web_ui/                # Frontend Vite/React application
│   ├── src/              # React source files
│   ├── dist/             # Built frontend assets
│   ├── package.json      # Frontend dependencies
│   ├── vite.config.ts    # Vite configuration
│   └── ...              # Other frontend config files
├── examples/              # Example scripts and usage demos
│   ├── hello_example.py
│   ├── investment_decision_example.py
│   ├── vacation_planning_example.py
│   ├── weather_tool_example.py
│   ├── run_examples.py   # Script to run all examples
│   └── shared_client.py  # Shared client configuration
├── tests/                 # Test suite
│   ├── test_canvas.py
│   └── ...
├── scripts/               # Build and generation scripts
│   ├── generate_client.py     # Generate OpenAPI client
│   ├── generate_openapi_schema.py # Generate OpenAPI schema
│   └── ...
├── doc/                   # Documentation
│   ├── business_plan.md
│   ├── canvas_client.md
│   ├── client_generation.md
│   ├── manage_canvas.md
│   ├── start_canvas_server.md
│   ├── server/           # Server documentation
│   └── web_ui/           # Web UI documentation
├── schemas/               # OpenAPI schema files
│   └── openapi.json      # Generated OpenAPI schema
├── dist/                  # Build artifacts
├── build.py              # Main build script
├── build_frontend.py     # Frontend build script
├── build.ps1             # PowerShell build script
├── build.sh              # Bash build script
├── pyproject.toml        # Python project configuration
├── uv.lock               # UV dependency lock file
└── README.md             # Project README
```

## Installation

```bash
# Install the complete package (server + client)
pip install llm-canvas

# Or install with specific components
pip install llm-canvas[server]  # Server components
pip install llm-canvas[client]  # Client components only
pip install llm-canvas[dev]     # Development dependencies

# For development, install from source with uv
uv pip install -e .
```

## Usage

### Server

```python
from llm_canvas.server import create_app

app = create_app()
```

### Client

```python
from llm_canvas.client import CanvasClient

client = CanvasClient()
```

### Combined (backward compatibility)

```python
import llm_canvas

# All components available through main package
client = llm_canvas.CanvasClient()
app = llm_canvas.create_app()
```

### Command Line Interface

```bash
# Start the server
llm-canvas

# Generate OpenAPI schema
llm-canvas-generate-openapi
```

## Development

### Build the Project

```bash
# Build the complete project (backend + frontend)
python build.py

# Or use platform-specific scripts
# Windows PowerShell:
.\build.ps1

# Unix/Linux/macOS:
./build.sh

# Build only the frontend
python build_frontend.py
```

### Generate OpenAPI Client

```bash
# Generate the OpenAPI schema and Python client
uv run python scripts/generate_client.py
```

This will:

1. Generate the OpenAPI schema to `schemas/openapi.json`
2. Generate the Python client to `generated_client/`
3. Update dependencies accordingly

### Running Tests

```bash
# Run all tests
pytest

# Run specific test files
pytest tests/test_canvas.py
```

### Running Examples

```bash
# Run all examples
python examples/run_examples.py

# Run individual examples
python examples/hello_example.py
python examples/investment_decision_example.py
python examples/vacation_planning_example.py
python examples/weather_tool_example.py
```

### Frontend Development

```bash
cd web_ui

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## Package Configuration

The project uses `pyproject.toml` for configuration with the following key features:

- **Build System**: Uses `hatchling` with version control support
- **Scripts**: Provides `llm-canvas` and `llm-canvas-generate-openapi` CLI commands
- **Optional Dependencies**: Separate server, client, and dev dependency groups
- **Code Quality**: Configured with `ruff`, `mypy`, and `pytest`
- **Packaging**: Includes built frontend assets in the wheel distribution

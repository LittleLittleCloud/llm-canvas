# Start the LLM Canvas Local Server

LLM Canvas offers a **free & open source** local server that provides complete visualization capabilities for Large Language Model conversations. The local deployment runs entirely in your environment, giving you full privacy control while offering all core features.

## Important Limitation

⚠️ **No Data Persistence** - The local server uses session-based storage only:

- Data is lost when the server restarts
- No backup or recovery mechanisms
- No cross-session data retention

_For permanent data storage and cross-device access, consider our [cloud-based plans](https://llm-canvas.com/pricing)._

## Installation

To install the local server, you need Python and pip installed. Then run:

```bash
pip install llm-canvas[server]
```

## Running the Server

Start the local server with the following command:

```bash
llm-canvas server --port 8000 --log-level info
```

### Command Options

- `--host`: Specify the host address (default: 127.0.0.1)
- `--port`: Specify the port number (default: 8000)
- `--log-level`: Set logging level (debug, info, warning, error)

### Alternative Commands

You can also use these commands:

```bash
# Just start the server with defaults
llm-canvas server

# Show help for server options
llm-canvas server --help
```

## Connecting to the Server

Once the server is running, you can connect to it using the `CanvasClient` and start creating canvases and messages:

```python
canvas_client = CanvasClient(host="localhost", port=8000)
canvas = canvas_client.create_canvas(
    title="My Local Canvas",
    description="A canvas for local LLM interactions"
)

# Add messages
user_message = canvas.commit_message({
    "content": "Hello, local world!",
    "role": "user"
})
```

## Who Should Use the Local Server?

The local server is perfect for:

- **Individual developers and researchers** exploring LLM conversations
- **Open source community contributors** building on the platform
- **Privacy-conscious users** who want complete data control
- **Development and testing environments** where persistence isn't needed

## Getting Started

1. Install the package: `pip install llm-canvas[server]`
2. Start the server: `llm-canvas server`
3. Open your browser to `http://localhost:8000`
4. Begin visualizing your LLM conversations!

_Note: All data will be session-based. For permanent storage, explore our cloud options._

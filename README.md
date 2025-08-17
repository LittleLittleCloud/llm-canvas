# LLM Canvas

**Visualize and navigate Large Language Model conversations like never before.**

LLM Canvas allows you to programmatically create interactive, branching conversation trees. Build complex conversation structures, explore different response paths, and visualize tool calls in a beautiful web interface — all while maintaining complete privacy with local deployment.

[![PyPI](https://img.shields.io/pypi/v/llm-canvas)](https://pypi.org/project/llm-canvas/)
![License](https://img.shields.io/badge/License-MIT-green)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)

## 📰 News

**🎉 August 2025**: LLM Canvas v0.1.1 released with improved branching API and enhanced web UI

## 🌟 Key Features

- **🌳 Branching Conversations**: Create and explore multiple conversation paths from any message
- **🔧 Tool Call Visualization**: See how your LLM uses tools with clear input/output flows
- **📦 Zero Dependencies**: Self-contained with built-in web UI

## 🚀 Quick Start

### Installation

```bash
pip install llm-canvas
llm-canvas server --port 8000
```

### Basic Usage

```python
from llm_canvas import CanvasClient

# Create a client and canvas
client = CanvasClient()
canvas = client.create_canvas("My Conversation", "Exploring LLM interactions")

# Add messages
user_msg_id = client.add_message(canvas.canvas_id, "What is machine learning?", "user")
client.add_message(
    canvas.canvas_id,
    "Machine learning is a subset of AI that enables computers to learn from data...",
    "assistant",
    parent_node_id=user_msg_id
)
```

### Start Local Server

```bash
# Start the local server
llm-canvas server --port 8000

# Server starts at http://localhost:8000
# Create and view your canvases in the web interface
```

## 💡 What Makes LLM Canvas Special?

### Git-Like Conversation Management

Just like Git manages code versions, LLM Canvas manages conversation versions:

- **Branches**: Multiple conversation paths within a single canvas
- **Commits**: Each message is committed to a branch
- **Checkout**: Switch between different conversation branches
- **Merge**: Explore different paths and outcomes

### Advanced Use Cases

#### 1. **Conversation Branching**

```python
# Create different response paths
main_branch = canvas.checkout("main", create_if_not_exists=True)
main_branch.commit_message({"role": "user", "content": "Explain quantum computing"})

# Create alternative explanations
simple_branch = canvas.checkout("simple-explanation", create_if_not_exists=True)
simple_branch.commit_message({"role": "assistant", "content": "Quantum computing uses quantum mechanics..."})

technical_branch = canvas.checkout("technical-explanation", create_if_not_exists=True)
technical_branch.commit_message({"role": "assistant", "content": "Quantum computing leverages superposition and entanglement..."})
```

#### 2. **Tool Usage Visualization**

```python
# Visualize how LLMs use tools
client.add_message(canvas_id, [
    {"type": "text", "text": "I'll check the weather for you."},
    {"type": "tool_use", "id": "weather_001", "name": "get_weather", "input": {"location": "San Francisco"}}
], "assistant")

client.add_message(canvas_id, [
    {"type": "tool_result", "tool_use_id": "weather_001", "content": '{"temperature": 72, "condition": "sunny"}'}
], "user")
```

## 🎯 Perfect For

- **🔬 AI Researchers**: Analyze conversation patterns and model behavior
- **👨‍💻 LLM Developers**: Debug and optimize chatbot interactions
- **📚 Educators**: Teach AI concepts with visual examples
- **🚀 Startups**: Prototype and demo conversational AI applications
- **🔒 Privacy-Conscious Users**: Keep all data local and secure

## 📚 Examples & Documentation

### Interactive Examples

Run the included examples to see LLM Canvas in action:

```bash
# Start the server first
llm-canvas server

# Then run examples (in a new terminal)
python -m examples.run_examples

# Or run specific examples:
python -m examples.hello_example          # Basic conversation
python -m examples.weather_tool_example   # Tool usage demo
python -m examples.vacation_planning_example  # Conversation branching
python -m examples.investment_decision_example  # Complex multi-branch scenario
```

Visit `http://localhost:8000` to see all your canvases in the web interface!

### Key Concepts

| Concept      | Description                       | Like Git       |
| ------------ | --------------------------------- | -------------- |
| **Canvas**   | A workspace for LLM conversations | Repository     |
| **Branch**   | Linear conversation threads       | Branch         |
| **Message**  | Individual conversation entries   | Commit         |
| **Checkout** | Switch between conversation paths | `git checkout` |
| **Commit**   | Add messages to a branch          | `git commit`   |

📝 **See detailed examples** → [examples/README.md](examples/README.md)

## 🛠️ Development

### Local Development Setup

```bash
git clone https://github.com/LittleLittleCloud/llm_canvas.git
cd llm_canvas

# Install dependencies
pip install -e ".[server,dev]"

# Build frontend
cd web_ui && npm install && npm run build && cd ..

# Start development server
llm-canvas server --port 8000
```

### Frontend Development

```bash
# Start backend server
llm-canvas server --port 8000

# Start frontend dev server (in another terminal)
cd web_ui
npm run dev  # Runs on http://localhost:5173
```

## 🔒 Privacy & Data

**Local-First Philosophy**: Your conversations stay on your machine.

- ✅ **No external API calls** for the visualization server
- ✅ **No data collection** or telemetry
- ✅ **No account required** for local usage
- ✅ **Full control** over your conversation data
- ⚠️ **Session-based storage** (data lost on server restart)

> **Note**: The local server does not persist data between sessions. For permanent storage, consider our [cloud plans](https://llm-canvas.com/pricing) or implement your own persistence layer.

## 🌐 Deployment Options

### Local Server (Free & Open Source)

- ✅ Complete privacy control
- ✅ All visualization features
- ❌ No data persistence
- ❌ Session-only storage

### Cloud Server (Coming Soon)

- ✅ Permanent data storage
- ✅ Cross-device access
- ✅ Team collaboration
- ✅ Backup & recovery

## 🤝 Contributing

We welcome contributions! LLM Canvas is open source and community-driven.

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/LittleLittleCloud/llm_canvas/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/LittleLittleCloud/llm_canvas/discussions)
- � **Pull Requests**: See our [Contributing Guide](CONTRIBUTING.md)
- 📖 **Documentation**: Help improve our docs

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

**Built with ❤️ for the AI community**

Transform your LLM conversations from linear logs into navigable, visual experiences. Start exploring today!

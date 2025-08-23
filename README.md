<p align="center">
    <img src="web_ui/public/assets/logo-icon-badge.svg" width="120" height="120" alt="LLM Canvas logo" />
  
</p>

<h1 align="center">LLM Canvas</h1>

<p align="center"><strong>Visualize complex LLM conversation flows in infinite canvas.</strong></p>

<p align="center">
    <a href="https://pypi.org/project/llm-canvas/"><img src="https://img.shields.io/pypi/v/llm-canvas" alt="PyPI" /></a>
    <a href="https://littlelittlecloud.github.io/llm-canvas/"><img src="https://img.shields.io/badge/Website-LLM_Canvas-blue" alt="Website" /></a>
    <img src="https://img.shields.io/badge/License-MIT-green" alt="License MIT" />
    <img src="https://img.shields.io/badge/Python-3.9%2B-blue" alt="Python 3.9+" />
</p>

As LLM applications evolve, conversation flows become increasingly complex. Conversations may branch into multiple paths, run in parallel, or require summarization across different threads. Managing and understanding these intricate conversation flows becomes a significant challenge in LLM ops.

LLM Canvas solves this by providing a powerful visualization tool for complex conversation flows. Create branching conversation trees, explore different response paths, and visualize tool interactions through an intuitive web interface — all while maintaining complete privacy with local deployment.

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
```

### Start Local Server

```bash
# Start the local server
llm-canvas server --port 8000

# Server starts at http://localhost:8000
# Create and view your canvases in the web interface
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

### Use Cases

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

📝 **More examples** → [examples/README.md](examples/README.md)

## 🤝 Contributing

We welcome contributions! LLM Canvas is open source and community-driven.

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/LittleLittleCloud/llm_canvas/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/LittleLittleCloud/llm_canvas/discussions)
- 🔀 **Pull Requests**: See our [Contributing Guide](CONTRIBUTING.md)
- 📖 **Documentation**: Help improve our docs

## LLM Canvas: Story Behind

Check out the [full story](https://dev.to/littlelittlecloud/llm-canvas-the-story-behind-11i6) to learn about the inspiration and development journey of LLM Canvas.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

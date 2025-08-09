# Canvas Management Guide

## Overview

The **Canvas** is the central concept in LLM Canvas. It represents a conversation workspace that can contain multiple messages, branches, and tool calls. Unlike traditional linear chat logs, a canvas allows for complex, non-linear interactions with sophisticated branching and history management.

## Key Concepts

Canvas management is inspired by Git version control, so if you're familiar with Git, you'll find these concepts familiar:

- **Canvas**: A workspace for your LLM conversations
- **Messages**: Individual conversation entries (user or assistant messages)
- **Branches**: Different conversation paths within the same canvas
- **HEAD**: The current position in your conversation history
- **Commit**: Adding a new message to the conversation history

## Getting Started

### 1. Creating a New Canvas

To start working with LLM Canvas, create a new canvas using the `create_canvas` method from `canvasClient`:

```python
from llm_canvas import canvasClient

# Create a canvas with name and description
canvas = canvasClient.create_canvas(
    name="My First Canvas",
    description="A canvas for exploring LLM interactions"
)
```

### 2. Adding Messages to Your Canvas

Once you have a canvas, you can add messages using the `commit_message` method. This method returns a message object containing metadata like message ID and timestamp.

```python
# Add a user message
user_message = canvas.commit_message({
    "content": "Hello, world!",
    "role": "user"
})

# Add an assistant response
assistant_message = canvas.commit_message({
    "content": "Hello! How can I help you today?",
    "role": "assistant"
})
```

> **Important:** The `commit_message` method always adds messages after the current HEAD of the canvas. The newly committed message becomes the new HEAD.

## Working with Branches

Branches allow you to explore different conversation paths from the same starting point. This is useful for comparing different responses or exploring alternative conversation flows.

### Creating and Switching Branches

```python
# Switch to the main branch (created by default)
canvas.checkout(name="main", description="Main conversation thread")

# Add a message to main branch
hello_main = canvas.commit_message({
    "content": "Hello, main branch!",
    "role": "user"
})

# Create and switch to a new branch
canvas.checkout(
    name="Alternative Path",
    description="Exploring different responses",
    create_if_not_exists=True
)

# Add message to the new branch
canvas.commit_message({
    "content": "Hello, alternative branch!",
    "role": "user"
})
```

### Branching from Specific Messages

You can create branches that start from any specific message in your conversation history:

```python
# Create a branch starting from a specific message
canvas.checkout(
    name="Branch from Hello",
    description="New path from the hello message",
    create_if_not_exists=True,
    commit_message=hello_main  # Start from this message
)

# Add messages to this branch
canvas.commit_message({
    "content": "This is a different direction!",
    "role": "user"
})
```

After these operations, your canvas structure looks like this:

```
main: hello_main

Alternative Path: hello_main → "Hello, alternative branch!"

Branch from Hello: hello_main → "This is a different direction!"
```

## Managing Your Canvas

### Viewing All Branches

To see all branches in your canvas and their latest messages:

```python
branches = canvas.list_branches()

for branch in branches:
    print(f"Branch: {branch['name']}")
    print(f"Latest message: {branch['latest_commit']['content']}")
    print("---")
```

### Deleting Branches

Remove branches you no longer need:

```python
# Delete a specific branch
canvas.delete_branch(name="Alternative Path")
```

> **Warning:** Branch deletion is permanent and cannot be undone. Make sure you no longer need the branch before deleting it.

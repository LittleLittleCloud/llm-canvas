# Canvas Management Guide

## Overview

The **Canvas** is the central concept in LLM Canvas. It represents a conversation workspace that can contain multiple messages, branches, and tool calls. Unlike traditional linear chat logs, a canvas allows for complex, non-linear interactions with sophisticated branching and history management.

## Key Concepts

Canvas management is inspired by Git version control, so if you're familiar with Git, you'll find these concepts familiar:

- **Canvas**: A workspace for your LLM conversations that can contain multiple branches. Each canvas starts with a default branch called 'main'
- **Branch**: A linear chat history within a canvas. All messages are committed to branches, not directly to the canvas. Each branch has a **Branch Head** that points to the latest message in that branch. When you checkout to a branch, you'll be positioned at the Branch Head by default. You can also work in a **Detached Head** state by using the checkout API with a specific message ID, where you're working from a specific message that isn't necessarily the latest in any branch
- **Commit Message**: Adding a new message to the current working branch
- **Merge Branch**: Combining conversation paths from multiple branches into a single branch. This allows you to integrate insights, responses, or tool outputs from different conversation threads. Merging preserves the history from all participating branches while creating a unified conversation flow

## Message Types

You can commit messages with various formats and content types to **Canvas**. For detailed information about supported message formats and content types, see [Supported Message Types](support_message_type.md).

## Getting Started

### 1. Creating a New Canvas

To start working with LLM Canvas, create a new canvas using the `create_canvas` method from `canvas_client`:

```python
from llm_canvas import canvas_client

# Create a canvas with title and description
canvas = canvas_client.create_canvas(
    title="My First Canvas",
    description="A canvas for exploring LLM interactions"
)
```

### 2. Working with Branches

Before adding messages to your canvas, you need to understand that **all messages are committed to branches, not directly to the canvas**. A canvas can contain multiple branches, and you must have an active working branch to commit messages.

#### Creating and Switching to a Branch

When you create a canvas, you need to create or switch to a branch before adding messages. The `checkout` method returns a branch object that you can use for future operations:

```python
# Switch to the main branch (you can create it if it doesn't exist)
branch = canvas.checkout(name="main", description="Main conversation thread", create_if_not_exists=True)
```

#### Adding Messages to Your Current Branch

Once you have a branch object, you can add messages using the `commit_message` method on the branch. This method commits messages to the branch and returns a message object containing metadata like message ID and timestamp.

```python
# Add a user message to the branch
user_message = branch.commit_message({
    "content": "Hello, world!",
    "role": "user"
})

# Add an assistant response to the branch
assistant_message = branch.commit_message({
    "content": "Hello! How can I help you today?",
    "role": "assistant"
})
```

### 3. Updating Existing Messages

You can update an existing message by using the `update_message` method on the branch. This allows you to modify the content or metadata of a message in the branch. This feature is particularly useful for streaming responses, where you can commit an initial message and then update it incrementally as more content arrives.

```python
# Update the user message
branch.update_message(user_message["id"], {
    "content": "Hello, world! (updated)",
    "role": "user"
})
```

### 4. Switching Between Branches

You can switch your working branch at any time to work on different conversation paths. Each checkout returns a branch object for future operations:

```python
# Switch to a different existing branch
experimental_branch = canvas.checkout(name="experimental")

# Create and switch to a new branch
new_branch = canvas.checkout(
    name="new-feature",
    description="Testing new features",
    create_if_not_exists=True
)

# Now you can commit messages to the new branch
new_branch.commit_message({
    "content": "Testing new feature",
    "role": "user"
})
```

## Working with Multiple Branches

Branches are linear chat histories within a canvas that allow you to organize and explore different conversation paths. Each branch maintains its own sequence of messages, and you can switch between branches to work on different aspects of your conversation.

### Creating Multiple Branches

```python
# Switch to the main branch and get branch reference
main_branch = canvas.checkout(name="main", description="Main conversation thread", create_if_not_exists=True)

# Add a message to main branch
hello_main = main_branch.commit_message({
    "content": "Hello, main branch!",
    "role": "user"
})

# Create and switch to a new branch
alt_branch = canvas.checkout(
    name="Alternative Path",
    description="Exploring different responses",
    create_if_not_exists=True
)

# Add message to the new branch
alt_branch.commit_message({
    "content": "Hello, alternative branch!",
    "role": "user"
})
```

### Branching from Specific Messages

You can create branches that start from any specific message in your conversation history:

```python
# Create a branch starting from a specific message
hello_branch = canvas.checkout(
    name="Branch from Hello",
    description="New path from the hello message",
    create_if_not_exists=True,
    commit_message=hello_main  # Start from this message
)

# Add messages to this branch
hello_branch.commit_message({
    "content": "This is a different direction!",
    "role": "user"
})
```

#### Example: Starting a New Conversation Path

Here's a practical example of starting a branch by committing after a specific message. Imagine you want to explore a different response to an earlier question:

```python
# First, let's say you have some conversation history in main branch
main_branch = canvas.checkout(name="main", create_if_not_exists=True)

# Add some initial conversation
question_msg = main_branch.commit_message({
    "content": "What's the best programming language for web development?",
    "role": "user"
})

response_msg = main_branch.commit_message({
    "content": "JavaScript is widely used for web development...",
    "role": "assistant"
})

# Now, let's create a new branch starting after the question to explore a different response
alt_response_branch = canvas.checkout(
    name="Alternative Response",
    description="Exploring a different answer to the programming language question",
    create_if_not_exists=True,
    commit_message=question_msg  # Start from the question message
)

# Add a different response in this branch
alt_response_branch.commit_message({
    "content": "Python is an excellent choice for web development because of its simplicity and powerful frameworks like Django and Flask...",
    "role": "assistant"
})

# Continue the conversation in this alternative path
alt_response_branch.commit_message({
    "content": "Can you tell me more about Django?",
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
    print(f"Latest message: {branch['latest_commit_message']['content']}")
    print("---")
```

### Deleting Branches

Remove branches you no longer need:

```python
# Delete a specific branch
canvas.delete_branch(name="Alternative Path")
```

> **Warning:** Branch deletion is permanent and cannot be undone. Make sure you no longer need the branch before deleting it.

# Merge Strategies Comparison

This document illustrates the differences between the two merge strategies available in LLM Canvas: **Linear** and **Explicit**.

## Overview

When merging branches in LLM Canvas, you can choose between two strategies that handle the conversation history differently:

- **Linear Merge**: Creates a simple linear continuation by appending the source branch to the target
- **Explicit Merge**: Creates a merge commit that maintains references to both branch histories

## Visual Comparison

### Before Merge

Both strategies start with the same initial state:

```
Main Branch:
A ── B ── C (HEAD)

Feature Branch:
A ── B ── D ── E (HEAD)
```

### Linear Merge Strategy

**Command**: `canvas.merge("feature", "main", strategy="linear")`

**Result**:

```
Main Branch:
A ── B ── C ── M (HEAD)
              │
              └─ "Merge branch 'feature' into 'main'"

Feature Branch:
A ── B ── D ── E (HEAD)
```

**Characteristics**:

- Creates a simple linear history
- Merge commit `M` is appended after the target branch HEAD (`C`)
- Source branch history (`D → E`) is referenced in metadata but not visually connected
- Results in a clean, linear conversation flow
- Best for: Simple integrations where you want to maintain linear readability

### Explicit Merge Strategy

**Command**: `canvas.merge("feature", "main", strategy="explicit")`

**Result**:

```
Main Branch:
A ── B ── C ──┐
              │
              M (HEAD)
              │
A ── B ── D ── E ──┘

Feature Branch:
A ── B ── D ── E (HEAD)
```

**Characteristics**:

- Creates an explicit merge commit that references both branches
- Merge commit `M` has two parents: `C` (target) and `E` (source)
- Preserves the complete branching history visually
- Both conversation paths remain visible in the graph
- Best for: Complex merges where you want to preserve the full conversation structure

## Code Examples

### Linear Merge Example

```python
from llm_canvas import Canvas

# Create canvas and branches
canvas = Canvas()
main = canvas.checkout("main", create_if_not_exists=True)
feature = canvas.checkout("feature", create_if_not_exists=True)

# Add messages to main
main.commit_message({"role": "user", "content": "What's the weather?"})
main.commit_message({"role": "assistant", "content": "I'll check for you."})

# Add messages to feature branch
feature_msg = main.commit_message({"role": "user", "content": "What's the weather?"})
feature.checkout("feature", commit_message=feature_msg, create_if_not_exists=True)
feature.commit_message({"role": "assistant", "content": "Let me use the weather tool."})
feature.commit_message({"role": "assistant", "content": "It's sunny, 72°F."})

# Linear merge
merge_node = canvas.merge("feature", "main", strategy="linear")
```

### Explicit Merge Example

```python
# Same setup as above...

# Explicit merge
merge_node = canvas.merge("feature", "main", strategy="explicit")

# The merge node will have metadata showing both branches
print(merge_node["meta"]["merged_branches"])  # ["feature", "main"]
print(merge_node["meta"]["source_head_id"])   # Points to feature branch HEAD
```

## When to Use Each Strategy

### Use Linear Merge When:

- You want a clean, linear conversation history
- The merged content should appear as a natural continuation
- You're integrating simple alternative responses
- Simplicity and readability are priorities

**Example Use Cases**:

- Merging an alternative explanation into the main conversation
- Integrating a refined response after experimentation
- Combining simple tool usage results

### Use Explicit Merge When:

- You want to preserve the full branching structure
- Both conversation paths provide valuable context
- You're merging complex, multi-step reasoning
- Traceability of different approaches is important

**Example Use Cases**:

- Merging parallel research paths that both contribute insights
- Combining results from different tool chains
- Integrating multiple expert perspectives on the same question
- Preserving decision trees for later analysis

## Metadata Differences

### Linear Merge Metadata

```python
{
    "merge_type": "linear",
    "source_branch": "feature",
    "target_branch": "main",
    "source_head_id": "node_id_of_source_head"
}
```

### Explicit Merge Metadata

```python
{
    "merge_type": "explicit",
    "source_branch": "feature",
    "target_branch": "main",
    "source_head_id": "node_id_of_source_head",
    "merged_branches": ["feature", "main"]
}
```

## Graph Representation

In the web UI, these strategies will be visualized differently:

- **Linear merges** appear as natural conversation continuations
- **Explicit merges** show clear merge points with multiple incoming paths
- **Node metadata** indicates the merge strategy used for transparency

Both strategies preserve the ability to trace back through the conversation history, but they present different visual and conceptual models for understanding how conversations have been combined.

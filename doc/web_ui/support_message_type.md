# Supported Message Types

This document describes the message types supported by the LLM Canvas web UI.

## Overview

The LLM Canvas supports various message types based on the Anthropic SDK, allowing for rich interactions between users and AI assistants. All message types are defined in `web_ui/src/types.ts`.

## Core Types

### MessageBlock

A union type that represents different types of content blocks within a message:

```typescript
export type MessageBlock =
  | TextBlockParam
  | ToolUseBlockParam
  | ToolResultBlockParam;
```

#### TextBlockParam

- **Purpose**: Contains plain text content
- **Source**: `@anthropic-ai/sdk/resources/messages`
- **Structure**:
  ```typescript
  {
    type: "text";
    text: string;
  }
  ```
- **Properties**:
  - `type`: Always `"text"` to identify this as a text block
  - `text`: The actual text content as a string
- **Usage**: Standard text messages from users or assistants
- **Examples**:
  ```javascript
  {
    type: "text",
    text: "Hello, how can I help you today?"
  }
  ```

#### ToolUseBlockParam

- **Purpose**: Represents a tool call request from the AI assistant
- **Source**: `@anthropic-ai/sdk/resources/messages`
- **Structure**:
  ```typescript
  {
    type: "tool_use";
    id: string;
    name: string;
    input: Record<string, any>;
  }
  ```
- **Properties**:
  - `type`: Always `"tool_use"` to identify this as a tool invocation
  - `id`: Unique identifier for this specific tool call (used for correlation with results)
  - `name`: The name of the tool/function being called
  - `input`: Object containing the parameters passed to the tool
- **Usage**: When the AI assistant needs to invoke a tool or function
- **Examples**:
  ```javascript
  {
    type: "tool_use",
    id: "toolu_01A09q90qw90lkasdjfl",
    name: "get_weather",
    input: {
      location: "San Francisco, CA",
      unit: "celsius"
    }
  }
  ```

#### ToolResultBlockParam

- **Purpose**: Contains the result of a tool execution
- **Source**: `@anthropic-ai/sdk/resources/messages`
- **Structure**:
  ```typescript
  {
    type: "tool_result";
    tool_use_id: string;
    content: string | Array<TextBlockParam | ImageBlockParam>;
    is_error?: boolean;
  }
  ```
- **Properties**:
  - `type`: Always `"tool_result"` to identify this as a tool execution result
  - `tool_use_id`: References the `id` from the corresponding `ToolUseBlockParam`
  - `content`: The result data, can be:
    - A simple string for text results
    - An array of content blocks for complex results (text and images)
  - `is_error`: Optional boolean indicating if the tool execution failed
- **Usage**: Response data from executed tools, provided by the user or system
- **Examples**:

  ```javascript
  // Simple text result
  {
    type: "tool_result",
    tool_use_id: "toolu_01A09q90qw90lkasdjfl",
    content: "The weather in San Francisco is 22°C and sunny."
  }

  // Error result
  {
    type: "tool_result",
    tool_use_id: "toolu_01A09q90qw90lkasdjfl",
    content: "Error: Unable to fetch weather data",
    is_error: true
  }

  // Complex result with multiple content blocks
  {
    type: "tool_result",
    tool_use_id: "toolu_01A09q90qw90lkasdjfl",
    content: [
      {
        type: "text",
        text: "Here's the weather forecast:"
      },
      {
        type: "text",
        text: "Temperature: 22°C\nCondition: Sunny\nHumidity: 65%"
      }
    ]
  }
  ```

### Message

The main message structure:

```typescript
export type Message = {
  content: string | MessageBlock[];
  role: "user" | "assistant" | "system";
};
```

#### Properties:

- **content**: Can be either:
  - A simple string for text-only messages
  - An array of `MessageBlock` objects for complex messages with multiple content types
- **role**: Defines the message sender:
  - `"user"`: Messages from the human user
  - `"assistant"`: Messages from the AI assistant
  - `"system"`: System-level messages (prompts, instructions)

# Supported Message Types

LLM Canvas supports rich message content that goes beyond simple text strings. Messages can contain various types of blocks to represent complex interactions including tool usage.

## Message Structure

Each message in LLM Canvas follows this structure:

```python
class Message(TypedDict):
    content: Union[str, list[MessageBlock]]
    role: Literal["user", "assistant", "system"]
```

## Content Types

**Simple Text Content:**

```python
message = {
    "content": "Hello, world!",
    "role": "user"
}
```

**Rich Content with Blocks:**
Messages can contain a list of different block types for more complex interactions:

```python
message = {
    "content": [
        {"type": "text", "text": "I'll analyze this image and check the weather for you."},
        {
            "type": "image",
            "source": {
                "type": "url",
                "url": "https://example.com/weather-map.jpg"
            }
        },
        {"type": "tool_use", "id": "weather_001", "name": "get_weather", "input": {"location": "San Francisco"}}
    ],
    "role": "assistant"
}
```

## Supported Block Types

LLM Canvas supports four main types of message blocks, compatible with Anthropic's message format:

1. **TextBlockParam**: Plain text content

   ```python
   {"type": "text", "text": "Your message content here"}
   ```

2. **ToolUseBlockParam**: Represents tool/function calls made by the assistant

   ```python
   {
       "type": "tool_use",
       "id": "unique_tool_call_id",
       "name": "function_name",
       "input": {"parameter": "value"}
   }
   ```

3. **ToolResultBlockParam**: Contains the results returned from tool executions

   ```python
   {
       "type": "tool_result",
       "tool_use_id": "unique_tool_call_id",
       "content": "Tool execution result"
   }
   ```

4. **ImageBlockParam**: Represents image content, supporting both base64-encoded images and URL references

   ```python
   # Base64 encoded image
   {
       "type": "image",
       "source": {
           "type": "base64",
           "media_type": "image/jpeg",  # or "image/png", "image/gif", "image/webp"
           "data": "base64_encoded_image_data"
       }
   }

   # URL-referenced image
   {
       "type": "image",
       "source": {
           "type": "url",
           "url": "https://example.com/image.jpg"
       }
   }
   ```

## Role Types

Messages can have one of three roles:

- **`"user"`**: Messages from the human user
- **`"assistant"`**: Messages from the AI assistant
- **`"system"`**: System-level instructions or metadata

This flexible message structure allows LLM Canvas to visualize complex tool-based conversations and multi-step reasoning processes in the web interface.

## Examples

### Simple Text Message

```python
user_message = {
    "content": "What's the weather like today?",
    "role": "user"
}
```

### Image Message

```python
# Message with base64 encoded image
image_message = {
    "content": [
        {"type": "text", "text": "Here's a screenshot of the issue:"},
        {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
            }
        }
    ],
    "role": "user"
}

# Message with URL image
url_image_message = {
    "content": [
        {"type": "text", "text": "Check out this diagram:"},
        {
            "type": "image",
            "source": {
                "type": "url",
                "url": "https://example.com/diagram.jpg"
            }
        }
    ],
    "role": "assistant"
}
```

### Tool Usage Flow

Here's an example of a complete tool usage flow:

```python
# Assistant initiates tool call
assistant_tool_call = {
    "content": [
        {"type": "text", "text": "I'll check the weather for you."},
        {
            "type": "tool_use",
            "id": "weather_001",
            "name": "get_weather",
            "input": {"location": "San Francisco", "units": "celsius"}
        }
    ],
    "role": "assistant"
}

# User provides tool result
tool_result = {
    "content": [
        {
            "type": "tool_result",
            "tool_use_id": "weather_001",
            "content": '{"temperature": 22, "condition": "sunny", "humidity": 65}'
        }
    ],
    "role": "user"
}

# Assistant responds with processed information
assistant_response = {
    "content": "Based on the weather data, it's a beautiful sunny day in San Francisco with a temperature of 22°C and 65% humidity. Perfect for outdoor activities!",
    "role": "assistant"
}
```

This message structure enables LLM Canvas to provide rich visualization of tool interactions, image content, and complex conversation flows in its web interface.

# Server-Side Events (SSE) API Endpoints

This document describes the new SSE endpoints added to the llm_canvas API for real-time event notifications.

## Endpoints

### 1. `/api/v1/canvas/sse` - Global Canvas Events

**Description**: Streams events for all canvas operations (create, update, delete).

**Method**: `GET`

**Parameters**: None

**Event Types**:

- `canvas_created`: Triggered when a new canvas is created
- `canvas_updated`: Triggered when a canvas is updated (future implementation)
- `canvas_deleted`: Triggered when a canvas is deleted

**Event Format**:

```
event: canvas_created
data: {
  "type": "canvas_created",
  "timestamp": 1693423200.123,
  "data": {
    "canvas_id": "uuid-string",
    "created_at": 1693423200.0,
    "root_ids": [],
    "node_count": 0,
    "title": "Canvas Title",
    "description": "Canvas Description",
    "meta": {}
  }
}

event: canvas_deleted
data: {
  "type": "canvas_deleted",
  "timestamp": 1693423200.123,
  "data": {
    "canvas_id": "uuid-string"
  }
}
```

**Headers**:

- `Cache-Control: no-cache`
- `Connection: keep-alive`
- `Access-Control-Allow-Origin: *`

### 2. `/api/v1/canvas/{canvas_id}/sse` - Canvas Message Events

**Description**: Streams events for message operations within a specific canvas.

**Method**: `GET`

**Parameters**:

- `canvas_id` (path): Canvas UUID to stream events for

**Event Types**:

- `message_committed`: Triggered when a new message is added to the canvas
- `message_updated`: Triggered when an existing message is updated
- `message_deleted`: Triggered when a message is deleted (future implementation)

**Event Format**:

```
event: message_committed
data: {
  "type": "message_committed",
  "timestamp": 1693423200.123,
  "canvas_id": "uuid-string",
  "data": {
    "id": "message-uuid",
    "message": {
      "content": "Message content",
      "role": "user"
    },
    "parent_id": null,
    "child_ids": [],
    "meta": {
      "timestamp": 1693423200000
    }
  }
}

event: message_updated
data: {
  "type": "message_updated",
  "timestamp": 1693423200.123,
  "canvas_id": "uuid-string",
  "data": {
    "id": "message-uuid",
    "message": {
      "content": "Updated message content",
      "role": "user"
    },
    "parent_id": null,
    "child_ids": [],
    "meta": {
      "timestamp": 1693423200000
    }
  }
}
```

**Error Responses**:

- `404`: Canvas not found

**Headers**: Same as global canvas SSE endpoint

## Connection Management

- **Heartbeat**: Connections receive heartbeat events every 30 seconds to keep the connection alive
- **Queue Management**: Each connection has a queue with a maximum size of 100 events
- **Automatic Cleanup**: Connections are automatically removed when clients disconnect
- **Error Handling**: Failed connections are gracefully removed from the event dispatcher

## Implementation Details

### Event Dispatcher

The `SSEEventDispatcher` class manages all SSE connections and event distribution:

- **Global Connections**: Set of connections listening for canvas CRUD events
- **Canvas Connections**: Dictionary mapping canvas IDs to sets of connections listening for message events
- **Thread Safety**: Uses asyncio locks for safe concurrent access
- **Background Tasks**: Events are dispatched as background tasks to prevent blocking

### Integration with Existing Endpoints

The following existing endpoints now trigger SSE events:

- `POST /api/v1/canvas` → `canvas_created` event
- `DELETE /api/v1/canvas/{canvas_id}` → `canvas_deleted` event
- `POST /api/v1/canvas/{canvas_id}/messages` → `message_committed` event
- `PUT /api/v1/canvas/{canvas_id}/messages/{message_id}` → `message_updated` event

## Usage Examples

### JavaScript Client

```javascript
// Listen for global canvas events
const canvasEventSource = new EventSource("/api/v1/canvas/sse");

canvasEventSource.addEventListener("canvas_created", (event) => {
  const data = JSON.parse(event.data);
  console.log("Canvas created:", data.data);
});

canvasEventSource.addEventListener("canvas_deleted", (event) => {
  const data = JSON.parse(event.data);
  console.log("Canvas deleted:", data.data.canvas_id);
});

// Listen for message events on a specific canvas
const canvasId = "your-canvas-uuid";
const messageEventSource = new EventSource(`/api/v1/canvas/${canvasId}/sse`);

messageEventSource.addEventListener("message_committed", (event) => {
  const data = JSON.parse(event.data);
  console.log("New message:", data.data);
});

messageEventSource.addEventListener("message_updated", (event) => {
  const data = JSON.parse(event.data);
  console.log("Message updated:", data.data);
});
```

### Python Client

```python
import httpx
import json

async def listen_canvas_events():
    async with httpx.AsyncClient() as client:
        async with client.stream("GET", "/api/v1/canvas/sse") as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    event_data = json.loads(line[6:])  # Remove "data: " prefix
                    print(f"Event: {event_data}")

async def listen_message_events(canvas_id: str):
    async with httpx.AsyncClient() as client:
        async with client.stream("GET", f"/api/v1/canvas/{canvas_id}/sse") as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    event_data = json.loads(line[6:])
                    print(f"Message event: {event_data}")
```

## Testing

Use the provided `test_sse_endpoints.py` script to test the SSE endpoints:

```bash
# Start the server first
python -m llm_canvas._server._server

# In another terminal, run the tests
python test_sse_endpoints.py
```

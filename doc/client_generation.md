# RESTful Client Generation Guide

This guide shows you how to generate RESTful clients for the LLM Canvas API.

## Quick Start - Generate OpenAPI Schema

You can now generate the OpenAPI schema using the built-in script:

```bash
# Using the uv script shortcut
uv run llm-canvas-generate-openapi

# Alternative: Run as module
uv run python -m scripts.generate_openapi_schema

# Alternative: Direct execution
uv run python scripts/generate_openapi_schema.py
```

This generates `schemas/openapi.json` which can be used to generate clients in various languages.

## Quick Start - Generate TypeScript Client

Generate TypeScript client directly for your web UI:

```bash
# Recommended: openapi-typescript approach (Node.js-based, no Java required)
# Step 1: Generate TypeScript types
npx openapi-typescript schemas/openapi.json -o web_ui/node_modules/@llm-canvas/api-types/index.d.ts

# Step 2: Create the types package structure
mkdir -p web_ui/node_modules/@llm-canvas/api-types
echo '{"name": "@llm-canvas/api-types", "version": "1.0.0", "types": "index.d.ts"}' > web_ui/node_modules/@llm-canvas/api-types/package.json

# Alternative: Generate types in src directory
npx openapi-typescript schemas/openapi.json -o web_ui/src/types/api.ts

# Java-based approach (if you have Java installed)
npx @openapitools/openapi-generator-cli generate \
  -i schemas/openapi.json \
  -g typescript-fetch \
  -o web_ui/node_modules/@llm-canvas/api-client \
  --additional-properties=typescriptThreePlus=true,npmName=@llm-canvas/api-client,npmVersion=1.0.0
```

### Using openapi-typescript Generated Types

After generating the types, create a simple client wrapper:

```typescript
// web_ui/src/api/client.ts
import type { paths } from "@llm-canvas/api-types";

type ApiPaths = paths;

class LLMCanvasAPIClient {
  constructor(private baseUrl: string = "http://127.0.0.1:8000") {}

  async request<T>(path: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${this.baseUrl}${path}`, {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  // Health check
  async healthCheck(): Promise<
    ApiPaths["/api/v1/health"]["get"]["responses"]["200"]["content"]["application/json"]
  > {
    return this.request("/api/v1/health");
  }

  // List canvases
  async listCanvases(): Promise<
    ApiPaths["/api/v1/canvas/list"]["get"]["responses"]["200"]["content"]["application/json"]
  > {
    return this.request("/api/v1/canvas/list");
  }

  // Create canvas
  async createCanvas(
    data: ApiPaths["/api/v1/canvas"]["post"]["requestBody"]["content"]["application/json"]
  ): Promise<
    ApiPaths["/api/v1/canvas"]["post"]["responses"]["200"]["content"]["application/json"]
  > {
    return this.request("/api/v1/canvas", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  // Get canvas
  async getCanvas(canvasId: string): Promise<any> {
    return this.request(
      `/api/v1/canvas?canvas_id=${encodeURIComponent(canvasId)}`
    );
  }

  // Delete canvas
  async deleteCanvas(
    canvasId: string
  ): Promise<
    ApiPaths["/api/v1/canvas/{canvas_id}"]["delete"]["responses"]["200"]["content"]["application/json"]
  > {
    return this.request(`/api/v1/canvas/${encodeURIComponent(canvasId)}`, {
      method: "DELETE",
    });
  }

  // Commit message
  async commitMessage(
    canvasId: string,
    data: ApiPaths["/api/v1/canvas/{canvas_id}/messages"]["post"]["requestBody"]["content"]["application/json"]
  ): Promise<
    ApiPaths["/api/v1/canvas/{canvas_id}/messages"]["post"]["responses"]["200"]["content"]["application/json"]
  > {
    return this.request(
      `/api/v1/canvas/${encodeURIComponent(canvasId)}/messages`,
      {
        method: "POST",
        body: JSON.stringify(data),
      }
    );
  }

  // Update message
  async updateMessage(
    canvasId: string,
    messageId: string,
    data: ApiPaths["/api/v1/canvas/{canvas_id}/messages/{message_id}"]["put"]["requestBody"]["content"]["application/json"]
  ): Promise<
    ApiPaths["/api/v1/canvas/{canvas_id}/messages/{message_id}"]["put"]["responses"]["200"]["content"]["application/json"]
  > {
    return this.request(
      `/api/v1/canvas/${encodeURIComponent(
        canvasId
      )}/messages/${encodeURIComponent(messageId)}`,
      {
        method: "PUT",
        body: JSON.stringify(data),
      }
    );
  }
}

export { LLMCanvasAPIClient };
export type { ApiPaths };
```

### Prerequisites for TypeScript Client Generation

#### Option 1: OpenAPI Generator CLI (requires Java)

```bash
# Install Java (if not already installed)
# Windows: Download from https://adoptium.net/
# macOS: brew install openjdk
# Ubuntu: sudo apt install openjdk-11-jre

# Then install the generator
npm install @openapitools/openapi-generator-cli -g
```

#### Option 2: openapi-typescript (no Java required)

```bash
# Install openapi-typescript
npm install -D openapi-typescript

# Generate TypeScript types only
npx openapi-typescript schemas/openapi.json -o web_ui/src/types/api.ts
```

#### Option 3: swagger-typescript-api (no Java required, generates full client)

```bash
# Install swagger-typescript-api
npm install -D swagger-typescript-api

# Generate full TypeScript client
npx swagger-typescript-api -p schemas/openapi.json -o web_ui/src/api -n api-client.ts --modular
```

## Client Generation Options

### Option 1: Python Client with `openapi-python-client`

Generate a fully-typed Python client:

```bash
# Install the generator
uv add --dev openapi-python-client

# Generate the client
uv run openapi-python-client generate --path schemas/openapi.json --config client-config.yaml
```

Create a `client-config.yaml` file:

```yaml
class_name: "LLMCanvasClient"
project_name: "llm-canvas-client"
package_name: "llm_canvas_client"
package_version: "0.1.0"
```

### Option 2: TypeScript/JavaScript Client

Generate a TypeScript client for web applications:

```bash
# Option A: OpenAPI Generator CLI (requires Java)
npm install @openapitools/openapi-generator-cli -g

# Generate TypeScript client (standard output)
openapi-generator-cli generate \
  -i schemas/openapi.json \
  -g typescript-fetch \
  -o generated-clients/typescript \
  --additional-properties=typescriptThreePlus=true

# Generate TypeScript client directly in web_ui/node_modules (for direct integration)
openapi-generator-cli generate \
  -i schemas/openapi.json \
  -g typescript-fetch \
  -o web_ui/node_modules/@llm-canvas/api-client \
  --additional-properties=typescriptThreePlus=true,npmName=@llm-canvas/api-client,npmVersion=1.0.0

# Option B: openapi-typescript (no Java required, types only)
npm install -D openapi-typescript
npx openapi-typescript schemas/openapi.json -o web_ui/src/types/api.ts

# Option C: swagger-typescript-api (no Java required, full client)
npm install -D swagger-typescript-api
npx swagger-typescript-api -p schemas/openapi.json -o web_ui/src/api -n api-client.ts --modular
```

#### Using the TypeScript Client in Your Web UI

Once generated in `web_ui/node_modules`, you can import it directly:

```typescript
// In your React/Vue/Angular components
import { Configuration, DefaultApi } from "@llm-canvas/api-client";

// Configure the client
const config = new Configuration({
  basePath: "http://127.0.0.1:8000",
});

const apiClient = new DefaultApi(config);

// Use the client
async function listCanvases() {
  const response = await apiClient.listCanvasesApiV1CanvasListGet();
  return response.canvases;
}

async function createCanvas(title: string, description?: string) {
  const response = await apiClient.createCanvasApiV1CanvasPost({
    createCanvasRequest: { title, description },
  });
  return response.canvas_id;
}
```

### Option 3: cURL Examples

Generate cURL examples for quick testing:

```bash
openapi-generator-cli generate \
  -i schemas/openapi.json \
  -g shell \
  -o generated-clients/curl-examples
```

### Option 4: Multiple Languages

Generate clients for multiple languages at once:

```bash
# Available generators: python, typescript-fetch, java, csharp, go, rust, etc.
for lang in python typescript-fetch java; do
  openapi-generator-cli generate \
    -i schemas/openapi.json \
    -g $lang \
    -o generated-clients/$lang
done
```

## Using the Generated Python Client

Example usage of a generated Python client:

```python
from llm_canvas_client import Client
from llm_canvas_client.api.v1 import list_canvases, create_canvas, get_canvas
from llm_canvas_client.models import CreateCanvasRequest

# Initialize client
client = Client(base_url="http://127.0.0.1:8000")

# List all canvases
canvases = list_canvases.sync(client=client)
print(f"Found {len(canvases.canvases)} canvases")

# Create a new canvas
request = CreateCanvasRequest(
    title="My New Canvas",
    description="A canvas for testing"
)
response = create_canvas.sync(client=client, body=request)
print(f"Created canvas: {response.canvas_id}")

# Get the canvas
canvas_data = get_canvas.sync(client=client, canvas_id=response.canvas_id)
print(f"Canvas title: {canvas_data.title}")
```

## Manual HTTP Client Examples

If you prefer to write your own client, here are the key endpoints:

### Health Check

```python
import requests
response = requests.get("http://127.0.0.1:8000/api/v1/health")
print(response.json())  # {"status": "healthy", "server_type": "local", "timestamp": null}
```

### List Canvases

```python
response = requests.get("http://127.0.0.1:8000/api/v1/canvas/list")
canvases = response.json()["canvases"]
```

### Create Canvas

```python
response = requests.post(
    "http://127.0.0.1:8000/api/v1/canvas",
    json={"title": "New Canvas", "description": "Description"}
)
canvas_id = response.json()["canvas_id"]
```

### Get Canvas

```python
response = requests.get(
    "http://127.0.0.1:8000/api/v1/canvas",
    params={"canvas_id": canvas_id}
)
canvas_data = response.json()
```

### Add Message to Canvas

```python
message_event = {
    "data": {
        "event_type": "commit_message",
        "canvas_id": canvas_id,
        "timestamp": time.time(),
        "data": {
            "id": "msg_001",
            "message": {
                "content": "Hello, world!",
                "role": "user"
            },
            "parent_id": None,
            "child_ids": [],
            "meta": {"timestamp": time.time()}
        }
    }
}

response = requests.post(
    f"http://127.0.0.1:8000/api/v1/canvas/{canvas_id}/messages",
    json=message_event
)
```

## Streaming (SSE)

The API also supports Server-Sent Events for real-time updates:

```python
import requests

response = requests.get(
    "http://127.0.0.1:8000/api/v1/canvas/stream",
    params={"canvas_id": canvas_id},
    stream=True,
    headers={"Accept": "text/event-stream"}
)

for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
```

## Additional Tools

### FastAPI Automatic Documentation

Your FastAPI server automatically provides interactive documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **OpenAPI JSON**: http://127.0.0.1:8000/openapi.json

### Postman Collection

You can import the OpenAPI schema directly into Postman:

1. Open Postman
2. Click "Import"
3. Upload `schemas/openapi.json`
4. Postman will create a collection with all endpoints

## Best Practices

1. **Type Safety**: Use generated clients for better type safety and IDE support
2. **Error Handling**: All endpoints return consistent error formats with `error` and `message` fields
3. **Authentication**: Currently no authentication required for local server
4. **Rate Limiting**: Not implemented in local server, but consider it for production
5. **Validation**: All request/response models are validated by FastAPI/Pydantic

## Troubleshooting

If the schema generation fails:

1. Ensure the server dependencies are installed: `uv sync`
2. Check that FastAPI routes are properly imported
3. Verify the script can import `llm_canvas._api.v1_router`

For client generation issues:

1. Ensure the OpenAPI schema is valid (test at https://editor.swagger.io)
2. Check that the generator supports your target language
3. Review generator documentation for language-specific options

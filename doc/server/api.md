# Server API Design (Draft)

Base URL: (development) `http://127.0.0.1:8000/`
Version Prefix: `/api/v1`

## Overview

The server exposes endpoints to list canvases and retrieve a single canvas by id. Future revisions may add create/update endpoints and streaming collaboration channels.

## Endpoints

### GET `/api/v1/canvas/list`

List all available canvases.

Query Params: none (future: pagination, filtering)

Response 200 JSON:

```
{
  "canvases": [
    {
      "canvas_id": "<uuid>",
      "created_at": 1723090000.123,
      "root_ids": ["node1", "node2"],
      "node_count": 42,
      "meta": {
        "last_updated": 1723091111.456
      }
    }
  ]
}
```

Notes:

- `node_count` is a lightweight count (avoid shipping all nodes in list call).
- `meta.last_updated` optional (server may compute based on latest node timestamp).

### GET `/api/v1/canvas/`

Retrieve a full canvas by id.

Query Params:

- `id` (string, required): canvas UUID.

Response 200 JSON (full canvas document):

```
{
  "canvas_id": "<uuid>",
  "created_at": 1723090000.123,
  "root_ids": ["<root-node-id>", ...],
  "nodes": {
    "<node-id>": {
      "id": "<node-id>",
      "role": "user|assistant|system",
      "content": [ { "type": "text", "text": "..." } ],
      "parent_id": null,
      "child_ids": ["..."] ,
      "meta": { "timestamp": 1723090044.321 }
    }
  }
}
```

Response 404 JSON:

```
{ "error": "canvas_not_found", "message": "Canvas not found" }
```

## Error Format

Errors SHOULD return consistent envelope:

```
{ "error": "<code>", "message": "Human readable" }
```

Common Error Codes:

- `canvas_not_found`
- `validation_error`
- `internal_error`

## Future / Planned

- SSE/WebSocket channel for live updates per canvas: `/api/v1/canvas/stream?id=...`
- Authn/Z (API keys / tokens) & rate limiting

## Open Questions

1. Persist canvases (filesystem? sqlite? pluggable adapter?) (future plan, not in scope now).

---

Status: Draft
Owner: server

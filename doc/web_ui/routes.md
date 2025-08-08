# Web UI Routes Design

This document describes the currently supported public routes of the llm-canvas web UI.

## Summary

| Route          | Purpose                                       | Primary Components                                  | Data Sources                                                      |
| -------------- | --------------------------------------------- | --------------------------------------------------- | ----------------------------------------------------------------- |
| `/`            | Canvas gallery listing all available canvases | `CanvasGallery` (planned)                           | Backend endpoint to list canvases (planned) / temporary mock data |
| `/canvas/{id}` | View & interact with a single canvas          | `CanvasView`, `MessageNode`, store in `canvasStore` | Backend canvas detail + live updates (planned) / mock data now    |

## Route Details

### `/` (Gallery)

Purpose: Provide an overview of all canvases so a user can select one to open.

Initial Implementation:

- Uses mock list (until backend list endpoint exists).
- Each item links to `/canvas/{id}`.

Future Enhancements:

- Search / filter bar.
- Pagination or infinite scroll.
- Create-new button (navigates to a fresh canvas id once created by backend).
- Last updated timestamps & ownership metadata.

### `/canvas/{id}` (Canvas Detail)

Purpose: Display and manipulate an individual canvas (messages / nodes / links).

Core Behaviors:

- Loads canvas state (mock now; real fetch later).
- Renders nodes via `MessageNode` components.
- State managed in `canvasStore` (Zustand) & `useCanvas` hook for selectors / actions.

Future Enhancements:

- Live collaboration (websocket/subscription) to sync updates.
- Autosave debounce to backend.
- Version history & branching.
- Share link / permissions model.

## Navigation & State

- Routing layer (not yet added) will likely use `react-router` or a minimal custom solution with `window.location` + state sync.
- Canvas state is isolated per id; navigating between canvases triggers store reset / rehydrate.

## Open Questions

1. Route for creating a new canvas: POST then redirect vs optimistic temp id?
2. Auth model & protected routes.
3. URL scheme for versions: `/canvas/{id}/v/{revision}`?

## Next Steps

1. Introduce a router dependency (recommend `react-router-dom`).
2. Implement gallery component scaffolding.
3. Add data fetching layer abstraction (so mocks swap to real API cleanly).
4. Define backend contract for list + detail endpoints.

---

Owner: web_ui
Status: Draft (initial route definition)

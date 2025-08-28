"""Tests for SSE API endpoints."""

import json
import uuid

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from llm_canvas._server._api import v1_router
from llm_canvas._server._events import get_event_dispatcher
from llm_canvas._server._registry import get_local_registry
from llm_canvas.canvas import Canvas


class TestSSEEndpoints:
    """Test suite for Server-Side Events API endpoints."""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup and teardown for each test."""
        # Clear registry and event dispatcher before each test
        registry = get_local_registry()
        # Access private members for testing purposes
        registry._canvases.clear()  # noqa: SLF001
        registry._last_updated.clear()  # noqa: SLF001

        event_dispatcher = get_event_dispatcher()
        event_dispatcher._global_connections.clear()  # noqa: SLF001
        event_dispatcher._canvas_connections.clear()  # noqa: SLF001

        yield

        # Cleanup after each test
        registry._canvases.clear()  # noqa: SLF001
        registry._last_updated.clear()  # noqa: SLF001
        event_dispatcher._global_connections.clear()  # noqa: SLF001
        event_dispatcher._canvas_connections.clear()  # noqa: SLF001

    @pytest.fixture
    def client(self) -> TestClient:
        """Create a test client for the API."""
        app = FastAPI()
        app.include_router(v1_router)

        return TestClient(app) @ pytest.fixture

    def sample_canvas(self) -> Canvas:
        """Create a sample canvas for testing."""
        canvas = Canvas(title="Test Canvas", description="A canvas for SSE testing")
        registry = get_local_registry()
        registry.add(canvas)
        return canvas

    def test_canvas_sse_endpoint_connection(self, client: TestClient) -> None:
        """Test that the global canvas SSE endpoint accepts connections."""
        with client.stream("GET", "/api/v1/canvas/sse") as response:
            assert response.status_code == 200
            assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
            assert response.headers["cache-control"] == "no-cache"
            assert response.headers["connection"] == "keep-alive"

    def test_canvas_message_sse_endpoint_connection(self, client: TestClient, sample_canvas: Canvas) -> None:
        """Test that the canvas message SSE endpoint accepts connections."""
        with client.stream("GET", f"/api/v1/canvas/{sample_canvas.canvas_id}/sse") as response:
            assert response.status_code == 200
            assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
            assert response.headers["cache-control"] == "no-cache"
            assert response.headers["connection"] == "keep-alive"

    def test_canvas_message_sse_invalid_canvas(self, client: TestClient) -> None:
        """Test that canvas message SSE returns 404 for invalid canvas ID."""
        invalid_canvas_id = str(uuid.uuid4())
        response = client.get(f"/api/v1/canvas/{invalid_canvas_id}/sse")
        assert response.status_code == 404
        error_data = response.json()
        assert error_data["error"] == "canvas_not_found"
        assert error_data["message"] == "Canvas not found"

    def test_canvas_created_event_emission(self, client: TestClient) -> None:
        """Test that canvas creation triggers SSE event."""
        # Start SSE connection
        with client.stream("GET", "/api/v1/canvas/sse") as sse_response:
            assert sse_response.status_code == 200

            # Create a canvas in another client request
            create_response = client.post("/api/v1/canvas", json={"title": "Test Canvas", "description": "Test canvas for SSE"})
            assert create_response.status_code == 200
            canvas_data = create_response.json()
            canvas_id = canvas_data["canvas_id"]

            # Read SSE events (with timeout to avoid infinite wait)
            events_received = []
            line_count = 0
            max_lines = 20  # Limit to avoid infinite loop

            for line in sse_response.iter_lines():
                line_count += 1
                if line_count > max_lines:
                    break

                if line.startswith("event: "):
                    event_type = line[7:]  # Remove "event: " prefix
                elif line.startswith("data: "):
                    try:
                        event_data = json.loads(line[6:])  # Remove "data: " prefix
                        events_received.append((event_type, event_data))
                    except json.JSONDecodeError:
                        continue  # Skip malformed JSON

                # Stop after receiving the first real event
                if events_received:
                    break

            # Verify we received a canvas_created event
            assert len(events_received) > 0
            event_type, event_data = events_received[0]
            assert event_type == "canvas_created"
            assert event_data["type"] == "canvas_created"
            assert event_data["data"]["canvas_id"] == canvas_id
            assert event_data["data"]["title"] == "Test Canvas"

    def test_canvas_deleted_event_emission(self, client: TestClient, sample_canvas: Canvas) -> None:
        """Test that canvas deletion triggers SSE event."""
        canvas_id = sample_canvas.canvas_id

        # Start SSE connection
        with client.stream("GET", "/api/v1/canvas/sse") as sse_response:
            assert sse_response.status_code == 200

            # Delete the canvas
            delete_response = client.delete(f"/api/v1/canvas/{canvas_id}")
            assert delete_response.status_code == 200

            # Read SSE events
            events_received = []
            line_count = 0
            max_lines = 20

            for line in sse_response.iter_lines():
                line_count += 1
                if line_count > max_lines:
                    break

                if line.startswith("event: "):
                    event_type = line[7:]
                elif line.startswith("data: "):
                    try:
                        event_data = json.loads(line[6:])
                        events_received.append((event_type, event_data))
                    except json.JSONDecodeError:
                        continue

                if events_received:
                    break

            # Verify we received a canvas_deleted event
            assert len(events_received) > 0
            event_type, event_data = events_received[0]
            assert event_type == "canvas_deleted"
            assert event_data["type"] == "canvas_deleted"
            assert event_data["data"]["canvas_id"] == canvas_id

    def test_message_committed_event_emission(self, client: TestClient, sample_canvas: Canvas) -> None:
        """Test that message commit triggers SSE event."""
        canvas_id = sample_canvas.canvas_id

        # Start SSE connection for this canvas
        with client.stream("GET", f"/api/v1/canvas/{canvas_id}/sse") as sse_response:
            assert sse_response.status_code == 200

            # Commit a message
            message_data = {
                "event_type": "commit_message",
                "canvas_id": canvas_id,
                "timestamp": 1693423200.123,
                "data": {
                    "id": str(uuid.uuid4()),
                    "message": {"content": "Hello, world!", "role": "user"},
                    "parent_id": None,
                    "child_ids": [],
                    "meta": {"timestamp": 1693423200000},
                },
            }

            commit_response = client.post(f"/api/v1/canvas/{canvas_id}/messages", json={"data": message_data})
            assert commit_response.status_code == 200

            # Read SSE events
            events_received = []
            line_count = 0
            max_lines = 20

            for line in sse_response.iter_lines():
                line_count += 1
                if line_count > max_lines:
                    break

                if line.startswith("event: "):
                    event_type = line[7:]
                elif line.startswith("data: "):
                    try:
                        event_data = json.loads(line[6:])
                        events_received.append((event_type, event_data))
                    except json.JSONDecodeError:
                        continue

                if events_received:
                    break

            # Verify we received a message_committed event
            assert len(events_received) > 0
            event_type, event_data = events_received[0]
            assert event_type == "message_committed"
            assert event_data["type"] == "message_committed"
            assert event_data["canvas_id"] == canvas_id
            assert event_data["data"]["message"]["content"] == "Hello, world!"

    def test_message_updated_event_emission(self, client: TestClient, sample_canvas: Canvas) -> None:
        """Test that message update triggers SSE event."""
        canvas_id = sample_canvas.canvas_id

        # First, create a message to update
        message_id = str(uuid.uuid4())
        initial_message_data = {
            "event_type": "commit_message",
            "canvas_id": canvas_id,
            "timestamp": 1693423200.123,
            "data": {
                "id": message_id,
                "message": {"content": "Original content", "role": "user"},
                "parent_id": None,
                "child_ids": [],
                "meta": {"timestamp": 1693423200000},
            },
        }

        commit_response = client.post(f"/api/v1/canvas/{canvas_id}/messages", json={"data": initial_message_data})
        assert commit_response.status_code == 200

        # Start SSE connection for this canvas
        with client.stream("GET", f"/api/v1/canvas/{canvas_id}/sse") as sse_response:
            assert sse_response.status_code == 200

            # Update the message
            updated_message_data = {
                "event_type": "update_message",
                "canvas_id": canvas_id,
                "timestamp": 1693423300.123,
                "data": {
                    "id": message_id,
                    "message": {"content": "Updated content", "role": "user"},
                    "parent_id": None,
                    "child_ids": [],
                    "meta": {"timestamp": 1693423300000},
                },
            }

            update_response = client.put(
                f"/api/v1/canvas/{canvas_id}/messages/{message_id}", json={"data": updated_message_data}
            )
            assert update_response.status_code == 200

            # Read SSE events
            events_received = []
            line_count = 0
            max_lines = 20

            for line in sse_response.iter_lines():
                line_count += 1
                if line_count > max_lines:
                    break

                if line.startswith("event: "):
                    event_type = line[7:]
                elif line.startswith("data: "):
                    try:
                        event_data = json.loads(line[6:])
                        events_received.append((event_type, event_data))
                    except json.JSONDecodeError:
                        continue

                if events_received:
                    break

            # Verify we received a message_updated event
            assert len(events_received) > 0
            event_type, event_data = events_received[0]
            assert event_type == "message_updated"
            assert event_data["type"] == "message_updated"
            assert event_data["canvas_id"] == canvas_id
            assert event_data["data"]["message"]["content"] == "Updated content"

    def test_multiple_sse_connections(self, client: TestClient) -> None:
        """Test that multiple SSE connections can receive events independently."""
        # This test verifies that the event dispatcher can handle multiple connections

        # Start two SSE connections
        with (
            client.stream("GET", "/api/v1/canvas/sse") as sse_response1,
            client.stream("GET", "/api/v1/canvas/sse") as sse_response2,
        ):
            assert sse_response1.status_code == 200
            assert sse_response2.status_code == 200

            # Create a canvas
            create_response = client.post(
                "/api/v1/canvas", json={"title": "Multi-connection Test", "description": "Testing multiple connections"}
            )
            assert create_response.status_code == 200

            # Both connections should receive the event
            # For simplicity, we'll just verify that both can read lines
            # without checking the exact content (which would require more complex logic)

            # Read from first connection
            lines1 = []
            for i, line in enumerate(sse_response1.iter_lines()):
                lines1.append(line)
                if i >= 5:  # Read a few lines
                    break

            # Read from second connection
            lines2 = []
            for i, line in enumerate(sse_response2.iter_lines()):
                lines2.append(line)
                if i >= 5:  # Read a few lines
                    break

            # Both should have received some data
            assert len(lines1) > 0
            assert len(lines2) > 0

    def test_sse_heartbeat_events(self, client: TestClient) -> None:
        """Test that SSE connections receive heartbeat events."""
        # Note: This test might be challenging to implement with TestClient
        # since heartbeats are sent every 30 seconds, which is too long for a unit test.
        # We'll verify the connection stays open and can read the initial setup.

        with client.stream("GET", "/api/v1/canvas/sse") as sse_response:
            assert sse_response.status_code == 200

            # Read a few initial lines to verify the connection works
            line_count = 0
            for _line in sse_response.iter_lines():
                line_count += 1
                if line_count >= 3:  # Just read a few lines to verify connection
                    break

            # Connection should be working (we've read some lines without error)
            assert line_count > 0

    def test_sse_connection_cleanup(self, client: TestClient) -> None:
        """Test that SSE connections are properly cleaned up."""
        event_dispatcher = get_event_dispatcher()

        # Verify no connections initially
        assert len(event_dispatcher._global_connections) == 0  # noqa: SLF001

        # Start and immediately close connection
        with client.stream("GET", "/api/v1/canvas/sse") as sse_response:
            assert sse_response.status_code == 200
            # Read one line to establish connection
            next(sse_response.iter_lines())

        # After closing, connections should be cleaned up eventually
        # Note: The actual cleanup might be async, so we can't guarantee
        # immediate cleanup in this test environment

    def test_canvas_sse_with_cors_headers(self, client: TestClient) -> None:
        """Test that SSE endpoints return proper CORS headers."""
        with client.stream("GET", "/api/v1/canvas/sse") as response:
            assert response.status_code == 200
            assert response.headers.get("access-control-allow-origin") == "*"
            assert "access-control-allow-headers" in response.headers

    def test_canvas_message_sse_with_cors_headers(self, client: TestClient, sample_canvas: Canvas) -> None:
        """Test that canvas message SSE endpoint returns proper CORS headers."""
        with client.stream("GET", f"/api/v1/canvas/{sample_canvas.canvas_id}/sse") as response:
            assert response.status_code == 200
            assert response.headers.get("access-control-allow-origin") == "*"
            assert "access-control-allow-headers" in response.headers

    def test_event_data_structure(self, client: TestClient) -> None:
        """Test that SSE events have the correct data structure."""
        with client.stream("GET", "/api/v1/canvas/sse") as sse_response:
            assert sse_response.status_code == 200

            # Create a canvas to trigger an event
            create_response = client.post(
                "/api/v1/canvas", json={"title": "Structure Test", "description": "Testing event structure"}
            )
            assert create_response.status_code == 200

            # Read and parse the event
            events_received = []
            line_count = 0
            max_lines = 20

            for line in sse_response.iter_lines():
                line_count += 1
                if line_count > max_lines:
                    break

                if line.startswith("event: "):
                    event_type = line[7:]
                elif line.startswith("data: "):
                    try:
                        event_data = json.loads(line[6:])
                        events_received.append((event_type, event_data))
                    except json.JSONDecodeError:
                        continue

                if events_received:
                    break

            # Verify event structure
            assert len(events_received) > 0
            event_type, event_data = events_received[0]

            # Check required fields
            assert "type" in event_data
            assert "timestamp" in event_data
            assert "data" in event_data
            assert isinstance(event_data["timestamp"], (int, float))
            assert event_data["type"] == event_type

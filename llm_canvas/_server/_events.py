"""Event system for Server-Side Events (SSE) in llm_canvas.

This module provides event dispatching and connection management for SSE endpoints.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import time
from collections import defaultdict
from collections.abc import AsyncGenerator

from llm_canvas.types import (
    CanvasSummary,
    MessageNode,
)

from ._types import (
    SSECanvasCreatedEvent,
    SSECanvasDeletedEvent,
    SSECanvasEvent,
    SSECanvasUpdatedEvent,
    SSEGlobalEvent,
    SSEMessageCommittedEvent,
    SSEMessageDeletedEvent,
    SSEMessageUpdatedEvent,
)

logger = logging.getLogger(__name__)


class SSEEventDispatcher:
    """Manages SSE connections and event distribution."""

    def __init__(self) -> None:
        # Global canvas events (for /canvas/sse)
        self._global_connections: set[asyncio.Queue[str]] = set()

        # Per-canvas events (for /canvas/{canvas_id}/sse)
        self._canvas_connections: dict[str, set[asyncio.Queue[str]]] = defaultdict(set)

        # Lock for thread-safe operations
        self._lock = asyncio.Lock()

        # Shutdown event to signal all connections to close
        self._shutdown_event = asyncio.Event()

    async def add_global_connection(self, queue: asyncio.Queue[str]) -> None:
        """Add a connection for global canvas events."""
        async with self._lock:
            self._global_connections.add(queue)
            logger.info(f"Added global SSE connection. Total: {len(self._global_connections)}")

    async def remove_global_connection(self, queue: asyncio.Queue[str]) -> None:
        """Remove a connection for global canvas events."""
        async with self._lock:
            self._global_connections.discard(queue)
            logger.info(f"Removed global SSE connection. Total: {len(self._global_connections)}")

    async def add_canvas_connection(self, canvas_id: str, queue: asyncio.Queue[str]) -> None:
        """Add a connection for specific canvas events."""
        async with self._lock:
            self._canvas_connections[canvas_id].add(queue)
            logger.info(f"Added canvas {canvas_id} SSE connection. Total: {len(self._canvas_connections[canvas_id])}")

    async def remove_canvas_connection(self, canvas_id: str, queue: asyncio.Queue[str]) -> None:
        """Remove a connection for specific canvas events."""
        async with self._lock:
            self._canvas_connections[canvas_id].discard(queue)
            if not self._canvas_connections[canvas_id]:
                del self._canvas_connections[canvas_id]
            logger.info(f"Removed canvas {canvas_id} SSE connection")

    async def broadcast_global_event(self, event_data: SSEGlobalEvent) -> None:
        """Broadcast an event to all global connections."""
        if not self._global_connections:
            return

        message = f"event: {event_data['type']}\ndata: {json.dumps(event_data)}\n\n"

        async with self._lock:
            disconnected_queues = set()

            # Process each queue and collect results
            for queue in self._global_connections:
                if queue.full():
                    logger.warning("SSE queue full, marking for removal")
                    disconnected_queues.add(queue)
                    continue

                try:
                    queue.put_nowait(message)
                except (RuntimeError, ValueError):
                    logger.exception("Error sending to SSE queue")
                    disconnected_queues.add(queue)

            # Remove disconnected queues
            for queue in disconnected_queues:
                self._global_connections.discard(queue)

    async def broadcast_canvas_event(self, canvas_id: str, event_data: SSECanvasEvent) -> None:
        """Broadcast an event to all connections for a specific canvas."""
        if canvas_id not in self._canvas_connections:
            return

        message = f"event: {event_data['type']}\ndata: {json.dumps(event_data)}\n\n"

        async with self._lock:
            disconnected_queues = set()

            # Process each queue and collect results
            for queue in self._canvas_connections[canvas_id]:
                if queue.full():
                    logger.warning("SSE queue full, marking for removal")
                    disconnected_queues.add(queue)
                    continue

                try:
                    queue.put_nowait(message)
                except (RuntimeError, ValueError):
                    logger.exception("Error sending to SSE queue")
                    disconnected_queues.add(queue)

            # Remove disconnected queues
            for queue in disconnected_queues:
                self._canvas_connections[canvas_id].discard(queue)

    async def canvas_created(self, canvas_summary: CanvasSummary) -> None:
        """Broadcast that a canvas was created."""
        await self.broadcast_global_event(
            SSECanvasCreatedEvent(type="canvas_created", timestamp=time.time(), data=canvas_summary)
        )

    async def canvas_updated(self, canvas_summary: CanvasSummary) -> None:
        """Broadcast that a canvas was updated."""
        await self.broadcast_global_event(
            SSECanvasUpdatedEvent(type="canvas_updated", timestamp=time.time(), data=canvas_summary)
        )

    async def canvas_deleted(self, canvas_id: str) -> None:
        """Broadcast that a canvas was deleted."""
        await self.broadcast_global_event(
            SSECanvasDeletedEvent(type="canvas_deleted", timestamp=time.time(), data={"canvas_id": canvas_id})
        )

    async def message_committed(self, canvas_id: str, message_data: MessageNode) -> None:
        """Broadcast that a message was committed to a canvas."""
        await self.broadcast_canvas_event(
            canvas_id,
            SSEMessageCommittedEvent(type="message_committed", timestamp=time.time(), canvas_id=canvas_id, data=message_data),
        )

    async def message_updated(self, canvas_id: str, message_data: MessageNode) -> None:
        """Broadcast that a message was updated in a canvas."""
        await self.broadcast_canvas_event(
            canvas_id,
            SSEMessageUpdatedEvent(type="message_updated", timestamp=time.time(), canvas_id=canvas_id, data=message_data),
        )

    async def message_deleted(self, canvas_id: str, message_id: str) -> None:
        """Broadcast that a message was deleted from a canvas."""
        await self.broadcast_canvas_event(
            canvas_id,
            SSEMessageDeletedEvent(
                type="message_deleted", timestamp=time.time(), canvas_id=canvas_id, data={"message_id": message_id}
            ),
        )

    async def shutdown(self) -> None:
        """Signal all connections to close and clean up."""
        logger.info("Shutting down SSE event dispatcher")
        self._shutdown_event.set()

        async with self._lock:
            # Send shutdown message to all connections
            shutdown_message = 'event: shutdown\ndata: {"message": "Server shutting down"}\n\n'

            # Notify all global connections
            for queue in self._global_connections.copy():
                with contextlib.suppress(RuntimeError, ValueError):
                    queue.put_nowait(shutdown_message)

            # Notify all canvas connections
            for canvas_connections in self._canvas_connections.values():
                for queue in canvas_connections.copy():
                    with contextlib.suppress(RuntimeError, ValueError):
                        queue.put_nowait(shutdown_message)

            # Clear all connections
            self._global_connections.clear()
            self._canvas_connections.clear()

        logger.info("SSE event dispatcher shutdown complete")

    @property
    def is_shutdown(self) -> bool:
        """Check if shutdown has been initiated."""
        return self._shutdown_event.is_set()

    async def wait_for_shutdown(self) -> None:
        """Wait for shutdown event to be set."""
        await self._shutdown_event.wait()


# Global event dispatcher instance
_event_dispatcher: SSEEventDispatcher | None = None


def get_event_dispatcher() -> SSEEventDispatcher:
    """Get the global event dispatcher instance."""
    global _event_dispatcher  # noqa: PLW0603
    if _event_dispatcher is None:
        _event_dispatcher = SSEEventDispatcher()
    return _event_dispatcher


async def create_sse_stream(queue: asyncio.Queue[str]) -> AsyncGenerator[str, None]:
    """Create an SSE stream from a queue."""
    event_dispatcher = get_event_dispatcher()

    try:
        while not event_dispatcher.is_shutdown:
            # Create tasks for message, timeout, and shutdown
            message_task = asyncio.create_task(queue.get())
            timeout_task = asyncio.create_task(asyncio.sleep(10.0))
            shutdown_task = asyncio.create_task(event_dispatcher.wait_for_shutdown())

            done, pending = await asyncio.wait([message_task, timeout_task, shutdown_task], return_when=asyncio.FIRST_COMPLETED)

            # Cancel any pending tasks
            for task in pending:
                task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await task

            if shutdown_task in done:
                # Shutdown requested, break the loop
                logger.info("SSE stream received shutdown signal")
                break
            elif message_task in done:
                # We received a message
                message = message_task.result()
                # Check if it's a shutdown message
                if "event: shutdown" in message:
                    yield message
                    break
                yield message
            else:
                # Timeout occurred, send heartbeat
                yield "event: heartbeat\ndata: {}\n\n"

    except asyncio.CancelledError:
        logger.info("SSE stream cancelled")
        raise
    except (RuntimeError, ValueError):
        logger.exception("Error in SSE stream")
        yield f"event: error\ndata: {json.dumps({'error': 'stream error'})}\n\n"
    finally:
        logger.info("SSE stream ended")

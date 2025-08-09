"""Shared pytest configuration and fixtures."""

import pytest


@pytest.fixture(scope="session")
def shared_canvas_client():
    """Provide a shared canvas client for tests."""
    from llm_canvas import canvas_client

    return canvas_client


@pytest.fixture
def clean_canvas(shared_canvas_client):
    """Provide a fresh canvas for each test."""
    return shared_canvas_client.create_canvas(title="Test Canvas", description="Canvas for testing")

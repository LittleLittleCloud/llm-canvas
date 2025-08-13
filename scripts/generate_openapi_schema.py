#!/usr/bin/env python3
"""Generate OpenAPI schema from the FastAPI application."""

import json
import sys
from pathlib import Path

# Create a minimal FastAPI app with just the API routes
from fastapi import FastAPI

from llm_canvas._server._api import v1_router


def generate_openapi_schema() -> Path:
    """Generate OpenAPI schema and save to file."""

    app = FastAPI(
        title="LLM Canvas API",
        version="0.1.0",
        description="RESTful API for LLM Canvas operations",
        separate_input_output_schemas=False,  # Disable separate schemas for input/output
    )

    # Include only the API router
    app.include_router(v1_router)

    # Generate OpenAPI schema
    openapi_schema = app.openapi()

    # Save to schemas directory
    schemas_dir = Path(__file__).parent.parent / "schemas"
    schemas_dir.mkdir(exist_ok=True)

    schema_file = schemas_dir / "openapi.json"
    with schema_file.open("w") as f:
        json.dump(openapi_schema, f, indent=2)

    print(f"OpenAPI schema generated: {schema_file}")
    return schema_file


def main() -> None:
    """Main entry point for CLI."""
    try:
        schema_file = generate_openapi_schema()
        print(f"✅ Successfully generated OpenAPI schema at: {schema_file}")
        sys.exit(0)
    except (OSError, ImportError, ValueError) as e:
        print(f"❌ Error generating OpenAPI schema: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

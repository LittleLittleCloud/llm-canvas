#!/usr/bin/env python3
"""Script to generate the Python OpenAPI client for LLM Canvas."""

import subprocess
import sys
from pathlib import Path


# ruff: noqa: S603
def main() -> None:
    """Generate the Python OpenAPI client."""
    repo_root = Path(__file__).parent.parent
    schemas_path = repo_root / "schemas" / "openapi.json"
    output_path = repo_root / "llm_canvas_generated_client"

    # Ensure the schemas directory exists
    schemas_path.parent.mkdir(exist_ok=True)

    # Generate OpenAPI schema first if it doesn't exist
    if not schemas_path.exists():
        print("Generating OpenAPI schema...")
        subprocess.run([sys.executable, "-m", "scripts.generate_openapi_schema"], check=True)

    # Generate the Python client
    print(f"Generating Python client to {output_path}...")
    cmd = [
        "openapi-python-client",
        "generate",
        "--path",
        str(schemas_path),
        "--output-path",
        str(output_path),
        "--overwrite",
    ]

    subprocess.run(cmd, check=True)
    print("Python client generated successfully!")


if __name__ == "__main__":
    main()

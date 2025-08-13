#!/usr/bin/env python3
"""Script to generate both Python and TypeScript OpenAPI clients for LLM Canvas."""

import shutil
import subprocess
import sys
from pathlib import Path


# ruff: noqa: S603
def generate_python_client(repo_root: Path, schemas_path: Path) -> None:
    """Generate the Python OpenAPI client."""
    output_path = repo_root / "llm_canvas_generated_client"

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


def generate_typescript_client(repo_root: Path) -> None:
    """Generate the TypeScript OpenAPI client."""
    web_ui_path = repo_root / "web_ui"

    print("Generating TypeScript client...")

    # Find npm executable
    npm_cmd = shutil.which("npm")
    if npm_cmd is None:
        msg = "npm not found in PATH. Please install Node.js and npm."
        raise FileNotFoundError(msg)

    # Change to web_ui directory and run the npm script
    subprocess.run(
        [npm_cmd, "run", "generate_openapi_client"],
        cwd=web_ui_path,
        check=True,
    )
    print("TypeScript client generated successfully!")


def main() -> None:
    """Generate both Python and TypeScript OpenAPI clients."""
    repo_root = Path(__file__).parent.parent
    schemas_path = repo_root / "schemas" / "openapi.json"

    # Ensure the schemas directory exists
    schemas_path.parent.mkdir(exist_ok=True)

    # Generate OpenAPI schema first if it doesn't exist
    if not schemas_path.exists():
        print("Generating OpenAPI schema...")
        subprocess.run([sys.executable, "-m", "scripts.generate_openapi_schema"], check=True)

    # Generate both clients
    generate_python_client(repo_root, schemas_path)
    generate_typescript_client(repo_root)


if __name__ == "__main__":
    main()

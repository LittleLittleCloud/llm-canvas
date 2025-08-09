#!/usr/bin/env python3
"""Run tests for LLM Canvas."""

import subprocess
import sys
from pathlib import Path


def main():
    """Run pytest with appropriate configuration."""
    # Get the project root directory
    project_root = Path(__file__).parent

    # Change to project directory
    import os

    os.chdir(project_root)

    # Run pytest
    cmd = [sys.executable, "-m", "pytest", "tests/", "-v"]

    try:
        result = subprocess.run(cmd, check=False)
        sys.exit(result.returncode)
    except FileNotFoundError:
        print("pytest not found. Install it with: pip install pytest")
        sys.exit(1)


if __name__ == "__main__":
    main()

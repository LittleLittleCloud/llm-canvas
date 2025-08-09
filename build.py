#!/usr/bin/env python3
"""Build script for llm_canvas with frontend integration."""

import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional


def build_frontend() -> Optional[bool]:
    """Build the React frontend."""
    root_dir = Path(__file__).parent
    web_ui_dir = root_dir / "web_ui"
    static_dir = root_dir / "llm_canvas" / "static"

    if not web_ui_dir.exists():
        print("No web_ui directory found, skipping frontend build")
        return

    print("Building frontend...")
    
    # Install dependencies and build
    try:
        # Copy built files to static directory
        dist_dir = web_ui_dir / "dist"
        if dist_dir.exists():
            if static_dir.exists():
                shutil.rmtree(static_dir)
            shutil.copytree(dist_dir, static_dir)
            print(f"✓ Frontend built and copied to {static_dir}")
        else:
            print("❌ Frontend build failed - no dist directory found")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend build failed: {e}")
        return False
    
    return True


def build_package() -> Optional[bool]:
    """Build the Python package."""
    print("Building Python package...")
    try:
        # Try uv build first (preferred)
        subprocess.run(["uv", "build"], check=True)
        print("✓ Package built successfully with uv")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Fallback to python -m build
            subprocess.run([sys.executable, "-m", "build"], check=True)
            print("✓ Package built successfully with build")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Package build failed: {e}")
            print("💡 Try installing build tools: uv add --dev build")
            return False


def main():
    """Main build function."""
    if len(sys.argv) > 1 and sys.argv[1] == "--frontend-only":
        return build_frontend()
    
    # Build frontend first, then package
    if not build_frontend():
        sys.exit(1)
    
    if not build_package():
        sys.exit(1)
    
    print("🎉 Build completed successfully!")


if __name__ == "__main__":
    main()

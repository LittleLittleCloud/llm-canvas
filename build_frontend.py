"""Custom build hook to build frontend and include static files."""
import os
import shutil
import subprocess
from pathlib import Path
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    PLUGIN_NAME = "custom"

    def initialize(self, version, build_data) -> None:
        """Build frontend and copy static files."""
        if self.target_name != "wheel":
            return

        root_dir = Path(self.root)
        web_ui_dir = root_dir / "web_ui"
        static_dir = root_dir / "llm_canvas" / "static"

        # Build frontend if web_ui exists
        if web_ui_dir.exists() and (web_ui_dir / "package.json").exists():
            print("Building frontend...")
            
            # Install dependencies and build
            subprocess.run(["npm", "ci"], cwd=web_ui_dir, check=True)
            subprocess.run(["npm", "run", "build"], cwd=web_ui_dir, check=True)
            
            # Copy built files to static directory
            dist_dir = web_ui_dir / "dist"
            if dist_dir.exists():
                if static_dir.exists():
                    shutil.rmtree(static_dir)
                shutil.copytree(dist_dir, static_dir)
                print(f"Copied frontend build to {static_dir}")

        # Ensure static files are included in the build
        if static_dir.exists():
            build_data.setdefault("force_include", {})
            for file_path in static_dir.rglob("*"):
                if file_path.is_file():
                    relative_path = file_path.relative_to(root_dir)
                    build_data["force_include"][str(relative_path)] = str(relative_path)

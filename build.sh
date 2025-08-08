#!/bin/bash
# Unix build script

set -e

echo "🔨 Building llm_canvas with uv..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv not found. Install from: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Install Node.js from: https://nodejs.org/"
    exit 1
fi

# Create virtual environment and install dependencies
echo "📦 Setting up Python environment..."
uv sync --extra server --extra dev

# Build frontend
echo "🎨 Building frontend..."
cd web_ui
npm ci
npm run build
cd ..

# Copy frontend build to static directory
echo "📁 Copying frontend assets..."
rm -rf llm_canvas/static
cp -r web_ui/dist llm_canvas/static
echo "✓ Frontend copied to llm_canvas/static"

# Build Python package
echo "🐍 Building Python package..."
uv build

echo "🎉 Build completed! Package available in dist/"
echo ""
echo "Next steps:"
echo "  • Install locally: uv pip install dist/*.whl"
echo "  • Run server: uv run llm-canvas-serve"
echo "  • Or: uv run python -m uvicorn llm_canvas.server:main --reload"

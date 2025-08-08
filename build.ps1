#!/usr/bin/env pwsh
# PowerShell build script for Windows

Write-Host "🔨 Building llm_canvas with uv..." -ForegroundColor Green

# Check if uv is installed
if (!(Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "❌ uv not found. Install from: https://docs.astral.sh/uv/getting-started/installation/" -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed
if (!(Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "❌ npm not found. Install Node.js from: https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Create virtual environment and install dependencies
Write-Host "📦 Setting up Python environment..." -ForegroundColor Blue
uv sync --extra server --extra dev

# Build frontend
Write-Host "🎨 Building frontend..." -ForegroundColor Blue
Set-Location web_ui
npm ci
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Frontend build failed" -ForegroundColor Red
    exit 1
}
Set-Location ..

# Copy frontend build to static directory
Write-Host "📁 Copying frontend assets..." -ForegroundColor Blue
$staticDir = "llm_canvas/static"
if (Test-Path $staticDir) {
    Remove-Item $staticDir -Recurse -Force
}
Copy-Item "web_ui/dist" $staticDir -Recurse
Write-Host "✓ Frontend copied to $staticDir" -ForegroundColor Green

# Build Python package
Write-Host "🐍 Building Python package..." -ForegroundColor Blue
uv build

Write-Host "🎉 Build completed! Package available in dist/" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  • Install locally: uv pip install dist/*.whl" -ForegroundColor White
Write-Host "  • Run server: uv run llm-canvas-serve" -ForegroundColor White
Write-Host "  • Or: uv run python -m uvicorn llm_canvas.server:main --reload" -ForegroundColor White

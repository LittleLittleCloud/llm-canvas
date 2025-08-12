# RESTful Client Generation Guide

This guide shows you how to generate RESTful clients for the LLM Canvas API.

## Quick Start - Generate OpenAPI Schema

You can now generate the OpenAPI schema using the built-in script:

```bash
# Using the uv script shortcut
uv run llm-canvas-generate-openapi

# Alternative: Run as module
uv run python -m scripts.generate_openapi_schema

# Alternative: Direct execution
uv run openapi-python-client generate --path schemas/openapi.json --output-path generated_client --config client-config.yaml --overwrite
```

This generates `schemas/openapi.json` which can be used to generate clients in various languages.

## Quick Start - Generate TypeScript Client

Generate TypeScript client directly for your web UI:

```bash
# Recommended: openapi-typescript approach (Node.js-based, no Java required)
# Step 1: Generate TypeScript types
npx openapi-typescript schemas/openapi.json -o web_ui/node_modules/@llm-canvas/api-types/index.d.ts

# Step 2: Create the types package structure
mkdir -p web_ui/node_modules/@llm-canvas/api-types
echo '{"name": "@llm-canvas/api-types", "version": "1.0.0", "types": "index.d.ts"}' > web_ui/node_modules/@llm-canvas/api-types/package.json

# Alternative: Generate types in src directory
npx openapi-typescript schemas/openapi.json -o web_ui/src/types/api.ts

# Java-based approach (if you have Java installed)
npx @openapitools/openapi-generator-cli generate \
  -i schemas/openapi.json \
  -g typescript-fetch \
  -o web_ui/node_modules/@llm-canvas/api-client \
  --additional-properties=typescriptThreePlus=true,npmName=@llm-canvas/api-client,npmVersion=1.0.0
```

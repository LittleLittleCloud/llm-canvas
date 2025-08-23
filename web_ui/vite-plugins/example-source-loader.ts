import { readFileSync } from "fs";
import { resolve } from "path";
import type { Plugin } from "vite";

interface ExampleConfig {
  [key: string]: string; // key -> relative path from project root
}

const exampleFiles: ExampleConfig = {
  image: "examples/claude/image.py",
  chain: "examples/claude/chain.py",
  parallelization: "examples/claude/parallelization.py",
  routing: "examples/claude/route.py",
};

export function exampleSourceLoader(): Plugin {
  return {
    name: "example-source-loader",
    resolveId(id) {
      if (id === "virtual:example-sources") {
        return id;
      }
    },
    load(id) {
      if (id === "virtual:example-sources") {
        // Read example files from the file system
        const projectRoot = resolve(__dirname, "../..");
        const sources: Record<string, string> = {};

        for (const [key, filePath] of Object.entries(exampleFiles)) {
          try {
            const fullPath = resolve(projectRoot, filePath);
            const content = readFileSync(fullPath, "utf-8");
            sources[key] = content;
          } catch (error) {
            console.warn(
              `Warning: Could not read example file ${filePath}:`,
              error
            );
            sources[key] = `// Error loading ${filePath}`;
          }
        }

        // Generate the TypeScript module with proper escaping
        const sourceEntries = Object.entries(sources)
          .map(([key, content]) => {
            // Escape backticks and ${} expressions in the content
            const escapedContent = content
              .replace(/\\/g, "\\\\")
              .replace(/`/g, "\\`")
              .replace(/\$\{/g, "\\${");
            return `  ${JSON.stringify(key)}: \`${escapedContent}\``;
          })
          .join(",\n");

        return `
// Auto-generated from example Python files
export const exampleSourceCode = {
${sourceEntries}
};

// Map canvas titles to source code keys
export const getSourceCodeForCanvas = (canvasTitle) => {
  const titleToKey = {
    "Image Comparison": "image",
    "Chain": "chain",
    "Parallelization": "parallelization",
    "Support Ticket Routing": "routing",
  };

  const key = titleToKey[canvasTitle];
  return key ? exampleSourceCode[key] : undefined;
};

// Generate GitHub links for example files
export const getGithubLinkForCanvas = (canvasTitle) => {
  const titleToKey = {
    "Image Comparison": "image",
    "Chain": "chain",
    "Parallelization": "parallelization",
    "Support Ticket Routing": "routing",
  };

  const exampleFiles = {
    image: "examples/claude/image.py",
    chain: "examples/claude/chain.py",
    parallelization: "examples/claude/parallelization.py",
    routing: "examples/claude/route.py",
  };

  const key = titleToKey[canvasTitle];
  const filePath = key ? exampleFiles[key] : undefined;
  
  return filePath ? \`https://github.com/LittleLittleCloud/llm-canvas/blob/main/\${filePath}\` : undefined;
};
`;
      }
    },
  };
}

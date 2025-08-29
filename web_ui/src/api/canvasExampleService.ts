import type { CanvasData, CanvasSummary } from "../client";

// Import the example canvas JSON files
import chainExample from "../examples/chain.json";
import imageExample from "../examples/image.json";
import parallelizationExample from "../examples/parallelization.json";
import routingExample from "../examples/routing.json";

class CanvasExampleService {
  private examples: CanvasData[] = [
    imageExample as CanvasData,
    chainExample as CanvasData,
    parallelizationExample as CanvasData,
    routingExample as CanvasData,
  ];

  /**
   * Lists all available canvas examples with summary information
   */
  async listExamples(): Promise<CanvasSummary[]> {
    return this.examples.map(canvas => this.toCanvasSummary(canvas));
  }

  /**
   * Fetches a specific canvas example by ID
   */
  async fetchCanvas(canvasId: string): Promise<CanvasData | null> {
    const example = this.examples.find(canvas => canvas.canvas_id === canvasId);
    return example || null;
  }

  /**
   * Gets all available example canvas IDs
   */
  getExampleIds(): string[] {
    return this.examples.map(canvas => canvas.canvas_id);
  }

  /**
   * Checks if a given canvas ID corresponds to an example
   */
  isExampleCanvas(canvasId: string): boolean {
    return this.getExampleIds().includes(canvasId);
  }

  /**
   * Gets example canvas by title (case-insensitive)
   */
  async fetchExampleByTitle(title: string): Promise<CanvasData | null> {
    const example = this.examples.find(
      canvas => canvas.title?.toLowerCase() === title.toLowerCase()
    );
    return example || null;
  }

  /**
   * Converts a CanvasData object to a CanvasSummary
   */
  private toCanvasSummary(canvas: CanvasData): CanvasSummary {
    // Count root nodes (nodes with no parent)
    const rootNodes = Object.values(canvas.nodes || {}).filter(
      node => !node.parent_id
    );

    return {
      canvas_id: canvas.canvas_id,
      title: canvas.title || "Untitled Canvas",
      description: canvas.description || null,
      created_at: canvas.created_at,
      node_count: Object.keys(canvas.nodes || {}).length,
      root_ids: rootNodes.map(node => node.id),
      meta: {}, // Add empty meta object as required by the type
    };
  }
}

// Export a singleton instance
export const canvasExampleService = new CanvasExampleService();
export default canvasExampleService;

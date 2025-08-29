import { AlertCircle, Loader2, RotateCcw } from "lucide-react";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { canvasExampleService } from "../api/canvasExampleService";
import { ExampleCard } from "../components/ExampleCard";
import {
  getGithubLinkForCanvas,
  getSourceCodeForCanvas,
} from "../examples/sourceCode";
import { CanvasData } from "../types";

export const GithubGalleryPage: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [canvasDatas, setCanvasDatas] = useState<CanvasData[]>([]);

  const loadCanvases = async () => {
    try {
      // Always use example service for GitHub Pages mode
      const examples = await canvasExampleService.listExamples();
      const canvasDatas: CanvasData[] = [];

      for (const example of examples) {
        const data = await canvasExampleService.fetchCanvas(example.canvas_id);
        canvasDatas.push(data!);
      }
      setCanvasDatas(canvasDatas);
      setError(null);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to load canvas examples"
      );
    }
  };

  useEffect(() => {
    const loadCanvasesWrapper = async () => {
      setLoading(true);
      await loadCanvases();
      setLoading(false);
    };

    // Load examples immediately
    loadCanvasesWrapper();

    // No periodic refresh needed for GitHub Pages mode since examples are static
  }, []);

  const handleOpenCanvas = (id: string) => {
    navigate(`/canvas/${encodeURIComponent(id)}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50 dark:from-gray-900 dark:to-slate-900">
        <div className="p-8">
          <div className="max-w-6xl mx-auto">
            <div className="flex justify-between items-center mb-12">
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                  Interactive Example Gallery
                </h1>
                <p className="text-gray-600 dark:text-gray-300 mt-2">
                  Loading example canvases...
                </p>
              </div>
              <div className="px-6 py-3 bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 font-medium rounded-xl border border-gray-200 dark:border-gray-700">
                <svg
                  className="w-5 h-5 mr-2 inline"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                  />
                </svg>
                Demo Mode
              </div>
            </div>
            <div className="flex items-center justify-center py-20">
              <div className="text-center">
                <div className="mx-auto w-16 h-16 bg-gradient-to-br from-indigo-100 to-purple-100 dark:from-indigo-900 dark:to-purple-900 rounded-full flex items-center justify-center mb-4">
                  <Loader2 className="w-8 h-8 text-indigo-600 dark:text-indigo-400 animate-spin" />
                </div>
                <p className="text-gray-600 dark:text-gray-300">
                  Loading example canvases...
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50 dark:from-gray-900 dark:to-slate-900">
        <div className="p-8">
          <div className="max-w-6xl mx-auto">
            <div className="flex justify-between items-center mb-12">
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                  Interactive Example Gallery
                </h1>
                <p className="text-red-600 dark:text-red-400 mt-2">
                  Failed to load example canvases
                </p>
              </div>
              <button
                onClick={() => loadCanvases()}
                className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-medium rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-all duration-200"
              >
                <RotateCcw className="w-5 h-5 mr-2 inline" />
                Retry
              </button>
            </div>
            <div className="flex items-center justify-center py-20">
              <div className="text-center">
                <div className="mx-auto w-16 h-16 bg-red-100 dark:bg-red-900 rounded-full flex items-center justify-center mb-4">
                  <AlertCircle className="w-8 h-8 text-red-600 dark:text-red-400" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
                  Something went wrong
                </h3>
                <p className="text-red-600 dark:text-red-400 mb-4">{error}</p>
                <button
                  onClick={() => loadCanvases()}
                  className="inline-flex items-center px-4 py-2 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors"
                >
                  Try again
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-8 bg-gradient-to-br from-slate-50 to-indigo-50 dark:from-gray-900 dark:to-slate-900">
      {/* Header with Demo Mode indicator */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
            Interactive Example Gallery
          </h1>
          <p className="text-gray-600 dark:text-gray-300 mt-2">
            Explore LLM Canvas examples with both source code and interactive
            previews
          </p>
        </div>
      </div>

      {/* Canvas Grid */}
      <div className="grid grid-cols-1 gap-4">
        {canvasDatas.map(canvas => (
          <ExampleCard
            key={canvas.canvas_id}
            canvas={canvas}
            sourceCode={getSourceCodeForCanvas(canvas.title || "")}
            sourceCodeLink={getGithubLinkForCanvas(canvas.title || "")}
          />
        ))}
      </div>
    </div>
  );
};

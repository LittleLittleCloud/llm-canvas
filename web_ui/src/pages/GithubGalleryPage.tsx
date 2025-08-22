import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { canvasExampleService } from "../api/canvasExampleService";
import { CanvasCard } from "../components/CanvasCard";
import { CanvasSummary } from "../types";

export const GithubGalleryPage: React.FC = () => {
  const navigate = useNavigate();
  const [canvasSummaries, setCanvasSummaries] = useState<CanvasSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadCanvases = async () => {
    try {
      // Always use example service for GitHub Pages mode
      const examples = await canvasExampleService.listExamples();
      setCanvasSummaries(examples);
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

  const handleCreateCanvas = async () => {
    // Canvas creation is disabled in GitHub Pages mode
    throw new Error(
      "Canvas creation is not available in GitHub Pages mode. This is a demo gallery showcasing example canvases."
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50 dark:from-gray-900 dark:to-slate-900">
        <div className="p-8">
          <div className="max-w-6xl mx-auto">
            <div className="flex justify-between items-center mb-12">
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                  Example Gallery
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
                  <svg
                    className="w-8 h-8 text-indigo-600 dark:text-indigo-400 animate-spin"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
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
                  Example Gallery
                </h1>
                <p className="text-red-600 dark:text-red-400 mt-2">
                  Failed to load example canvases
                </p>
              </div>
              <button
                onClick={() => loadCanvases()}
                className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-medium rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-all duration-200"
              >
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
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
                Retry
              </button>
            </div>
            <div className="flex items-center justify-center py-20">
              <div className="text-center">
                <div className="mx-auto w-16 h-16 bg-red-100 dark:bg-red-900 rounded-full flex items-center justify-center mb-4">
                  <svg
                    className="w-8 h-8 text-red-600 dark:text-red-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50 dark:from-gray-900 dark:to-slate-900">
      <div className="p-8">
        <div className="max-w-6xl mx-auto">
          {/* Header with Demo Mode indicator */}
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                Example Gallery
              </h1>
              <p className="text-gray-600 dark:text-gray-300 mt-2">
                Explore interactive examples of LLM Canvas conversations
              </p>
            </div>
            <div className="flex items-center space-x-3">
              <div className="px-4 py-2 bg-amber-100 dark:bg-amber-900/30 text-amber-800 dark:text-amber-300 font-medium rounded-lg border border-amber-200 dark:border-amber-800">
                <svg
                  className="w-4 h-4 mr-2 inline"
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
          </div>

          {/* Gallery Content */}
          {canvasSummaries.length === 0 ? (
            <div className="text-center py-20">
              <div className="mx-auto w-24 h-24 bg-gradient-to-br from-indigo-100 to-purple-100 dark:from-indigo-900/30 dark:to-purple-900/30 rounded-full flex items-center justify-center mb-6">
                <svg
                  className="w-12 h-12 text-indigo-600 dark:text-indigo-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">
                No examples available
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-8 max-w-md mx-auto">
                Example canvases will appear here once they are loaded.
              </p>
            </div>
          ) : (
            <>
              {/* Canvas Grid */}
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {canvasSummaries.map(canvas => (
                  <CanvasCard
                    key={canvas.canvas_id}
                    canvas={canvas}
                    onOpen={handleOpenCanvas}
                    showDeleteButton={false} // Always hide delete button in GitHub Pages mode
                  />
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

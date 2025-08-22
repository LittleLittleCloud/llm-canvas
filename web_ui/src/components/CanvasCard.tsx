import React from "react";
import { CanvasSummary } from "../types";

interface CanvasCardProps {
  canvas: CanvasSummary;
  onOpen: (id: string) => void;
  onDelete?: (id: string, e: React.MouseEvent) => void;
  showDeleteButton?: boolean;
  isDeleting?: boolean;
}

const formatTs = (ts: number) => {
  try {
    const d = new Date(ts * 1000);
    return d.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  } catch {
    return "";
  }
};

const formatTimeAgo = (ts: number) => {
  try {
    const now = Date.now();
    const diff = now - ts * 1000;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor(diff / (1000 * 60));

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return "Just now";
  } catch {
    return "";
  }
};

export const CanvasCard: React.FC<CanvasCardProps> = ({
  canvas,
  onOpen,
  onDelete,
  showDeleteButton = true,
  isDeleting = false,
}) => {
  return (
    <div
      key={canvas.canvas_id}
      className="group relative bg-white dark:bg-gray-800 rounded-2xl shadow-sm hover:shadow-xl border border-gray-100 dark:border-gray-700 overflow-hidden transition-all duration-300 hover:scale-[1.02] hover:-translate-y-1"
    >
      {/* Canvas Header with Gradient */}
      <div className="h-2 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500" />

      {/* Canvas Content */}
      <div className="relative">
        {/* Main clickable area */}
        <button
          onClick={() => onOpen(canvas.canvas_id)}
          className="w-full p-6 text-left focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-inset"
        >
          {/* Title */}
          <div className="mb-2">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 truncate group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
              {canvas.title || "Untitled Canvas"}
            </h3>
          </div>

          {/* Stats - right below title */}
          <div className="flex items-center gap-4 mb-4">
            <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
              <svg
                className="w-4 h-4 mr-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"
                />
              </svg>
              {canvas.node_count} nodes
            </div>
            <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
              <svg
                className="w-4 h-4 mr-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
              {canvas.root_ids.length} roots
            </div>
          </div>

          {/* Description - fixed height */}
          <div className="mb-4 h-16">
            {canvas.description ? (
              <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-3 leading-relaxed">
                {canvas.description}
              </p>
            ) : (
              <p className="text-sm text-gray-400 dark:text-gray-500 italic">
                No description provided
              </p>
            )}
          </div>

          {/* Footer */}
          <div className="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-gray-700">
            <div className="text-xs text-gray-500 dark:text-gray-400">
              Created {formatTs(canvas.created_at)}
            </div>
            <div className="text-xs text-gray-400 dark:text-gray-500">
              {formatTimeAgo(canvas.created_at)}
            </div>
          </div>

          {/* Hover indicator */}
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500 to-purple-500 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300" />
        </button>

        {/* Delete button positioned absolutely */}
        {showDeleteButton && onDelete && (
          <button
            onClick={e => onDelete(canvas.canvas_id, e)}
            disabled={isDeleting}
            className="absolute top-4 right-4 p-2 text-gray-400 hover:text-red-500 dark:text-gray-500 dark:hover:text-red-400 focus:outline-none focus:text-red-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed bg-white dark:bg-gray-800 rounded-lg shadow-sm opacity-0 group-hover:opacity-100 hover:shadow-md"
            title="Delete canvas"
          >
            {isDeleting ? (
              <svg
                className="w-4 h-4 animate-spin"
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
            ) : (
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            )}
          </button>
        )}
      </div>
    </div>
  );
};

import React, { useState } from "react";
import { CanvasSummary } from "../types";

interface Props {
  canvasSummaries: CanvasSummary[];
  onOpen: (id: string) => void;
  onCreate: (title?: string, description?: string) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
  showCreateButton?: boolean; // Optional prop to control Create Canvas button visibility
  showDeleteButton?: boolean; // Optional prop to control delete button visibility
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

// Modal Component
const CreateCanvasModal: React.FC<{
  isOpen: boolean;
  onClose: () => void;
  onCreate: (title?: string, description?: string) => Promise<void>;
}> = ({ isOpen, onClose, onCreate }) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [isCreating, setIsCreating] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsCreating(true);
    try {
      await onCreate(title || undefined, description || undefined);
      setTitle("");
      setDescription("");
      onClose();
    } catch (error) {
      console.error("Failed to create canvas:", error);
    } finally {
      setIsCreating(false);
    }
  };

  const handleClose = () => {
    if (!isCreating) {
      setTitle("");
      setDescription("");
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
        onClick={handleClose}
      />

      {/* Modal */}
      <div className="flex min-h-full items-center justify-center p-4">
        <div className="relative transform overflow-hidden rounded-2xl bg-white dark:bg-gray-800 shadow-2xl transition-all w-full max-w-md">
          {/* Header */}
          <div className="px-6 pt-6 pb-4">
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                Create New Canvas
              </h3>
              <button
                onClick={handleClose}
                disabled={isCreating}
                className="rounded-lg p-1 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                <svg
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="px-6 pb-6">
            <div className="space-y-4">
              <div>
                <label
                  htmlFor="modal-title"
                  className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                >
                  Title
                </label>
                <input
                  type="text"
                  id="modal-title"
                  value={title}
                  onChange={e => setTitle(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl shadow-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  placeholder="Enter a descriptive title..."
                  disabled={isCreating}
                />
              </div>

              <div>
                <label
                  htmlFor="modal-description"
                  className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                >
                  Description
                </label>
                <textarea
                  id="modal-description"
                  value={description}
                  onChange={e => setDescription(e.target.value)}
                  rows={3}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl shadow-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all resize-none"
                  placeholder="What will you use this canvas for?"
                  disabled={isCreating}
                />
              </div>
            </div>

            {/* Actions */}
            <div className="flex gap-3 mt-6">
              <button
                type="button"
                onClick={handleClose}
                disabled={isCreating}
                className="flex-1 px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-xl hover:bg-gray-200 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={isCreating}
                className="flex-1 px-4 py-3 text-sm font-medium text-white bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isCreating ? (
                  <div className="flex items-center justify-center">
                    <svg
                      className="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
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
                      ></circle>
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      ></path>
                    </svg>
                    Creating...
                  </div>
                ) : (
                  "Create Canvas"
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export const CanvasGallery: React.FC<Props> = ({
  canvasSummaries,
  onOpen,
  onCreate,
  onDelete,
  showCreateButton = true, // Default to true for backward compatibility
  showDeleteButton = true, // Default to true for backward compatibility
}) => {
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [deletingIds, setDeletingIds] = useState<Set<string>>(new Set());

  const handleDeleteCanvas = async (canvasId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (
      !confirm(
        "Are you sure you want to delete this canvas? This action cannot be undone."
      )
    ) {
      return;
    }

    setDeletingIds(prev => new Set([...prev, canvasId]));
    try {
      await onDelete(canvasId);
    } catch (error) {
      console.error("Failed to delete canvas:", error);
    } finally {
      setDeletingIds(prev => {
        const newSet = new Set(prev);
        newSet.delete(canvasId);
        return newSet;
      });
    }
  };

  if (!canvasSummaries.length) {
    return (
      <div className="h-full bg-gradient-to-br from-slate-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
        <div className="p-8">
          <div className="max-w-6xl mx-auto">
            {/* Header */}
            <div className="flex justify-between items-center mb-12">
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 dark:from-gray-100 dark:to-gray-400 bg-clip-text text-transparent">
                  Canvas Gallery
                </h1>
                <p className="text-gray-600 dark:text-gray-400 mt-2">
                  Create and manage your AI conversation canvases
                </p>
              </div>
              {showCreateButton && (
                <button
                  onClick={() => setShowCreateModal(true)}
                  className="group relative overflow-hidden px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-medium rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-all duration-200"
                >
                  <span className="relative z-10 flex items-center">
                    <svg
                      className="w-5 h-5 mr-2"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 4v16m8-8H4"
                      />
                    </svg>
                    Create Canvas
                  </span>
                  <div className="absolute inset-0 bg-gradient-to-r from-indigo-700 to-purple-700 opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
                </button>
              )}
            </div>

            {/* Empty State */}
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
                No canvases yet
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-8 max-w-md mx-auto">
                Get started by creating your first canvas. Perfect for AI
                conversations, brainstorming, and collaborative thinking.
              </p>
              {showCreateButton && (
                <button
                  onClick={() => setShowCreateModal(true)}
                  className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-medium rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-all duration-200"
                >
                  <svg
                    className="w-5 h-5 mr-2"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 4v16m8-8H4"
                    />
                  </svg>
                  Create Your First Canvas
                </button>
              )}
            </div>
          </div>
        </div>

        {showCreateButton && (
          <CreateCanvasModal
            isOpen={showCreateModal}
            onClose={() => setShowCreateModal(false)}
            onCreate={onCreate}
          />
        )}
      </div>
    );
  }

  return (
    <div className="h-full bg-gradient-to-br from-slate-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
      <div className="p-8">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="flex justify-between items-center mb-12">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 dark:from-gray-100 dark:to-gray-400 bg-clip-text text-transparent">
                Canvas Gallery
              </h1>
              <p className="text-gray-600 dark:text-gray-400 mt-2">
                {canvasSummaries.length} canvas
                {canvasSummaries.length !== 1 ? "es" : ""} available
              </p>
            </div>
            {showCreateButton && (
              <button
                onClick={() => setShowCreateModal(true)}
                className="group relative overflow-hidden px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-medium rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-all duration-200"
              >
                <span className="relative z-10 flex items-center">
                  <svg
                    className="w-5 h-5 mr-2"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 4v16m8-8H4"
                    />
                  </svg>
                  Create Canvas
                </span>
                <div className="absolute inset-0 bg-gradient-to-r from-indigo-700 to-purple-700 opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
              </button>
            )}
          </div>

          {/* Canvas Grid */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {canvasSummaries.map(canvas => (
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

                    {/* Footer without delete button */}
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
                  {showDeleteButton && (
                    <button
                      onClick={e => handleDeleteCanvas(canvas.canvas_id, e)}
                      disabled={deletingIds.has(canvas.canvas_id)}
                      className="absolute top-4 right-4 p-2 text-gray-400 hover:text-red-500 dark:text-gray-500 dark:hover:text-red-400 focus:outline-none focus:text-red-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed bg-white dark:bg-gray-800 rounded-lg shadow-sm opacity-0 group-hover:opacity-100 hover:shadow-md"
                      title="Delete canvas"
                    >
                      {deletingIds.has(canvas.canvas_id) ? (
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
            ))}
          </div>
        </div>
      </div>

      {showCreateButton && (
        <CreateCanvasModal
          isOpen={showCreateModal}
          onClose={() => setShowCreateModal(false)}
          onCreate={onCreate}
        />
      )}
    </div>
  );
};

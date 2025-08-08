import React from "react";
import { CanvasData } from "../types";

interface Props {
  canvases: CanvasData[];
  onOpen: (id: string) => void;
}

const formatTs = (ts: number) => {
  try {
    const d = new Date(ts * 1000);
    return d.toLocaleString();
  } catch {
    return "";
  }
};

export const CanvasGallery: React.FC<Props> = ({ canvases, onOpen }) => {
  if (!canvases.length) {
    return (
      <div className="p-8 text-center text-gray-500 text-sm">
        No canvases available.
      </div>
    );
  }

  return (
    <div className="p-6 max-w-5xl mx-auto grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {canvases.map(c => (
        <button
          key={c.canvas_id}
          onClick={() => onOpen(c.canvas_id)}
          className="group text-left rounded border bg-white shadow-sm p-4 hover:shadow-md transition flex flex-col gap-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          <div className="flex items-center justify-between gap-2">
            <h2 className="font-semibold text-sm truncate group-hover:text-indigo-600">
              {c.title || c.canvas_id}
            </h2>
            <span className="text-[10px] font-mono px-1 py-0.5 rounded bg-indigo-50 text-indigo-600 border border-indigo-200">
              {c.root_ids.length} roots
            </span>
          </div>
          {c.description && (
            <p className="text-xs text-gray-600 line-clamp-3">
              {c.description}
            </p>
          )}
          <div className="mt-auto flex items-center justify-between text-[10px] text-gray-400 pt-2 border-t">
            <span>{formatTs(c.created_at)}</span>
            <span className="italic">{Object.keys(c.nodes).length} nodes</span>
          </div>
        </button>
      ))}
    </div>
  );
};

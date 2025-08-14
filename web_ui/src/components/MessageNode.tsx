import React from "react";
import { MessageNode } from "../types";
import { MessageBlockView } from "./MessageBlockView";

interface Props {
  node: MessageNode;
}

export const MessageNodeComponent: React.FC<Props> = ({ node }) => {
  const role = node.message.role;
  const content = node.message.content;

  return (
    <div className="rounded-xl border-0 p-2 space-y-3 text-sm leading-relaxed">
      <div className="flex items-center gap-2 mb-3">
        <div
          className={`w-2 h-2 rounded-full ${
            role === "user"
              ? "bg-gradient-to-r from-blue-500 to-cyan-500"
              : role === "assistant"
                ? "bg-gradient-to-r from-indigo-500 to-purple-500"
                : "bg-gradient-to-r from-gray-400 to-gray-500"
          }`}
        ></div>
        <div className="text-xs uppercase tracking-wider text-gray-600 font-semibold">
          {role}
        </div>
      </div>
      <div className="overflow-y-auto max-h-96 message-content">
        {/* Add content here */}
        {typeof content === "string" && (
          <div className="whitespace-pre-wrap text-gray-800 leading-relaxed">
            {content}
          </div>
        )}
        {Array.isArray(content) && (
          <div className="space-y-2">
            {content.map((b, i) => (
              <MessageBlockView key={i} block={b} index={i} />
            ))}
          </div>
        )}
      </div>
      {node.meta != null && typeof node.meta["model"] === "string" && (
        <div className="text-xs text-gray-500 pt-3 border-t border-gray-100 flex items-center gap-1">
          <svg
            className="w-3 h-3"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
            />
          </svg>
          model: {node.meta["model"] as string}
        </div>
      )}
    </div>
  );
};

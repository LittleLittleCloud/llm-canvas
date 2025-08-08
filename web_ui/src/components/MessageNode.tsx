import React from "react";
import { MessageBlock, MessageNode } from "../types";
import { MessageBlockView } from "./MessageBlockView";

interface Props {
  node: MessageNode;
}

export const MessageNodeComponent: React.FC<Props> = ({ node }) => {
  const role = node.content.role;
  const content = node.content.content;
  const blocks: MessageBlock[] | null = Array.isArray(content) ? content : null;

  return (
    <div className="rounded border bg-white shadow-sm p-3 space-y-1 text-[13px] leading-snug">
      <div className="text-[10px] uppercase tracking-wide text-gray-500 font-semibold">
        {role}
      </div>
      <div className="overflow-y-auto">
        {/* Add content here */}
        {typeof content === "string" && (
          <div className="whitespace-pre-wrap text-sm">{content}</div>
        )}
        {blocks && (
          <div className="space-y-1">
            {blocks.map((b, i) => (
              <MessageBlockView key={i} block={b} index={i} />
            ))}
          </div>
        )}
      </div>
      {node.meta?.model && (
        <div className="text-[10px] text-gray-400 pt-1">
          model: {node.meta.model}
        </div>
      )}
    </div>
  );
};

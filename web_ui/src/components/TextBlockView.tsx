import { TextBlockParam } from "@anthropic-ai/sdk/resources/messages";
import React from "react";
import { CopyButton } from "./CopyButton";
import { MarkdownRenderer } from "./MarkdownRenderer";

interface Props {
  block: TextBlockParam;
}

export const TextBlockView: React.FC<Props> = ({ block }) => {
  return (
    <div className="text-sm relative group">
      <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity z-10">
        <CopyButton content={block.text} />
      </div>
      <MarkdownRenderer
        content={block.text}
        className="leading-snug"
        preserveLineBreaks={true}
      />
    </div>
  );
};

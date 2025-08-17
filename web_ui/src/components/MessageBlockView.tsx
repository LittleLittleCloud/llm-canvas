import React from "react";
import { MessageBlock } from "../types";
import { TextBlockView } from "./TextBlockView";
import { ToolResultBlockView } from "./ToolResultBlockView";
import { ToolUseBlockView } from "./ToolUseBlockView";

interface Props {
  block: MessageBlock;
  index?: number;
}

export const MessageBlockView: React.FC<Props> = ({ block }) => {
  switch (block.type) {
    case "text":
      return <TextBlockView block={block} />;
    case "tool_use":
      return <ToolUseBlockView block={block} />;
    case "tool_result":
      return <ToolResultBlockView block={block} />;
    default:
      return (
        <div className="text-xs text-gray-400 dark:text-gray-500">
          Unsupported block
        </div>
      );
  }
};

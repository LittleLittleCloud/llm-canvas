import { TextBlockParam } from "@anthropic-ai/sdk/resources/messages";
import React from "react";

interface Props {
  block: TextBlockParam;
}

export const TextBlockView: React.FC<Props> = ({ block }) => {
  return (
    <div className="text-sm whitespace-pre-wrap leading-snug">{block.text}</div>
  );
};

import { ToolUseBlockParam } from "@anthropic-ai/sdk/resources/messages";
import React from "react";

interface Props {
  block: ToolUseBlockParam;
}

const truncate = (val: string, max = 400) =>
  val.length > max ? val.slice(0, max) + "…" : val;

export const ToolUseBlockView: React.FC<Props> = ({ block }) => {
  return (
    <div className="rounded border border-indigo-200 bg-indigo-50 px-2 py-1 space-y-1">
      <div className="flex items-center gap-2 text-[10px] uppercase tracking-wide text-indigo-600 font-semibold">
        <span className="px-1 rounded bg-indigo-600 text-white">TOOL</span>
        <span className="font-mono text-[11px]">{block.name}</span>
      </div>
      {block.input ? (
        <pre className="m-0 p-0 text-xs leading-tight font-mono text-indigo-800 overflow-x-auto max-h-28">
          {truncate(JSON.stringify(block.input as any, null, 2))}
        </pre>
      ) : null}
    </div>
  );
};

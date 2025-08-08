import {
  ImageBlockParam,
  TextBlockParam,
  ToolResultBlockParam,
} from "@anthropic-ai/sdk/resources/messages";
import React from "react";

interface Props {
  block: ToolResultBlockParam;
}

const truncate = (val: string, max = 600) =>
  val.length > max ? val.slice(0, max) + "…" : val;

export const ToolResultBlockView: React.FC<Props> = ({ block }) => {
  const isError = (block as any).is_error as boolean | undefined;
  const badgeClr = isError
    ? "bg-rose-600 text-white"
    : "bg-emerald-600 text-white";
  const badgeLabel = isError ? "ERROR" : "RESULT";
  const content = block.content as
    | string
    | (TextBlockParam | ImageBlockParam)[];

  return (
    <div
      className={`rounded border px-2 py-1 space-y-1 ${
        isError
          ? "border-rose-300 bg-rose-50"
          : "border-emerald-200 bg-emerald-50"
      }`}
    >
      <div className="flex items-center gap-2 text-[10px] uppercase tracking-wide font-semibold">
        <span className={`px-1 rounded ${badgeClr}`}>{badgeLabel}</span>
        <span className="text-[10px] text-gray-500 font-mono">
          ↔ {block.tool_use_id}
        </span>
      </div>
      {typeof content === "string" ? (
        <pre className="m-0 p-0 text-xs leading-tight font-mono whitespace-pre-wrap">
          {truncate(content)}
        </pre>
      ) : (
        <div className="space-y-1">
          {content.map((c, i) => (
            <div
              key={i}
              className="text-xs whitespace-pre-wrap leading-snug font-mono"
            >
              {c.type === "text" && truncate((c as TextBlockParam).text, 400)}
              {c.type !== "text" && <span>[unsupported block]</span>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

import type { TextBlockParam } from "./TextBlockParam";
import type { ToolResultBlockParam } from "./ToolResultBlockParam";
import type { ToolUseBlockParam } from "./ToolUseBlockParam";

/**
 * Message structure for canvas conversations.
 */
export type Message = {
  content:
    | string
    | Array<
        TextBlockParam | ToolUseBlockParam | ToolResultBlockParam | unknown
      >;
  role: "user" | "assistant" | "system";
};

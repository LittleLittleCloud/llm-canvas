import {
  ImageBlockParam,
  TextBlockParam,
  ToolResultBlockParam,
  ToolUseBlockParam,
} from "./client";

// Re-export the generated client types and add custom union types
export * from "./client";

// Custom union type for message blocks
export type MessageBlock =
  | TextBlockParam
  | ToolUseBlockParam
  | ToolResultBlockParam
  | ImageBlockParam;

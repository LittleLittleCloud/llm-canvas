import {
  TextBlockParam,
  ToolResultBlockParam,
  ToolUseBlockParam,
} from "@anthropic-ai/sdk/resources/messages";

export type MessageBlock =
  | TextBlockParam
  | ToolUseBlockParam
  | ToolResultBlockParam;

export type Message = {
  content: string | MessageBlock[];
  role: "user" | "assistant" | "system";
};

export interface MessageNode {
  id: string;
  content: Message;
  parent_id?: string | null;
  child_ids: string[];
  meta?: Record<string, any>;
}

export interface CanvasData {
  title?: string;
  last_updated?: number;
  description?: string;
  canvas_id: string;
  created_at: number;
  root_ids: string[];
  nodes: Record<string, MessageNode>;
}

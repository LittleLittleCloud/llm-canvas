import type { CacheControlEphemeralParam } from "./CacheControlEphemeralParam";

export type ToolUseBlockParam = {
  id: string;
  input: unknown;
  name: string;
  type: "tool_use";
  cache_control?: CacheControlEphemeralParam | null;
};

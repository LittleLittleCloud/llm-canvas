import type { CacheControlEphemeralParam } from "./CacheControlEphemeralParam";
import type { ImageBlockParam } from "./ImageBlockParam";
import type { SearchResultBlockParam } from "./SearchResultBlockParam";
import type { TextBlockParam } from "./TextBlockParam";

export type ToolResultBlockParam = {
  tool_use_id: string;
  type: "tool_result";
  cache_control?: CacheControlEphemeralParam | null;
  content?:
    | string
    | Array<TextBlockParam | ImageBlockParam | SearchResultBlockParam>;
  is_error?: boolean;
};

import type { CacheControlEphemeralParam } from "./CacheControlEphemeralParam";
import type { CitationsConfigParam } from "./CitationsConfigParam";
import type { TextBlockParam } from "./TextBlockParam";

export type SearchResultBlockParam = {
  content: Array<TextBlockParam>;
  source: string;
  title: string;
  type: "search_result";
  cache_control?: CacheControlEphemeralParam | null;
  citations?: CitationsConfigParam;
};

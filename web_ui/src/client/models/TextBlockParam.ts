import type { CacheControlEphemeralParam } from "./CacheControlEphemeralParam";
import type { CitationCharLocationParam } from "./CitationCharLocationParam";
import type { CitationContentBlockLocationParam } from "./CitationContentBlockLocationParam";
import type { CitationPageLocationParam } from "./CitationPageLocationParam";
import type { CitationSearchResultLocationParam } from "./CitationSearchResultLocationParam";
import type { CitationWebSearchResultLocationParam } from "./CitationWebSearchResultLocationParam";

export type TextBlockParam = {
  text: string;
  type: "text";
  cache_control?: CacheControlEphemeralParam | null;
  citations?: Array<
    | CitationCharLocationParam
    | CitationPageLocationParam
    | CitationContentBlockLocationParam
    | CitationWebSearchResultLocationParam
    | CitationSearchResultLocationParam
  > | null;
};

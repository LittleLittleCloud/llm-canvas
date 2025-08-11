export type CitationSearchResultLocationParam = {
  cited_text: string;
  end_block_index: number;
  search_result_index: number;
  source: string;
  start_block_index: number;
  title: string | null;
  type: "search_result_location";
};

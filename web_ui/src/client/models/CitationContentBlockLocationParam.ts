export type CitationContentBlockLocationParam = {
  cited_text: string;
  document_index: number;
  document_title: string | null;
  end_block_index: number;
  start_block_index: number;
  type: "content_block_location";
};

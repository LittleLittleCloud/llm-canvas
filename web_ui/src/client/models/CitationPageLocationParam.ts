export type CitationPageLocationParam = {
  cited_text: string;
  document_index: number;
  document_title: string | null;
  end_page_number: number;
  start_page_number: number;
  type: "page_location";
};

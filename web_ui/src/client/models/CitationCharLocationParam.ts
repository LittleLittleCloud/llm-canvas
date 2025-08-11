export type CitationCharLocationParam = {
  cited_text: string;
  document_index: number;
  document_title: string | null;
  end_char_index: number;
  start_char_index: number;
  type: "char_location";
};

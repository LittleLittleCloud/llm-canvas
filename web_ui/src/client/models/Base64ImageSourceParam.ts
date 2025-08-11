export type Base64ImageSourceParam = {
  data: string;
  media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp";
  type: "base64";
};

import type { Base64ImageSourceParam } from "./Base64ImageSourceParam";
import type { CacheControlEphemeralParam } from "./CacheControlEphemeralParam";
import type { URLImageSourceParam } from "./URLImageSourceParam";

export type ImageBlockParam = {
  source: Base64ImageSourceParam | URLImageSourceParam;
  type: "image";
  cache_control?: CacheControlEphemeralParam | null;
};

import React from "react";
import { ImageBlockParam } from "../types";

interface Props {
  block: ImageBlockParam;
}

export const ImageBlockView: React.FC<Props> = ({ block }) => {
  const { source } = block;

  // Handle different image source types
  const getImageSrc = () => {
    if (source.type === "base64") {
      return `data:${source.media_type};base64,${source.data}`;
    } else if (source.type === "url") {
      return source.url;
    }
    return "";
  };

  const imageSrc = getImageSrc();

  if (!imageSrc) {
    return (
      <div className="text-xs text-gray-400 dark:text-gray-500 p-2 border border-gray-200 dark:border-gray-700 rounded">
        Invalid image source
      </div>
    );
  }

  return (
    <div className="text-sm relative group">
      <div className="max-w-full">
        <img
          src={imageSrc}
          alt="Image content"
          className="max-w-full h-auto rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm"
          style={{ maxHeight: "500px" }}
          onError={e => {
            const target = e.target as HTMLImageElement;
            target.style.display = "none";
            const errorDiv = document.createElement("div");
            errorDiv.className =
              "text-xs text-red-400 p-2 border border-red-200 dark:border-red-700 rounded";
            errorDiv.textContent = "Failed to load image";
            target.parentNode?.insertBefore(errorDiv, target);
          }}
        />
      </div>
    </div>
  );
};

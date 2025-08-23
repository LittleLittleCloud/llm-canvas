import { Code } from "lucide-react";
import React, { useState } from "react";
import { CanvasData } from "../types";
import { CanvasView } from "./CanvasView";
import { CopyButton } from "./CopyButton";
import { SyntaxHighlighter } from "./SyntaxHighlighter";

interface ExampleCardProps {
  canvas: CanvasData;
  sourceCode?: string;
  sourceCodeLink?: string;
}

export const ExampleCard: React.FC<ExampleCardProps> = ({
  canvas,
  sourceCode,
  sourceCodeLink,
}) => {
  const [activeTab, setActiveTab] = useState<"preview" | "code">("preview");

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden border border-gray-200 dark:border-gray-700 transition-all duration-300">
      {/* Header */}
      <div className="p-6 pb-0  border-gray-200 dark:border-gray-700">
        <h3 className="text-xl font-bold text-gray-900 dark:text-gray-100 mb-3">
          {canvas.title}
        </h3>
        {canvas.description && (
          <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-3 leading-relaxed">
            {canvas.description.trim()}
          </p>
        )}
      </div>

      {/* Content */}
      <div className="h-[50rem]">
        {activeTab === "preview" ? (
          <div className="p-6 h-full flex flex-col">
            <CanvasView
              canvas={canvas}
              showControls={true}
              showMiniMap={true}
              showPanel={true}
            />
          </div>
        ) : (
          <div className="h-full relative">
            {sourceCode ? (
              <>
                {/* Header with Copy Button and Source Link */}
                <div className="absolute top-3 right-3 z-10 flex gap-2">
                  {sourceCodeLink && (
                    <a
                      href={sourceCodeLink}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 px-3 py-1.5 text-xs font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200 shadow-sm"
                      title="View source on GitHub"
                    >
                      <Code className="w-3 h-3" />
                      View Source
                    </a>
                  )}
                  <CopyButton content={sourceCode} />
                </div>
                <div className="h-full overflow-auto p-6">
                  <SyntaxHighlighter
                    code={sourceCode}
                    language="python"
                    showLineNumbers={true}
                    customStyle={{
                      height: "100%",
                      background: "transparent",
                    }}
                  />
                </div>
              </>
            ) : sourceCodeLink ? (
              <div className="h-full flex items-center justify-center p-6">
                <div className="text-center">
                  <div className="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mb-4">
                    <Code className="w-8 h-8 text-gray-500 dark:text-gray-400" />
                  </div>
                  <h4 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
                    View Source Code
                  </h4>
                  <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
                    The source code for this example is available on GitHub.
                  </p>
                  <a
                    href={sourceCodeLink}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-600 rounded-lg transition-colors duration-200 shadow-sm"
                  >
                    <Code className="w-4 h-4" />
                    View on GitHub
                  </a>
                </div>
              </div>
            ) : (
              <div className="h-full flex items-center justify-center p-6">
                <div className="text-center">
                  <div className="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mb-4">
                    <Code className="w-8 h-8 text-gray-500 dark:text-gray-400" />
                  </div>
                  <h4 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
                    Source Code Not Available
                  </h4>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    The source code for this example is not currently available.
                  </p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Tab Switcher */}
      <div className="px-6 pb-3 border-gray-200 dark:border-gray-700 flex justify-center">
        <div className="inline-flex bg-gray-100 dark:bg-gray-700 rounded-md p-0.5">
          <button
            onClick={() => setActiveTab("preview")}
            className={`px-3 py-1.5 text-xs font-medium rounded-sm transition-all duration-200 ${
              activeTab === "preview"
                ? "bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 shadow-sm"
                : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200"
            }`}
          >
            Preview
          </button>
          <button
            onClick={() => setActiveTab("code")}
            className={`px-3 py-1.5 text-xs font-medium rounded-sm transition-all duration-200 ${
              activeTab === "code"
                ? "bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 shadow-sm"
                : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200"
            }`}
          >
            Code
          </button>
        </div>
      </div>
    </div>
  );
};

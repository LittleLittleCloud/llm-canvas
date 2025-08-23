import { Code, Eye } from "lucide-react";
import React, { useState } from "react";
import { CanvasData } from "../types";
import { CanvasView } from "./CanvasView";
import { CopyButton } from "./CopyButton";
import { SyntaxHighlighter } from "./SyntaxHighlighter";

interface ExampleCardProps {
  canvas: CanvasData;
  sourceCode?: string;
  onOpenCanvas: (id: string) => void;
}

export const ExampleCard: React.FC<ExampleCardProps> = ({
  canvas,
  sourceCode,
}) => {
  const [activeTab, setActiveTab] = useState<"preview" | "code">("preview");

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden border border-gray-200 dark:border-gray-700 transition-all duration-300">
      {/* Header */}
      <div className="p-6 border-b border-gray-200 dark:border-gray-700">
        <h3 className="text-xl font-bold text-gray-900 dark:text-gray-100 mb-3">
          {canvas.title}
        </h3>
        {canvas.description && (
          <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-3 leading-relaxed">
            {canvas.description.trim()}
          </p>
        )}
      </div>

      {/* Tab Navigation */}
      <div className="flex border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50">
        <button
          onClick={() => setActiveTab("preview")}
          className={`flex-1 px-6 py-4 text-sm font-semibold transition-all duration-200 ${
            activeTab === "preview"
              ? "bg-white dark:bg-gray-800 text-indigo-600 dark:text-indigo-400 border-b-2 border-indigo-600 dark:border-indigo-400 shadow-sm"
              : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-white/50 dark:hover:bg-gray-800/50"
          }`}
        >
          <Eye className="w-4 h-4 mr-2 inline" />
          Canvas Preview
        </button>
        <button
          onClick={() => setActiveTab("code")}
          className={`flex-1 px-6 py-4 text-sm font-semibold transition-all duration-200 ${
            activeTab === "code"
              ? "bg-white dark:bg-gray-800 text-indigo-600 dark:text-indigo-400 border-b-2 border-indigo-600 dark:border-indigo-400 shadow-sm"
              : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-white/50 dark:hover:bg-gray-800/50"
          }`}
        >
          <Code className="w-4 h-4 mr-2 inline" />
          Source Code
        </button>
      </div>

      {/* Content */}
      <div className="h-[48rem]">
        {activeTab === "preview" ? (
          <div className="p-6 h-full flex flex-col">
            <CanvasView
              canvas={canvas}
              showControls={false}
              showMiniMap={true}
              showPanel={false}
            />
          </div>
        ) : (
          <div className="h-full relative">
            {sourceCode ? (
              <>
                {/* Copy Button */}
                <div className="absolute top-3 right-3 z-10">
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
    </div>
  );
};

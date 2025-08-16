import React from "react";
import ReactMarkdown from "react-markdown";
import rehypeHighlight from "rehype-highlight";
import rehypeKatex from "rehype-katex";
import remarkBreaks from "remark-breaks";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";

interface MarkdownRendererProps {
  content: string;
  className?: string;
  preserveLineBreaks?: boolean;
}

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({
  content,
  className = "",
  preserveLineBreaks = true,
}) => {
  const remarkPlugins: any[] = [remarkGfm, remarkMath];
  if (preserveLineBreaks) {
    remarkPlugins.push(remarkBreaks);
  }

  return (
    <div className={`markdown-renderer ${className}`}>
      <ReactMarkdown
        remarkPlugins={remarkPlugins}
        rehypePlugins={[rehypeKatex, rehypeHighlight]}
        components={{
          // Customize code blocks
          code: ({ className, children, ...props }: any) => {
            const match = /language-(\w+)/.exec(className || "");
            const language = match ? match[1] : "";
            const inline = !className?.includes("language-");

            if (!inline) {
              return (
                <div className="relative">
                  {language && (
                    <div className="absolute top-2 right-2 px-2 py-1 text-xs text-gray-500 bg-gray-100 rounded">
                      {language}
                    </div>
                  )}
                  <pre className="bg-gray-50 border rounded-lg p-4 overflow-x-auto">
                    <code className={className} {...props}>
                      {children}
                    </code>
                  </pre>
                </div>
              );
            }

            return (
              <code
                className="bg-gray-100 px-1 py-0.5 rounded text-sm font-mono"
                {...props}
              >
                {children}
              </code>
            );
          },

          // Customize tables
          table: ({ children }) => (
            <div className="overflow-x-auto my-4">
              <table className="min-w-full border-collapse border border-gray-300">
                {children}
              </table>
            </div>
          ),

          th: ({ children }) => (
            <th className="border border-gray-300 bg-gray-50 px-4 py-2 text-left font-semibold">
              {children}
            </th>
          ),

          td: ({ children }) => (
            <td className="border border-gray-300 px-4 py-2">{children}</td>
          ),

          // Customize headings
          h1: ({ children }) => (
            <h1 className="text-2xl font-bold mb-4 mt-6 first:mt-0 border-b border-gray-200 pb-2">
              {children}
            </h1>
          ),

          h2: ({ children }) => (
            <h2 className="text-xl font-bold mb-3 mt-5 first:mt-0">
              {children}
            </h2>
          ),

          h3: ({ children }) => (
            <h3 className="text-lg font-bold mb-2 mt-4 first:mt-0">
              {children}
            </h3>
          ),

          h4: ({ children }) => (
            <h4 className="text-base font-bold mb-2 mt-3 first:mt-0">
              {children}
            </h4>
          ),

          // Customize paragraphs
          p: ({ children }) => (
            <p className="mb-4 last:mb-0 leading-relaxed">{children}</p>
          ),

          // Customize lists
          ul: ({ children }) => (
            <ul className="list-disc list-inside mb-4 space-y-1">{children}</ul>
          ),

          ol: ({ children }) => (
            <ol className="list-decimal list-inside mb-4 space-y-1">
              {children}
            </ol>
          ),

          li: ({ children }) => <li className="leading-relaxed">{children}</li>,

          // Customize blockquotes
          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-gray-300 pl-4 italic my-4 text-gray-700">
              {children}
            </blockquote>
          ),

          // Customize links
          a: ({ href, children }) => (
            <a
              href={href}
              className="text-blue-600 hover:text-blue-800 underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              {children}
            </a>
          ),

          // Customize horizontal rules
          hr: () => <hr className="my-6 border-gray-300" />,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};

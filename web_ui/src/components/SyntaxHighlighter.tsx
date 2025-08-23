import React from "react";
import { Prism as ReactSyntaxHighlighter } from "react-syntax-highlighter";
import {
  oneDark,
  oneLight,
} from "react-syntax-highlighter/dist/esm/styles/prism";
import { useTheme } from "../hooks/useTheme";

interface SyntaxHighlighterProps {
  code: string;
  language?: string;
  showLineNumbers?: boolean;
  className?: string;
  customStyle?: React.CSSProperties;
}

export const SyntaxHighlighter: React.FC<SyntaxHighlighterProps> = ({
  code,
  language = "python",
  showLineNumbers = true,
  className = "",
  customStyle = {},
}) => {
  const { isDark } = useTheme();

  const defaultStyle: React.CSSProperties = {
    margin: 0,
    borderRadius: "0.5rem",
    fontSize: "0.875rem",
    lineHeight: "1.5",
    ...customStyle,
  };

  return (
    <div className={`syntax-highlighter ${className}`}>
      <ReactSyntaxHighlighter
        language={language}
        style={isDark ? oneDark : oneLight}
        showLineNumbers={showLineNumbers}
        customStyle={defaultStyle}
        codeTagProps={{
          style: {
            fontSize: "0.875rem",
            fontFamily:
              'ui-monospace, SFMono-Regular, "SF Mono", Monaco, Consolas, "Liberation Mono", "Courier New", monospace',
          },
        }}
        lineNumberStyle={{
          minWidth: "3em",
          paddingRight: "1em",
          textAlign: "right",
          userSelect: "none",
          opacity: 0.6,
        }}
      >
        {code}
      </ReactSyntaxHighlighter>
    </div>
  );
};

// Primary Logo Component
export const LLMCanvasPrimaryLogo = ({
  size = 200,
  className = "",
  style = "cartoon",
}) => {
  const isCartoon = style === "cartoon";

  return (
    <div className={`inline-flex items-center gap-3 ${className}`}>
      <svg
        width={size * 0.15}
        height={size * 0.15}
        viewBox="0 0 24 24"
        fill="none"
        className="flex-shrink-0"
      >
        {/* Main conversation nodes with varying sizes */}
        <circle cx="5" cy="5" r="2.5" fill="white" opacity="0.9" />
        <circle cx="5" cy="12" r="3" fill="white" />
        <circle cx="5" cy="19" r="2" fill="white" opacity="0.8" />

        {/* Branch conversation nodes */}
        <circle cx="19" cy="8" r="2" fill="white" opacity="0.9" />
        <circle cx="19" cy="16" r="2.5" fill="white" opacity="0.8" />

        {/* Playful curved connection lines */}
        <path
          d="M5 7.5 Q5 9 5 9.5"
          stroke="white"
          strokeWidth="2.5"
          strokeLinecap="round"
        />
        <path
          d="M5 15 Q5 17 5 17"
          stroke="white"
          strokeWidth="2"
          strokeLinecap="round"
        />

        {/* Dynamic branching curves */}
        <path
          d="M7.5 5 Q12 3 17 8"
          stroke="white"
          strokeWidth="2"
          strokeLinecap="round"
          opacity="0.9"
        />
        <path
          d="M8 12 Q14 10 17 16"
          stroke="white"
          strokeWidth="2.5"
          strokeLinecap="round"
        />

        {/* Small sparkle effect */}
        <circle cx="10" cy="7" r="0.8" fill="white" opacity="0.6" />
        <circle cx="13" cy="14" r="0.5" fill="white" opacity="0.7" />
      </svg>
      <span
        className={`font-semibold text-white ${isCartoon ? "font-comic" : ""}`}
        style={{
          fontSize: size * 0.12,
          fontFamily: isCartoon
            ? "Comic Sans MS, cursive"
            : "system-ui, -apple-system, sans-serif",
        }}
      >
        LLM Canvas
      </span>
    </div>
  );
};

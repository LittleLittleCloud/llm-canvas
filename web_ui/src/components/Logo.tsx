// Primary Logo Component
import { useThemeStore } from "../store/themeStore";

export const LLMCanvasPrimaryLogo = ({
  size = 200,
  className = "",
  style = "cartoon",
}: {
  size?: number;
  className?: string;
  style?: "cartoon" | "system" | string;
}) => {
  const isCartoon = style === "cartoon";

  // Use centralized theme store to determine current actual theme
  const actualTheme = useThemeStore(s => s.actualTheme);
  const base = import.meta.env.BASE_URL || "/";
  const iconSrc = `${base}${actualTheme === "dark" ? "logo-icon-dark.svg" : "logo-icon-light.svg"}`;

  return (
    <div className={`inline-flex items-center gap-3 ${className}`}>
      <img
        src={iconSrc}
        width={size * 0.15}
        height={size * 0.15}
        alt={`LLM Canvas icon (${actualTheme})`}
        className="flex-shrink-0 select-none"
        draggable={false}
      />
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

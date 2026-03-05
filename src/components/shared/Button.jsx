export function Button({ children, variant = "outline", onClick, style = {}, disabled = false }) {
  const base = {
    padding: "9px 16px",
    border: "none",
    borderRadius: 8,
    fontWeight: 600,
    fontSize: 13,
    cursor: disabled ? "not-allowed" : "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: 6,
    transition: "opacity 0.2s",
    opacity: disabled ? 0.6 : 1,
    fontFamily: "inherit",
  };

  const variants = {
    dark: {
      background: "#111827",
      color: "#fff",
      border: "none",
    },
    outline: {
      background: "#fff",
      color: "#111827",
      border: "1.5px solid #d1d5db",
    },
    primary: {
      background: "#6366f1",
      color: "#fff",
      border: "none",
    },
    danger: {
      background: "#ef4444",
      color: "#fff",
      border: "none",
    },
    ghost: {
      background: "transparent",
      color: "#6b7280",
      border: "none",
    },
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{ ...base, ...variants[variant], ...style }}
    >
      {children}
    </button>
  );
}

export function Toast({ toast }) {
  if (!toast) return null;

  const bg = toast.type === "info" ? "#1d4ed8"
    : toast.type === "error" ? "#dc2626"
    : "#111827";

  const icon = toast.type === "error" ? "✕"
    : toast.type === "info" ? "ℹ"
    : "✓";

  return (
    <div style={{
      position: "fixed",
      bottom: 24,
      right: 24,
      zIndex: 9999,
      background: bg,
      color: "#fff",
      padding: "12px 20px",
      borderRadius: 10,
      fontWeight: 600,
      fontSize: 13,
      boxShadow: "0 4px 20px rgba(0,0,0,0.2)",
      animation: "slideIn 0.3s ease",
      display: "flex",
      alignItems: "center",
      gap: 10,
    }}>
      <span style={{ fontSize: 15 }}>{icon}</span>
      {toast.msg}
    </div>
  );
}

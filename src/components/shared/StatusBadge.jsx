const STATUS_STYLES = {
  online:  { bg: "#dcfce7", color: "#15803d" },
  offline: { bg: "#fee2e2", color: "#dc2626" },
  warning: { bg: "#fef9c3", color: "#ca8a04" },
};

export function StatusBadge({ status }) {
  const s = STATUS_STYLES[status] || STATUS_STYLES.online;
  return (
    <span style={{
      background: s.bg,
      color: s.color,
      padding: "2px 10px",
      borderRadius: 20,
      fontSize: 12,
      fontWeight: 600,
    }}>
      {status}
    </span>
  );
}

export function StatusDot({ status }) {
  const colors = { online: "#22c55e", offline: "#ef4444", warning: "#f59e0b" };
  const c = colors[status] || "#22c55e";
  return (
    <span style={{
      width: 10,
      height: 10,
      borderRadius: "50%",
      background: c,
      display: "inline-block",
      flexShrink: 0,
      boxShadow: `0 0 0 3px ${c}33`,
    }} />
  );
}

import { ANALYTICS_DATA } from "../../data/analytics";

function MetricCard({ label, value, change, changeType }) {
  const isPositive = changeType === "positive";
  return (
    <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: "20px 24px" }}>
      <div style={{ fontSize: 13, color: "#6b7280", fontWeight: 500 }}>{label}</div>
      <div style={{ fontSize: 32, fontWeight: 800, marginTop: 6 }}>{value}</div>
      <div style={{ fontSize: 12, color: isPositive ? "#15803d" : "#dc2626", fontWeight: 600, marginTop: 4 }}>
        {isPositive ? "↑" : "↓"} {change}
      </div>
    </div>
  );
}

function BarChart({ data, label }) {
  const max = Math.max(...data.map((d) => d.value));
  return (
    <div>
      <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 12 }}>{label}</div>
      <div style={{ display: "flex", alignItems: "flex-end", gap: 6, height: 140 }}>
        {data.map((d, i) => (
          <div key={i} style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
            <div style={{ fontSize: 10, color: "#6b7280", fontWeight: 600 }}>{d.value}</div>
            <div style={{
              width: "100%", height: `${(d.value / max) * 110}px`,
              background: `linear-gradient(180deg, #6366f1, #818cf8)`, borderRadius: "4px 4px 0 0",
              minHeight: 4,
            }} />
            <div style={{ fontSize: 10, color: "#9ca3af" }}>{d.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function LogTable({ logs }) {
  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
        <thead>
          <tr style={{ borderBottom: "1.5px solid #e5e7eb" }}>
            {["Timestamp", "Event", "Device", "Status"].map((h) => (
              <th key={h} style={{ textAlign: "left", padding: "8px 12px", fontWeight: 600, color: "#6b7280", fontSize: 12 }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {logs.map((log, i) => (
            <tr key={i} style={{ borderBottom: "1px solid #f3f4f6" }}>
              <td style={{ padding: "10px 12px", color: "#9ca3af", fontSize: 12 }}>{log.time}</td>
              <td style={{ padding: "10px 12px", fontWeight: 500 }}>{log.event}</td>
              <td style={{ padding: "10px 12px", color: "#6b7280" }}>{log.device}</td>
              <td style={{ padding: "10px 12px" }}>
                <span style={{
                  background: log.status === "Success" ? "#dcfce7" : log.status === "Warning" ? "#fef9c3" : "#fee2e2",
                  color: log.status === "Success" ? "#15803d" : log.status === "Warning" ? "#ca8a04" : "#dc2626",
                  padding: "2px 10px", borderRadius: 20, fontSize: 11, fontWeight: 600,
                }}>{log.status}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function AnalyticsTab() {
  const { metrics, weeklyRecoveries, recentLogs } = ANALYTICS_DATA;
  return (
    <div>
      <h2 style={{ fontSize: 26, fontWeight: 800, margin: "0 0 4px" }}>Analytics Dashboard</h2>
      <p style={{ color: "#6b7280", fontSize: 14, margin: "0 0 24px" }}>System performance and recovery metrics</p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, marginBottom: 24 }}>
        {metrics.map((m) => <MetricCard key={m.label} {...m} />)}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginBottom: 24 }}>
        <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: 24 }}>
          <BarChart data={weeklyRecoveries} label="Weekly Recovery Operations" />
        </div>
        <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: 24 }}>
          <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 12 }}>System Health Score</div>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: 140 }}>
            <div style={{ position: "relative", width: 120, height: 120 }}>
              <svg width="120" height="120" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="50" fill="none" stroke="#f3f4f6" strokeWidth="10" />
                <circle cx="60" cy="60" r="50" fill="none" stroke="url(#grad)" strokeWidth="10" strokeDasharray={`${94.2 * 0.01 * 94.2} ${94.2 * 3.14}`} strokeLinecap="round" transform="rotate(-90 60 60)" />
                <defs><linearGradient id="grad"><stop offset="0%" stopColor="#6366f1" /><stop offset="100%" stopColor="#22c55e" /></linearGradient></defs>
              </svg>
              <div style={{ position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)", textAlign: "center" }}>
                <div style={{ fontSize: 28, fontWeight: 800 }}>94</div>
                <div style={{ fontSize: 10, color: "#6b7280" }}>/ 100</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: 24 }}>
        <h3 style={{ margin: "0 0 16px", fontWeight: 700, fontSize: 15 }}>Recent Activity Log</h3>
        <LogTable logs={recentLogs} />
      </div>
    </div>
  );
}

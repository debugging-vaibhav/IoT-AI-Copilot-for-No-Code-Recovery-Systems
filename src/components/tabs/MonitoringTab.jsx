import { useState } from "react";
import { DeviceCard } from "../DeviceCard";
import { SearchIcon, RefreshIcon } from "../Icons";

function StatCard({ label, value, bg, textColor }) {
  return (
    <div style={{
      background: bg,
      border: "1px solid #e5e7eb",
      borderRadius: 12,
      padding: "20px 24px",
    }}>
      <div style={{ fontSize: 13, color: textColor === "#111827" ? "#6b7280" : textColor, fontWeight: 500 }}>
        {label}
      </div>
      <div style={{ fontSize: 36, fontWeight: 800, color: textColor, marginTop: 6 }}>
        {value}
      </div>
    </div>
  );
}

export function MonitoringTab({ devices, onAction }) {
  const [search, setSearch] = useState("");

  const online  = devices.filter((d) => d.status === "online").length;
  const warning = devices.filter((d) => d.status === "warning").length;
  const offline = devices.filter((d) => d.status === "offline").length;

  const filtered = devices.filter((d) =>
    d.name.toLowerCase().includes(search.toLowerCase()) ||
    d.subtitle.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      {/* Page heading */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 24 }}>
        <div>
          <h2 style={{ fontSize: 26, fontWeight: 800, margin: 0 }}>Device Monitoring</h2>
          <p style={{ color: "#6b7280", margin: "4px 0 0", fontSize: 14 }}>
            Monitor and manage your IoT devices
          </p>
        </div>
        <button
          onClick={() => window.location.reload()}
          style={{
            display: "flex", alignItems: "center", gap: 6,
            padding: "8px 16px", background: "#fff",
            border: "1.5px solid #d1d5db", borderRadius: 8,
            cursor: "pointer", fontWeight: 600, fontSize: 13,
            fontFamily: "inherit",
          }}
        >
          <RefreshIcon size={14} />
          Refresh
        </button>
      </div>

      {/* Stats row */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, marginBottom: 24 }}>
        <StatCard label="Total Devices" value={devices.length} bg="#fff"      textColor="#111827" />
        <StatCard label="Online"        value={online}         bg="#f0fdf4"   textColor="#15803d" />
        <StatCard label="Warning"       value={warning}        bg="#fefce8"   textColor="#ca8a04" />
        <StatCard label="Offline"       value={offline}        bg="#fef2f2"   textColor="#dc2626" />
      </div>

      {/* Search */}
      <div style={{ position: "relative", marginBottom: 24 }}>
        <span style={{ position: "absolute", left: 14, top: "50%", transform: "translateY(-50%)" }}>
          <SearchIcon />
        </span>
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search devices..."
          style={{
            width: "100%", padding: "12px 12px 12px 42px",
            border: "1.5px solid #e5e7eb", borderRadius: 10,
            fontSize: 14, outline: "none", boxSizing: "border-box",
            fontFamily: "inherit",
          }}
        />
      </div>

      {/* Device grid */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16 }}>
        {filtered.map((d) => (
          <DeviceCard key={d.id} device={d} onAction={onAction} />
        ))}
        {filtered.length === 0 && (
          <div style={{ gridColumn: "span 3", textAlign: "center", padding: 40, color: "#9ca3af", fontSize: 14 }}>
            No devices match your search.
          </div>
        )}
      </div>
    </div>
  );
}

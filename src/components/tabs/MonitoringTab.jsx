import { useState, useEffect, useCallback } from "react";
import { DeviceCard } from "../DeviceCard";
import { SearchIcon, RefreshIcon } from "../Icons";
import { fetchDeviceList, fetchDeviceLiveStatus, executeDirect } from "../../data/apiClient";

function StatCard({ label, value, bg, textColor }) {
  return (
    <div style={{ background: bg, border: "1px solid #e5e7eb", borderRadius: 12, padding: "20px 24px" }}>
      <div style={{ fontSize: 13, color: textColor === "#111827" ? "#6b7280" : textColor, fontWeight: 500 }}>{label}</div>
      <div style={{ fontSize: 36, fontWeight: 800, color: textColor, marginTop: 6 }}>{value}</div>
    </div>
  );
}

function ConnectedDevicePanel({ connectedDevices }) {
  const entries = Object.entries(connectedDevices || {});
  if (entries.length === 0) return null;

  return (
    <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: 20, marginBottom: 24 }}>
      <h3 style={{ margin: "0 0 14px", fontWeight: 700, fontSize: 15, display: "flex", alignItems: "center", gap: 8 }}>
        <span style={{ width: 10, height: 10, borderRadius: "50%", background: "#22c55e", display: "inline-block" }} />
        Connected RPi Devices
      </h3>
      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {entries.map(([id, info]) => (
          <div key={id} style={{
            display: "flex", justifyContent: "space-between", alignItems: "center",
            background: info.status === "ONLINE" ? "#f0fdf4" : "#fef2f2",
            border: `1px solid ${info.status === "ONLINE" ? "#86efac" : "#fca5a5"}`,
            borderRadius: 8, padding: "10px 16px",
          }}>
            <div>
              <div style={{ fontWeight: 700, fontSize: 14 }}>{id}</div>
              <div style={{ fontSize: 12, color: "#6b7280" }}>
                {info.device_url} {info.simulated ? "(simulated)" : "(hardware)"}
              </div>
            </div>
            <span style={{
              background: info.status === "ONLINE" ? "#dcfce7" : "#fee2e2",
              color: info.status === "ONLINE" ? "#15803d" : "#dc2626",
              padding: "2px 10px", borderRadius: 20, fontSize: 12, fontWeight: 600,
            }}>
              {info.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export function MonitoringTab({ devices, onAction, backendStatus, connectedDevices, showToast }) {
  const [search, setSearch] = useState("");
  const [rpiStatus, setRpiStatus] = useState(null);

  const online = devices.filter((d) => d.status === "online").length;
  const warning = devices.filter((d) => d.status === "warning").length;
  const offline = devices.filter((d) => d.status === "offline").length;

  const filtered = devices.filter(
    (d) =>
      d.name.toLowerCase().includes(search.toLowerCase()) ||
      d.subtitle.toLowerCase().includes(search.toLowerCase())
  );

  // Try to fetch live RPi pin status
  const refreshRpiStatus = useCallback(async () => {
    const devEntries = Object.entries(connectedDevices || {});
    if (devEntries.length > 0) {
      try {
        const data = await fetchDeviceLiveStatus(devEntries[0][0]);
        setRpiStatus(data);
      } catch {
        setRpiStatus(null);
      }
    }
  }, [connectedDevices]);

  useEffect(() => {
    refreshRpiStatus();
  }, [refreshRpiStatus]);

  return (
    <div>
      {/* Page heading */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 24 }}>
        <div>
          <h2 style={{ fontSize: 26, fontWeight: 800, margin: 0 }}>Device Monitoring</h2>
          <p style={{ color: "#6b7280", margin: "4px 0 0", fontSize: 14 }}>
            Monitor and manage your IoT devices
            {backendStatus === "offline" && (
              <span style={{ color: "#dc2626", fontWeight: 600 }}> — Backend offline</span>
            )}
          </p>
        </div>
        <button
          onClick={() => { refreshRpiStatus(); showToast("Refreshed", "info"); }}
          style={{
            display: "flex", alignItems: "center", gap: 6,
            padding: "8px 16px", background: "#fff",
            border: "1.5px solid #d1d5db", borderRadius: 8,
            cursor: "pointer", fontWeight: 600, fontSize: 13, fontFamily: "inherit",
          }}
        >
          <RefreshIcon size={14} />
          Refresh
        </button>
      </div>

      {/* Connected RPi panel */}
      <ConnectedDevicePanel connectedDevices={connectedDevices} />

      {/* Live RPi pin status */}
      {rpiStatus && (
        <div style={{ background: "#f8f7ff", border: "1px solid #e5e7eb", borderRadius: 12, padding: 20, marginBottom: 24 }}>
          <h3 style={{ margin: "0 0 10px", fontWeight: 700, fontSize: 15 }}>
            Live RPi Status — {rpiStatus.device_id || "unknown"}
          </h3>
          <div style={{ display: "flex", gap: 20, flexWrap: "wrap" }}>
            <div>
              <div style={{ fontSize: 12, color: "#6b7280", fontWeight: 500 }}>Hardware</div>
              <div style={{ fontSize: 16, fontWeight: 700, color: "#15803d" }}>{rpiStatus.status}</div>
            </div>
            <div>
              <div style={{ fontSize: 12, color: "#6b7280", fontWeight: 500 }}>Active Pins</div>
              <div style={{ fontSize: 16, fontWeight: 700 }}>
                {Object.keys(rpiStatus.pin_states || {}).length || 0}
              </div>
            </div>
            <div>
              <div style={{ fontSize: 12, color: "#6b7280", fontWeight: 500 }}>Sensor Streams</div>
              <div style={{ fontSize: 16, fontWeight: 700 }}>
                {Object.keys(rpiStatus.sensor_readings || {}).length || 0}
              </div>
            </div>
            <div>
              <div style={{ fontSize: 12, color: "#6b7280", fontWeight: 500 }}>Mode</div>
              <div style={{ fontSize: 16, fontWeight: 700 }}>
                {rpiStatus.simulated ? "Simulated" : "Hardware"}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Stats row */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, marginBottom: 24 }}>
        <StatCard label="Total Devices" value={devices.length} bg="#fff" textColor="#111827" />
        <StatCard label="Online" value={online} bg="#f0fdf4" textColor="#15803d" />
        <StatCard label="Warning" value={warning} bg="#fefce8" textColor="#ca8a04" />
        <StatCard label="Offline" value={offline} bg="#fef2f2" textColor="#dc2626" />
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
            fontSize: 14, outline: "none", boxSizing: "border-box", fontFamily: "inherit",
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

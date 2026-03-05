import { StatusBadge } from "./shared/StatusBadge";
import { Button } from "./shared/Button";
import {
  ChipIcon, WifiIcon, ThermometerIcon,
  UptimeIcon, ClockIcon, CheckIcon, XIcon, WarningIcon,
} from "./Icons";

function DeviceStatusIcon({ status }) {
  const wrapStyle = (bg) => ({
    width: 44, height: 44, borderRadius: 10,
    background: bg,
    display: "flex", alignItems: "center", justifyContent: "center",
  });

  if (status === "online")
    return <div style={wrapStyle("#f0fdf4")}><CheckIcon size={20} color="#22c55e" /></div>;
  if (status === "offline")
    return <div style={wrapStyle("#fef2f2")}><XIcon size={20} color="#ef4444" /></div>;
  return <div style={wrapStyle("#fffbeb")}><WarningIcon size={20} color="#f59e0b" /></div>;
}

function InfoRow({ icon, text }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 7, fontSize: 13, color: "#374151" }}>
      {icon}
      <span>{text}</span>
    </div>
  );
}

export function DeviceCard({ device, onAction }) {
  return (
    <div style={{
      background: "#fff",
      border: "1px solid #e5e7eb",
      borderRadius: 12,
      padding: 20,
      display: "flex",
      flexDirection: "column",
      gap: 10,
    }}>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <DeviceStatusIcon status={device.status} />
          <div>
            <div style={{ fontWeight: 700, fontSize: 15 }}>{device.name}</div>
            <div style={{ color: "#6b7280", fontSize: 12 }}>{device.subtitle}</div>
          </div>
        </div>
        <StatusBadge status={device.status} />
      </div>

      {/* Info rows */}
      <div style={{ display: "flex", flexDirection: "column", gap: 6, marginTop: 4 }}>
        <InfoRow icon={<ChipIcon />} text={`Pin: ${device.pin}`} />
        <InfoRow icon={<WifiIcon />} text={device.type} />
        {device.temp !== null && device.temp !== undefined && (
          <InfoRow icon={<ThermometerIcon />} text={`${device.temp}°C`} />
        )}
        {device.uptime && (
          <InfoRow icon={<UptimeIcon />} text={`Uptime: ${device.uptime}`} />
        )}
        <InfoRow icon={<ClockIcon />} text={`Last seen: ${device.lastSeen}`} />
      </div>

      {/* Recovery label */}
      <div style={{
        background: "#f9fafb",
        border: "1px solid #e5e7eb",
        borderRadius: 8,
        padding: "8px 12px",
        fontSize: 12,
        color: "#6b7280",
      }}>
        Recovery: {device.recovery}
      </div>

      {/* Action buttons */}
      <div style={{ display: "flex", gap: 8, marginTop: 4 }}>
        {device.status === "offline" && (
          <Button
            variant="dark"
            onClick={() => onAction(device.id, "recover")}
            style={{ flex: 1 }}
          >
            Auto-Recover
          </Button>
        )}
        {device.status === "warning" && (
          <Button
            variant="outline"
            onClick={() => onAction(device.id, "diagnose")}
            style={{ flex: 1 }}
          >
            Run Diagnostics
          </Button>
        )}
        <Button
          variant="outline"
          onClick={() => onAction(device.id, "configure")}
          style={{ flex: 1 }}
        >
          Configure
        </Button>
      </div>
    </div>
  );
}

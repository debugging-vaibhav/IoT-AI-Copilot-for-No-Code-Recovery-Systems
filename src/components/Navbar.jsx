import { RobotIcon } from "./Icons";

const TABS = [
  { key: "monitoring",  label: "Monitoring",  Icon: () => <MonIcon /> },
  { key: "configure",   label: "Configure",   Icon: () => <ConfIcon /> },
  { key: "ai-copilot",  label: "AI Copilot",  Icon: () => <AIIcon /> },
  { key: "workflows",   label: "Workflows",   Icon: () => <WFIcon /> },
  { key: "analytics",   label: "Analytics",   Icon: () => <AnIcon /> },
];

function MonIcon() {
  return <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12" /></svg>;
}
function ConfIcon() {
  return <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="3" /><path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14" /></svg>;
}
function AIIcon() {
  return <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2L2 7l10 5 10-5-10-5z" /><path d="M2 17l10 5 10-5" /><path d="M2 12l10 5 10-5" /></svg>;
}
function WFIcon() {
  return <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="18" cy="18" r="3" /><circle cx="6" cy="6" r="3" /><path d="M13 6h3a2 2 0 0 1 2 2v7" /><line x1="6" y1="9" x2="6" y2="21" /></svg>;
}
function AnIcon() {
  return <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="18" y1="20" x2="18" y2="10" /><line x1="12" y1="20" x2="12" y2="4" /><line x1="6" y1="20" x2="6" y2="14" /></svg>;
}

export function Topbar() {
  return (
    <div style={{
      background: "#111827",
      color: "#fff",
      height: 44,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      position: "relative",
      padding: "0 24px",
    }}>
      <div style={{ position: "absolute", left: 24, display: "flex", alignItems: "center", gap: 8 }}>
        <div style={{
          width: 28, height: 28, background: "#374151",
          borderRadius: 6, display: "flex", alignItems: "center",
          justifyContent: "center", fontSize: 11, fontWeight: 800, color: "#fff",
          letterSpacing: "-0.5px",
        }}>
          AI
        </div>
      </div>

      <div style={{ display: "flex", alignItems: "center", gap: 7, fontWeight: 600, fontSize: 14 }}>
        IoT AI Copilot
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </div>

      <div style={{ position: "absolute", right: 24 }}>
        <button style={{
          background: "#3b82f6", color: "#fff",
          border: "none", padding: "5px 16px",
          borderRadius: 6, fontWeight: 700, fontSize: 13, cursor: "pointer",
          fontFamily: "inherit",
        }}>
          Share
        </button>
      </div>
    </div>
  );
}

export function AppHeader() {
  return (
    <div style={{
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      padding: "24px 0 20px",
    }}>
      <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
        <div style={{
          width: 52, height: 52,
          background: "linear-gradient(135deg, #7c3aed, #6366f1)",
          borderRadius: 12,
          display: "flex", alignItems: "center", justifyContent: "center",
        }}>
          <RobotIcon size={26} color="#fff" />
        </div>
        <div>
          <h1 style={{ margin: 0, fontSize: 20, fontWeight: 800 }}>Robotics AI Copilot</h1>
          <p style={{ margin: 0, fontSize: 13, color: "#6b7280" }}>No-Code Recovery &amp; Control System</p>
        </div>
      </div>

      <div style={{
        background: "#f0fdf4",
        border: "1.5px solid #86efac",
        color: "#15803d",
        padding: "6px 16px",
        borderRadius: 20,
        fontWeight: 700,
        fontSize: 13,
      }}>
        System Active
      </div>
    </div>
  );
}

export function TabNav({ activeTab, setActiveTab }) {
  return (
    <div style={{
      background: "#f3f4f6",
      borderRadius: 10,
      padding: 4,
      display: "flex",
      marginBottom: 32,
    }}>
      {TABS.map(({ key, label, Icon }) => {
        const isActive = activeTab === key;
        return (
          <button
            key={key}
            onClick={() => setActiveTab(key)}
            style={{
              flex: 1,
              padding: "9px 0",
              border: "none",
              borderRadius: 8,
              cursor: "pointer",
              fontWeight: 600,
              fontSize: 13,
              background: isActive ? "#fff" : "transparent",
              color: isActive ? "#111827" : "#6b7280",
              boxShadow: isActive ? "0 1px 3px rgba(0,0,0,0.12)" : "none",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 7,
              transition: "all 0.2s",
              fontFamily: "inherit",
            }}
          >
            <Icon />
            {label}
          </button>
        );
      })}
    </div>
  );
}

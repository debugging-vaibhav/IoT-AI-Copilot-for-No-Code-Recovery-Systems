import { useState, useEffect, useCallback } from "react";
import { Topbar, AppHeader, TabNav } from "./components/Navbar";
import { MonitoringTab } from "./components/tabs/MonitoringTab";
import { ConfigureTab } from "./components/tabs/ConfigureTab";
import { AICopilotTab } from "./components/tabs/AICopilotTab";
import { WorkflowsTab } from "./components/tabs/WorkflowsTab";
import { AnalyticsTab } from "./components/tabs/AnalyticsTab";
import { Toast } from "./components/shared/Toast";
import { useToast } from "./hooks/useToast";
import { INITIAL_DEVICES, INITIAL_COMPONENTS } from "./data/devices";
import { fetchSystemStatus } from "./data/apiClient";

export default function App() {
  const [activeTab, setActiveTab] = useState("monitoring");
  const [devices, setDevices] = useState(INITIAL_DEVICES);
  const [components, setComponents] = useState(INITIAL_COMPONENTS);
  const [backendStatus, setBackendStatus] = useState("checking"); // "online" | "offline" | "checking"
  const [connectedDevices, setConnectedDevices] = useState({});
  const { toast, showToast } = useToast();

  // Poll backend status every 5 seconds
  const checkBackend = useCallback(async () => {
    try {
      const data = await fetchSystemStatus();
      setBackendStatus("online");
      setConnectedDevices(data.devices || {});

      // If RPi is connected, update our device list status
      const hasOnlineDevice = Object.values(data.devices || {}).some(
        (d) => d.status === "ONLINE"
      );
      if (hasOnlineDevice) {
        setDevices((prev) =>
          prev.map((d) =>
            d.id === 1
              ? { ...d, status: "online", lastSeen: "just now" }
              : d
          )
        );
      }
    } catch {
      setBackendStatus("offline");
      setConnectedDevices({});
    }
  }, []);

  useEffect(() => {
    checkBackend();
    const interval = setInterval(checkBackend, 5000);
    return () => clearInterval(interval);
  }, [checkBackend]);

  const handleDeviceAction = (id, action) => {
    if (action === "recover") {
      setDevices((prev) =>
        prev.map((d) =>
          d.id === id
            ? { ...d, status: "online", lastSeen: "just now", uptime: "0d 0h 1m" }
            : d
        )
      );
      showToast("Device recovered successfully!");
    } else if (action === "diagnose") {
      showToast("Running diagnostics...", "info");
    } else if (action === "configure") {
      setActiveTab("configure");
      showToast("Navigated to Configure tab", "info");
    }
  };

  return (
    <div
      style={{
        fontFamily: "'DM Sans', system-ui, sans-serif",
        background: "#f9fafb",
        minHeight: "100vh",
      }}
    >
      <Topbar backendStatus={backendStatus} connectedDevices={connectedDevices} />

      <div style={{ maxWidth: 1360, margin: "0 auto", padding: "0 24px" }}>
        <AppHeader
          backendStatus={backendStatus}
          connectedDevices={connectedDevices}
        />
        <TabNav activeTab={activeTab} setActiveTab={setActiveTab} />

        <div style={{ paddingBottom: 60 }}>
          {activeTab === "monitoring" && (
            <MonitoringTab
              devices={devices}
              onAction={handleDeviceAction}
              backendStatus={backendStatus}
              connectedDevices={connectedDevices}
              showToast={showToast}
            />
          )}
          {activeTab === "configure" && (
            <ConfigureTab
              components={components}
              setComponents={setComponents}
              showToast={showToast}
            />
          )}
          {activeTab === "ai-copilot" && (
            <AICopilotTab backendStatus={backendStatus} showToast={showToast} />
          )}
          {activeTab === "workflows" && <WorkflowsTab />}
          {activeTab === "analytics" && <AnalyticsTab />}
        </div>
      </div>

      <Toast toast={toast} />
    </div>
  );
}

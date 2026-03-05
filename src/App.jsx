import { useState } from "react";
import { Topbar, AppHeader, TabNav } from "./components/Navbar";
import { MonitoringTab } from "./components/tabs/MonitoringTab";
import { ConfigureTab }  from "./components/tabs/ConfigureTab";
import { AICopilotTab } from "./components/tabs/AICopilotTab";
import { WorkflowsTab } from "./components/tabs/WorkflowsTab";
import { AnalyticsTab } from "./components/tabs/AnalyticsTab";
import { Toast }         from "./components/shared/Toast";
import { useToast }      from "./hooks/useToast";
import { INITIAL_DEVICES, INITIAL_COMPONENTS } from "./data/devices";

export default function App() {
  const [activeTab,  setActiveTab]  = useState("monitoring");
  const [devices,    setDevices]    = useState(INITIAL_DEVICES);
  const [components, setComponents] = useState(INITIAL_COMPONENTS);
  const { toast, showToast } = useToast();

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
    <div style={{ fontFamily: "'DM Sans', system-ui, sans-serif", background: "#f9fafb", minHeight: "100vh" }}>
      <Topbar />

      <div style={{ maxWidth: 1360, margin: "0 auto", padding: "0 24px" }}>
        <AppHeader />
        <TabNav activeTab={activeTab} setActiveTab={setActiveTab} />

        <div style={{ paddingBottom: 60 }}>
          {activeTab === "monitoring"  && <MonitoringTab devices={devices} onAction={handleDeviceAction} />}
          {activeTab === "configure"   && <ConfigureTab components={components} setComponents={setComponents} />}
          {activeTab === "ai-copilot"  && <AICopilotTab />}
          {activeTab === "workflows"   && <WorkflowsTab />}
          {activeTab === "analytics"   && <AnalyticsTab />}
        </div>
      </div>

      <Toast toast={toast} />
    </div>
  );
}

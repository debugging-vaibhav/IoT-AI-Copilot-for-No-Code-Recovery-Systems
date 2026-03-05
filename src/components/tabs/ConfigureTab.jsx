import { useState } from "react";
import { MissionIcon, ControlIcon, TrashIcon } from "../Icons";
import { Button } from "../shared/Button";

const labelStyle = {
  fontSize: 13,
  fontWeight: 600,
  color: "#374151",
  display: "block",
  marginBottom: 6,
};

const inputStyle = {
  width: "100%",
  padding: "10px 12px",
  border: "1.5px solid #e5e7eb",
  borderRadius: 8,
  fontSize: 13,
  outline: "none",
  boxSizing: "border-box",
  background: "#f9fafb",
  fontFamily: "inherit",
};

function FormField({ label, value, onChange, placeholder }) {
  return (
    <div>
      <label style={labelStyle}>{label}</label>
      <input value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} style={inputStyle} />
    </div>
  );
}

export function ConfigureTab({ components, setComponents }) {
  const [form, setForm] = useState({ name: "", type: "Sensor", pin: "", desc: "" });
  const [missionObjective, setMissionObjective] = useState(
    "Maintain stable hover at 5 meters altitude and respond to directional commands via radio control"
  );
  const [controlBehavior, setControlBehavior] = useState(
    "Use IMU data for stabilization. Map PWM signals to motor speed. Apply PID control for balance."
  );
  const [summary, setSummary] = useState([
    "Read IMU data via I2C protocol on GPIO 14, 15",
    "Calculate PID correction for roll, pitch, yaw",
    "Output PWM signals to motor driver on pins 5, 6, 9, 10",
    "Maintain 5m altitude using control feedback loop",
  ]);
  const [generating, setGenerating] = useState(false);

  const addComponent = () => {
    if (!form.name.trim()) return;
    setComponents((prev) => [...prev, { id: Date.now(), ...form }]);
    setForm({ name: "", type: "Sensor", pin: "", desc: "" });
  };

  const removeComponent = (id) =>
    setComponents((prev) => prev.filter((c) => c.id !== id));

  const generateLogic = () => {
    setGenerating(true);
    setTimeout(() => {
      const sensor   = components.find((c) => c.type === "Sensor");
      const actuator = components.find((c) => c.type === "Actuator");
      setSummary([
        `Read ${sensor?.name || "sensor"} data via configured protocol`,
        "Calculate control corrections using defined algorithm",
        `Output signals to ${actuator?.name || "actuator"} on configured pins`,
        "Monitor system state and apply recovery logic on failure",
      ]);
      setGenerating(false);
    }, 1500);
  };

  return (
    <div>
      <h2 style={{ fontSize: 26, fontWeight: 800, margin: "0 0 4px" }}>Hardware Configuration</h2>
      <p style={{ color: "#6b7280", fontSize: 14, margin: "0 0 24px" }}>
        Describe your robotic system setup without writing code
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
        {/* ── Left column ── */}
        <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          {/* Add New Component */}
          <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: 24 }}>
            <h3 style={{ margin: "0 0 20px", fontWeight: 700, display: "flex", alignItems: "center", gap: 8 }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="3" />
                <path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14" />
              </svg>
              Add New Component
            </h3>

            <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
              <FormField
                label="Component Name"
                value={form.name}
                onChange={(v) => setForm((f) => ({ ...f, name: v }))}
                placeholder="e.g., LiDAR Module, GPS Sensor"
              />

              <div>
                <label style={labelStyle}>Component Type</label>
                <select
                  value={form.type}
                  onChange={(e) => setForm((f) => ({ ...f, type: e.target.value }))}
                  style={inputStyle}
                >
                  <option>Sensor</option>
                  <option>Actuator</option>
                  <option>Controller</option>
                  <option>Communication</option>
                </select>
              </div>

              <FormField
                label="Pin Configuration"
                value={form.pin}
                onChange={(v) => setForm((f) => ({ ...f, pin: v }))}
                placeholder="e.g., GPIO 14, 15 or PWM 5-8"
              />

              <div>
                <label style={labelStyle}>Component Description</label>
                <textarea
                  value={form.desc}
                  onChange={(e) => setForm((f) => ({ ...f, desc: e.target.value }))}
                  placeholder="Describe what this component does and how it should behave"
                  style={{ ...inputStyle, minHeight: 80, resize: "vertical" }}
                />
              </div>

              <button
                onClick={addComponent}
                style={{
                  padding: "12px 0",
                  background: "#111827",
                  color: "#fff",
                  border: "none",
                  borderRadius: 8,
                  fontWeight: 700,
                  fontSize: 14,
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: 8,
                  fontFamily: "inherit",
                }}
              >
                + Add Component
              </button>
            </div>
          </div>

          {/* Current Components */}
          <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: 24 }}>
            <h3 style={{ margin: "0 0 16px", fontWeight: 700 }}>Current Components</h3>
            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              {components.length === 0 && (
                <div style={{ color: "#9ca3af", fontSize: 13, textAlign: "center", padding: 20 }}>
                  No components added yet
                </div>
              )}
              {components.map((c) => (
                <div key={c.id} style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: "12px 14px" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                    <div style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6b7280" strokeWidth="2" style={{ marginTop: 2 }}>
                        <rect x="7" y="7" width="10" height="10" rx="1" />
                        <path d="M7 12H4m13 0h3M12 7V4m0 13v3" />
                      </svg>
                      <div>
                        <div style={{ fontWeight: 700, fontSize: 14 }}>{c.name}</div>
                        <div style={{ fontSize: 12, color: "#6b7280" }}>{c.pin}</div>
                      </div>
                    </div>
                    <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                      <span style={{
                        background: "#f3f4f6", color: "#374151",
                        padding: "2px 10px", borderRadius: 20,
                        fontSize: 12, fontWeight: 600,
                      }}>
                        {c.type}
                      </span>
                      <button
                        onClick={() => removeComponent(c.id)}
                        style={{ background: "none", border: "none", cursor: "pointer", padding: 4, display: "flex" }}
                      >
                        <TrashIcon size={16} color="#9ca3af" />
                      </button>
                    </div>
                  </div>
                  {c.desc && (
                    <div style={{ fontSize: 12, color: "#6b7280", marginTop: 6 }}>{c.desc}</div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* ── Right column ── */}
        <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          {/* Mission Objective */}
          <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: 24 }}>
            <h3 style={{ margin: "0 0 16px", fontWeight: 700, display: "flex", alignItems: "center", gap: 8 }}>
              <MissionIcon size={18} /> Mission Objective
            </h3>
            <label style={labelStyle}>Describe Mission Objective</label>
            <textarea
              value={missionObjective}
              onChange={(e) => setMissionObjective(e.target.value)}
              style={{ ...inputStyle, minHeight: 90, resize: "vertical" }}
            />
            <div style={{ fontSize: 12, color: "#9ca3af", marginTop: 4 }}>
              Explain what the robot should accomplish in the field
            </div>
          </div>

          {/* Control Behavior */}
          <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: 24 }}>
            <h3 style={{ margin: "0 0 16px", fontWeight: 700, display: "flex", alignItems: "center", gap: 8 }}>
              <ControlIcon size={18} /> Control Behavior
            </h3>
            <label style={labelStyle}>Describe Desired Control Logic</label>
            <textarea
              value={controlBehavior}
              onChange={(e) => setControlBehavior(e.target.value)}
              style={{ ...inputStyle, minHeight: 90, resize: "vertical" }}
            />
            <div style={{ fontSize: 12, color: "#9ca3af", marginTop: 4 }}>
              Explain how components should interact and respond
            </div>
          </div>

          {/* AI Summary */}
          <div style={{ background: "#f8f7ff", border: "1px solid #e5e7eb", borderRadius: 12, padding: 24 }}>
            <h3 style={{ margin: "0 0 8px", fontWeight: 700 }}>AI-Generated Control Summary</h3>
            <p style={{ fontSize: 13, color: "#6b7280", margin: "0 0 14px" }}>
              Based on your configuration, the AI Copilot will:
            </p>
            <ul style={{ margin: 0, paddingLeft: 20, display: "flex", flexDirection: "column", gap: 8 }}>
              {summary.map((s, i) => (
                <li key={i} style={{ fontSize: 13, color: "#374151" }}>{s}</li>
              ))}
            </ul>
            <div style={{ display: "flex", gap: 10, marginTop: 20 }}>
              <button
                onClick={generateLogic}
                disabled={generating}
                style={{
                  flex: 1, padding: "11px 0",
                  background: "#111827", color: "#fff",
                  border: "none", borderRadius: 8,
                  fontWeight: 700, fontSize: 13, cursor: "pointer",
                  fontFamily: "inherit", opacity: generating ? 0.7 : 1,
                }}
              >
                {generating ? "Generating..." : "Generate Control Logic"}
              </button>
              <button
                style={{
                  flex: 1, padding: "11px 0",
                  background: "#fff", color: "#111827",
                  border: "1.5px solid #d1d5db", borderRadius: 8,
                  fontWeight: 700, fontSize: 13, cursor: "pointer",
                  fontFamily: "inherit",
                }}
              >
                Deploy to System
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

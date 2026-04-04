export const CONDITIONS = [
  { id: "c1", label: "Sensor Offline", desc: "Triggers when a sensor stops responding", icon: "📡", color: "#fef3c7", border: "#fde68a", text: "#92400e" },
  { id: "c2", label: "Temperature High", desc: "When temp exceeds safe threshold", icon: "🌡️", color: "#fef3c7", border: "#fde68a", text: "#92400e" },
  { id: "c3", label: "Signal Lost", desc: "Communication link interrupted", icon: "📶", color: "#fef3c7", border: "#fde68a", text: "#92400e" },
  { id: "c4", label: "Motor Stall", desc: "Motor current exceeds normal range", icon: "⚙️", color: "#fef3c7", border: "#fde68a", text: "#92400e" },
];

export const ACTIONS = [
  { id: "a1", label: "Power Cycle", desc: "Toggle power to reset component", icon: "🔄", color: "#ede9fe", border: "#c4b5fd", text: "#5b21b6" },
  { id: "a2", label: "Send Alert", desc: "Notify operator via dashboard", icon: "🔔", color: "#ede9fe", border: "#c4b5fd", text: "#5b21b6" },
  { id: "a3", label: "Safe Mode", desc: "Reduce power and enter safe state", icon: "🛡️", color: "#ede9fe", border: "#c4b5fd", text: "#5b21b6" },
  { id: "a4", label: "Recalibrate", desc: "Re-run sensor calibration routine", icon: "🎯", color: "#ede9fe", border: "#c4b5fd", text: "#5b21b6" },
  { id: "a5", label: "Switch Backup", desc: "Activate redundant component", icon: "🔀", color: "#ede9fe", border: "#c4b5fd", text: "#5b21b6" },
];

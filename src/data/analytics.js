export const UPTIME_DATA = [
  { time: "00:00", value: 95.2 },
  { time: "04:00", value: 97.8 },
  { time: "08:00", value: 92.1 },
  { time: "12:00", value: 96.5 },
  { time: "16:00", value: 98.2 },
  { time: "20:00", value: 96.8 },
  { time: "24:00", value: 97.1 },
];

export const RECOVERY_DATA = [
  { month: "Jul", successful: 45, failed: 3 },
  { month: "Aug", successful: 52, failed: 2 },
  { month: "Sep", successful: 49, failed: 4 },
  { month: "Oct", successful: 61, failed: 1 },
  { month: "Nov", successful: 58, failed: 2 },
  { month: "Dec", successful: 65, failed: 1 },
  { month: "Jan", successful: 72, failed: 2 },
];

export const TEMP_DATA = [
  { time: "00:00", value: 23 },
  { time: "04:00", value: 22 },
  { time: "08:00", value: 24.5 },
  { time: "12:00", value: 25 },
  { time: "16:00", value: 31.5 },
  { time: "20:00", value: 26 },
  { time: "24:00", value: 23.5 },
];

export const DEVICE_DIST = [
  { name: "Environmental", value: 40, color: "#6366f1" },
  { name: "Industrial",    value: 25, color: "#8b5cf6" },
  { name: "Security",      value: 20, color: "#10b981" },
  { name: "Actuators",     value: 15, color: "#f59e0b" },
];

export const KPI_CARDS = [
  {
    label: "Avg Uptime",
    value: "96.8%",
    change: "+2.3%",
    up: true,
    iconBg: "#dcfce7",
    iconColor: "#22c55e",
  },
  {
    label: "Recovery Rate",
    value: "97.2%",
    change: "+1.8%",
    up: true,
    iconBg: "#ede9fe",
    iconColor: "#7c3aed",
  },
  {
    label: "Avg Recovery Time",
    value: "2.4 min",
    change: "-0.5 min",
    up: false,
    iconBg: "#f3e8ff",
    iconColor: "#a855f7",
  },
  {
    label: "Active Workflows",
    value: "12",
    change: "+3 new",
    up: true,
    iconBg: "#ffedd5",
    iconColor: "#f59e0b",
  },
];

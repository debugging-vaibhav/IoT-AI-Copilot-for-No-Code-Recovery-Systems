export const ANALYTICS_DATA = {
  metrics: [
    { label: "Total Recoveries", value: "247", change: "+12% this week", changeType: "positive" },
    { label: "Success Rate", value: "94.2%", change: "+2.1% vs last month", changeType: "positive" },
    { label: "Avg Recovery Time", value: "3.2s", change: "-0.8s improvement", changeType: "positive" },
    { label: "Active Alerts", value: "3", change: "+1 since yesterday", changeType: "negative" },
  ],
  weeklyRecoveries: [
    { label: "Mon", value: 32 },
    { label: "Tue", value: 28 },
    { label: "Wed", value: 45 },
    { label: "Thu", value: 38 },
    { label: "Fri", value: 52 },
    { label: "Sat", value: 18 },
    { label: "Sun", value: 12 },
  ],
  recentLogs: [
    { time: "14:32:01", event: "Auto-recovery triggered", device: "Motor Driver", status: "Success" },
    { time: "14:28:45", event: "Temperature warning", device: "Motor Driver", status: "Warning" },
    { time: "14:15:22", event: "Sensor recalibrated", device: "IMU Module", status: "Success" },
    { time: "13:58:10", event: "Connection lost", device: "LiDAR Sensor", status: "Failed" },
    { time: "13:45:33", event: "Firmware updated", device: "GPS Module", status: "Success" },
    { time: "13:30:00", event: "Heartbeat received", device: "RPi 5 Controller", status: "Success" },
    { time: "12:55:18", event: "PID values adjusted", device: "Flight Controller", status: "Success" },
    { time: "12:40:05", event: "Battery low warning", device: "Power Module", status: "Warning" },
  ],
};

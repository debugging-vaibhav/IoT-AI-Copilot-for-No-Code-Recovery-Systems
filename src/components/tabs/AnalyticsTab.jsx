import {
  AreaChart, Area, BarChart, Bar, LineChart, Line,
  PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer,
} from "recharts";
import { UPTIME_DATA, RECOVERY_DATA, TEMP_DATA, DEVICE_DIST, KPI_CARDS } from "../../data/analytics";
import { PulseIcon } from "../Icons";

function KPICard({ label, value, change, up, iconBg, iconColor }) {
  return (
    <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: "20px 22px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <div style={{ fontSize: 13, color: "#6b7280", fontWeight: 500 }}>{label}</div>
        <div style={{ width: 34, height: 34, background: iconBg, borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <PulseIcon size={16} color={iconColor} />
        </div>
      </div>
      <div style={{ fontSize: 28, fontWeight: 800, margin: "10px 0 4px" }}>{value}</div>
      <div style={{ fontSize: 12, color: up ? "#16a34a" : "#dc2626", display: "flex", alignItems: "center", gap: 4 }}>
        {up ? "↑" : "↓"} {change}
      </div>
    </div>
  );
}

function ChartCard({ title, children }) {
  return (
    <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: 24 }}>
      <h3 style={{ margin: "0 0 20px", fontWeight: 700 }}>{title}</h3>
      {children}
    </div>
  );
}

export function AnalyticsTab() {
  return (
    <div>
      <h2 style={{ fontSize: 26, fontWeight: 800, margin: "0 0 4px" }}>Analytics &amp; Insights</h2>
      <p style={{ color: "#6b7280", fontSize: 14, margin: "0 0 24px" }}>
        Monitor performance and recovery metrics
      </p>

      {/* KPI row */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, marginBottom: 24 }}>
        {KPI_CARDS.map((k) => <KPICard key={k.label} {...k} />)}
      </div>

      {/* Charts row 1 */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginBottom: 20 }}>
        <ChartCard title="System Uptime (24h)">
          <ResponsiveContainer width="100%" height={220}>
            <AreaChart data={UPTIME_DATA}>
              <defs>
                <linearGradient id="uptimeGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%"  stopColor="#6366f1" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0}   />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
              <XAxis dataKey="time"  tick={{ fontSize: 11 }} />
              <YAxis domain={[90, 100]} tick={{ fontSize: 11 }} />
              <Tooltip />
              <Area type="monotone" dataKey="value" stroke="#6366f1" fill="url(#uptimeGrad)" strokeWidth={2} />
            </AreaChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Recovery Success vs Failed">
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={RECOVERY_DATA}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
              <XAxis dataKey="month" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Legend />
              <Bar dataKey="successful" fill="#10b981" radius={[3, 3, 0, 0]} />
              <Bar dataKey="failed"     fill="#ef4444" radius={[3, 3, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      {/* Charts row 2 */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
        <ChartCard title="Average Temperature Trend">
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={TEMP_DATA}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
              <XAxis dataKey="time"  tick={{ fontSize: 11 }} />
              <YAxis domain={[0, 40]} tick={{ fontSize: 11 }} />
              <Tooltip />
              <Line type="monotone" dataKey="value" stroke="#f59e0b" strokeWidth={2.5} dot={{ fill: "#f59e0b", r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Device Distribution">
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie
                data={DEVICE_DIST}
                cx="50%" cy="50%"
                outerRadius={85}
                dataKey="value"
                label={({ name, value }) => `${name}: ${value}%`}
                labelLine={true}
              >
                {DEVICE_DIST.map((d, i) => (
                  <Cell key={i} fill={d.color} />
                ))}
              </Pie>
              <Tooltip formatter={(v) => `${v}%`} />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>
    </div>
  );
}

# 🤖 IoT AI Copilot — Robotics Dashboard

A full-featured **No-Code IoT Monitoring & Control System** built in React.
Includes Device Monitoring, Hardware Configuration, AI Chat Copilot, Workflow Builder, and Analytics.

---

## 📁 Project Structure

```
iot-ai-copilot/
│
├── public/
│   └── index.html              ← HTML entry point with Google Fonts
│
├── src/
│   ├── index.js                ← React DOM root mount
│   ├── index.css               ← Global styles & animations
│   ├── App.jsx                 ← Root component, tab routing, global state
│   │
│   ├── data/
│   │   ├── devices.js          ← Device & component seed data
│   │   ├── analytics.js        ← Chart data & KPI cards
│   │   ├── workflows.js        ← Conditions & Actions for drag-drop builder
│   │   └── aiResponses.js      ← Suggested prompts & AI response map
│   │
│   ├── hooks/
│   │   └── useToast.js         ← Custom hook for toast notifications
│   │
│   └── components/
│       ├── Icons.jsx            ← All SVG icon components
│       ├── DeviceCard.jsx       ← Individual device card with actions
│       ├── Navbar.jsx           ← Topbar, AppHeader, TabNav
│       │
│       ├── shared/
│       │   ├── StatusBadge.jsx  ← online/offline/warning badge
│       │   ├── Toast.jsx        ← Toast notification overlay
│       │   └── Button.jsx       ← Reusable button (dark/outline/primary)
│       │
│       └── tabs/
│           ├── MonitoringTab.jsx   ← Device grid, search, stat cards
│           ├── ConfigureTab.jsx    ← Add component, mission, AI summary
│           ├── AICopilotTab.jsx    ← Chat UI with AI responses
│           ├── WorkflowsTab.jsx    ← Drag-and-drop workflow builder
│           └── AnalyticsTab.jsx    ← Charts: uptime, recovery, temp, distribution
│
├── package.json
└── README.md
```

---

## 🚀 Step-by-Step Setup in VS Code

### Step 1 — Prerequisites

Make sure you have these installed:

```bash
node --version    # Need v16 or higher
npm --version     # Need v8 or higher
```

Download Node.js from https://nodejs.org if needed.

---

### Step 2 — Open Folder in VS Code

1. Open **VS Code**
2. Go to **File → Open Folder**
3. Select the `iot-ai-copilot` folder
4. You should see the full project tree in the Explorer panel

---

### Step 3 — Install Dependencies

Open the integrated terminal in VS Code:
- Press `` Ctrl + ` `` (backtick) on Windows/Linux
- Press `` Cmd + ` `` on Mac

Then run:

```bash
npm install
```

This installs:
- `react` and `react-dom` (v18)
- `react-scripts` (Create React App toolchain)
- `recharts` (charts library)

---

### Step 4 — Start the Development Server

```bash
npm start
```

- The app opens automatically at **http://localhost:3000**
- Hot-reload is enabled — changes appear instantly

---

### Step 5 — Build for Production (optional)

```bash
npm run build
```

Outputs optimized static files to the `build/` folder.

---

## 🖥️ Features & Tabs

| Tab | Features |
|---|---|
| **Monitoring** | Device grid, online/offline/warning stats, search, Auto-Recover, Run Diagnostics |
| **Configure** | Add components (sensor/actuator), mission objective, control behavior, AI-generated summary |
| **AI Copilot** | Chat interface, typing indicator, suggested prompts, pre-wired AI responses |
| **Workflows** | Drag-and-drop conditions & actions onto canvas, deploy workflow |
| **Analytics** | KPI cards, uptime area chart, recovery bar chart, temperature line chart, device pie chart |

---

## 🎨 Tech Stack

- **React 18** — functional components + hooks
- **Recharts** — all chart visualizations
- **DM Sans** (Google Fonts) — typography
- **Inline styles** — zero CSS dependencies

---

## 🛠️ Customization

### Add a new device
Edit `src/data/devices.js` → add an entry to `INITIAL_DEVICES`.

### Add AI responses
Edit `src/data/aiResponses.js` → add a key-value pair to `AI_RESPONSES`.

### Add workflow blocks
Edit `src/data/workflows.js` → add to `CONDITIONS` or `ACTIONS` arrays.

### Change chart data
Edit `src/data/analytics.js` → update any of the exported arrays.

---

## 📝 VS Code Recommended Extensions

Install these for the best experience:

- **ES7+ React/Redux/React-Native snippets** (`dsznajder.es7-react-js-snippets`)
- **Prettier - Code formatter** (`esbenp.prettier-vscode`)
- **Auto Rename Tag** (`formulahendry.auto-rename-tag`)
- **Color Highlight** (`naumovs.color-highlight`)

---

## ❓ Troubleshooting

**Port 3000 already in use?**
```bash
# React will ask you to use another port — press Y
# Or kill the process on 3000:
npx kill-port 3000
```

**Module not found errors?**
```bash
rm -rf node_modules
npm install
```

**Charts not rendering?**
Make sure `recharts` installed correctly:
```bash
npm install recharts
```

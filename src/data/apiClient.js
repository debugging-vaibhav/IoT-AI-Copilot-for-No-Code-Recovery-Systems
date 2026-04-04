/**
 * API Client — all calls from the frontend go through here.
 *
 * Change BACKEND_URL to your laptop's LAN IP if accessing
 * from another device on the same network.
 */

const BACKEND_URL =
  process.env.REACT_APP_BACKEND_URL || "http://localhost:8000/api";

async function apiFetch(path, options = {}) {
  const url = `${BACKEND_URL}${path}`;
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || data.message || `API error ${res.status}`);
  }
  return data;
}

// ─── Health ────────────────────────────────

export function fetchHealth() {
  return apiFetch("/");
}

export function fetchSystemStatus() {
  return apiFetch("/status");
}

// ─── Devices (RPi registry) ───────────────

export function fetchDeviceList() {
  return apiFetch("/device/list");
}

export function fetchDeviceLiveStatus(deviceId) {
  return apiFetch(`/device/${deviceId}/status`);
}

// ─── AI Copilot ───────────────────────────

export function describeRobot(description) {
  return apiFetch("/describe-robot", {
    method: "POST",
    body: JSON.stringify({ description }),
  });
}

export function generateLogic(description) {
  return apiFetch("/generate-logic", {
    method: "POST",
    body: JSON.stringify({ description }),
  });
}

// ─── Execution ────────────────────────────

export function applyRecovery(logic) {
  return apiFetch("/recover", {
    method: "POST",
    body: JSON.stringify({ logic }),
  });
}

export function executeDirect(command) {
  return apiFetch("/execute-direct", {
    method: "POST",
    body: JSON.stringify(command),
  });
}

// ─── Logs ─────────────────────────────────

export function fetchLogs() {
  return apiFetch("/logs");
}

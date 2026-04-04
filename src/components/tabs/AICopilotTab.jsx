import { useState, useRef, useEffect, useCallback } from "react";
import { SUGGEST_PROMPTS, AI_RESPONSES, DEFAULT_AI_RESPONSE } from "../../data/aiResponses";
import { describeRobot, applyRecovery } from "../../data/apiClient";
import { SendIcon } from "../Icons";

function TypingIndicator() {
  return (
    <div style={{ display: "flex", gap: 4, padding: "4px 0" }}>
      {[0, 1, 2].map((i) => (
        <div key={i} style={{
          width: 7, height: 7, background: "#9ca3af", borderRadius: "50%",
          animation: `bounce 1s ${i * 0.2}s infinite`,
        }} />
      ))}
    </div>
  );
}

function BotAvatar() {
  return (
    <div style={{
      width: 34, height: 34,
      background: "linear-gradient(135deg, #7c3aed, #a78bfa)",
      borderRadius: 8,
      display: "flex", alignItems: "center", justifyContent: "center",
      flexShrink: 0,
    }}>
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2">
        <path d="M12 2L2 7l10 5 10-5-10-5z" />
        <path d="M2 17l10 5 10-5" />
        <path d="M2 12l10 5 10-5" />
      </svg>
    </div>
  );
}

function ChatMessage({ message, onApply }) {
  const isUser = message.role === "user";
  return (
    <div style={{ display: "flex", gap: 12, flexDirection: isUser ? "row-reverse" : "row", alignItems: "flex-end" }}>
      {!isUser && <BotAvatar />}
      <div style={{ maxWidth: "75%" }}>
        <div style={{
          background: isUser ? "#111827" : "#f3f4f6",
          color: isUser ? "#fff" : "#111827",
          padding: "12px 16px",
          borderRadius: isUser ? "16px 16px 4px 16px" : "16px 16px 16px 4px",
          fontSize: 14, lineHeight: 1.65, whiteSpace: "pre-wrap",
        }}>
          {message.text}
        </div>
        {message.logic && message.isSafe && (
          <button
            onClick={() => onApply(message.logic)}
            disabled={message.applied}
            style={{
              marginTop: 8, padding: "8px 18px",
              background: message.applied ? "#d1d5db" : "#15803d",
              color: "#fff", border: "none", borderRadius: 8,
              fontSize: 13, fontWeight: 600, cursor: message.applied ? "default" : "pointer",
              fontFamily: "inherit",
            }}
          >
            {message.applied ? "Applied" : "Apply to Hardware"}
          </button>
        )}
        <div style={{ fontSize: 11, color: "#9ca3af", marginTop: 4, textAlign: isUser ? "right" : "left" }}>
          {message.time}
          {message.source && (
            <span style={{ marginLeft: 8, fontStyle: "italic" }}>({message.source})</span>
          )}
        </div>
      </div>
    </div>
  );
}

export function AICopilotTab({ backendStatus, showToast }) {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "👋 Hello! I'm your Robotics AI Copilot. I help you configure sensors and actuators, generate control logic, and recover from hardware failures—all without code.\n\nI'm connected to the backend and can send real commands to your Raspberry Pi. How can I assist you today?",
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" }),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const send = useCallback(
    async (text) => {
      if (!text.trim() || loading) return;

      const now = () => new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
      setMessages((prev) => [...prev, { role: "user", text, time: now() }]);
      setInput("");
      setLoading(true);

      // Try the real backend first, fall back to local responses
      if (backendStatus === "online") {
        try {
          const data = await describeRobot(text);
          const logic = data.logic;
          const isSafe = data.is_safe;

          let reply = isSafe
            ? `✅ AI Analysis Complete\n\n`
            : `⚠️ Validation Failed\n\n`;

          reply += `Safe to execute: ${isSafe ? "Yes" : "No"}\n`;
          reply += `Message: ${data.message}\n`;

          if (logic) {
            reply += `\nGenerated Command:\n`;
            reply += `  Action: ${logic.action}\n`;
            reply += `  Pin: GPIO ${logic.pin}\n`;
            if (logic.angle != null) {
              reply += `  Angle: ${logic.angle}°\n`;
            }
            if (logic.sensor) {
              reply += `  Sensor: ${logic.sensor}\n`;
            }
            if (logic.rule) {
              reply += `\nReasoning: ${logic.rule}`;
            }
          } else {
            reply += "\nNo logic generated.";
          }

          setMessages((prev) => [
            ...prev,
            {
              role: "assistant", text: reply, time: now(), source: "AI-LAM",
              logic: logic || null, isSafe,
            },
          ]);
          setLoading(false);
          return;
        } catch (err) {
          // Backend call failed, fall through to local
          showToast && showToast("Backend unreachable, using local response", "info");
        }
      }

      // Local fallback
      setTimeout(() => {
        const reply = AI_RESPONSES[text] || DEFAULT_AI_RESPONSE(text);
        setMessages((prev) => [...prev, { role: "assistant", text: reply, time: now(), source: "local" }]);
        setLoading(false);
      }, 800);
    },
    [loading, backendStatus, showToast]
  );

  const handleApply = useCallback(
    async (logic) => {
      const now = () => new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
      try {
        const result = await applyRecovery(logic);
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            text: `🚀 ${result.message}`,
            time: now(),
            source: "hardware",
          },
        ]);
        // Mark the command message as applied
        setMessages((prev) =>
          prev.map((m) => (m.logic === logic ? { ...m, applied: true } : m))
        );
        showToast && showToast("Command applied to hardware", "success");
      } catch (err) {
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            text: `❌ Failed to apply: ${err.message}`,
            time: now(),
            source: "error",
          },
        ]);
        showToast && showToast(`Apply failed: ${err.message}`, "error");
      }
    },
    [showToast]
  );

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send(input);
    }
  };

  return (
    <div style={{ maxWidth: 860, margin: "0 auto" }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 14, marginBottom: 28 }}>
        <div style={{
          width: 48, height: 48,
          background: "linear-gradient(135deg, #7c3aed, #a78bfa)",
          borderRadius: 12,
          display: "flex", alignItems: "center", justifyContent: "center",
        }}>
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2">
            <path d="M12 2L2 7l10 5 10-5-10-5z" />
            <path d="M2 17l10 5 10-5" />
            <path d="M2 12l10 5 10-5" />
          </svg>
        </div>
        <div>
          <h2 style={{ margin: 0, fontSize: 22, fontWeight: 800 }}>AI Copilot</h2>
          <p style={{ margin: 0, fontSize: 13, color: "#6b7280" }}>
            Your intelligent IoT assistant —{" "}
            <span style={{ color: backendStatus === "online" ? "#15803d" : "#dc2626", fontWeight: 600 }}>
              {backendStatus === "online" ? "connected to backend" : "offline mode"}
            </span>
          </p>
        </div>
      </div>

      <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, overflow: "hidden" }}>
        {/* Messages */}
        <div style={{
          minHeight: 320, maxHeight: 440, overflowY: "auto", padding: 24,
          display: "flex", flexDirection: "column", gap: 18,
        }}>
          {messages.map((m, i) => (
            <ChatMessage key={i} message={m} onApply={handleApply} />
          ))}
          {loading && (
            <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
              <BotAvatar />
              <div style={{ background: "#f3f4f6", padding: "12px 16px", borderRadius: "16px 16px 16px 4px" }}>
                <TypingIndicator />
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Suggested prompts */}
        <div style={{ padding: "0 24px 14px", borderTop: "1px solid #f3f4f6" }}>
          <div style={{ padding: "12px 0 8px", fontSize: 12, color: "#6b7280", fontWeight: 500 }}>Try asking:</div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            {SUGGEST_PROMPTS.map((p) => (
              <button
                key={p}
                onClick={() => send(p)}
                style={{
                  padding: "6px 14px", background: "#fff",
                  border: "1.5px solid #d1d5db", borderRadius: 20,
                  fontSize: 12, cursor: "pointer", fontWeight: 500,
                  color: "#374151", fontFamily: "inherit",
                }}
              >
                {p}
              </button>
            ))}
          </div>
        </div>

        {/* Input area */}
        <div style={{ display: "flex", gap: 10, padding: "12px 24px 20px", borderTop: "1px solid #e5e7eb" }}>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask the AI Copilot..."
            style={{
              flex: 1, padding: "12px 16px",
              border: "1.5px solid #e5e7eb", borderRadius: 10,
              fontSize: 14, outline: "none", fontFamily: "inherit",
            }}
          />
          <button
            onClick={() => send(input)}
            style={{
              width: 44, height: 44, background: "#111827",
              border: "none", borderRadius: 10, cursor: "pointer",
              display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0,
            }}
          >
            <SendIcon size={18} color="#fff" />
          </button>
        </div>
      </div>
    </div>
  );
}

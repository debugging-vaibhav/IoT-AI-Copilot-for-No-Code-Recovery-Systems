import { useState, useRef } from "react";
import { CONDITIONS, ACTIONS } from "../../data/workflows";
import { InfoIcon, ActionBoltIcon } from "../Icons";

function BlockItem({ item, type, onDragStart }) {
  return (
    <div
      draggable
      onDragStart={() => onDragStart(item, type)}
      style={{
        background: item.color,
        border: `1.5px solid ${item.border}`,
        borderRadius: 8,
        padding: "10px 14px",
        cursor: "grab",
        userSelect: "none",
      }}
    >
      <div style={{ fontWeight: 700, fontSize: 13, color: item.text, display: "flex", alignItems: "center", gap: 6 }}>
        {item.icon && <span>{item.icon}</span>}
        {!item.icon && (type === "condition"
          ? <InfoIcon size={14} color={item.text} />
          : <ActionBoltIcon size={14} color={item.text} />
        )}
        {item.label}
      </div>
      <div style={{ fontSize: 11, color: item.text, opacity: 0.7, marginTop: 2 }}>
        {item.desc}
      </div>
    </div>
  );
}

function CanvasBlock({ block, onRemove }) {
  const colors = {
    condition: { bg: "#fef3c7", border: "#fde68a", text: "#92400e" },
    action:    { bg: "#ede9fe", border: "#c4b5fd", text: "#5b21b6" },
  };
  const c = colors[block.blockType] || colors.action;

  return (
    <div style={{ background: c.bg, border: `1.5px solid ${c.border}`, borderRadius: 8, padding: "12px 16px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
      <div>
        <div style={{ fontWeight: 700, fontSize: 13, color: c.text }}>
          {block.icon && <span style={{ marginRight: 6 }}>{block.icon}</span>}
          {block.label}
        </div>
        <div style={{ fontSize: 11, color: c.text, opacity: 0.75 }}>{block.desc}</div>
      </div>
      <button
        onClick={() => onRemove(block.uid)}
        style={{ background: "none", border: "none", cursor: "pointer", fontSize: 18, color: c.text, opacity: 0.5, lineHeight: 1 }}
      >
        ×
      </button>
    </div>
  );
}

export function WorkflowsTab() {
  const [canvasBlocks, setCanvasBlocks] = useState([]);
  const [dragging, setDragging] = useState(null);
  const [deployed, setDeployed]   = useState(false);
  const [dragOver, setDragOver]   = useState(false);

  const handleDragStart = (item, type) => setDragging({ ...item, blockType: type });
  const handleDragOver  = (e) => { e.preventDefault(); setDragOver(true); };
  const handleDragLeave = () => setDragOver(false);

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    if (dragging) {
      setCanvasBlocks((prev) => [...prev, { ...dragging, uid: Date.now() }]);
      setDragging(null);
    }
  };

  const removeBlock = (uid) => setCanvasBlocks((prev) => prev.filter((b) => b.uid !== uid));
  const clearCanvas = () => setCanvasBlocks([]);

  const deploy = () => {
    if (canvasBlocks.length === 0) return;
    setDeployed(true);
    setTimeout(() => setDeployed(false), 2000);
  };

  return (
    <div>
      <h2 style={{ fontSize: 26, fontWeight: 800, margin: "0 0 4px" }}>No-Code Workflow Builder</h2>
      <p style={{ color: "#6b7280", fontSize: 14, margin: "0 0 24px" }}>
        Create automated recovery protocols with drag and drop
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "320px 1fr", gap: 20 }}>
        {/* ── Sidebar ── */}
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          {/* Conditions */}
          <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: 20 }}>
            <h3 style={{ margin: "0 0 14px", fontWeight: 700, fontSize: 15, display: "flex", alignItems: "center", gap: 8 }}>
              <InfoIcon size={16} /> Conditions
            </h3>
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {CONDITIONS.map((c) => (
                <BlockItem key={c.id} item={c} type="condition" onDragStart={handleDragStart} />
              ))}
            </div>
          </div>

          {/* Actions */}
          <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: 20 }}>
            <h3 style={{ margin: "0 0 14px", fontWeight: 700, fontSize: 15, display: "flex", alignItems: "center", gap: 8 }}>
              <ActionBoltIcon size={16} /> Actions
            </h3>
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {ACTIONS.map((a) => (
                <BlockItem key={a.id} item={a} type="action" onDragStart={handleDragStart} />
              ))}
            </div>
          </div>
        </div>

        {/* ── Canvas ── */}
        <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: 20 }}>
          {/* Canvas toolbar */}
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
            <h3 style={{ margin: 0, fontWeight: 700, fontSize: 15 }}>Workflow Canvas</h3>
            <div style={{ display: "flex", gap: 10 }}>
              <button
                onClick={clearCanvas}
                style={{
                  display: "flex", alignItems: "center", gap: 6,
                  padding: "7px 14px", background: "#fff",
                  border: "1.5px solid #d1d5db", borderRadius: 8,
                  fontWeight: 600, fontSize: 13, cursor: "pointer",
                  fontFamily: "inherit",
                }}
              >
                🗑 Clear
              </button>
              <button
                onClick={deploy}
                style={{
                  display: "flex", alignItems: "center", gap: 6,
                  padding: "7px 18px",
                  background: deployed ? "#22c55e" : "#111827",
                  color: "#fff", border: "none", borderRadius: 8,
                  fontWeight: 700, fontSize: 13, cursor: "pointer",
                  transition: "background 0.3s",
                  fontFamily: "inherit",
                }}
              >
                ▶ {deployed ? "Deployed!" : "Deploy Workflow"}
              </button>
            </div>
          </div>

          {/* Drop zone */}
          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            style={{
              minHeight: 360,
              border: `2px dashed ${dragOver ? "#6366f1" : "#d1d5db"}`,
              borderRadius: 10,
              padding: 20,
              display: "flex",
              flexDirection: "column",
              gap: 10,
              transition: "border-color 0.2s",
              background: dragOver ? "#f8f7ff" : "transparent",
            }}
          >
            {canvasBlocks.length === 0 ? (
              <div style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", color: "#9ca3af", gap: 8 }}>
                <div style={{ fontSize: 36 }}>+</div>
                <div style={{ fontWeight: 600 }}>Drag and drop blocks here to build your workflow</div>
                <div style={{ fontSize: 13 }}>Start with a condition, then add actions</div>
              </div>
            ) : (
              canvasBlocks.map((block, idx) => (
                <div key={block.uid}>
                  {idx > 0 && (
                    <div style={{ display: "flex", justifyContent: "center", margin: "4px 0 8px" }}>
                      <div style={{ width: 2, height: 16, background: "#d1d5db" }} />
                    </div>
                  )}
                  <CanvasBlock block={block} onRemove={removeBlock} />
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

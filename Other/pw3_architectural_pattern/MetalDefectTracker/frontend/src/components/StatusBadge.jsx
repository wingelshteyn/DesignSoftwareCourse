/**
 * components/StatusBadge.jsx
 * Renders a coloured inline badge for InspectionRecord.status values.
 *
 * FRQ-5 status lifecycle: queued → pending → accepted | rejected
 */

import React from "react";

const COLOR_MAP = {
  queued:   { background: "#e0c000", color: "#000" },
  pending:  { background: "#1a73e8", color: "#fff" },
  accepted: { background: "#188038", color: "#fff" },
  rejected: { background: "#c5221f", color: "#fff" },
};

const DEFAULT_STYLE = { background: "#757575", color: "#fff" };

export default function StatusBadge({ status }) {
  const style = COLOR_MAP[status] ?? DEFAULT_STYLE;
  return (
    <span
      style={{
        ...style,
        padding: "2px 8px",
        borderRadius: "12px",
        fontSize: "0.78rem",
        fontWeight: 600,
        textTransform: "uppercase",
        letterSpacing: "0.04em",
        display: "inline-block",
      }}
    >
      {status ?? "unknown"}
    </span>
  );
}

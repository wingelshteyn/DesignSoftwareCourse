/**
 * components/DefectList.jsx
 *
 * FRQ-6.3  Operator can view detected defects and exclude individual ones.
 *
 * Props:
 *   defects       {Array}   [{ id, defect_type, confidence }]
 *   excludedIds   {Set}     IDs currently excluded
 *   onToggleExclude {fn}    callback(defectId)
 */

import React from "react";

export default function DefectList({ defects = [], excludedIds = new Set(), onToggleExclude }) {
  if (defects.length === 0) {
    return <p>No defects detected.</p>;
  }

  return (
    <section>
      <h3>Detected Defects</h3>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {defects.map((d) => {
          const excluded = excludedIds.has(d.id);
          return (
            <li
              key={d.id}
              style={{
                display: "flex",
                alignItems: "center",
                gap: "0.5rem",
                opacity: excluded ? 0.5 : 1,
                marginBottom: "0.4rem",
              }}
            >
              <input
                type="checkbox"
                id={`defect-${d.id}`}
                checked={!excluded}
                onChange={() => onToggleExclude(d.id)}
              />
              <label htmlFor={`defect-${d.id}`}>
                <strong>{d.defect_type}</strong> - confidence:{" "}
                {(d.confidence * 100).toFixed(1)}%
              </label>
            </li>
          );
        })}
      </ul>
    </section>
  );
}

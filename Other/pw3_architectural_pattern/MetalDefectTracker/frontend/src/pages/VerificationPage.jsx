/**
 * pages/VerificationPage.jsx
 *
 * FRQ-6  - operator sees the image, the detected defects list, and accepts /
 *           rejects the record; can exclude individual auto-detected defects.
 * FRQ-7  - operator can add / edit manual defect bounding boxes on the image.
 *
 * Layout:
 *   Left column  - <DefectCanvas> with defect boxes overlaid on the image
 *   Right column - <DefectList> + decision controls
 */

import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { imagesApi } from "../api/imagesApi";
import DefectCanvas from "../components/DefectCanvas";
import DefectList from "../components/DefectList";
import StatusBadge from "../components/StatusBadge";

export default function VerificationPage() {
  const { inspectionId } = useParams();
  const navigate = useNavigate();

  const [inspection, setInspection] = useState(null);
  const [detection, setDetection] = useState(null);
  const [excludedIds, setExcludedIds] = useState(new Set());
  const [manualDefects, setManualDefects] = useState([]); // { defect_type, bbox_x, bbox_y, bbox_w, bbox_h }
  const [decision, setDecision] = useState(null); // "accepted" | "rejected"
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([
      imagesApi.get(inspectionId),
      imagesApi.getDetection(inspectionId),
    ])
      .then(([{ data: insp }, { data: det }]) => {
        setInspection(insp);
        setDetection(det);
      })
      .catch((err) => setError(err.message));
  }, [inspectionId]);

  const toggleExclude = (defectId) =>
    setExcludedIds((prev) => {
      const next = new Set(prev);
      next.has(defectId) ? next.delete(defectId) : next.add(defectId);
      return next;
    });

  const handleAddManualDefect = (bbox) => {
    // bbox = { defect_type, bbox_x, bbox_y, bbox_w, bbox_h }
    setManualDefects((prev) => [...prev, bbox]);
  };

  const handleSubmit = async () => {
    if (!decision) return;
    setSubmitting(true);
    try {
      await imagesApi.submitVerification(inspectionId, {
        decision,
        excluded_defect_ids: [...excludedIds],
        manual_defects: manualDefects,
      });
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.detail ?? err.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (error) return <p role="alert">{error}</p>;
  if (!inspection || !detection) return <p>Loading…</p>;

  const activeDefects = (detection.defects ?? []).filter(
    (d) => !excludedIds.has(d.id)
  );

  return (
    <main style={{ display: "flex", gap: "1rem" }}>
      {/* ── Left: image + defect bboxes ── */}
      <section style={{ flex: "1 1 60%" }}>
        <h2>
          Inspection #{inspectionId}{" "}
          <StatusBadge status={inspection.status} />
        </h2>
        <DefectCanvas
          imageUrl={inspection.image}
          detectedDefects={detection.defects ?? []}
          excludedIds={excludedIds}
          manualDefects={manualDefects}
          onAddManualDefect={handleAddManualDefect}
        />
      </section>

      {/* ── Right: defect list + controls ── */}
      <section style={{ flex: "0 0 320px" }}>
        <DefectList
          defects={detection.defects ?? []}
          excludedIds={excludedIds}
          onToggleExclude={toggleExclude}
        />

        <hr />

        <fieldset>
          <legend>Decision</legend>
          <label>
            <input
              type="radio"
              name="decision"
              value="accepted"
              checked={decision === "accepted"}
              onChange={() => setDecision("accepted")}
            />
            Accept
          </label>
          <label>
            <input
              type="radio"
              name="decision"
              value="rejected"
              checked={decision === "rejected"}
              onChange={() => setDecision("rejected")}
            />
            Reject
          </label>
        </fieldset>

        {error && <p role="alert">{error}</p>}

        <button
          onClick={handleSubmit}
          disabled={!decision || submitting}
        >
          {submitting ? "Submitting…" : "Submit"}
        </button>
      </section>
    </main>
  );
}

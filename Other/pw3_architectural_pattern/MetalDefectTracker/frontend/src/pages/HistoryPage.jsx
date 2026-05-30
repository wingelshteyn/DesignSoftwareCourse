/**
 * pages/HistoryPage.jsx
 * FRQ-8  - Inspection history with rich filtering
 */

import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { analyticsApi } from "../api/analyticsApi";
import StatusBadge from "../components/StatusBadge";

const STATUSES = ["queued", "pending", "accepted", "rejected"];

export default function HistoryPage() {
  const navigate = useNavigate();

  const [filters, setFilters] = useState({
    status: "",
    has_defects: "",
    date_from: "",
    date_to: "",
    zone_id: "",
    camera_id: "",
    operator_id: "",
  });
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchHistory = () => {
    setLoading(true);
    // Strip empty filter values before sending
    const params = Object.fromEntries(
      Object.entries(filters).filter(([, v]) => v !== "")
    );
    analyticsApi
      .history(params)
      .then(({ data }) => setRecords(data.results ?? data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  };

  // Initial load
  useEffect(fetchHistory, []); // eslint-disable-line react-hooks/exhaustive-deps

  const handleFilter = (e) => {
    e.preventDefault();
    fetchHistory();
  };

  const setField = (name, value) =>
    setFilters((prev) => ({ ...prev, [name]: value }));

  return (
    <main>
      <h1>Inspection History</h1>

      {/* ── Filters ── */}
      <form onSubmit={handleFilter}>
        <select
          value={filters.status}
          onChange={(e) => setField("status", e.target.value)}
        >
          <option value="">All statuses</option>
          {STATUSES.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>

        <select
          value={filters.has_defects}
          onChange={(e) => setField("has_defects", e.target.value)}
        >
          <option value="">Defects: any</option>
          <option value="true">With defects</option>
          <option value="false">Without defects</option>
        </select>

        <input
          type="date"
          value={filters.date_from}
          onChange={(e) => setField("date_from", e.target.value)}
          placeholder="From"
        />
        <input
          type="date"
          value={filters.date_to}
          onChange={(e) => setField("date_to", e.target.value)}
          placeholder="To"
        />

        <input
          type="number"
          value={filters.zone_id}
          onChange={(e) => setField("zone_id", e.target.value)}
          placeholder="Zone ID"
          min={1}
        />
        <input
          type="number"
          value={filters.camera_id}
          onChange={(e) => setField("camera_id", e.target.value)}
          placeholder="Camera ID"
          min={1}
        />
        <input
          type="number"
          value={filters.operator_id}
          onChange={(e) => setField("operator_id", e.target.value)}
          placeholder="Operator ID"
          min={1}
        />

        <button type="submit">Apply</button>
      </form>

      {/* ── Results ── */}
      {loading && <p>Loading…</p>}
      {error && <p role="alert">{error}</p>}

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Camera</th>
            <th>Zone</th>
            <th>Received</th>
            <th>Status</th>
            <th>Defects</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {records.map((rec) => (
            <tr key={rec.id}>
              <td>{rec.id}</td>
              <td>{rec.camera}</td>
              <td>{rec.zone}</td>
              <td>{new Date(rec.received_at).toLocaleString()}</td>
              <td>
                <StatusBadge status={rec.status} />
              </td>
              <td>{rec.defect_count ?? "-"}</td>
              <td>
                <button
                  onClick={() => navigate(`/history/${rec.id}`)}
                >
                  Details
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}

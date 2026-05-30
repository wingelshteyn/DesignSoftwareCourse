/**
 * pages/StatisticsPage.jsx
 * FRQ-9  - Statistical dashboards (technologist + administrator)
 */

import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { analyticsApi } from "../api/analyticsApi";
import { selectUser } from "../store/authSlice";

export default function StatisticsPage() {
  const user = useSelector(selectUser);
  const [overall, setOverall] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    analyticsApi
      .overallStats()
      .then(({ data }) => setOverall(data))
      .catch((err) => setError(err.message));
  }, []);

  return (
    <main>
      <h1>Statistics</h1>
      {error && <p role="alert">{error}</p>}

      {overall && (
        <section>
          <h2>Overall</h2>
          <dl>
            <dt>Total inspections</dt>
            <dd>{overall.total_inspections}</dd>

            <dt>Accepted</dt>
            <dd>{overall.accepted}</dd>

            <dt>Rejected</dt>
            <dd>{overall.rejected}</dd>

            <dt>Pending</dt>
            <dd>{overall.pending}</dd>

            <dt>Avg. defects per record</dt>
            <dd>{overall.avg_defects_per_record?.toFixed(2) ?? "-"}</dd>
          </dl>
        </section>
      )}

      {/* FRQ-9.3 - per-operator breakdown (administrator only) */}
      {user?.role === "administrator" && (
        <OperatorBreakdown />
      )}
    </main>
  );
}

function OperatorBreakdown() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    analyticsApi
      .overallStats() // re-use; backend returns per_operator array when role=admin
      .then(({ data }) => setStats(data.per_operator ?? []))
      .catch((err) => setError(err.message));
  }, []);

  return (
    <section>
      <h2>Per-Operator Breakdown</h2>
      {error && <p role="alert">{error}</p>}
      {stats && (
        <table>
          <thead>
            <tr>
              <th>Operator</th>
              <th>Verified</th>
              <th>Accepted</th>
              <th>Rejected</th>
              <th>Avg. time (s)</th>
            </tr>
          </thead>
          <tbody>
            {stats.map((row) => (
              <tr key={row.operator_id}>
                <td>{row.username}</td>
                <td>{row.total_verified}</td>
                <td>{row.accepted}</td>
                <td>{row.rejected}</td>
                <td>{row.avg_time_to_verify_s?.toFixed(1) ?? "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}

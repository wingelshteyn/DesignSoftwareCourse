/**
 * pages/DashboardPage.jsx
 *
 * Entry point after login.
 * Shows a queue of inspection records that are pending operator review (FRQ-5,
 * FRQ-6). The operator clicks a record to open VerificationPage.
 * Technologists and administrators see recently received images.
 */

import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { selectUser } from "../store/authSlice";
import { imagesApi } from "../api/imagesApi";
import StatusBadge from "../components/StatusBadge";

export default function DashboardPage() {
  const user = useSelector(selectUser);
  const navigate = useNavigate();

  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const params = user?.role === "operator" ? { status: "pending" } : {};
    imagesApi
      .list(params)
      .then(({ data }) => setRecords(data.results ?? data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [user]);

  return (
    <main>
      <h1>Dashboard</h1>
      {loading && <p>Loading…</p>}
      {error && <p role="alert">{error}</p>}
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Camera</th>
            <th>Received at</th>
            <th>Status</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {records.map((rec) => (
            <tr key={rec.id}>
              <td>{rec.id}</td>
              <td>{rec.camera}</td>
              <td>{new Date(rec.received_at).toLocaleString()}</td>
              <td>
                <StatusBadge status={rec.status} />
              </td>
              <td>
                {rec.status === "pending" && user?.role === "operator" && (
                  <button onClick={() => navigate(`/verification/${rec.id}`)}>
                    Verify
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}

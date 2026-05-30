/**
 * pages/AdminPage.jsx
 * FRQ-2   User management
 * FRQ-10  Camera configuration
 * FRQ-11  Defect catalog + retraining
 * FRQ-12  Model version management
 */

import React, { useEffect, useState } from "react";
import { adminApi } from "../api/adminApi";

// ── Cameras ───────────────────────────────────────────────────────────────────

function CamerasSection() {
  const [cameras, setCameras] = useState([]);

  useEffect(() => {
    adminApi.listCameras().then(({ data }) => setCameras(data.results ?? data));
  }, []);

  return (
    <section>
      <h2>Cameras</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Zone</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {cameras.map((cam) => (
            <tr key={cam.id}>
              <td>{cam.id}</td>
              <td>{cam.name}</td>
              <td>{cam.zone}</td>
              <td>{cam.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

// ── Defect types ──────────────────────────────────────────────────────────────

function DefectTypesSection() {
  const [types, setTypes] = useState([]);
  const [newCode, setNewCode] = useState("");
  const [newLabel, setNewLabel] = useState("");

  useEffect(() => {
    adminApi.listDefectTypes().then(({ data }) => setTypes(data.results ?? data));
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    const { data } = await adminApi.createDefectType({
      code: newCode,
      label: newLabel,
    });
    setTypes((prev) => [...prev, data]);
    setNewCode("");
    setNewLabel("");
  };

  return (
    <section>
      <h2>Defect Types</h2>
      <ul>
        {types.map((dt) => (
          <li key={dt.code}>
            <strong>{dt.code}</strong> - {dt.label}
            {dt.is_builtin && " (built-in)"}
          </li>
        ))}
      </ul>
      <form onSubmit={handleCreate}>
        <input
          value={newCode}
          onChange={(e) => setNewCode(e.target.value)}
          placeholder="Code (e.g. RS)"
          required
        />
        <input
          value={newLabel}
          onChange={(e) => setNewLabel(e.target.value)}
          placeholder="Label"
          required
        />
        <button type="submit">Add defect type</button>
      </form>
    </section>
  );
}

// ── Model versions ────────────────────────────────────────────────────────────

function ModelVersionsSection() {
  const [versions, setVersions] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    adminApi
      .listModelVersions()
      .then(({ data }) => setVersions(data.results ?? data))
      .catch((err) => setError(err.message));
  }, []);

  const deploy = async (id) => {
    await adminApi.deployModel(id);
    const { data } = await adminApi.listModelVersions();
    setVersions(data.results ?? data);
  };

  const rollback = async (id) => {
    await adminApi.rollbackModel(id);
    const { data } = await adminApi.listModelVersions();
    setVersions(data.results ?? data);
  };

  return (
    <section>
      <h2>Model Versions</h2>
      {error && <p role="alert">{error}</p>}
      <table>
        <thead>
          <tr>
            <th>Tag</th>
            <th>Status</th>
            <th>Confidence</th>
            <th>Deployed at</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {versions.map((v) => (
            <tr key={v.id}>
              <td>{v.version_tag}</td>
              <td>{v.status}</td>
              <td>{v.confidence_threshold}</td>
              <td>{v.deployed_at ? new Date(v.deployed_at).toLocaleString() : "-"}</td>
              <td>
                {v.status === "staging" && (
                  <button onClick={() => deploy(v.id)}>Deploy</button>
                )}
                {v.status === "active" && (
                  <button onClick={() => rollback(v.id)}>Rollback</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

// ── Page root ─────────────────────────────────────────────────────────────────

export default function AdminPage() {
  return (
    <main>
      <h1>Administration</h1>
      <CamerasSection />
      <DefectTypesSection />
      <ModelVersionsSection />
    </main>
  );
}

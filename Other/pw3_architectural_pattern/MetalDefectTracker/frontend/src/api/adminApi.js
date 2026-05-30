/**
 * api/adminApi.js
 * FRQ-10  Camera configuration
 * FRQ-11  Defect catalog + retraining
 * FRQ-12  Model version management
 */

import apiClient from "./client";

export const adminApi = {
  // ── Cameras (FRQ-10) ───────────────────────────────────────────────────────

  listCameras: () => apiClient.get("/admin-panel/cameras/"),

  /** GET /api/admin-panel/cameras/<id>/settings/ */
  getCameraSettings: (cameraId) =>
    apiClient.get(`/admin-panel/cameras/${cameraId}/settings/`),

  /** PUT /api/admin-panel/cameras/<id>/settings/ */
  updateCameraSettings: (cameraId, data) =>
    apiClient.put(`/admin-panel/cameras/${cameraId}/settings/`, data),

  // ── Defect types (FRQ-11) ─────────────────────────────────────────────────

  listDefectTypes: () => apiClient.get("/admin-panel/defect-types/"),

  createDefectType: (data) =>
    apiClient.post("/admin-panel/defect-types/", data),

  getOtherGroup: () => apiClient.get("/admin-panel/defect-types/other-group/"),

  // ── Model versions (FRQ-12) ───────────────────────────────────────────────

  listModelVersions: () => apiClient.get("/admin-panel/models/"),

  /**
   * POST /api/admin-panel/models/<id>/deploy/
   * Promotes a version to "active" status
   */
  deployModel: (modelId) =>
    apiClient.post(`/admin-panel/models/${modelId}/deploy/`),

  /**
   * POST /api/admin-panel/models/<id>/rollback/
   * Rolls active version back to the previous one
   */
  rollbackModel: (modelId) =>
    apiClient.post(`/admin-panel/models/${modelId}/rollback/`),

  /**
   * PATCH /api/admin-panel/models/<id>/confidence/
   * @param {{ confidence_threshold: number }} data
   */
  setConfidence: (modelId, data) =>
    apiClient.patch(`/admin-panel/models/${modelId}/confidence/`, data),

  // ── Retraining (FRQ-11) ───────────────────────────────────────────────────

  startRetraining: (data) =>
    apiClient.post("/admin-panel/retraining/start/", data),

  getRetrainingJob: (jobId) =>
    apiClient.get(`/admin-panel/retraining/${jobId}/`),
};

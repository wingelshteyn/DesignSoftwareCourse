/**
 * api/imagesApi.js
 * FRQ-6   Operator verification
 * FRQ-8   Inspection history
 */

import apiClient from "./client";

export const imagesApi = {
  /** GET /api/images/list/ - inspection history (FRQ-8.1) */
  list: (params) => apiClient.get("/images/list/", { params }),

  /** GET /api/images/<id>/ - single inspection record */
  get: (id) => apiClient.get(`/images/${id}/`),

  /** GET /api/detections/<id>/ - detection result with defect bboxes (FRQ-6.2) */
  getDetection: (inspectionId) => apiClient.get(`/detections/${inspectionId}/`),

  /** GET /api/verification/<id>/ - stored verification action */
  getVerification: (inspectionId) =>
    apiClient.get(`/verification/${inspectionId}/`),

  /**
   * POST /api/verification/<id>/submit/
   * FRQ-6.3, FRQ-6.4, FRQ-7.1, FRQ-7.2, FRQ-7.3
   * @param {number} inspectionId
   * @param {{ decision, excluded_defect_ids, manual_defects }} payload
   */
  submitVerification: (inspectionId, payload) =>
    apiClient.post(`/verification/${inspectionId}/submit/`, payload),

  /** GET /api/verification/<id>/audit/ - full audit trail (FRQ-7.4) */
  getAudit: (inspectionId) =>
    apiClient.get(`/verification/${inspectionId}/audit/`),
};

/**
 * api/analyticsApi.js
 * FRQ-8   Inspection history with rich filtering
 * FRQ-9   Statistical dashboards
 */

import apiClient from "./client";

export const analyticsApi = {
  // ── FRQ-8 ──────────────────────────────────────────────────────────────────

  /**
   * GET /api/analytics/history/
   * Supported filters: status, has_defects, defect_types,
   *   date_from, date_to, zone_id, camera_id, operator_id
   */
  history: (params) => apiClient.get("/analytics/history/", { params }),

  /** GET /api/analytics/history/<id>/ */
  historyDetail: (id) => apiClient.get(`/analytics/history/${id}/`),

  // ── FRQ-9 ──────────────────────────────────────────────────────────────────

  /** GET /api/analytics/stats/me/ - own stats for the current operator */
  myStats: () => apiClient.get("/analytics/stats/me/"),

  /** GET /api/analytics/stats/ - overall system stats (technologist / admin) */
  overallStats: () => apiClient.get("/analytics/stats/"),

  /**
   * GET /api/analytics/stats/<user_id>/
   * Breakdown for a specific operator (admin only)
   */
  userStats: (userId) => apiClient.get(`/analytics/stats/${userId}/`),
};

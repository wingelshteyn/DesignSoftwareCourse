/**
 * api/authApi.js
 * FRQ-1.1  Authentication endpoints
 */

import apiClient from "./client";

export const authApi = {
  /** POST /api/auth/login/ - returns { access, refresh } */
  login: (username, password) =>
    apiClient.post("/auth/login/", { username, password }),

  /** POST /api/auth/refresh/ - returns { access } */
  refresh: (refresh) =>
    apiClient.post("/auth/refresh/", { refresh }),

  /** GET /api/auth/me/ - returns current user profile */
  me: () => apiClient.get("/auth/me/"),
};

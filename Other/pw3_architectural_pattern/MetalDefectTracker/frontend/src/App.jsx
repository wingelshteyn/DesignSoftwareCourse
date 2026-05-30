/**
 * App.jsx - root router
 *
 * Route guards:
 *   <PrivateRoute>          - user must be authenticated
 *   <RoleRoute roles={[…]}> - user must have one of the listed roles
 *
 * Roles (from accounts.User):
 *   "operator"       - FRQ-6, FRQ-7, FRQ-8 (own stats)
 *   "technologist"   - FRQ-8, FRQ-9
 *   "administrator"  - all, including FRQ-2, FRQ-10, FRQ-11, FRQ-12
 */

import React, { useEffect } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { fetchMeThunk, selectIsAuthenticated, selectUser } from "./store/authSlice";

import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import VerificationPage from "./pages/VerificationPage";
import HistoryPage from "./pages/HistoryPage";
import StatisticsPage from "./pages/StatisticsPage";
import AdminPage from "./pages/AdminPage";

// ── Route guard components ────────────────────────────────────────────────────

function PrivateRoute({ children }) {
  const isAuthenticated = useSelector(selectIsAuthenticated);
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

function RoleRoute({ roles, children }) {
  const user = useSelector(selectUser);
  if (!user) return null; // still loading
  return roles.includes(user.role) ? (
    children
  ) : (
    <Navigate to="/" replace />
  );
}

// ── App ───────────────────────────────────────────────────────────────────────

export default function App() {
  const dispatch = useDispatch();
  const isAuthenticated = useSelector(selectIsAuthenticated);

  // Rehydrate user info on page refresh
  useEffect(() => {
    if (isAuthenticated) {
      dispatch(fetchMeThunk());
    }
  }, [dispatch, isAuthenticated]);

  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      {/* Operator + Technologist + Administrator */}
      <Route
        path="/"
        element={
          <PrivateRoute>
            <DashboardPage />
          </PrivateRoute>
        }
      />

      {/* FRQ-6 / FRQ-7 - operator verification */}
      <Route
        path="/verification/:inspectionId"
        element={
          <PrivateRoute>
            <RoleRoute roles={["operator", "administrator"]}>
              <VerificationPage />
            </RoleRoute>
          </PrivateRoute>
        }
      />

      {/* FRQ-8  -  inspection history */}
      <Route
        path="/history"
        element={
          <PrivateRoute>
            <HistoryPage />
          </PrivateRoute>
        }
      />

      {/* FRQ-9 - statistics */}
      <Route
        path="/statistics"
        element={
          <PrivateRoute>
            <RoleRoute roles={["technologist", "administrator"]}>
              <StatisticsPage />
            </RoleRoute>
          </PrivateRoute>
        }
      />

      {/* FRQ-2, FRQ-10, FRQ-11, FRQ-12 - admin panel */}
      <Route
        path="/admin"
        element={
          <PrivateRoute>
            <RoleRoute roles={["administrator"]}>
              <AdminPage />
            </RoleRoute>
          </PrivateRoute>
        }
      />

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

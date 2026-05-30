/**
 * store/authSlice.js
 * Manages authentication state: current user, JWT tokens, login / logout.
 */

import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { authApi } from "../api/authApi";

// ── Thunks ────────────────────────────────────────────────────────────────────

export const loginThunk = createAsyncThunk(
  "auth/login",
  async ({ username, password }, { rejectWithValue }) => {
    try {
      const { data } = await authApi.login(username, password);
      // data = { access, refresh, user: { id, username, role, zone } }
      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);
      return data;
    } catch (err) {
      return rejectWithValue(
        err.response?.data?.detail ?? "Login failed"
      );
    }
  }
);

export const fetchMeThunk = createAsyncThunk(
  "auth/fetchMe",
  async (_, { rejectWithValue }) => {
    try {
      const { data } = await authApi.me();
      return data; // { id, username, role, zone, ... }
    } catch (err) {
      return rejectWithValue(err.response?.data?.detail ?? "Unauthorized");
    }
  }
);

// ── Slice ─────────────────────────────────────────────────────────────────────

const initialState = {
  user: null,         // { id, username, role, zone }
  isAuthenticated: !!localStorage.getItem("access_token"),
  loading: false,
  error: null,
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    logout(state) {
      state.user = null;
      state.isAuthenticated = false;
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    },
    clearError(state) {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    // login
    builder
      .addCase(loginThunk.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loginThunk.fulfilled, (state, action) => {
        state.loading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
      })
      .addCase(loginThunk.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });

    // fetchMe
    builder
      .addCase(fetchMeThunk.fulfilled, (state, action) => {
        state.user = action.payload;
        state.isAuthenticated = true;
      })
      .addCase(fetchMeThunk.rejected, (state) => {
        state.user = null;
        state.isAuthenticated = false;
      });
  },
});

export const { logout, clearError } = authSlice.actions;

// ── Selectors ─────────────────────────────────────────────────────────────────

export const selectUser = (state) => state.auth.user;
export const selectIsAuthenticated = (state) => state.auth.isAuthenticated;
export const selectAuthLoading = (state) => state.auth.loading;
export const selectAuthError = (state) => state.auth.error;

export default authSlice.reducer;

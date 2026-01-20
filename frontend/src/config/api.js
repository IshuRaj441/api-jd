// frontend/src/config/api.js

// 1️⃣ Resolve base URL (env → fallback)
const RAW_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  import.meta.env.VITE_API_URL ||
  "http://localhost:8000";

// 2️⃣ Normalize trailing slash
const NORMALIZED_BASE_URL = RAW_BASE_URL.endsWith("/")
  ? RAW_BASE_URL
  : `${RAW_BASE_URL}/`;

// 3️⃣ Append API version (single source of truth)
export const API_BASE = `${NORMALIZED_BASE_URL}api/v1/`;

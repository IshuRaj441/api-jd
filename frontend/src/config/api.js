// frontend/src/config/api.js

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'https://api-jd.onrender.com/api/v1';

if (!API_BASE) {
  console.warn("VITE_API_BASE_URL is not defined, using default API URL");
}

// Ensure the API base URL doesn't end with a slash
export const API_BASE_URL = API_BASE.endsWith('/') ? API_BASE.slice(0, -1) : API_BASE;

// Optional debug (remove after verification)
console.log("API_BASE_URL =", API_BASE_URL);

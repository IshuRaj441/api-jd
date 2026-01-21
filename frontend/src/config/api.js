// frontend/src/config/api.js

const API_BASE =
  import.meta.env.VITE_API_BASE_URL ||
  "https://api-jd.onrender.com";

export { API_BASE };

// Debug (keep for now)
console.log("API_BASE =", API_BASE);

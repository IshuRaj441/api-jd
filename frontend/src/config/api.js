// frontend/src/config/api.js

const API_BASE = import.meta.env.VITE_API_BASE_URL;

if (!API_BASE) {
  throw new Error("VITE_API_BASE_URL is not defined");
}

export { API_BASE };

// Optional debug (remove after verification)
console.log("API_BASE =", API_BASE);

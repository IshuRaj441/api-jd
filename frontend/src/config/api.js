// Get base URL from environment variable or use default
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "https://api-jd-1-9vjq.onrender.com";

// Ensure the base URL ends with a slash
const normalizedBase = BASE_URL.endsWith('/') ? BASE_URL : `${BASE_URL}/`;

// Export the full API base URL with version
const API_BASE = `${normalizedBase}api/v1`;

export default API_BASE;

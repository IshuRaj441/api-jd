const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const apiFetch = async (endpoint, options = {}) => {
  const defaultOptions = {
    headers: {
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'Pragma': 'no-cache',
      'Expires': '0',
      ...options.headers,
    },
    cache: 'no-store',
    ...options,
  };

  const response = await fetch(`${API_BASE}${endpoint}`, defaultOptions);
  
  if (!response.ok) {
    const error = new Error(`HTTP error! status: ${response.status}`);
    error.status = response.status;
    throw error;
  }

  return response.json();
};

// Helper functions for specific endpoints
export const fetchProfile = () => apiFetch('/profile');
export const fetchPythonProjects = () => apiFetch('/projects?skill=python');
export const search = (query) => apiFetch(`/search?q=${encodeURIComponent(query)}`);

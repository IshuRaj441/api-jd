// API Configuration
import { API_BASE } from '@/config/api';

// Helper function to create full URL with query parameters
const createUrl = (endpoint, params = {}) => {
  // Ensure endpoint doesn't have a leading slash to prevent double slashes
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.substring(1) : endpoint;
  const url = new URL(`${API_BASE}/${cleanEndpoint}`);
  
  // Add query parameters if provided
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        if (Array.isArray(value)) {
          value.forEach(v => url.searchParams.append(key, v));
        } else {
          url.searchParams.append(key, value);
        }
      }
    });
  }
  
  return url.toString();
};

// Default headers for all requests
const defaultHeaders = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Cache-Control': 'no-cache, no-store, must-revalidate',
  'Pragma': 'no-cache',
  'Expires': '0'
};

/**
 * Generic API fetch wrapper with error handling
 */
export const apiFetch = async (endpoint, options = {}) => {
  const { params = {}, ...fetchOptions } = options;
  const url = createUrl(endpoint, params);
  
  const requestOptions = {
    ...fetchOptions,
    credentials: 'same-origin',
    mode: 'cors',
    headers: {
      ...defaultHeaders,
      ...(fetchOptions.headers || {})
    },
    cache: 'no-store'
  };

  try {
    const response = await fetch(url, requestOptions);
    
    // Handle empty responses (204 No Content)
    if (response.status === 204) {
      return null;
    }
    
    // Get content type
    const contentType = response.headers.get('content-type');
    
    // Parse response based on content type
    if (contentType && contentType.includes('application/json')) {
      const data = await response.json();
      
      if (!response.ok) {
        const error = new Error(data.message || `HTTP error! status: ${response.status}`);
        error.status = response.status;
        error.data = data;
        throw error;
      }
      
      return data;
    }
    
    // For non-JSON responses
    const text = await response.text();
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return text;
  } catch (error) {
    console.error(`API request failed for ${url}:`, error);
    
    // Handle CORS and network errors specifically
    if (error instanceof TypeError) {
      if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        console.error('Network error detected. Please check:');
        console.error('1. Is the backend server running?');
        console.error('2. Is the API URL correct?', API_BASE);
        throw new Error('Unable to connect to the server. Please check your connection and try again.');
      }
      
      if (error.message.includes('CORS')) {
        console.error('CORS error detected. Please check:');
        console.error('1. Are CORS headers properly configured on the backend?');
        console.error('2. Is the frontend making requests to the correct origin?');
        throw new Error('Request was blocked due to CORS policy. Please contact support if the issue persists.');
      }
    }
    
    // Re-throw the original error if it's not a network/CORS error
    throw error;
  }
};

// Helper functions for specific endpoints
export const fetchProfile = async () => {
  return apiFetch('/profile');
};

/**
 * Fetch projects with optional skill filter
 * @param {string} [skill] - Optional skill to filter projects
 * @returns {Promise<Array>} Array of projects
 */
export const fetchProjects = async (skill = null) => {
  const params = {};
  if (skill) params.skill = skill;
  
  const data = await apiFetch('/projects', { params });
  return Array.isArray(data) ? data : [];
};

// Alias for backward compatibility
export const fetchPythonProjects = () => fetchProjects('python');

/**
 * Check API health status
 * @returns {Promise<Object>} Health status object
 */
export const checkApiHealth = async () => {
  try {
    const response = await apiFetch('/health');
    return {
      status: 'ok',
      version: response.version || 'unknown',
      timestamp: new Date().toISOString(),
      ...response
    };
  } catch (error) {
    console.error('Health check failed:', error);
    return {
      status: 'error',
      error: error.message,
      timestamp: new Date().toISOString()
    };
  }
};

/**
 * Search for projects or profiles
 * @param {string} query - Search query
 * @returns {Promise<Array>} Search results
 */
export const search = async (query) => {
  if (!query || typeof query !== 'string' || query.trim() === '') {
    return [];
  }
  
  try {
    const data = await apiFetch(`/search`, { params: { q: query.trim() } });
    
    // Handle different response formats
    const results = [];
    
    // Handle case where data is an array (direct projects response)
    if (Array.isArray(data)) {
      return data.map(item => ({
        ...item,
        type: 'Project',
        name: item.title || item.name || 'Untitled Project'
      }));
    }
    
    // Handle object with projects and skills
    if (data.projects && Array.isArray(data.projects)) {
      results.push(...data.projects.map(project => ({
        ...project,
        type: 'Project',
        name: project.title || project.name || 'Untitled Project'
      })));
    }
    
    if (data.skills && Array.isArray(data.skills)) {
      results.push(...data.skills.map(skill => ({
        ...skill,
        type: 'Skill',
        name: skill.name || 'Unnamed Skill'
      })));
    }
    
    return results;
  } catch (error) {
    console.error('Search error:', error);
    return []; // Return empty array on error to prevent UI breakage
  }
};

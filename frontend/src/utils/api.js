// API Configuration
import { API_BASE } from '@/config/api';

// Base API path
const API_BASE_URL = API_BASE.endsWith('/') ? API_BASE : `${API_BASE}/`;
const API_VERSION = 'api/v1';

/**
 * Helper function to create a properly formatted URL with query parameters
 * @param {string} endpoint - The API endpoint (e.g., 'profile', 'projects')
 * @param {Object} [params={}] - Optional query parameters
 * @returns {string} Fully formatted URL
 */
const createUrl = (endpoint, params = {}) => {
  // Remove leading/trailing slashes from endpoint
  const cleanEndpoint = endpoint.replace(/^\/+|\/+$/g, '');
  
  // Create URL object with the base URL and version
  const baseUrl = new URL(API_BASE_URL);
  const pathSegments = [baseUrl.pathname.replace(/\/+$/, ''), API_VERSION, cleanEndpoint].filter(Boolean);
  const url = new URL(pathSegments.join('/'), baseUrl.origin);
  
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
 * Generic API fetch wrapper with error handling and automatic retry
 * @param {string} endpoint - The API endpoint
 * @param {Object} [options={}] - Fetch options
 * @param {Object} [options.params={}] - Query parameters
 * @param {number} [retries=2] - Number of retry attempts
 * @returns {Promise<*>} The API response data
 */
const apiFetch = async (endpoint, { params = {}, retries = 2, ...fetchOptions } = {}) => {
  const url = createUrl(endpoint, params);
  
  const requestOptions = {
    method: 'GET',
    headers: {
      ...defaultHeaders,
      ...(fetchOptions.headers || {})
    },
    ...fetchOptions
  };

  try {
    const response = await fetch(url, requestOptions);
    
    // Handle empty responses (204 No Content)
    if (response.status === 204) {
      return null;
    }
    
    const data = await response.json().catch(() => ({}));
    
    // Handle rate limiting (429) with retry
    if (response.status === 429 && retries > 0) {
      const retryAfter = response.headers.get('Retry-After') || 1;
      await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
      return apiFetch(endpoint, { params, retries: retries - 1, ...fetchOptions });
    }
    
    // Check for error responses
    if (!response.ok) {
      const error = new Error(data.detail || response.statusText || 'Request failed');
      error.status = response.status;
      error.data = data;
      throw error;
    }
    
    return data;
  } catch (error) {
    console.error(`API request to ${endpoint} failed:`, error);
    throw error;
  }
};

/**
 * Fetches the user's profile
 * @returns {Promise<Object>} User profile data
 */
export const fetchProfile = async () => {
  return apiFetch('profile');
};

/**
 * Fetches projects with optional skill filter
 * @param {string} [skill] - Optional skill to filter projects
 * @returns {Promise<Array>} Array of projects
 */
export const fetchProjects = async (skill = null) => {
  const params = {};
  if (skill) params.skill = skill;
  
  const data = await apiFetch('projects', { params });
  return Array.isArray(data) ? data : [];
};

/**
 * Fetches a specific project by ID
 * @param {string} projectId - The ID of the project to fetch
 * @returns {Promise<Object>} Project data
 */
export const fetchProjectById = async (projectId) => {
  if (!projectId) throw new Error('Project ID is required');
  return apiFetch(`projects/${projectId}`);
};

/**
 * Fetches Python projects (alias for fetchProjects with 'python' filter)
 * @returns {Promise<Array>} Array of Python projects
 */
export const fetchPythonProjects = () => fetchProjects('python');

/**
 * Checks the health status of the API
 * @returns {Promise<Object>} Health status information
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
      timestamp: new Date().toISOString(),
      statusCode: error.status
    };
  }
};

/**
 * Searches for projects and profiles
 * @param {string} query - Search query
 * @returns {Promise<Array>} Search results
 */
export const search = async (query) => {
  if (!query || typeof query !== 'string' || query.trim() === '') {
    return [];
  }
  
  try {
    const data = await apiFetch('/search', { 
      params: { 
        q: query.trim(),
        limit: 50 // Limit results to prevent performance issues
      } 
    });
    
    // Handle different response formats
    const results = [];
    
    // Handle case where data is an array (direct projects response)
    if (Array.isArray(data)) {
      return data.map(item => ({
        ...item,
        type: 'Project',
        name: item.title || item.name || 'Untitled Project',
        _score: item._score || 1.0
      }));
    }
    
    // Handle case where data is an object with projects and/or profiles
    if (data.projects) {
      results.push(...data.projects.map(project => ({
        ...project,
        type: 'Project',
        name: project.title || project.name || 'Untitled Project',
        _score: project._score || 1.0
      })));
    }
    
    if (data.profiles) {
      results.push(...data.profiles.map(profile => ({
        ...profile,
        type: 'Profile',
        name: profile.name || 'Unnamed Profile',
        _score: profile._score || 1.0
      })));
    }
    
    // If no results but we have a direct response, use that
    if (results.length === 0 && data && typeof data === 'object') {
      results.push({
        ...data,
        type: data.type || 'Result',
        name: data.title || data.name || 'Untitled',
        _score: data._score || 1.0
      });
    }
    
    // Sort by score if available
    return results.sort((a, b) => (b._score || 0) - (a._score || 0));
  } catch (error) {
    console.error('Search error:', error);
    // Return empty array on error to prevent UI breakage
    return []; 
  }
};

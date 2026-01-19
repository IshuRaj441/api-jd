// Use environment variable with fallback to production URL
const API_BASE = import.meta.env.VITE_API_BASE_URL || 'https://api-jd.onrender.com';

// Helper function to create full URL
const createUrl = (endpoint) => {
  // Ensure endpoint starts with a slash
  const path = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  return `${API_BASE}${path}`;
};

export const apiFetch = async (endpoint, options = {}) => {
  const url = createUrl(endpoint);
  
  const defaultOptions = {
    credentials: 'include', // Include cookies in CORS requests
    mode: 'cors', // Enable CORS mode
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'Pragma': 'no-cache',
      'Expires': '0',
      ...options.headers,
    },
    cache: 'no-store',
    ...options,
  };

  try {
    const response = await fetch(url, defaultOptions);
    
    // Handle non-2xx responses
    if (!response.ok) {
      let errorData;
      try {
        errorData = await response.json();
      } catch (e) {
        errorData = await response.text();
      }
      
      const error = new Error(
        errorData?.message || `HTTP error! status: ${response.status}`
      );
      error.status = response.status;
      error.data = errorData;
      throw error;
    }

    // Handle empty responses
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return response.json();
    }
    return response.text();
  } catch (error) {
    console.error(`API request failed for ${url}:`, error);
    
    // Handle CORS errors specifically
    if (error instanceof TypeError) {
      if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        throw new Error('Network error: Unable to connect to the server. Please check your connection.');
      }
      if (error.message.includes('CORS')) {
        throw new Error('CORS error: The request was blocked due to CORS policy. Please contact support.');
      }
    }
    
    throw error;
  }
};

// Helper functions for specific endpoints
export const fetchProfile = async () => {
  const data = await apiFetch('/profile');
  // Handle case where profile might be an array
  return Array.isArray(data) ? data[0] : data;
};

export const fetchPythonProjects = async () => {
  try {
    const data = await apiFetch('/projects?skill=python');
    // Handle both array and object with projects property
    if (Array.isArray(data)) {
      return data;
    } else if (data && Array.isArray(data.projects)) {
      return data.projects;
    }
    return [];
  } catch (error) {
    console.error('Error fetching Python projects:', error);
    throw error; // Re-throw to be handled by the component
  }
};

export const search = async (query) => {
  try {
    if (!query || typeof query !== 'string' || !query.trim()) {
      return [];
    }
    
    const data = await apiFetch(`/search?q=${encodeURIComponent(query.trim())}`);
    
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
    throw error; // Re-throw to be handled by the component
  }
};

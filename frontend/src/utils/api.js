const API_BASE = 'https://me-api-playground.onrender.com';

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

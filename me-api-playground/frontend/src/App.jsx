import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Use Vite's environment variable for the API URL
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create an axios instance with the base URL
const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

function App() {
  const [profile, setProfile] = useState(null);
  const [projects, setProjects] = useState([]);
  const [searchResults, setSearchResults] = useState(null);
  const [searchQuery, setSearchQuery] = useState('test');
  const [loading, setLoading] = useState({
    profile: true,
    projects: true,
    search: false
  });
  const [error, setError] = useState(null);

  // Fetch profile data
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await api.get('/profile');
        setProfile(response.data);
        setLoading(prev => ({ ...prev, profile: false }));
      } catch (err) {
        setError('Failed to fetch profile');
        setLoading(prev => ({ ...prev, profile: false }));
      }
    };

    fetchProfile();
  }, []);

  // Fetch projects with Python skill
  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await api.get('/projects?skill=python');
        setProjects(response.data);
        setLoading(prev => ({ ...prev, projects: false }));
      } catch (err) {
        setError('Failed to fetch projects');
        setLoading(prev => ({ ...prev, projects: false }));
      }
    };

    fetchProjects();
  }, []);

  // Handle search
  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    
    setLoading(prev => ({ ...prev, search: true }));
    try {
      const response = await api.get(`/search?q=${encodeURIComponent(searchQuery)}`);
      setSearchResults(response.data);
    } catch (err) {
      setError('Search failed');
    } finally {
      setLoading(prev => ({ ...prev, search: false }));
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Portfolio API Frontend</h1>
      
      {error && <div style={{ color: 'red' }}>{error}</div>}
      
      <section>
        <h2>Profile</h2>
        {loading.profile ? (
          <div>Loading profile...</div>
        ) : profile ? (
          <div>
            <p><strong>Name:</strong> {profile.name}</p>
            <p><strong>Email:</strong> {profile.email}</p>
          </div>
        ) : (
          <div>No profile data available</div>
        )}
      </section>

      <section style={{ marginTop: '30px' }}>
        <h2>Projects (Python)</h2>
        {loading.projects ? (
          <div>Loading projects...</div>
        ) : projects && projects.length > 0 ? (
          <ul>
            {projects.map((project) => (
              <li key={project.id} style={{ marginBottom: '15px' }}>
                <h3>{project.title}</h3>
                <p>{project.description}</p>
              </li>
            ))}
          </ul>
        ) : (
          <div>No projects found</div>
        )}
      </section>

      <section style={{ marginTop: '30px' }}>
        <h2>Search</h2>
        <form onSubmit={handleSearch}>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search..."
            style={{ padding: '5px', marginRight: '10px' }}
          />
          <button type="submit" disabled={loading.search}>
            {loading.search ? 'Searching...' : 'Search'}
          </button>
        </form>
        
        {loading.search ? (
          <div>Searching...</div>
        ) : searchResults ? (
          <div style={{ marginTop: '10px' }}>
            <h3>Search Results (raw JSON):</h3>
            <pre style={{ 
              background: '#f5f5f5', 
              padding: '10px', 
              borderRadius: '4px',
              maxHeight: '300px',
              overflow: 'auto'
            }}>
              {JSON.stringify(searchResults, null, 2)}
            </pre>
          </div>
        ) : null}
      </section>
    </div>
  );
}

export default App;

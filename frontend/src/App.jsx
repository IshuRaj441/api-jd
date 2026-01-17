import { useState, useEffect } from 'react';
import './App.css';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function App() {
  const [loading, setLoading] = useState({
    profile: true,
    pythonProjects: true,
    search: false
  });
  const [error, setError] = useState({
    profile: null,
    pythonProjects: null,
    search: null
  });
  const [profile, setProfile] = useState(null);
  const [pythonProjects, setPythonProjects] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [searchQuery, setSearchQuery] = useState('test');

  // Fetch profile data
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        setLoading(prev => ({ ...prev, profile: true }));
        const response = await fetch(`${API_BASE}/profile`);
        if (!response.ok) throw new Error('Failed to fetch profile');
        const data = await response.json();
        setProfile(data);
        setError(prev => ({ ...prev, profile: null }));
      } catch (err) {
        console.error('Profile fetch error:', err);
        setError(prev => ({ ...prev, profile: err.message }));
      } finally {
        setLoading(prev => ({ ...prev, profile: false }));
      }
    };

    fetchProfile();
  }, []);

  // Fetch Python projects
  useEffect(() => {
    const fetchPythonProjects = async () => {
      try {
        setLoading(prev => ({ ...prev, pythonProjects: true }));
        const response = await fetch(`${API_BASE}/projects?skill=python`);
        if (!response.ok) throw new Error('Failed to fetch Python projects');
        const data = await response.json();
        setPythonProjects(data);
        setError(prev => ({ ...prev, pythonProjects: null }));
      } catch (err) {
        console.error('Python projects fetch error:', err);
        setError(prev => ({ ...prev, pythonProjects: err.message }));
      } finally {
        setLoading(prev => ({ ...prev, pythonProjects: false }));
      }
    };

    fetchPythonProjects();
  }, []);

  // Handle search
  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    
    try {
      setLoading(prev => ({ ...prev, search: true }));
      const response = await fetch(`${API_BASE}/search?q=${encodeURIComponent(searchQuery)}`);
      if (!response.ok) throw new Error('Search failed');
      const data = await response.json();
      setSearchResults(data);
      setError(prev => ({ ...prev, search: null }));
    } catch (err) {
      console.error('Search error:', err);
      setError(prev => ({ ...prev, search: err.message }));
    } finally {
      setLoading(prev => ({ ...prev, search: false }));
    }
  };

  // Initial search on component mount
  useEffect(() => {
    const initialSearch = async () => {
      try {
        setLoading(prev => ({ ...prev, search: true }));
        const response = await fetch(`${API_BASE}/search?q=test`);
        if (!response.ok) throw new Error('Initial search failed');
        const data = await response.json();
        setSearchResults(data);
      } catch (err) {
        console.error('Initial search error:', err);
        setError(prev => ({ ...prev, search: err.message }));
      } finally {
        setLoading(prev => ({ ...prev, search: false }));
      }
    };

    initialSearch();
  }, []);

  // Render loading state
  if (loading.profile && loading.pythonProjects) {
    return <div style={{ padding: '20px' }}>Loading application data...</div>;
  }

  // Render error state if both profile and projects fail to load
  if ((error.profile && error.pythonProjects) || (!profile && !pythonProjects.length)) {
    return (
      <div style={{ padding: '20px', color: 'red' }}>
        <h2>Error Loading Data</h2>
        {error.profile && <p>Profile: {error.profile}</p>}
        {error.pythonProjects && <p>Projects: {error.pythonProjects}</p>}
        <p>Please check your connection and try again.</p>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>{profile?.name || 'Me-API Playground'}</h1>
      
      {/* Profile Section */}
      <section style={{ marginBottom: '40px' }}>
        <h2>Profile</h2>
        {loading.profile ? (
          <p>Loading profile...</p>
        ) : error.profile ? (
          <p style={{ color: 'red' }}>Error loading profile: {error.profile}</p>
        ) : profile ? (
          <div>
            <h3>{profile.name}</h3>
            <p>{profile.title}</p>
            <p>{profile.summary}</p>
          </div>
        ) : null}
      </section>

      {/* Python Projects Section */}
      <section style={{ marginBottom: '40px' }}>
        <h2>Python Projects</h2>
        {loading.pythonProjects ? (
          <p>Loading projects...</p>
        ) : error.pythonProjects ? (
          <p style={{ color: 'red' }}>Error loading projects: {error.pythonProjects}</p>
        ) : pythonProjects.length > 0 ? (
          <ul>
            {pythonProjects.map(project => (
              <li key={project.id} style={{ marginBottom: '10px' }}>
                <h4>{project.name}</h4>
                <p>{project.description}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>No Python projects found.</p>
        )}
      </section>

      {/* Search Section */}
      <section>
        <h2>Search</h2>
        <form onSubmit={handleSearch} style={{ marginBottom: '20px' }}>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search..."
            style={{ marginRight: '10px', padding: '5px' }}
          />
          <button type="submit" disabled={loading.search}>
            {loading.search ? 'Searching...' : 'Search'}
          </button>
        </form>
        
        {error.search && <p style={{ color: 'red' }}>Search error: {error.search}</p>}
        
        <h3>Search Results for "{searchQuery}"</h3>
        {loading.search ? (
          <p>Searching...</p>
        ) : searchResults.length > 0 ? (
          <ul>
            {searchResults.map((result, index) => (
              <li key={index} style={{ marginBottom: '10px' }}>
                <h4>{result.type}: {result.name || result.title}</h4>
                <p>{result.description || result.summary}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>No results found for "{searchQuery}"</p>
        )}
      </section>
    </div>
  );
}

export default App;

import { useEffect, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function App() {
  const [health, setHealth] = useState("checking...");
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState("");
  const [projects, setProjects] = useState([]);
  const [skill, setSkill] = useState("python");
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState(null);

  // Health check
  useEffect(() => {
    fetch(`${API_BASE}/health`)
      .then((res) => (res.ok ? "OK" : "ERROR"))
      .then(setHealth)
      .catch(() => setHealth("ERROR"));
  }, []);

  // Load profile
  useEffect(() => {
    fetch(`${API_BASE}/profile`)
      .then((res) => res.json())
      .then(setProfile)
      .catch(() => setError("Failed to load profile"));
  }, []);

  // Load projects when skill changes
  useEffect(() => {
    fetch(`${API_BASE}/projects?skill=${encodeURIComponent(skill)}`)
      .then((res) => res.json())
      .then(setProjects)
      .catch(() => setError("Failed to load projects"));
  }, [skill]);

  const runSearch = () => {
    if (!searchQuery.trim()) return;
    
    fetch(`${API_BASE}/search?q=${encodeURIComponent(searchQuery)}`)
      .then((res) => res.json())
      .then(setSearchResults)
      .catch(() => setError("Search failed"));
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Me-API Playground</h1>

      <p><strong>Backend health:</strong> {health}</p>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <h2>Profile</h2>
      {profile ? (
        <div>
          <p><b>Name:</b> {profile.name || 'N/A'}</p>
          <p><b>Email:</b> {profile.email || 'N/A'}</p>
          <p><b>Education:</b> {profile.education || 'N/A'}</p>
        </div>
      ) : (
        <p>Loading profile…</p>
      )}

      <h2>Projects</h2>
      <div>
        <label>
          Filter by skill:
          <input 
            type="text" 
            value={skill} 
            onChange={(e) => setSkill(e.target.value)}
            style={{ marginLeft: '10px' }}
          />
        </label>
      </div>
      {projects.length > 0 ? (
        <ul>
          {projects.map((project) => (
            <li key={project.id}>
              <h3>{project.title}</h3>
              <p>{project.description}</p>
              <p><i>Skills: {project.skills?.join(', ') || 'N/A'}</i></p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No projects found for this skill.</p>
      )}

      <h2>Search</h2>
      <div>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search term..."
          style={{ marginRight: '10px' }}
        />
        <button onClick={runSearch}>Search</button>
      </div>
      {searchResults && (
        <div>
          <h3>Search Results:</h3>
          <pre style={{ 
            background: '#f5f5f5', 
            padding: '1rem', 
            borderRadius: '4px',
            maxHeight: '300px',
            overflow: 'auto'
          }}>
            {JSON.stringify(searchResults, null, 2)}
          </pre>
        </div>
      )}
    </div>
  )
}

export default App

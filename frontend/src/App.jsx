import { useState, useEffect } from 'react';
import './App.css';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function App() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [profile, setProfile] = useState(null);
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch profile
        const profileResponse = await fetch(`${API_BASE_URL}/profile`);
        if (!profileResponse.ok) throw new Error('Failed to fetch profile');
        const profileData = await profileResponse.json();
        setProfile(profileData);
        
        // Fetch projects
        const projectsResponse = await fetch(`${API_BASE_URL}/projects`);
        if (!projectsResponse.ok) throw new Error('Failed to fetch projects');
        const projectsData = await projectsResponse.json();
        setProjects(projectsData);
        
      } catch (err) {
        console.error('Error fetching data:', err);
        setError(err.message || 'An error occurred while fetching data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (error) {
    return <div className="error" style={{ color: 'red' }}>Error: {error}</div>;
  }

  return (
    <div className="app">
      <header>
        <h1>{profile?.name || 'My Portfolio'}</h1>
        <p>{profile?.title || 'Software Developer'}</p>
      </header>
      
      <section className="projects">
        <h2>Projects</h2>
        {projects.length === 0 ? (
          <p>No projects found</p>
        ) : (
          <div className="project-list">
            {projects.map(project => (
              <div key={project.id} className="project-card">
                <h3>{project.name}</h3>
                <p>{project.description}</p>
                <div className="skills">
                  {project.skills?.map(skill => (
                    <span key={skill} className="skill-tag">{skill}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  )
}

export default App

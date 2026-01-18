import { useState, useEffect } from 'react';
import './App.css';
import { fetchProfile, fetchPythonProjects, search } from './utils/api';

// Loading spinner component
const LoadingSpinner = ({ size = 24 }) => (
  <div style={{
    display: 'inline-block',
    width: size,
    height: size,
    border: `3px solid rgba(0, 0, 0, 0.1)`,
    borderRadius: '50%',
    borderTopColor: '#1e88e5',
    animation: 'spin 1s ease-in-out infinite',
    margin: '0 auto',
    '@keyframes spin': {
      to: { transform: 'rotate(360deg)' }
    }
  }} />
);

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
  const [searchQuery, setSearchQuery] = useState('');

  // Fetch profile data
  useEffect(() => {
    const loadProfile = async () => {
      try {
        setLoading(prev => ({ ...prev, profile: true }));
        const data = await fetchProfile();
        setProfile(data);
        setError(prev => ({ ...prev, profile: null }));
      } catch (err) {
        console.error('Profile fetch error:', err);
        setError(prev => ({ ...prev, profile: 'Failed to load profile. Please try again later.' }));
      } finally {
        setLoading(prev => ({ ...prev, profile: false }));
      }
    };

    loadProfile();
  }, []);

  // Fetch Python projects
  useEffect(() => {
    const loadPythonProjects = async () => {
      try {
        setLoading(prev => ({ ...prev, pythonProjects: true }));
        const data = await fetchPythonProjects();
        setPythonProjects(Array.isArray(data) ? data : []);
        setError(prev => ({ ...prev, pythonProjects: null }));
      } catch (err) {
        console.error('Python projects fetch error:', err);
        setError(prev => ({ ...prev, pythonProjects: 'Failed to load projects. Please try again later.' }));
      } finally {
        setLoading(prev => ({ ...prev, pythonProjects: false }));
      }
    };

    loadPythonProjects();
  }, []);

  // Handle search
  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      setSearchResults([]);
      return;
    }
    
    try {
      setLoading(prev => ({ ...prev, search: true }));
      const data = await search(searchQuery);
      setSearchResults(Array.isArray(data) ? data : []);
      setError(prev => ({ ...prev, search: null }));
    } catch (err) {
      console.error('Search error:', err);
      setError(prev => ({ ...prev, search: 'Search failed. Please try again.' }));
      setSearchResults([]);
    } finally {
      setLoading(prev => ({ ...prev, search: false }));
    }
  };

  // Initial search on component mount
  useEffect(() => {
    const initialSearch = async () => {
      if (!searchQuery.trim()) return;
      
      try {
        setLoading(prev => ({ ...prev, search: true }));
        const data = await search(searchQuery);
        setSearchResults(Array.isArray(data) ? data : []);
      } catch (err) {
        console.error('Initial search error:', err);
        setError(prev => ({ ...prev, search: 'Initial search failed.' }));
      } finally {
        setLoading(prev => ({ ...prev, search: false }));
      }
    };

    initialSearch();
  }, []);

  // Render loading state
  if (loading.profile && loading.pythonProjects) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        flexDirection: 'column',
        gap: '20px'
      }}>
        <LoadingSpinner size={40} />
        <h2>Loading application data...</h2>
      </div>
    );
  }

  // Render error state if both profile and projects fail to load
  if ((error.profile && error.pythonProjects) || (!profile && !pythonProjects.length)) {
    return (
      <div style={{ 
        maxWidth: '800px', 
        margin: '40px auto', 
        padding: '30px',
        backgroundColor: '#fff8f8',
        borderRadius: '8px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
        textAlign: 'center'
      }}>
        <h2 style={{ color: '#d32f2f', marginBottom: '20px' }}>Error Loading Data</h2>
        <div style={{ 
          backgroundColor: '#ffebee', 
          padding: '15px', 
          borderRadius: '6px',
          marginBottom: '20px',
          textAlign: 'left'
        }}>
          {error.profile && <p style={{ margin: '5px 0' }}>• Profile: {error.profile}</p>}
          {error.pythonProjects && <p style={{ margin: '5px 0' }}>• Projects: {error.pythonProjects}</p>}
        </div>
        <p style={{ color: '#555' }}>Please check your connection and try again.</p>
        <button 
          onClick={() => window.location.reload()}
          style={{
            marginTop: '20px',
            padding: '10px 20px',
            backgroundColor: '#1e88e5',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '16px',
            transition: 'background-color 0.2s'
          }}
          onMouseOver={e => e.target.style.backgroundColor = '#1565c0'}
          onMouseOut={e => e.target.style.backgroundColor = '#1e88e5'}
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div style={{ 
      maxWidth: '1000px', 
      margin: '0 auto', 
      padding: '20px',
      fontFamily: '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
      lineHeight: 1.6,
      color: '#333'
    }}>
      <header style={{ 
        marginBottom: '40px',
        paddingBottom: '20px',
        borderBottom: '1px solid #eaeaea'
      }}>
        <h1 style={{ 
          color: '#1a237e',
          margin: '0 0 10px 0',
          fontSize: '2.5em'
        }}>
          {profile?.name || 'Me-API Playground'}
        </h1>
        {profile?.title && (
          <p style={{
            color: '#555',
            fontSize: '1.2em',
            margin: '0 0 10px 0'
          }}>
            {profile.title}
          </p>
        )}
      </header>
      
      {/* Profile Section */}
      <section style={{ 
        marginBottom: '50px',
        backgroundColor: '#f8f9fa',
        padding: '25px',
        borderRadius: '8px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.05)'
      }}>
        <h2 style={{
          color: '#1a237e',
          borderBottom: '2px solid #e0e0e0',
          paddingBottom: '10px',
          marginTop: 0
        }}>
          Profile
        </h2>
        
        {loading.profile ? (
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <LoadingSpinner size={30} />
            <p>Loading profile information...</p>
          </div>
        ) : error.profile ? (
          <div style={{
            backgroundColor: '#ffebee',
            color: '#c62828',
            padding: '15px',
            borderRadius: '4px',
            borderLeft: '4px solid #f44336'
          }}>
            <p style={{ margin: 0 }}>Error loading profile: {error.profile}</p>
          </div>
        ) : profile ? (
          <div style={{ display: 'flex', gap: '30px', flexWrap: 'wrap' }}>
            {profile.avatar && (
              <div style={{ flex: '0 0 150px' }}>
                <img 
                  src={profile.avatar} 
                  alt={profile.name}
                  style={{
                    width: '100%',
                    borderRadius: '8px',
                    boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
                  }}
                />
              </div>
            )}
            <div style={{ flex: '1', minWidth: '250px' }}>
              <h3 style={{ marginTop: 0, color: '#283593' }}>{profile.name}</h3>
              {profile.summary && (
                <p style={{ 
                  color: '#424242',
                  marginBottom: '15px',
                  fontSize: '1.1em',
                  lineHeight: 1.6
                }}>
                  {profile.summary}
                </p>
              )}
              
              <div style={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: '15px',
                marginTop: '20px'
              }}>
                {profile.email && (
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    backgroundColor: '#e3f2fd',
                    padding: '8px 15px',
                    borderRadius: '20px',
                    fontSize: '0.9em'
                  }}>
                    <span>📧</span>
                    <a 
                      href={`mailto:${profile.email}`}
                      style={{
                        color: '#1565c0',
                        textDecoration: 'none',
                        wordBreak: 'break-all'
                      }}
                    >
                      {profile.email}
                    </a>
                  </div>
                )}
                
                {profile.website && (
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    backgroundColor: '#e8f5e9',
                    padding: '8px 15px',
                    borderRadius: '20px',
                    fontSize: '0.9em'
                  }}>
                    <span>🌐</span>
                    <a 
                      href={profile.website.startsWith('http') ? profile.website : `https://${profile.website}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        color: '#2e7d32',
                        textDecoration: 'none',
                        wordBreak: 'break-all'
                      }}
                    >
                      {profile.website.replace(/^https?:\/\//, '')}
                    </a>
                  </div>
                )}
              </div>
              
              {profile.socials && Object.keys(profile.socials).length > 0 && (
                <div style={{ marginTop: '20px' }}>
                  <h4 style={{ margin: '15px 0 10px 0', color: '#455a64' }}>Connect</h4>
                  <div style={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    gap: '10px'
                  }}>
                    {Object.entries(profile.socials).map(([platform, url]) => (
                      <a
                        key={platform}
                        href={url}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{
                          backgroundColor: '#f5f5f5',
                          color: '#333',
                          padding: '6px 12px',
                          borderRadius: '4px',
                          textDecoration: 'none',
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '6px',
                          fontSize: '0.9em',
                          transition: 'all 0.2s',
                          ':hover': {
                            backgroundColor: '#e0e0e0',
                            transform: 'translateY(-2px)'
                          }
                        }}
                      >
                        {platform === 'github' && '🐙'}
                        {platform === 'linkedin' && '💼'}
                        {platform === 'twitter' && '🐦'}
                        {!['github', 'linkedin', 'twitter'].includes(platform) && '🔗'}
                        {platform.charAt(0).toUpperCase() + platform.slice(1)}
                      </a>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div style={{
            backgroundColor: '#fff8e1',
            padding: '20px',
            borderRadius: '4px',
            textAlign: 'center',
            color: '#e65100'
          }}>
            <p style={{ margin: 0 }}>No profile information available.</p>
          </div>
        )}
      </section>

      {/* Python Projects Section */}
      <section style={{ 
        marginBottom: '50px',
        backgroundColor: '#f8f9fa',
        padding: '25px',
        borderRadius: '8px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.05)'
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '20px',
          flexWrap: 'wrap',
          gap: '15px'
        }}>
          <h2 style={{
            color: '#1a237e',
            borderBottom: '2px solid #e0e0e0',
            paddingBottom: '10px',
            margin: 0,
            flex: '1',
            minWidth: '200px'
          }}>
            Python Projects
          </h2>
          <div style={{
            fontSize: '0.9em',
            color: '#555',
            backgroundColor: '#e8eaf6',
            padding: '5px 12px',
            borderRadius: '12px',
            fontWeight: 500
          }}>
            {loading.pythonProjects ? '...' : pythonProjects.length} Projects
          </div>
        </div>
        
        {loading.pythonProjects ? (
          <div style={{ 
            textAlign: 'center', 
            padding: '40px 20px',
            backgroundColor: 'rgba(255, 255, 255, 0.7)',
            borderRadius: '8px'
          }}>
            <LoadingSpinner size={40} />
            <p style={{ marginTop: '15px', color: '#555' }}>Loading projects...</p>
          </div>
        ) : error.pythonProjects ? (
          <div style={{
            backgroundColor: '#ffebee',
            color: '#c62828',
            padding: '15px',
            borderRadius: '4px',
            borderLeft: '4px solid #f44336',
            marginBottom: '20px'
          }}>
            <p style={{ margin: 0 }}>Error loading projects: {error.pythonProjects}</p>
          </div>
        ) : (
          <div style={{
            textAlign: 'center',
            padding: '40px 20px',
            backgroundColor: 'white',
            borderRadius: '8px',
            border: '1px dashed #e0e0e0'
          }}>
            <div style={{ fontSize: '48px', marginBottom: '15px' }}>🐍</div>
            <h3 style={{ margin: '0 0 10px 0', color: '#333' }}>No Python projects found in your portfolio.</h3>
            <p style={{ color: '#666', margin: 0 }}>Start by adding your Python projects to showcase them here.</p>
          </div>
        )}
      </section>

      {/* Search Section */}
      <section style={{
        backgroundColor: '#f8f9fa',
        padding: '25px',
        borderRadius: '8px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.05)'
      }}>
        <h2 style={{
          color: '#1a237e',
          borderBottom: '2px solid #e0e0e0',
          paddingBottom: '10px',
          marginTop: 0
        }}>
          Search Projects & Skills
        </h2>
        
        <form 
          onSubmit={handleSearch} 
          style={{ 
            marginBottom: '25px',
            display: 'flex',
            gap: '12px',
            flexWrap: 'wrap',
            alignItems: 'center'
          }}
        >
          <div style={{ 
            flex: '1',
            minWidth: '250px',
            position: 'relative',
            maxWidth: '600px'
          }}>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search projects, skills, or technologies..."
              style={{ 
                width: '100%',
                padding: '12px 15px',
                paddingRight: '45px',
                border: '1px solid #ddd',
                borderRadius: '6px',
                fontSize: '16px',
                transition: 'border-color 0.2s, box-shadow 0.2s',
                ':focus': {
                  outline: 'none',
                  borderColor: '#1e88e5',
                  boxShadow: '0 0 0 3px rgba(30, 136, 229, 0.2)'
                }
              }}
              aria-label="Search projects and skills"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => {
                  setSearchQuery('');
                  setSearchResults([]);
                }}
                style={{
                  position: 'absolute',
                  right: '10px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  background: 'none',
                  border: 'none',
                  color: '#999',
                  cursor: 'pointer',
                  fontSize: '18px',
                  padding: '0',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  width: '24px',
                  height: '24px',
                  borderRadius: '50%',
                  transition: 'background-color 0.2s',
                  ':hover': {
                    backgroundColor: 'rgba(0, 0, 0, 0.05)'
                  }
                }}
                aria-label="Clear search"
              >
                ×
              </button>
            )}
          </div>
          
          <button 
            type="submit" 
            disabled={loading.search}
            style={{
              padding: '12px 24px',
              backgroundColor: '#1e88e5',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              fontSize: '16px',
              fontWeight: 500,
              display: 'inline-flex',
              alignItems: 'center',
              gap: '8px',
              transition: 'background-color 0.2s, transform 0.1s',
              ':hover:not(:disabled)': {
                backgroundColor: '#1565c0'
              },
              ':active:not(:disabled)': {
                transform: 'translateY(1px)'
              },
              ':disabled': {
                opacity: 0.7,
                cursor: 'not-allowed'
              }
            }}
          >
            {loading.search ? (
              <>
                <LoadingSpinner size={18} />
                <span>Searching...</span>
              </>
            ) : (
              <>
                <span>🔍</span>
                <span>Search</span>
              </>
            )}
          </button>
        </form>
        
        {error.search && (
          <div style={{
            backgroundColor: '#ffebee',
            color: '#c62828',
            padding: '12px 16px',
            borderRadius: '6px',
            marginBottom: '20px',
            display: 'flex',
            alignItems: 'flex-start',
            gap: '10px',
            borderLeft: '4px solid #f44336'
          }}>
            <span style={{ fontSize: '18px' }}>⚠️</span>
            <div>
              <p style={{ margin: '0 0 5px 0', fontWeight: 500 }}>Search Error</p>
              <p style={{ margin: 0, fontSize: '0.95em' }}>{error.search}</p>
            </div>
          </div>
        )}
        
        <div style={{ marginTop: '30px' }}>
          <h3 style={{
            color: '#1a237e',
            margin: '0 0 15px 0',
            display: 'flex',
            alignItems: 'center',
            gap: '10px'
          }}>
            <span>Search Results</span>
            {searchQuery && (
              <span style={{
                backgroundColor: '#e3f2fd',
                color: '#1565c0',
                fontSize: '0.7em',
                padding: '2px 8px',
                borderRadius: '10px',
                fontWeight: 'normal'
              }}>
                "{searchQuery}"
              </span>
            )}
          </h3>
          
          {loading.search ? (
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              padding: '40px 20px',
              backgroundColor: 'rgba(255, 255, 255, 0.7)',
              borderRadius: '8px'
            }}>
              <LoadingSpinner size={40} />
              <p style={{ margin: '15px 0 0 0', color: '#555' }}>Searching for projects and skills...</p>
            </div>
          ) : searchResults.length > 0 ? (
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
              gap: '20px',
              marginTop: '15px'
            }}>
              {searchResults.map((result, index) => (
                <div 
                  key={`${result.type}-${result.id || index}`}
                  style={{
                    backgroundColor: 'white',
                    borderRadius: '8px',
                    overflow: 'hidden',
                    boxShadow: '0 2px 10px rgba(0,0,0,0.05)',
                    borderLeft: `4px solid ${
                      result.type === 'Skill' ? '#4caf50' : 
                      result.type === 'Project' ? '#2196f3' : '#9c27b0'
                    }`,
                    transition: 'transform 0.2s, box-shadow 0.2s',
                    ':hover': {
                      transform: 'translateY(-3px)',
                      boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
                    }
                  }}
                >
                  <div style={{ padding: '20px' }}>
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      marginBottom: '12px',
                      gap: '10px'
                    }}>
                      <span style={{
                        backgroundColor: 
                          result.type === 'Skill' ? '#e8f5e9' : 
                          result.type === 'Project' ? '#e3f2fd' : '#f3e5f5',
                        color: 
                          result.type === 'Skill' ? '#2e7d32' : 
                          result.type === 'Project' ? '#1565c0' : '#7b1fa2',
                        padding: '4px 10px',
                        borderRadius: '12px',
                        fontSize: '0.75em',
                        fontWeight: 600,
                        textTransform: 'uppercase',
                        letterSpacing: '0.5px'
                      }}>
                        {result.type}
                      </span>
                      
                      {result.date && (
                        <span style={{
                          color: '#757575',
                          fontSize: '0.85em',
                          backgroundColor: '#f5f5f5',
                          padding: '2px 8px',
                          borderRadius: '10px'
                        }}>
                          {new Date(result.date).getFullYear()}
                        </span>
                      )}
                    </div>
                    
                    <h4 style={{
                      margin: '0 0 10px 0',
                      color: '#1a237e',
                      fontSize: '1.1em',
                      lineHeight: 1.3
                    }}>
                      {result.name || result.title || 'Untitled'}
                    </h4>
                    
                    {(result.description || result.summary) && (
                      <p style={{
                        color: '#424242',
                        margin: '0 0 15px 0',
                        fontSize: '0.95em',
                        lineHeight: 1.5
                      }}>
                        {result.description || result.summary}
                      </p>
                    )}
                    
                    {result.type === 'Project' && result.skills && result.skills.length > 0 && (
                      <div style={{ marginTop: '15px' }}>
                        <div style={{
                          fontSize: '0.85em',
                          color: '#616161',
                          marginBottom: '8px',
                          fontWeight: 500
                        }}>
                          Skills Used:
                        </div>
                        <div style={{
                          display: 'flex',
                          flexWrap: 'wrap',
                          gap: '6px'
                        }}>
                          {result.skills.slice(0, 3).map((skill, i) => (
                            <span 
                              key={`${result.id}-skill-${i}`}
                              style={{
                                backgroundColor: '#e3f2fd',
                                color: '#1565c0',
                                padding: '2px 8px',
                                borderRadius: '10px',
                                fontSize: '0.75em',
                                fontWeight: 500,
                                whiteSpace: 'nowrap',
                                overflow: 'hidden',
                                textOverflow: 'ellipsis',
                                maxWidth: '100%',
                                display: 'inline-block'
                              }}
                              title={skill.name || skill}
                            >
                              {skill.name || skill}
                            </span>
                          ))}
                          {result.skills.length > 3 && (
                            <span style={{
                              backgroundColor: '#f5f5f5',
                              color: '#757575',
                              padding: '2px 8px',
                              borderRadius: '10px',
                              fontSize: '0.75em',
                              fontWeight: 500
                            }}>
                              +{result.skills.length - 3} more
                            </span>
                          )}
                        </div>
                      </div>
                    )}
                    
                    {result.links && (
                      <div style={{ marginTop: '15px' }}>
                        <a 
                          href={result.links} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          style={{
                            color: '#1e88e5',
                            textDecoration: 'none',
                            fontWeight: 500,
                            fontSize: '0.9em',
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '6px',
                            transition: 'color 0.2s',
                            ':hover': {
                              color: '#0d47a1',
                              textDecoration: 'underline'
                            }
                          }}
                        >
                          <span>View {result.type === 'Project' ? 'Project' : 'Details'}</span>
                          <span style={{ fontSize: '1.1em' }}>↗</span>
                        </a>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : searchQuery ? (
            <div style={{
              backgroundColor: '#fff8e1',
              padding: '25px',
              borderRadius: '8px',
              textAlign: 'center',
              borderLeft: '4px solid #ffc107',
              color: '#e65100',
              marginTop: '15px'
            }}>
              <p style={{ margin: '0 0 10px 0', fontWeight: 500 }}>No results found</p>
              <p style={{ margin: 0, fontSize: '0.95em' }}>
                We couldn't find any projects or skills matching "{searchQuery}". Try different keywords or check your spelling.
              </p>
            </div>
          ) : (
            <div style={{
              backgroundColor: '#e8f5e9',
              padding: '25px',
              borderRadius: '8px',
              textAlign: 'center',
              borderLeft: '4px solid #4caf50',
              color: '#1b5e20',
              marginTop: '15px'
            }}>
              <p style={{ margin: '0 0 10px 0', fontWeight: 500 }}>Search for projects and skills</p>
              <p style={{ margin: 0, fontSize: '0.95em' }}>
                Enter keywords in the search box above to find projects, skills, or technologies in your portfolio.
              </p>
            </div>
          )}
        </div>
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
              <li key={`${result.type}-${result.id || index}`} style={{ 
                marginBottom: '15px', 
                padding: '10px', 
                border: '1px solid #eee', 
                borderRadius: '4px' 
              }}>
                <h4>{result.type}: {result.name || result.title || 'Untitled'}</h4>
                <p>{result.description || result.summary || 'No description available'}</p>
                {result.type === 'Project' && result.skills && result.skills.length > 0 && (
                  <div>
                    <strong>Skills:</strong>{' '}
                    {result.skills.map(skill => typeof skill === 'object' ? skill.name : skill).join(', ')}
                  </div>
                )}
                {result.type === 'Project' && result.links && (
                  <div>
                    <strong>Links:</strong>{' '}
                    <a href={result.links} target="_blank" rel="noopener noreferrer">
                      {result.links}
                    </a>
                  </div>
                )}
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

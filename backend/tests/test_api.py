import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import Base, get_db
from app.main import app
from app.core.config import settings

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Test data
test_profile = {
    "name": "Test User",
    "title": "Software Developer",
    "about": "Test about section",
    "email": "test@example.com"
}

test_project = {
    "name": "Test Project",
    "description": "A test project",
    "skills": ["Python", "FastAPI"]
}

def setup_module(module):
    """Set up test data before tests run"""
    # Create a test profile
    response = client.post("/api/v1/profile/", json=test_profile)
    assert response.status_code == 200
    
    # Create a test project
    response = client.post("/api/v1/projects/", json=test_project)
    assert response.status_code == 200

def teardown_module(module):
    """Clean up after tests"""
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test.db"):
        os.remove("test.db")

def test_health():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_profile():
    """Test creating a profile"""
    response = client.post("/api/v1/profile/", json=test_profile)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_profile["name"]
    assert data["email"] == test_profile["email"]

def test_get_profile():
    """Test retrieving the profile"""
    response = client.get("/profile")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "email" in data

def test_update_profile():
    """Test updating the profile"""
    update_data = {"name": "Updated Name"}
    response = client.put("/api/v1/profile/", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"

def test_list_projects():
    """Test listing all projects"""
    response = client.get("/api/v1/projects/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_projects_filter():
    """Test filtering projects by skill"""
    response = client.get("/projects?skill=python")
    assert response.status_code == 200
    projects = response.json()
    assert isinstance(projects, list)
    if projects:
        assert "title" in projects[0]
        assert "description" in projects[0]

def test_get_top_skills():
    """Test getting top skills"""
    response = client.get("/api/v1/skills/top/")
    assert response.status_code == 200
    skills = response.json()
    assert isinstance(skills, list)
    if skills:  # If there are skills
        assert all("name" in skill and "count" in skill for skill in skills)

def test_search():
    """Test the search functionality"""
    response = client.get("/api/v1/search/?q=test")
    assert response.status_code == 200
    data = response.json()
    assert "projects" in data
    assert "skills" in data
    assert isinstance(data["projects"], list)
    assert isinstance(data["skills"], list)

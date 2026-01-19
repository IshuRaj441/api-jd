from typing import List, Dict, Optional
from datetime import datetime

# Sample projects data
SAMPLE_PROJECTS = [
    {
        "id": 1,
        "title": "API JD Platform",
        "description": "A professional API development platform",
        "skills": ["Python", "FastAPI", "React", "PostgreSQL"],
        "status": "active",
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": 2,
        "title": "E-commerce API",
        "description": "RESTful API for e-commerce platform",
        "skills": ["Node.js", "Express", "MongoDB"],
        "status": "completed",
        "created_at": "2023-11-15T00:00:00Z"
    }
]

async def get_projects(skill: Optional[str] = None) -> List[Dict]:
    """
    Get list of projects, optionally filtered by skill
    """
    if skill:
        # Filter projects by skill (case-insensitive)
        skill_lower = skill.lower()
        return [
            project for project in SAMPLE_PROJECTS
            if any(skill_lower in s.lower() for s in project["skills"])
        ]
    return SAMPLE_PROJECTS

async def get_project(project_id: int) -> Optional[Dict]:
    """
    Get a single project by ID
    """
    for project in SAMPLE_PROJECTS:
        if project["id"] == project_id:
            return project
    return None

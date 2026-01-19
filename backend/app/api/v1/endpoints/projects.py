from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from app.db.session import get_db
from app.schemas.project import ProjectResponse
from app.repositories.project import project_repo

router = APIRouter()

@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    skill: Optional[str] = Query(None, description="Filter projects by skill"),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """
    Get a list of projects, optionally filtered by skill.
    """
    try:
        # In a real app, you would query the database with the skill filter
        # For now, we'll return mock data
        projects = [
            {
                "id": 1,
                "title": "Project 1",
                "description": "A sample project",
                "skills": ["python", "fastapi"],
                "github_url": "https://github.com/example/project1",
                "demo_url": "https://example.com/project1"
            },
            {
                "id": 2,
                "title": "Project 2",
                "description": "Another sample project",
                "skills": ["react", "typescript"],
                "github_url": "https://github.com/example/project2",
                "demo_url": "https://example.com/project2"
            }
        ]
        
        if skill:
            skill_lower = skill.lower()
            projects = [
                p for p in projects 
                if any(skill_lower in s.lower() for s in p["skills"])
            ]
            
        return projects
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching projects: {str(e)}"
        )

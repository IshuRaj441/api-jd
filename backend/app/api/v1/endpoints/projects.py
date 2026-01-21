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
                "title": "E-Commerce API",
                "description": "A RESTful API for an e-commerce platform built with FastAPI and PostgreSQL",
                "skills": ["python", "fastapi", "postgresql", "sqlalchemy", "pydantic"],
                "github_url": "https://github.com/example/ecommerce-api",
                "demo_url": "https://api.example.com/ecommerce"
            },
            {
                "id": 2,
                "title": "Portfolio Website",
                "description": "A responsive portfolio website built with React and TypeScript",
                "skills": ["react", "typescript", "tailwindcss"],
                "github_url": "https://github.com/example/portfolio",
                "demo_url": "https://example.com"
            },
            {
                "id": 3,
                "title": "Data Analysis Tool",
                "description": "A Python tool for analyzing and visualizing data using pandas and matplotlib",
                "skills": ["python", "pandas", "matplotlib", "numpy", "jupyter"],
                "github_url": "https://github.com/example/data-analysis",
                "demo_url": "https://example.com/data-analysis"
            }
        ]
        
        if skill:
            skill_lower = skill.lower()
            projects = [
                p for p in projects 
                if any(skill_lower == s.lower() for s in p["skills"])
            ]
            
        return projects
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching projects: {str(e)}"
        )

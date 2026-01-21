from fastapi import APIRouter, Depends, HTTPException, Query, Body, Path, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from uuid import uuid4

from app.db.session import get_db
from app.schemas.project import ProjectResponse, ProjectCreate, ProjectUpdate
from app.repositories.project import project_repo

router = APIRouter()

# In-memory storage for demo purposes (replace with database in production)
projects_db = {}

class Project(BaseModel):
    id: str
    title: str
    description: str
    skills: List[str]
    github_url: Optional[HttpUrl] = None
    demo_url: Optional[HttpUrl] = None
    created_at: datetime
    updated_at: datetime

# Initialize with some sample data
if not projects_db:
    sample_projects = [
        {
            "id": str(uuid4()),
            "title": "E-Commerce API",
            "description": "A RESTful API for an e-commerce platform built with FastAPI and PostgreSQL",
            "skills": ["python", "fastapi", "postgresql", "sqlalchemy", "pydantic"],
            "github_url": "https://github.com/example/ecommerce-api",
            "demo_url": "https://api.example.com/ecommerce",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": str(uuid4()),
            "title": "Portfolio Website",
            "description": "A responsive portfolio website built with React and TypeScript",
            "skills": ["react", "typescript", "tailwindcss"],
            "github_url": "https://github.com/example/portfolio",
            "demo_url": "https://example.com",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": str(uuid4()),
            "title": "Data Analysis Tool",
            "description": "A Python tool for analyzing and visualizing data using pandas and matplotlib",
            "skills": ["python", "pandas", "matplotlib", "numpy", "jupyter"],
            "github_url": "https://github.com/example/data-analysis",
            "demo_url": "https://example.com/data-analysis",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    for project in sample_projects:
        projects_db[project["id"]] = project

@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    skill: Optional[str] = Query(None, description="Filter projects by skill"),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """
    Get a list of projects, optionally filtered by skill.
    
    - **skill**: Filter projects by skill (case-insensitive)
    - **skip**: Number of records to skip for pagination
    - **limit**: Maximum number of records to return (max 100)
    """
    try:
        projects = list(projects_db.values())
        
        if skill:
            skill_lower = skill.lower()
            projects = [
                p for p in projects 
                if any(skill_lower == s.lower() for s in p["skills"])
            ]
            
        # Apply pagination
        return projects[skip:skip + limit]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving projects: {str(e)}"
        )

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str = Path(..., description="The ID of the project to retrieve"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get a single project by ID.
    """
    if project_id not in projects_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    return projects_db[project_id]

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Create a new project.
    """
    try:
        project_id = str(uuid4())
        now = datetime.utcnow()
        
        project_data = project.dict()
        project_data.update({
            "id": project_id,
            "created_at": now,
            "updated_at": now
        })
        
        projects_db[project_id] = project_data
        return project_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating project: {str(e)}"
        )

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Update an existing project.
    """
    if project_id not in projects_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    
    try:
        update_data = project_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        # Update only the fields that were provided
        for field, value in update_data.items():
            if field in projects_db[project_id]:
                projects_db[project_id][field] = value
                
        return projects_db[project_id]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating project: {str(e)}"
        )

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a project.
    """
    if project_id not in projects_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    
    try:
        del projects_db[project_id]
        return None
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting project: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching projects: {str(e)}"
        )

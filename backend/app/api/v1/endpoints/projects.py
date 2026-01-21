from fastapi import APIRouter, HTTPException, Query, status, Path
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

router = APIRouter()

class Project(BaseModel):
    id: str
    title: str
    description: str
    skills: List[str]
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    created_at: str
    updated_at: str

# Sample projects data
sample_projects = [
    {
        "id": "1",
        "title": "Portfolio Website",
        "description": "A personal portfolio website built with React and FastAPI",
        "skills": ["react", "typescript", "fastapi", "python"],
        "github_url": "https://github.com/IshuRaj441/api-jd",
        "demo_url": "https://api-jd-ishuraj441.vercel.app/",
        "created_at": "2024-01-21T00:00:00",
        "updated_at": "2024-01-21T00:00:00"
    },
    {
        "id": "2",
        "title": "E-Commerce API",
        "description": "A RESTful API for an e-commerce platform",
        "skills": ["python", "fastapi", "postgresql"],
        "github_url": "https://github.com/IshuRaj441",
        "demo_url": "#",
        "created_at": "2024-01-21T00:00:00",
        "updated_at": "2024-01-21T00:00:00"
    },
    {
        "id": "3",
        "title": "Task Management App",
        "description": "A full-stack task management application",
        "skills": ["react", "nodejs", "mongodb"],
        "github_url": "https://github.com/IshuRaj441",
        "demo_url": "#",
        "created_at": "2024-01-21T00:00:00",
        "updated_at": "2024-01-21T00:00:00"
    }
]

projects_db = {project["id"]: project for project in sample_projects}

@router.get(
    "/",
    response_model=List[Project],
    summary="List all projects",
    description="Retrieve all projects, optionally filtered by skill.",
    responses={
        200: {"description": "List of projects"},
        500: {"description": "Internal server error"}
    }
)
async def get_projects(
    skill: Optional[str] = Query(None, description="Filter projects by skill")
):
    """
    Get a list of projects, optionally filtered by skill.
    
    - **skill**: Filter projects by skill (case-insensitive)
    """
    try:
        if skill:
            skill_lower = skill.lower()
            filtered_projects = [
                project for project in projects_db.values()
                if any(skill_lower in s.lower() for s in project["skills"])
            ]
            return filtered_projects
            
        return list(projects_db.values())
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving projects: {str(e)}"
        )

@router.get(
    "/{project_id}",
    response_model=Project,
    summary="Get project by ID",
    responses={
        200: {"description": "Project found"},
        404: {"description": "Project not found"}
    }
)
async def get_project(
    project_id: str = Path(..., description="The ID of the project to retrieve")
):
    """
    Get a single project by ID.
    """
    if project_id not in projects_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    return projects_db[project_id]

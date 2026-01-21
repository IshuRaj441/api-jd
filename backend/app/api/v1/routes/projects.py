from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.db.session import get_db
from app.crud.project import (
    get_project, get_projects, create_project, 
    update_project, delete_project
)
from app.schemas.project import Project, ProjectCreate, ProjectUpdate

router = APIRouter()
logger = logging.getLogger(__name__)

def project_matches_skill(project: Project, skill: str) -> bool:
    """Check if any of the project's skills match the given skill (case-insensitive)."""
    project_skills = project.skills or []
    return any(skill.lower() in s.lower() for s in project_skills)

@router.get("/", response_model=List[Project], summary="List all projects")
def read_projects(
    skip: int = Query(0, ge=0, description="Number of projects to skip"),
    limit: int = Query(100, le=100, description="Maximum number of projects to return"),
    featured: Optional[bool] = Query(None, description="Filter by featured status"),
    status: Optional[str] = Query(None, description="Filter by project status"),
    skill: Optional[str] = Query(None, description="Filter by skill"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of projects with optional filtering and pagination.
    
    - **skip**: Number of projects to skip (for pagination)
    - **limit**: Maximum number of projects to return (max 100)
    - **featured**: Filter by featured status (true/false)
    - **status**: Filter by project status (active/completed/archived)
    - **skill**: Filter by skill name (case-insensitive)
    """
    try:
        projects = get_projects(
            db=db,
            skip=skip,
            limit=limit,
            featured=featured,
            status=status
        )
        
        # Apply skill filter if provided
        if skill:
            projects = [p for p in projects if project_matches_skill(p, skill)]
            
        return projects
        
    except Exception as e:
        logger.error(f"Error fetching projects: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching projects"
        )

@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED, summary="Create a new project")
def create_new_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """
    Create a new project.
    
    - **title**: Project title (required)
    - **description**: Detailed project description (optional)
    - **skills**: List of skills/technologies used (optional)
    - **github_url**: GitHub repository URL (optional)
    - **demo_url**: Live demo URL (optional)
    - **image_url**: URL to project image (optional)
    - **is_featured**: Whether the project is featured (default: false)
    - **status**: Project status (default: "active")
    - **project_metadata**: Additional metadata (optional)
    """
    try:
        return create_project(db=db, obj_in=project)
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating project: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the project"
        )

@router.get("/{project_id}", response_model=Project, summary="Get project by ID")
def read_project(project_id: int, db: Session = Depends(get_db)):
    """
    Get a specific project by its ID.
    
    - **project_id**: The ID of the project to retrieve
    """
    db_project = get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return db_project

@router.put("/{project_id}", response_model=Project, summary="Update a project")
def update_existing_project(
    project_id: int, 
    project: ProjectUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update a project's information.
    
    - **project_id**: The ID of the project to update
    - All other fields are optional and will only be updated if provided
    """
    try:
        db_project = get_project(db, project_id=project_id)
        if db_project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        return update_project(db=db, db_obj=db_project, obj_in=project)
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating project {project_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the project"
        )

@router.delete("/{project_id}", response_model=Project, summary="Delete a project")
def delete_existing_project(project_id: int, db: Session = Depends(get_db)):
    """
    Delete a project.
    
    - **project_id**: The ID of the project to delete
    """
    try:
        db_project = delete_project(db, project_id=project_id)
        if db_project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        return db_project
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting project {project_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the project"
        )

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
import json
import logging

from app.db.session import get_db
from app.db.models.project import Project

logger = logging.getLogger(__name__)

router = APIRouter()

def project_matches_skill(project: Project, skill: str) -> bool:
    """Check if a project matches the given skill (case-insensitive)."""
    if not skill:
        return True
    
    # Ensure skills is a list
    project_skills = project.skills or []
    if isinstance(project_skills, str):
        try:
            project_skills = json.loads(project_skills)
        except json.JSONDecodeError:
            project_skills = []
    
    # Check if any skill matches (case-insensitive)
    return any(skill.lower() in s.lower() for s in project_skills)

@router.get("/")
async def get_projects(
    request: Request,
    skill: Optional[str] = Query(None, description="Filter projects by skill"),
    db: Session = Depends(get_db)
):
    try:
        # Get user profile from request state (set by auth middleware)
        user_profile = getattr(request.state, 'user', None)
        if not user_profile:
            logger.warning("Unauthorized access to projects endpoint")
            return []

        # Get user ID from profile
        user_id = user_profile.get('id')
        if not user_id:
            logger.warning("No user ID found in profile")
            return []

        # Query only projects that belong to the current user
        query = db.query(Project).filter(
            Project.status == 'active',
            Project.user_id == user_id  # Assuming there's a user_id column in projects
        )
        
        # Apply skill filter if provided
        if skill:
            projects = query.all()
            projects = [p for p in projects if project_matches_skill(p, skill)]
        else:
            projects = query.all()
        
        # Convert to list of dicts
        result = [
            {
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "skills": p.skills if p.skills else [],
                "github_url": p.github_url,
                "demo_url": p.demo_url,
                "image_url": p.image_url,
                "is_featured": p.is_featured,
                "created_at": p.created_at.isoformat() if p.created_at else None,
                "updated_at": p.updated_at.isoformat() if p.updated_at else None
            }
            for p in projects
        ]
        
        logger.info(f"Returning {len(result)} projects for user {user_id}")
        return result
        
    except Exception as e:
        # Log the error and return a 500 response
        logger.error(f"Error fetching projects: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching projects"
        )

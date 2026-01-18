from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.db.database import get_db
from app.models.models import Project as DBProject, Skill as DBSkill
from app.schemas import Project, ProjectCreate, ProjectUpdate

router = APIRouter()

@router.get("/projects", response_model=List[Project])
def list_projects(
    skill: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(DBProject)
        
        if skill:
            # Normalize the skill name (lowercase and trim)
            skill = skill.strip().lower()
            # Join with skills through the association table and filter case-insensitively
            query = (
                query.join(DBProject.skills_meta)
                .join(DBSkill)
                .filter(func.lower(DBSkill.name) == skill)
            )
        
        # Execute query and return results
        projects = query.distinct().all()
        return projects
    except Exception as e:
        print(f"Error in list_projects: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
def search_projects(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    # Convert query to lowercase for case-insensitive search
    search_term = f"%{q.lower()}%"
    
    # Search projects by title, description, or associated skills
    projects = db.query(DBProject).join(DBProject.skills).filter(
        (DBProject.title.ilike(search_term)) |
        (DBProject.description.ilike(search_term)) |
        (DBSkill.name.ilike(search_term))
    ).distinct().all()
    
    # Search skills separately
    skills = db.query(DBSkill).filter(
        DBSkill.name.ilike(search_term)
    ).all()
    
    return {
        "projects": projects,
        "skills": skills
    }

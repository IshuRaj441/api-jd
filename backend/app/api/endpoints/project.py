from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
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
    query = db.query(DBProject)
    
    if skill:
        query = query.join(DBProject.skills).filter(DBSkill.name.ilike(f"%{skill}%"))
    
    return query.all()

@router.get("/search")
def search_projects(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    results = {
        "projects": [],
        "skills": []
    }
    
    # Search projects
    projects = db.query(DBProject).filter(
        (DBProject.title.ilike(f"%{q}%")) |
        (DBProject.description.ilike(f"%{q}%"))
    ).all()
    
    # Search skills
    skills = db.query(DBSkill).filter(
        DBSkill.name.ilike(f"%{q}%")
    ).all()
    
    return {
        "projects": projects,
        "skills": skills
    }

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.models import Skill as DBSkill, project_skills
from sqlalchemy import func

router = APIRouter()

@router.get("/skills/top")
def get_top_skills(limit: int = 5, db: Session = Depends(get_db)):
    # Query to get top skills by project count
    top_skills = db.query(
        DBSkill,
        func.count(project_skills.c.skill_id).label('project_count')
    ).join(
        project_skills
    ).group_by(
        DBSkill.id
    ).order_by(
        func.count(project_skills.c.skill_id).desc()
    ).limit(limit).all()
    
    # Format the response
    return [
        {
            "id": skill.id,
            "name": skill.name,
            "project_count": project_count
        }
        for skill, project_count in top_skills
    ]
